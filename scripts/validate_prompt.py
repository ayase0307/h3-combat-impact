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

    # 字數預算
    words = len(body.split())
    limit = 520
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
