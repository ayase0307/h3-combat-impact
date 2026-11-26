#!/usr/bin/env python3
"""檢查 H3 提示詞是否符合官方輸出格式，能否直接貼進模型。

用法：
    python validate_prompt.py prompt.txt --duration 8
    python validate_prompt.py --dir ./prompts

退出碼：0 = 全部通過（可能有 WARN）；1 = 有 FAIL。
"""

import argparse
import glob
import json
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
    "kick": r"\b(kick|kicks|knee|knees|shin|stomp(s|ed|ing)?|stamps?)\b",
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

# 動作物理防呆正則：姿態—位移衝突與溜冰滑行詞攔截
GROUNDED_STATIC = re.compile(
    r"\b(kneels?|kneeling|knelt|crouches?|crouching|squats?|squatting|"
    r"sits?|sitting|seated|meditates?|meditating|on\s+(?:one|both|his|her)\s+knees?)\b",
    re.I,
)
FAST_TRANSLATE = re.compile(
    r"\b(sprints?|sprinting|dashes?|dashing|hurtles?|hurtling|streaks?\s+across|"
    r"charges?\s+across|rushes?\s+across|rockets?\s+forward|tracks?\s+sideways\s+fast|"
    r"whip[- ]pans?)\b",
    re.I,
)
POSTURE_RELEASE = re.compile(
    r"\b(rises?|rising|stands?\s+up|leaps?\s+up|springs?\s+up|explodes?\s+upward|"
    r"pushes?\s+off|drives?\s+off|launches?\s+up)\b",
    re.I,
)
SKID_SLIDE = re.compile(
    r"\b(skids?|skidding|skidded|slides?|sliding|slid|glides?\s+across|"
    r"gliding\s+across|skates?|skating)\b",
    re.I,
)
BLADE_SLIDE_EXC = re.compile(
    r"\b(blades?\s+slides?|sword\s+slides?|steel\s+slides?|edge\s+slides?|"
    r"slides?\s+along\s+the\s+(?:blade|shaft|guard|edge)|slides?\s+off\s+(?:his|her|the)\s+(?:blade|fan|shield|guard))\b",
    re.I,
)

# v4.0 防動態破圖：空泛無身體機制的抽象打鬥句（只比對片語，不比對單字 epic/fierce）
ABSTRACT_FIGHT = re.compile(
    r"\b(attacks?\s+(?:fiercely|furiously|wildly|intensely|relentlessly)|"
    r"fights?\s+(?:fiercely|intensely|furiously|wildly|hard)|"
    r"fighting\s+(?:fiercely|intensely|furiously|wildly)|"
    r"battles?\s+(?:fiercely|intensely|furiously)|"
    r"(?:epic|intense|fierce|furious|chaotic)\s+(?:battle|fight|fighting|combat|clash|showdown)|"
    r"(?:exchange|trade)s?\s+(?:fierce\s+|furious\s+|rapid\s+)?blows|"
    r"clash(?:es)?\s+(?:fiercely|intensely|furiously)|"
    r"engages?\s+in\s+(?:a\s+|an\s+)?(?:fierce\s+|intense\s+|epic\s+)?(?:battle|combat|fight))\b",
    re.I,
)
# 身體機制詞：有這些詞，抽象句才算有落點（重心／支點／發力部位）
BODY_MECH = re.compile(
    r"\b(weight|balance|heels?|hips?|soles?|plants?|planted|planting|pivots?|pivoting|"
    r"stance|shoulders?|elbows?|wrists?|knees?|forearms?|fists?|palms?|torso|spine|"
    r"ribs?|thighs?|shins?|ankles?|feet|foot|toes?|boots?|waist|chest|knuckles?)\b",
    re.I,
)
# v4.0 防肢體融化：短鏡內堆疊全身翻轉／旋轉詞
SPIN_FLIP = re.compile(
    r"\b(spins?|spinning|flips?|flipping|backflips?|somersaults?|somersaulting|"
    r"whirls?|whirling|cartwheels?|cartwheeling|pirouettes?|twists?\s+mid-?air|twisting\s+mid-?air)\b",
    re.I,
)
SPIN_SHOT_MAX_DUR = 1.5
SPIN_STACK_LIMIT = 4

# 劇本式（references/screenplay-format.md）欄位：必填且順序固定
SCREENPLAY_REQUIRED = ["參考鎖", "畫風", "本段", "聲音", "連續性", "硬約束"]
SCREENPLAY_ROW = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*[-–—~]\s*(\d+(?:\.\d+)?)\s*秒\s*[｜|]", re.M)
SCREENPLAY_MAX_SEC = 8.0

MUSCLE = re.compile(
    r"\b(brows?|eyelids?|lids?|jaw|jaws|teeth|clench\w*|lips?|mouth|throat|"
    r"nostrils?|temple|cheeks?|chin|breath\w*|gasp\w*|swallow\w*|"
    r"heaves?|heaving|sweat\w*|flinch\w*|wince\w*|grimace\w*)\b", re.I)
# 只描述眼睛形狀／打光、不含肌肉的寫法
FAKE_FACE = re.compile(
    r"\b(irises?|pupils?|eyes?)\s+(narrow\w*|widen\w*|glow\w*|lit|lit up|"
    r"reflecting|reflected)\b", re.I)
# 美型角色（國漫／AI 漫劇／仙俠）過激毀臉詞：容易讓 H3 拉扯出齜牙咧嘴的醜臉
HARSH_FACE = re.compile(
    r"\b(teeth\s+clench\w*|clenched\s+teeth|lips?\s+peel\w*\s+back|"
    r"mouth\s+wrench\w*\s+open|jaw\s+muscles?\s+bunch\w*|jaw\s+bunch\w*|"
    r"brows?\s+slam\w*\s+down|spit\s+flying|vein\s+stands?\s+out)\b", re.I)
TS = re.compile(r"At\s+(\d{2}):(\d{2}\.\d{2,3})")
SHOT = re.compile(r"\[Shot (\d+)\]")
LABEL = re.compile(r"<(Subject|Picture|Video|Audio) (\d+)>")
# 五小節（打鬥版）：每鏡必須照這個順序出現
FIVE = ["Camera", "Motion", "Performance", "Light", "Sound"]
CAM_MOVE = re.compile(
    r"\b(push(es|ing)? in|pull(s|ing)? (out|back)|pan(s|ning)?|tilt(s|ing)?|"
    r"zoom(s|ing)?|truck(s|ing)?|doll(y|ies|ying)|pedestal(s|ing)?|"
    r"track(s|ing)?|orbit(s|ing)?|arc(s|ing)?|crane(s|d)?)\b", re.I)
WEIGHT = re.compile(
    r"\b(weight|balance|base|heel|heels|hips?|soles?|plant(s|ed|ing)?|"
    r"pivot(s|ed|ing)?|lever|levered|centre of mass|center of mass|"
    r"off[- ]balance\w*|counterweight|stance)\b", re.I)

# 模式設定：同一個結構在不同打法下，部分 WARN 是誤報（見 docs/research/
# 2026-11-18-strengthen-combat-impact.md T5）。用 front-matter `#!profile: X`
# 或 --profile 指定；預設 fight。
PROFILES = {
    "fight": {},
    "ultra": {"skip_moves": {"throw", "sweep"}, "blade_cap": 75.0, "word_cap": 620},
    "blade-light": {"skip_moves": {"throw", "sweep"}, "blade_cap": 85.0},
    "impact": {"skip_face": True, "skip_moves": True},
    "material": {"skip_face": True, "skip_moves": True},
    "facial": {"skip_moves": True},
    "fl2va": {"word_cap": 1300},
}


def strip_meta(text):
    """移除 `#!` 開頭的 front-matter／註解行（不會送進模型）。"""
    return "\n".join(ln for ln in text.splitlines() if not ln.lstrip().startswith("#!"))


def read_profile(raw, path=None):
    """檔案內 `#!profile:` 優先；其次同目錄 profiles.json 的檔名對照；預設 fight。"""
    m = re.search(r"^#!\s*profile\s*:\s*([a-z-]+)", raw, re.M)
    if m and m.group(1) in PROFILES:
        return m.group(1)
    if path:
        man = os.path.join(os.path.dirname(os.path.abspath(path)), "profiles.json")
        if os.path.exists(man):
            try:
                d = json.load(open(man, encoding="utf-8"))
                name = os.path.basename(path)
                if d.get(name) in PROFILES:
                    return d[name]
            except (OSError, ValueError):
                pass
    return "fight"



def extract(text):
    blocks = re.findall(r"```(?:text)?\s*\n(.*?)\n```", text, re.S)
    if blocks:
        # 雙語檔案可能含中文與英文多區塊，優先擷取包含官方 H3 欄位的區塊
        for b in blocks:
            if re.search(r"^\s*(?:subject_definitions|integrated_multimodal_description)\s*:", b, re.M):
                return b.strip()
        return max(blocks, key=len).strip()
    return text.strip()


def extract_zh_part(raw):
    """擷取雙語檔中位於英文 H3 區塊之前的中文導演母稿（若有）。"""
    m = re.search(r"```(?:text)?\s*\n\s*(?:subject_definitions|integrated_multimodal_description)\s*:", raw, re.M)
    if not m:
        m = re.search(r"^\s*(?:subject_definitions|integrated_multimodal_description)\s*:", raw, re.M)
    if not m or m.start() < 30:
        return ""
    head = raw[:m.start()].strip()
    return head if re.search(r"[\u4e00-\u9fff]{10,}", head) else ""


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


def read_face_style(raw, body, requested):
    """決定表情顏值檔：顯式參數 > 檔頭 #!face-style > 自動偵測國漫/漫劇/仙俠美型關鍵字。"""
    if requested in ("aesthetic", "rugged"):
        return requested
    m = re.search(r"^#!\s*face[-_]style\s*:\s*(aesthetic|rugged)", raw, re.M | re.I)
    if m:
        return m.group(1).lower()
    if re.search(r"\b(donghua|manju|guoman|xianxia|2\.5d)\b", body, re.I) or re.search(r"國漫|漫劇|仙俠|美型", raw):
        return "aesthetic"
    return "rugged"


def check_five_part(body, fields):
    """五小節檢查：標籤齊全、順序正確、五小節內沒有第二個運鏡動詞。"""
    out = []
    seg = section(body, "integrated_multimodal_description", fields)
    if not seg:
        seg = section(body, "detailed_description", fields)
    blocks = re.split(r"(?=\[Shot \d+\])", seg)
    for blk in blocks:
        m = SHOT.search(blk)
        if not m:
            continue
        n = m.group(1)
        found = []
        for lbl in FIVE:
            hit = re.search(rf"\b{lbl}\s*:", blk)
            if hit:
                found.append((hit.start(), lbl))
        names = [lbl for _, lbl in found]
        if names != FIVE:
            missing = [x for x in FIVE if x not in names]
            out.append(("FAIL", f"[Shot {n}] 五小節不完整或順序錯："
                                f"現有 {names or '無'}"
                                + (f"，缺 {missing}" if missing else "，需照 "
                                   "Camera→Motion→Performance→Light→Sound")))
            continue
        body_start = found[0][0]
        tail = blk[body_start:]
        if re.search(r"\bthe camera\b", tail, re.I):
            out.append(("FAIL", f"[Shot {n}] 五小節內出現 the camera"
                                "（運鏡詞只能出現在頭句）"))
        elif CAM_MOVE.search(tail.replace("push off", "").replace("pushes off", "")):
            hit = CAM_MOVE.search(tail)
            out.append(("WARN", f"[Shot {n}] 五小節內疑似出現第二個運鏡動詞"
                                f"「{hit.group(0)}」——檢查是否為動作詞"))
    return out


def is_screenplay(text):
    """劇本式（中文方括號欄位）而非官方 H3 欄位。"""
    has_h3 = re.search(r"^\s*(?:subject_definitions|integrated_multimodal_description)\s*:", text, re.M)
    return not has_h3 and bool(re.search(r"^\[本段\]", text, re.M)) and bool(re.search(r"^\[參考鎖\]", text, re.M))


def check_screenplay(text, duration):
    """劇本式檢核：欄位齊全且有序、[本段] 逐秒時間軸連續、聲音／連續性／硬約束必填項。

    劇本式依設計把禁止項集中在 [硬約束]，因此不跑否定詞與 H3 欄位檢查。
    """
    out = []
    heads = {m.group(1): m.start() for m in re.finditer(r"^\[([^\]\n]+)\]", text, re.M)}
    missing = [h for h in SCREENPLAY_REQUIRED if h not in heads]
    if missing:
        out.append(("FAIL", f"劇本式缺少欄位：{', '.join('[' + h + ']' for h in missing)}"))
    present = [h for h in SCREENPLAY_REQUIRED if h in heads]
    if present != sorted(present, key=lambda h: heads[h]):
        out.append(("FAIL", "劇本式欄位順序錯誤（應為 參考鎖→畫風→本段→聲音→連續性→硬約束）"))

    def body_of(name):
        if name not in heads:
            return ""
        start = heads[name]
        later = [p for p in heads.values() if p > start]
        return text[start:min(later) if later else len(text)]

    rows = [(float(a), float(b)) for a, b in SCREENPLAY_ROW.findall(body_of("本段"))]
    if not rows:
        out.append(("FAIL", "[本段] 找不到逐秒時間軸（格式：0.0-2.5秒｜…）"))
    else:
        prev_end = 0.0
        for a, b in rows:
            if b <= a or abs(a - prev_end) > 0.05:
                out.append(("FAIL", f"[本段] 時間軸不連續或倒退：{a}-{b}秒（上一段結束於 {prev_end}）"))
                break
            prev_end = b
        end = rows[-1][1]
        if duration and end > duration + 0.05:
            out.append(("FAIL", f"[本段] 時間軸結束於 {end}s，超出時長 {duration}s"))
        elif duration and end < duration - 0.05:
            out.append(("WARN", f"[本段] 時間軸只寫到 {end}s，時長 {duration}s 的尾段沒有動作"))
        if end > SCREENPLAY_MAX_SEC + 0.05:
            out.append(("WARN", f"劇本式單段 {end}s 超過 {SCREENPLAY_MAX_SEC:.0f}s，請改用官方骨架或拆段"))
    if not re.search(r"說話|嘴唇|對白", body_of("聲音")):
        out.append(("WARN", "[聲音] 沒寫有沒有人說話／嘴唇是否閉著，模型會自己補對白"))
    cont = body_of("連續性")
    if cont and not ("首態" in cont and "尾態" in cont):
        out.append(("WARN", "[連續性] 缺首態或尾態"))
    hard = body_of("硬約束")
    if hard and "字幕" not in hard:
        out.append(("WARN", "[硬約束] 沒有寫無字幕"))
    return out, len(rows)


def check(path, duration, profile="auto", check_sync=False, face_style="auto", strict_physics=False, five_part=False):
    raw = open(path, encoding="utf-8").read()
    if is_screenplay(strip_meta(raw)):
        sp_out, nrows = check_screenplay(strip_meta(raw), duration)
        print(f"\n{os.path.basename(path)}  mode=Screenplay  rows={nrows}  duration={duration or '?'}")
        if not sp_out:
            print("  [PASS] 劇本式格式完全符合，可直接使用")
        for lv, msg in sp_out:
            print(f"  [{lv}] {msg}")
        return sum(1 for lv, _ in sp_out if lv == "FAIL")
    body = extract(strip_meta(raw))
    prof = read_profile(raw, path) if profile in (None, "auto") else profile
    rules = PROFILES.get(prof, {})
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

    # Shot 1 不得有時間碼，並逐鏡解析時長與動作物理合理性
    desc_field = "detailed_description" if is_ref else "integrated_multimodal_description"
    seg1 = section(body, desc_field, fields)
    s1 = re.search(r"\[Shot 1\](.*?)(?=\[Shot 2\]|$)", seg1, re.S)
    if s1 and TS.search(s1.group(1)):
        out.append(("FAIL", "[Shot 1] 出現時間碼")); fail += 1

    # 逐鏡動作物理防呆：1) 接地靜態姿態 × 高速平移衝突；2) 單鏡短時長動作超載
    shot_blocks = list(re.finditer(r"\[Shot (\d+)\](.*?)(?=\[Shot \d+\]|\Z)", seg1, re.S))
    shot_starts = [0.0] + stamps
    use_strict_physics = strict_physics or bool(re.search(r"^#!\s*physics\s*:\s*strict\b", raw, re.M | re.I))

    for idx, sb in enumerate(shot_blocks):
        s_num = int(sb.group(1))
        s_txt = sb.group(2)
        s_start = shot_starts[idx] if idx < len(shot_starts) else 0.0
        s_end = shot_starts[idx + 1] if (idx + 1) < len(shot_starts) else (duration or (s_start + 2.5))
        s_dur = max(0.2, s_end - s_start)

        g_match = GROUNDED_STATIC.search(s_txt)
        f_match = FAST_TRANSLATE.search(s_txt)
        if g_match and f_match and not POSTURE_RELEASE.search(s_txt):
            out.append((
                "FAIL",
                f"[Shot {s_num}] 姿態—位移物理衝突：接地鎖死姿態 '{g_match.group(0)}' 與高速平移 '{f_match.group(0)}' 同鏡且無蹬離起身詞，必導致角色貼地滑行！"
            ))
            fail += 1

        # v4.0 防動態破圖 1：抽象打鬥句且整鏡沒有任何發力部位／重心詞
        abstract = ABSTRACT_FIGHT.search(s_txt)
        if abstract and not BODY_MECH.search(s_txt):
            out.append((
                "WARN",
                f"[Shot {s_num}] 空泛打鬥句「{abstract.group(0)}」且本鏡沒有任何身體機制詞（重心／發力部位／支點）—— H3 會畫成糊成一團的亂揮破圖；請改寫成「誰用哪個部位、沿哪條線、打到哪裡」"
            ))
            warn += 1

        # v4.0 防動態破圖 2：短鏡內堆疊全身翻轉／旋轉詞，H3 易肢體融化
        spins = [m.group(0).lower() for m in SPIN_FLIP.finditer(s_txt)]
        if s_dur < SPIN_SHOT_MAX_DUR and len(spins) >= SPIN_STACK_LIMIT:
            out.append((
                "WARN",
                f"[Shot {s_num}] 時長僅 {s_dur:.2f}s 卻堆疊 {len(spins)} 個翻轉／旋轉詞（{', '.join(spins)}）—— H3 極易肢體融化、多出手腳；請每鏡只留 1 個全身旋轉，其餘改成單一部位發力或拆到下一鏡"
            ))
            warn += 1

        if use_strict_physics and prof not in ("ultra", "blade-light"):
            core_verbs = sum(
                len(re.findall(MOVE_CATS[k], s_txt, re.I))
                for k in ("blade", "kick", "punch", "throw", "sweep", "grab")
            )
            if s_dur < 1.8 and core_verbs >= 5:
                out.append((
                    "WARN",
                    f"[Shot {s_num}] 時長僅 {s_dur:.2f}s 卻塞入 {core_verbs} 個核心攻防動詞（幀數不足演完跨步與轉胯，易變瞬移或原地空揮，建議拉長至 2.2-2.8s 或精簡動作）"
                ))
                warn += 1

    # v3.0 嚴格物理閘門（--strict-physics 或檔頭 #!physics: strict 啟用）：溜冰滑行與打地板陷阱
    if use_strict_physics:
        cleaned_slide_txt = BLADE_SLIDE_EXC.sub("", seg1)
        skid_hits = [m.group(0).lower() for m in SKID_SLIDE.finditer(cleaned_slide_txt)]
        if len(skid_hits) >= 2:
            out.append((
                "FAIL",
                f"偵測到 {len(skid_hits)} 處地面滑行詞（{', '.join(skid_hits)}）—— 濫用 slide/skid 會誘發角色腳不沾地溜冰步！請改用離散步態動詞（plants boot / drives off / steps / pivots）"
            ))
            fail += 1
        elif len(skid_hits) == 1:
            out.append((
                "WARN",
                f"含 1 處滑行詞（{skid_hits[0]}），請確認僅用於重擊硬直短促退步，而非主動進攻滑行"
            ))
            warn += 1

        if prof == "fight":
            floor_refs = re.findall(
                r"\b(boots?|platform|floor|ground|deck|metal\s+plates?|bronze\s+seam|sinks?\s+(?:his|her)\s+stance)\b",
                seg1,
                re.I,
            )
            down_strikes = re.findall(
                r"\b(plunging\s+downward|low\s+upward\s+cut|slams?\s+[^.;]{0,40}\bonto\s+the\s+(?:brass|bronze|platform|floor|deck))\b",
                seg1,
                re.I,
            )
            if down_strikes:
                out.append((
                    "WARN",
                    f"偵測到向下撲擊/砸地高危句（{', '.join(set(x.lower() for x in down_strikes))}）—— H3 極易畫成彎腰捶地板爆火花！建議改鎖胸肩高度（at chest/shoulder height）與垂直牆面受擊"
                ))
                warn += 1
            if len(floor_refs) >= 6:
                out.append((
                    "WARN",
                    f"近戰描述出現 {len(floor_refs)} 次靴底/平台地板詞 —— 易迫使鏡頭拉成俯視地板遠景導致短兵構不到人而砍地板！建議改用 tight waist-up / thigh-up two-shot within arm's reach"
                ))
                warn += 1

    # 大招光束「倒退拉鏡反向錯覺（Reverse-Beam Pullback）」檢核
    for idx, sb in enumerate(shot_blocks):
        s_num = int(sb.group(1))
        s_txt = sb.group(2)
        if (
            re.search(r"\b(beam|cannon|ray|torrent)\b", s_txt, re.I)
            and re.search(r"\bpulls?\s+(?:far\s+)?back\b", s_txt, re.I)
            and re.search(r"\b(pulverized|shattered|cratered|ruined)\b", s_txt, re.I)
        ):
            out.append((
                "WARN",
                f"[Shot {s_num}] 光束鏡同時含 'pulls back' 與已毀滅狀態詞 —— 鏡頭從爆炸靶心倒退拉回發射者手部，視覺上會像衝擊波打完倒吸回手裡！建議改用 locked aerial shot 並描述波環 away from hand toward target 引爆"
            ))
            warn += 1

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
    if close_ups and not rules.get("skip_face"):
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
    if not MUSCLE.search(body) and not rules.get("skip_face"):
        out.append(("WARN", "全篇沒有任何表情肌肉動作"
                            "（brow/jaw/teeth/lip/throat/breath…），"
                            "角色會全程面無表情"))
        warn += 1
    if len(FAKE_FACE.findall(body)) >= 2 and not MUSCLE.search(body) and not rules.get("skip_face"):
        out.append(("WARN", "用眼睛形狀代替表情（如 irises narrow），"
                            "那不是肌肉動作"))
        warn += 1
    eff_face = read_face_style(raw, body, face_style)
    if eff_face == "aesthetic" and not rules.get("skip_face"):
        harsh = sorted(set(m.group(0).lower() for m in HARSH_FACE.finditer(body)))
        if harsh:
            out.append(("WARN", f"偵測到美型臉過激詞（{', '.join(harsh)}），"
                                "國漫／AI 漫劇角色易被 H3 拉扭曲；建議改 A 檔微表情詞"
                                "（或改傳 --face-style rugged）"))
            warn += 1
# 招式多樣性：看「刀路佔比」，不是絕對次數（長提示詞刀路次數自然高）
    counts = {k: len(re.findall(v, body, re.I)) for k, v in MOVE_CATS.items()}
    blade = counts.get("blade", 0)
    others = sum(v for k, v in counts.items() if k != "blade")
    total = blade + others
    if total >= 8 and not rules.get("skip_moves") is True:
        blade_pct = 100.0 * blade / total
        # 15 秒以上容許刀路 55%；8 秒容許 60%（短片段沒空間放全套）
        cap = rules.get("blade_cap", 55.0 if (duration and duration >= 12) else 60.0)
        if blade_pct > cap:
            out.append(("WARN",
                        f"刀路佔比 {blade_pct:.0f}%（刀路 {blade} / 其他 {others}，"
                        f"上限 {cap:.0f}%）—— 招式單一。"
                        "加踢擊/拳肘/摔投/下盤/擒拿，"
                        "見 references/choreography.md 的配額表"))
            warn += 1
        skip_set = rules.get("skip_moves") if isinstance(rules.get("skip_moves"), set) else set()
        if counts.get("throw", 0) == 0 and blade >= 4 and "throw" not in skip_set:
            out.append(("WARN", "完全沒有摔投/擒拿 —— 距離不會變化，"
                                "容易變成兩人站著互砍"))
            warn += 1
        if counts.get("sweep", 0) == 0 and "sweep" not in skip_set:
            out.append(("WARN", "完全沒有下盤/絆 —— 全程在同一個高度打"))
            warn += 1

    # 雙語時間線同步檢查（--check-sync）
    if check_sync:
        zh = extract_zh_part(strip_meta(raw))
        if not zh:
            out.append(("WARN", "啟用 --check-sync 但未偵測到中文導演母稿"))
            warn += 1
        else:
            zh_ts = [int(m.group(1)) * 60 + float(m.group(2))
                     for m in re.finditer(r"(?:At\s+|切鏡\s*[:：]?\s*|[\[(【])(\d{2}):(\d{2}\.\d{1,3})", zh)]
            # [Shot 1] 在英文官方規格中不寫 00:00.000，中文母稿若標了 00:00.000 則略過首項再比對後續切點
            if zh_ts and zh_ts[0] == 0.0 and (not stamps or stamps[0] > 0.0):
                zh_ts = zh_ts[1:]
            if zh_ts and [round(x, 2) for x in zh_ts] != [round(x, 2) for x in stamps]:
                out.append(("FAIL", f"中英文切鏡時間碼不同步：中文 {zh_ts} vs 英文 {stamps}"))
                fail += 1

    # 字數預算與送件字元上限
    words = len(body.split())
    chars = len(body)
    default_limit = (900 if five_part else 820) if is_ref else (900 if five_part else 520)
    limit = rules.get("word_cap") or default_limit
    if words > limit:
        out.append(("WARN", f"字數 {words} 超過預算 {limit}，末段約束易失效")); warn += 1

    if five_part:
        for lv, msg in check_five_part(body, fields):
            out.append((lv, msg))
            if lv == "FAIL":
                fail += 1
            else:
                warn += 1
        if not WEIGHT.search(body):
            out.append(("WARN", "五小節版沒有任何重心／支撐描述"
                                "（weight/heels/hips/base…）—— 打擊感會偏軟"))
            warn += 1

    if chars > 7500:
        out.append(("WARN", f"字元數 {chars} 超過送件端上限 7500")); warn += 1

    print(f"\n{os.path.basename(path)}  mode={mode}  profile={prof}  shots={nshot}  words={words}  "
          f"chars={chars}  duration={duration or '?'}")
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
    ap.add_argument("--profile", default="auto",
                    choices=["auto"] + list(PROFILES),
                    help="打法模式；auto = 讀檔頭 #!profile，沒有就 fight")
    ap.add_argument("--check-sync", action="store_true",
                    help="雙語檔案額外檢查中文母稿與英文 H3 的切鏡時間碼同步")
    ap.add_argument("--face-style", default="auto", choices=["auto", "aesthetic", "rugged"],
                    help="表情顏值檔：auto=國漫/漫劇/仙俠自動走 aesthetic 美型檢核；aesthetic=強制檢核過激毀臉詞；rugged=粗獷寫實/野獸")
    ap.add_argument("--strict-physics", action="store_true",
                    help="啟用 v3.0 嚴格物理防滑與防打地板檢核（亦可在檔頭寫 #!physics: strict）")
    ap.add_argument("--five-part", action="store_true",
                    help="啟用每鏡五小節（Camera/Motion/Performance/Light/Sound）與重心檢核")
    a = ap.parse_args()

    files = [a.file] if a.file else []
    if a.dir:
        files += sorted(glob.glob(os.path.join(a.dir, "*.md")) +
                        glob.glob(os.path.join(a.dir, "*.txt")))
    if not files:
        ap.print_help()
        return 1

    total = sum(check(f, a.duration, a.profile, a.check_sync, a.face_style, a.strict_physics, a.five_part) for f in files)
    print(f"\n合計 FAIL {total} 項")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
