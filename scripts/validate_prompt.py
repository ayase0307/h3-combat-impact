#!/usr/bin/env python3
"""檢查 H3 提示詞是否符合官方輸出格式，能否直接貼進模型。

用法：
    python validate_prompt.py prompt.txt --duration 8
    python validate_prompt.py --dir ./prompts --duration 8
    python validate_prompt.py impact.txt --duration 4 --impact-clip   # P3 衝擊片本身
    python validate_prompt.py main.txt --duration 8 --impact-plan plan.md

檢查：欄位、對齊句、時間碼、末鏡長度、否定詞、Markdown、<d> 配對、標籤定義、
表情肌肉、招式多樣性、鏡長等距（節拍器）、字數預算（依時長），以及衝擊幀規則：
  - 有大招／必殺／爆炸卻沒有任何衝擊幀（也沒宣告衝擊幀計畫）      → WARN
  - H3 慢詞（near-freeze、hangs poised、like a meteor…）          → WARN
  - 主片同段寫漫畫格                                                → FAIL（P2 衝擊幀串內降為 WARN）
  - 閃白配持續震屏、震屏沒有衰減、閃白用模糊時長、寫幀數控制       → WARN
  - 衝擊幀串沒寫每張停多久／同構圖                                  → WARN

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
NEG_OK = re.compile(r"with no (visible travel|normal frame in between)", re.I)
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
# ---- 衝擊幀規則（2026-10-26，見 SKILL.md §3 衝擊幀決策卡）----
BIG = re.compile(
    r"\b(ultimate|finishing (move|blow|strike)|finisher|killing blow|special move|"
    r"signature move|one-hit kill|single killing|annihilat\w*|obliterat\w*|"
    r"cataclysm\w*|world-ending|earth-shattering|"
    r"explo(de|des|ded|sion|sions)|detonat\w*|shockwave|shock wave)\b", re.I)
ULT = re.compile(
    r"\b(ultimate|finishing (move|blow|strike)|finisher|killing blow|special move|"
    r"signature move|one-hit kill|annihilat\w*|obliterat\w*|cataclysm\w*|"
    r"world-ending|earth-shattering)\b", re.I)
IMPACT = re.compile(
    r"(blows? out to (pure |full )?white|flash\w* (to |into )?(pure )?white|"
    r"white-?out|inverts?\b|colou?r negative|negative of the (whole )?frame|"
    r"impact frames?|manga panel|radial speed lines|radial (streaks?|lines|spikes|smear)|"
    r"black silhouettes? (on|against)|silhouettes? on white|star-?burst|"
    r"ink (burst|spikes|flash)|background (slams?|flips?|snaps?) to|"
    r"rekeys? the palette|exposure (drops|crushes|plunges)|frame (drops|goes|plunges) (dark|black))",
    re.I)
SLOW = re.compile(
    r"(near-?freeze|decelerates? to a|hangs? poised|poised and still|"
    r"(holds?|stays?|hangs?|remains?) (perfectly |completely )?still for (half a|a|one|two) seconds?|"
    r"like a meteor|for half a second|swallows the whole frame|time stops)", re.I)
SLOW_BIG = re.compile(r"\b(slowly|gradually)\b", re.I)
FRAME_COUNT = re.compile(r"\bfor (one|two|three|four|\d+) frames?\b", re.I)
VAGUE_FLASH = re.compile(
    r"(flash\w* (to )?white|blows? out to white)[^.;]{0,40}"
    r"(for a moment|briefly|momentarily|for an instant|for a split second)", re.I)
MANGA = re.compile(r"(manga panel|black-and-white (manga |comic )?panel|comic panel)", re.I)
BURST = re.compile(r"(burst of (\w+ )?impact frames|impact frames?:|\b(three|four|five|six|seven|eight|nine|ten|\d+) "
                   r"(still )?(hand-drawn )?(impact )?(frames|images) (of the same composition|cut one after another))", re.I)
BURST_HOLD = re.compile(r"(each|every one) (held|holds|lasting|lasts|for) (about |roughly )?\d|"
                        r"each held|held about|held for about", re.I)
SAME_COMP = re.compile(r"same composition", re.I)
FLASH = re.compile(r"(blows? out to (pure )?white|flash\w* (to |into )?(pure )?white|white-?out)", re.I)
CONT_SHAKE = re.compile(
    r"(shak\w* continuously|continuous(ly)? shak\w*|keeps? shaking|"
    r"shak\w* (throughout|the whole (time|shot|clip))|constant(ly)? shak\w*|"
    r"shak\w* nonstop|never stops shaking)", re.I)
SHAKE = re.compile(r"\b(shakes?|shaking|jolts?|jolting|judders?)\b", re.I)
SHAKE_DECAY = re.compile(
    r"(decays?|settl\w*|steadies|steady|each smaller|smaller than the last|"
    r"dies (down|away)|almost immediately|within (a|half a|a third of a|a quarter) second|"
    r"for a few frames|three times|camera steadies)", re.I)
PLAN_MARK = re.compile(r"(衝擊幀計畫|impact[_ ]plan|本段無衝擊幀)", re.I)


def word_limit(duration, is_ref):
    """字數預算：與 SKILL.md §5、references/output-format.md 同一張表。"""
    base = 700 if (duration and duration > 8) else 520
    return base + (300 if is_ref else 0)


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


def check(path, duration, impact_clip=False, impact_plan=None):
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

    # 負面約束（實測有效、刻意保留的兩句不算：with no visible travel／with no normal frame in between）
    negs = NEG.findall(NEG_OK.sub("", body))
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
    if not MUSCLE.search(body) and not impact_clip:
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

    # 鏡長等距（節拍器）：參考片鏡長 CV 0.90–1.17；等距 0.7s 一鏡＝單調
    if len(stamps) >= 6:
        gaps = [b - a for a, b in zip(stamps, stamps[1:]) if b > a]
        if len(gaps) >= 5:
            mean = sum(gaps) / len(gaps)
            sd = (sum((g - mean) ** 2 for g in gaps) / len(gaps)) ** 0.5
            cv = sd / mean if mean else 0
            if cv < 0.4:
                out.append(("WARN", f"時間碼間隔幾乎等距（CV {cv:.2f} < 0.4）—— 鏡長像節拍器。"
                                    "改成雙峰：1–2 個 1.2–2.0s 長鏡＋大量 0.25–0.6s 短鏡（SKILL.md §4）"))
                warn += 1

    # ---- 衝擊幀 ----
    w, f = check_impact(raw, body, nshot, impact_clip, impact_plan, out)
    warn += w; fail += f

    # 字數預算（依時長；Ref2VA +300）
    words = len(body.split())
    limit = word_limit(duration, is_ref)
    if words > limit:
        span = "9–15 秒" if (duration and duration > 8) else "4–8 秒"
        out.append(("WARN", f"字數 {words} 超過預算 {limit}（{span}{'、Ref2VA +300' if is_ref else ''}），"
                            "末段約束易失效")); warn += 1

    print(f"\n{os.path.basename(path)}  mode={mode}  shots={nshot}  words={words}  "
          f"duration={duration or '?'}")
    if not out:
        print("  [PASS] 格式完全符合，可直接使用")
    for lv, msg in out:
        print(f"  [{lv}] {msg}")
    return fail


def check_impact(raw, body, nshot, impact_clip, impact_plan, out):
    """衝擊幀規則。回傳 (warn 數, fail 數)，訊息直接 append 到 out。"""
    warn = fail = 0
    has_burst = bool(BURST.search(body))
    has_impact = bool(IMPACT.search(body)) or has_burst
    raw_outside = re.sub(r"```.*?```", "", raw, flags=re.S)
    has_plan = bool(impact_plan) or bool(PLAN_MARK.search(raw_outside))

    if not impact_clip:
        big = BIG.search(body)
        if big and not has_impact and not has_plan:
            out.append(("WARN", f"[IMPACT] 有「{big.group(0)}」（大招／爆炸／衝擊波），但沒有任何衝擊幀，"
                                "也沒宣告衝擊幀計畫。先列衝擊點清單並選 P0–P3（SKILL.md §3）；"
                                "主片走 P3 不寫衝擊幀時，加 --impact-plan 或在 code block 外附「衝擊幀計畫」表"))
            warn += 1

    slow = sorted(set(m.group(0).lower() for m in SLOW.finditer(body)))
    if slow:
        out.append(("WARN", f"[IMPACT] 含 H3 慢詞 {slow}：H3 會放大成 0.5–3.7s 空等或長時間發光；"
                            "停頓改在組裝做（impact_frame.py ramp／composite）")); warn += 1
    if ULT.search(body) and SLOW_BIG.search(body):
        out.append(("WARN", "[IMPACT] 大招段出現 slowly／gradually：大招段整段會變慢；"
                            "慢只留給收尾，命中段寫 instantly／within a single frame")); warn += 1

    if not impact_clip:
        fc = sorted(set(m.group(0).lower() for m in FRAME_COUNT.finditer(body)))
        if fc:
            out.append(("WARN", f"[IMPACT] 寫了幀數控制 {fc}：H3 不遵守（白閃實測亮 11–45 幀、"
                                "漫畫格 21–23 幀）。改寫 then snaps straight back，精準幀數交給組裝"))
            warn += 1

    if MANGA.search(body) and nshot > 1 and not impact_clip:
        if has_burst:
            out.append(("WARN", "[IMPACT] 衝擊幀串裡有漫畫格：可以，但確認每張都寫了停多久、"
                                "同構圖，組裝時加速（burst-strip.md）")); warn += 1
        else:
            out.append(("FAIL", "[IMPACT] 主片同段寫漫畫格：H3 實測 21–23 幀、角色會消失。"
                                "改走 P3（另生衝擊片再 composite）或 P2 衝擊幀串；"
                                "若這支就是衝擊片，加 --impact-clip")); fail += 1
    if re.search(r"then one frame of black", body, re.I):
        out.append(("WARN", "[IMPACT] `then one frame of black` 會把回彩色一起拖長（實測 21 幀、角色消失）；"
                            "黑尾在組裝時插（composite --black）")); warn += 1

    if VAGUE_FLASH.search(body):
        out.append(("WARN", "[IMPACT] 閃白用模糊時長（for a moment／briefly）：H3 給長閃像燈光故障。"
                            "改 then snaps straight back，精準長度交給組裝")); warn += 1
    if FLASH.search(body) and CONT_SHAKE.search(body):
        out.append(("WARN", "[IMPACT] 閃白配持續震屏：衝擊被手持晃動稀釋。震屏二選一——"
                            "最大衝擊鏡相機鎖死，或回原鏡頭第一格猛震三下、0.5s 內停穩")); warn += 1
    elif CONT_SHAKE.search(body):
        out.append(("WARN", "[IMPACT] shakes continuously 類寫法會變成手持鏡頭")); warn += 1
    if SHAKE.search(body) and not SHAKE_DECAY.search(body) and not impact_clip:
        out.append(("WARN", "[IMPACT] 有震屏但沒寫衰減與回穩（峰值→衰減→停穩）")); warn += 1

    if has_burst:
        if not BURST_HOLD.search(body):
            out.append(("WARN", "[IMPACT] 衝擊幀串沒寫每張停多久（each held about 0.2 seconds）："
                                "時間給短了模型會擠成分格")); warn += 1
        if not SAME_COMP.search(body):
            out.append(("WARN", "[IMPACT] 衝擊幀串沒寫 same composition：每張構圖會亂跳，"
                                "組裝加速後讀不成同一擊")); warn += 1
    return warn, fail


def main():
    ap = argparse.ArgumentParser(
        description="檢查 H3 提示詞是否符合官方格式、能否直接貼進模型，並檢查打鬥／衝擊幀規則。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="範例：\n"
               "  python validate_prompt.py prompt.txt --duration 8\n"
               "  python validate_prompt.py impact.txt --duration 4 --impact-clip\n"
               "  python validate_prompt.py main.txt --duration 8 --impact-plan plan.md\n")
    ap.add_argument("file", nargs="?", help="提示詞檔（.txt／.md；有 code block 時取最長的那個）")
    ap.add_argument("--dir", help="批次檢查資料夾內所有 .txt／.md")
    ap.add_argument("--duration", type=float, default=None,
                    help="實際生成時長（秒），用於檢查時間碼、末鏡長度與字數預算（>8 秒用 700 字）")
    ap.add_argument("--impact-clip", action="store_true",
                    help="這支是 P3 衝擊片本身：豁免漫畫格、幀數、表情與『大招沒衝擊幀』規則")
    ap.add_argument("--impact-plan", default=None,
                    help="衝擊幀計畫表檔案（或任意字串，例如 P3）：宣告衝擊幀走組裝，主片不寫也不報")
    a = ap.parse_args()

    files = [a.file] if a.file else []
    if a.dir:
        files += sorted(glob.glob(os.path.join(a.dir, "*.md")) +
                        glob.glob(os.path.join(a.dir, "*.txt")))
    if not files:
        ap.print_help()
        return 1

    total = sum(check(f, a.duration, a.impact_clip, a.impact_plan) for f in files)
    print(f"\n合計 FAIL {total} 項")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
