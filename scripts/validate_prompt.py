#!/usr/bin/env python3
"""檢查 H3 提示詞是否符合官方輸出格式，能否直接貼進模型。

用法：
    python validate_prompt.py prompt.txt --duration 8
    python validate_prompt.py --dir ./prompts

退出碼：0 = 全部通過（可能有 WARN）；1 = 有 FAIL。
"""

import argparse
import glob
import os
import re
import sys

BASE_FIELDS = ["integrated_multimodal_description", "overall_soundscape", "non_diegetic_music"]
REF_FIELDS = ["subject_definitions", "summary", "retention_analysis",
              "detailed_description", "overall_soundscape", "non_diegetic_music"]

NEG = re.compile(r"\b(no|not|never|without|instead of|rather than)\b", re.I)
# 表情肌肉詞：沒有這些詞的「情緒描述」等於沒寫
# 招式類別詞（用來自動檢查招式多樣性）
MOVE_CATS = {
    # 只算「刀路動詞」，不含 blade/katana 這類名詞（名詞每個鏡頭都會出現，會誤判）
    "blade": r"\b(cut|cuts|cutting|slash|slashes|thrust|thrusts|rip|rips|"
             r"cleave|swings?|stabs?|strikes?|drives through|"
             r"descending cut|rising cut|overhead cut)\b",
    "kick": r"\b(kick|kicks|knee|knees|shin|stomp|stamps?)\b",
    "punch": r"\b(punch|punches|hook|hooks|elbow|elbows|backfist|jab|"
             r"palm|palms|fist|forearm|headbutt)\b",
    "throw": r"\b(throw|throws|hip-throw|hurl|hurls|slam|slams|dump|dumps|"
             r"underhook|overhook|mounts?|pins?)\b",
    "sweep": r"\b(sweep|sweeps|sweeping|trip|trips|low kick|ankle|take her legs)\b",
    "grab": r"\b(grab|grabs|grapple|seize|seizes|wrist|wrench|wrenches|"
            r"choke|chokes|clinched|clinch)\b",
    "block": r"\b(parr(y|ies|ied)|block|blocks|blocked|catches|catching|"
             r"guards? against|deflect|deflects|absorbs)\b",
    "move": r"\b(vault|vaults|leaps|dash|dashes|sidestep|sidesteps|rolls|"
            r"slides|spins|charges|closes the gap|backpedal)\b",
}
BLADE_LIMIT_15 = 12
BLADE_LIMIT_8 = 7

MUSCLE = re.compile(
    r"\b(brows?|eyelids?|lids?|jaw|jaws|teeth|clench\w*|lips?|mouth|throat|"
    r"nostrils?|temple|cheeks?|chin|breath\w*|gasp\w*|swallow\w*|"
    r"heaves?|heaving|sweat\w*|flinch\w*|wince\w*|grimace\w*)\b", re.I)
# 只描述眼睛形狀／打光、不含肌肉的寫法
FAKE_FACE = re.compile(
    r"\b(irises?|pupils?|eyes?)\s+(narrow\w*|widen\w*|glow\w*|lit|lit up|"
    r"reflecting|reflected)\b", re.I)
TS = re.compile(r"At\s+(\d{2}):(\d{2}\.\d{2,3})")
SHOT = re.compile(r"\[Shot (\d+)\]")
LABEL = re.compile(r"<(Subject|Picture|Video|Audio) (\d+)>")


def extract(text):
    blocks = re.findall(r"```(?:text)?\s*\n(.*?)\n```", text, re.S)
    if blocks:
        return max(blocks, key=len).strip()
    return text.strip()


def field_positions(body):
    pos = {}
    for name in BASE_FIELDS + REF_FIELDS:
        m = re.search(rf"^\s*{name}\s*:", body, re.M)
        if m:
            pos[name] = m.start()
    return pos


def section(body, name, all_names):
    m = re.search(rf"^\s*{name}\s*:", body, re.M)
    if not m:
        return ""
    start = m.end()
    nxt = [re.search(rf"^\s*{n}\s*:", body[m.end():], re.M) for n in all_names if n != name]
    offs = [o.start() for o in nxt if o]
    end = m.end() + min(offs) if offs else len(body)
    return body[start:end]


def check(path, duration):
    raw = open(path, encoding="utf-8").read()
    body = extract(raw)
    out = []
    fail = warn = 0

    is_ref = bool(re.search(r"^\s*subject_definitions\s*:", body, re.M))
    fields = REF_FIELDS if is_ref else BASE_FIELDS
    mode = "Ref2VA" if is_ref else "T2VA/I2VA/FL2VA/L2VA"

    pos = field_positions(body)
    missing = [f for f in fields if f not in pos]
    if missing:
        out.append(("FAIL", f"缺少欄位：{', '.join(missing)}")); fail += 1
    order = [f for f in fields if f in pos]
    if order != sorted(order, key=lambda f: pos[f]):
        out.append(("FAIL", "欄位順序錯誤")); fail += 1

    # 關鍵幀首行
    head = body.split("\n", 3)[0].strip()
    align_i2va = body.startswith("For the target video")
    align_fl = body.startswith("How the reference pictures align")
    declared = re.search(r"模式\s*[:：]\s*(I2VA|FL2VA|L2VA|T2VA|Ref2VA)", raw)
    if declared:
        want = declared.group(1)
        if want == "I2VA" and not align_i2va:
            out.append(("FAIL", "標註 I2VA 但缺少首行對齊句")); fail += 1
        if want in ("FL2VA", "L2VA") and not align_fl:
            out.append(("FAIL", f"標註 {want} 但缺少首行對齊句")); fail += 1
        if want == "Ref2VA" and not is_ref:
            out.append(("FAIL", "標註 Ref2VA 但缺少六欄位結構")); fail += 1
    if align_i2va or align_fl:
        m = re.search(r"^\s*integrated_multimodal_description\s*:", body, re.M)
        if m and m.start() < body.find(head):
            out.append(("WARN", "對齊句不在最前面"))
            warn += 1
    if re.search(r"^\s*integrated_multimodal_description\s*:\s*\n", body, re.M):
        out.append(("FAIL", "欄位名後換行才寫內容，應接在同一行")); fail += 1

    # 鏡頭與時間碼
    shots = [int(x) for x in SHOT.findall(body)]
    nshot = max(shots) if shots else 0
    if nshot == 0:
        out.append(("FAIL", "找不到 [Shot N] 標記")); fail += 1

    stamps = []
    for m in TS.finditer(body):
        stamps.append(int(m.group(1)) * 60 + float(m.group(2)))
    if stamps != sorted(stamps):
        out.append(("FAIL", "時間碼未嚴格遞增")); fail += 1
    if duration and stamps and stamps[-1] >= duration:
        out.append(("FAIL", f"時間碼 {stamps[-1]:.2f}s 超出時長 {duration}s")); fail += 1

    # Shot 1 不得有時間碼
    seg1 = section(body, "integrated_multimodal_description", fields)
    s1 = re.search(r"\[Shot 1\](.*?)(?=\[Shot 2\]|$)", seg1, re.S)
    if s1 and TS.search(s1.group(1)):
        out.append(("FAIL", "[Shot 1] 出現時間碼")); fail += 1

    # 末鏡長度
    if duration and stamps:
        last_len = duration - stamps[-1]
        ratio = last_len / duration
        if ratio > 0.30:
            out.append(("FAIL", f"末鏡過長 {last_len:.2f}s（總長 {ratio*100:.0f}%），"
                                "會被填成站定畫面")); fail += 1

    # 負面約束
    negs = NEG.findall(body)
    if negs:
        out.append(("WARN", f"含 {len(negs)} 處否定詞（{', '.join(sorted(set(n.lower() for n in negs)))}）"
                            "，建議改成正面動作")); warn += 1

    # Markdown 殘留
    bad = [ln for ln in body.splitlines()
           if re.match(r"^\s*([-*#]|\d+\.)\s", ln) or "**" in ln]
    if bad:
        out.append(("FAIL", f"含 Markdown 殘留 {len(bad)} 行（清單/粗體/標題）")); fail += 1

    # 對白
    if body.count("<d>") != body.count("</d>"):
        out.append(("FAIL", "<d> 與 </d> 數量不符")); fail += 1

    # 標籤定義
    if is_ref:
        defs = section(body, "subject_definitions", fields)
        defined = set(LABEL.findall(defs))
        used = set(LABEL.findall(body))
        undef = used - defined
        if undef:
            names = ", ".join(f"<{a} {b}>" for a, b in sorted(undef))
            out.append(("FAIL", f"標籤未定義：{names}")); fail += 1
    else:
        if LABEL.search(body) and not re.search(r"<Picture \d+>", body):
            out.append(("WARN", "出現標籤但無對應 Picture 引用"))
            warn += 1

    # 表情：有臉部特寫卻沒有肌肉動作 = 死人臉
    # 特寫的判斷窗：從 close-up 起算到「本鏡結束」（下一個 [Shot 或欄位）
    close_ups = re.findall(
        r"(?:extreme )?close[- ]up.*?(?=\[Shot\s|\n\n|\Z)", body, re.I | re.S)
    if close_ups:
        # 只有「畫面裡有人臉」的特寫才需要肌肉動作；兵器/手部特寫不算
        FACE = re.compile(r"\b(face|faces|eyes?|irises?|expression)\b", re.I)
        BLADE_FACE = re.compile(r"flat faces|blade faces|faces of the", re.I)
        face_cu = [c for c in close_ups
                   if FACE.search(c) and not BLADE_FACE.search(c)]
        no_muscle = [c for c in face_cu if not MUSCLE.search(c)]
        if no_muscle:
            out.append(("WARN",
                        f"{len(no_muscle)}/{len(face_cu)} 個臉部特寫沒有肌肉動作"
                        "（只寫眼睛形狀/打光會得到死人臉；改寫眉毛、下眼瞼、"
                        "咀嚼肌、嘴、喉）"))
            warn += 1
    if not MUSCLE.search(body):
        out.append(("WARN", "全篇沒有任何表情肌肉動作"
                            "（brow/jaw/teeth/lip/throat/breath…），"
                            "角色會全程面無表情"))
        warn += 1
    if len(FAKE_FACE.findall(body)) >= 2 and not MUSCLE.search(body):
        out.append(("WARN", "用眼睛形狀代替表情（如 irises narrow），"
                            "那不是肌肉動作"))
        warn += 1
# 招式多樣性：看「刀路佔比」，不是絕對次數（長提示詞刀路次數自然高）
    counts = {k: len(re.findall(v, body, re.I)) for k, v in MOVE_CATS.items()}
    blade = counts.get("blade", 0)
    others = sum(v for k, v in counts.items() if k != "blade")
    total = blade + others
    if total >= 8:
        blade_pct = 100.0 * blade / total
        # 15 秒以上容許刀路 55%；8 秒容許 60%（短片段沒空間放全套）
        cap = 55.0 if (duration and duration >= 12) else 60.0
        if blade_pct > cap:
            out.append(("WARN",
                        f"刀路佔比 {blade_pct:.0f}%（刀路 {blade} / 其他 {others}，"
                        f"上限 {cap:.0f}%）—— 招式單一。"
                        "加踢擊/拳肘/摔投/下盤/擒拿，"
                        "見 references/choreography.md 的配額表"))
            warn += 1
        if counts.get("throw", 0) == 0 and blade >= 4:
            out.append(("WARN", "完全沒有摔投/擒拿 —— 距離不會變化，"
                                "容易變成兩人站著互砍"))
            warn += 1
        if counts.get("sweep", 0) == 0:
            out.append(("WARN", "完全沒有下盤/絆 —— 全程在同一個高度打"))
            warn += 1

    # 字數預算
    words = len(body.split())
    limit = 820 if is_ref else 520
    if words > limit:
        out.append(("WARN", f"字數 {words} 超過預算 {limit}，末段約束易失效")); warn += 1

    print(f"\n{os.path.basename(path)}  mode={mode}  shots={nshot}  words={words}  "
          f"duration={duration or '?'}")
    if not out:
        print("  [PASS] 格式完全符合，可直接使用")
    for lv, msg in out:
        print(f"  [{lv}] {msg}")
    return fail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?")
    ap.add_argument("--dir")
    ap.add_argument("--duration", type=float, default=None,
                    help="實際生成時長（秒），用於檢查時間碼與末鏡長度")
    a = ap.parse_args()

    files = [a.file] if a.file else []
    if a.dir:
        files += sorted(glob.glob(os.path.join(a.dir, "*.md")) +
                        glob.glob(os.path.join(a.dir, "*.txt")))
    if not files:
        ap.print_help()
        return 1

    total = sum(check(f, a.duration) for f in files)
    print(f"\n合計 FAIL {total} 項")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
