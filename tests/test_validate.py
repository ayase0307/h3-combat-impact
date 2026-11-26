#!/usr/bin/env python3
"""validate_prompt.py 的回歸測試。

規則（來自 2026-11-18 的 T5 校準）：
  1. 好樣本（examples/）FAIL 必須是 0 —— 檢查器不能把自家出過片的提示詞判死。
  2. 壞樣本（tests/fixtures/bad/）FAIL 必須 ≥1 —— 每個都是已知會壞的寫法。
  3. 好樣本的 WARN 數量固定；多一個少一個都要在這裡看到，避免規則漂移。

跑法：python -m unittest discover -s tests -v
"""

import os
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VALIDATOR = os.path.join(ROOT, "scripts", "validate_prompt.py")
EXAMPLES = os.path.join(ROOT, "examples")
V3 = os.path.join(EXAMPLES, "v3-manju")
BAD = os.path.join(ROOT, "tests", "fixtures", "bad")

# 子程序一律以 UTF-8 輸出，避免 Windows 管線預設 cp950 讓中文訊息比對失敗
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")

# 檔名 -> (標註時長, 允許的 WARN 數量)
GOOD = {
    "six-beat-single-hit.txt": (8, 0),
    "continuous-brawl.txt": (8, 0),
    "ultra-speed-drone.txt": (8, 0),
    "blade-light-21x9.txt": (8, 0),
    "force-field-explosion.txt": (5, 0),
    "ink-wash.txt": (5, 0),
    "facial-performance.txt": (5, 0),
    "impact-frame-source.txt": (4, 1),
    "impact-frame-inline.txt": (8, 0),
    "impact-frame-screenplay.txt": (7, 0),
    "anime-ref2va-part1.txt": (15, 0),
    "anime-ref2va-part2.txt": (15, 1),
    # 單人招牌技能長稿：字數超預算與無下盤屬已知取捨（見 docs/research/2026-11-26-legacy-examples-audit.md）
    "bloodmoon-ultimate-ref2va.txt": (10, 2),
    "jade-rift-summon-ref2va.txt": (10, 1),
}

# v3 旗艦雙語劇本：全部 --check-sync --strict-physics 0 FAIL
V3_FLAGSHIPS = {
    "orig01_v13_crimson_frost_blade_duel.txt": 15,
    "orig02_bamboo_lantern_umbrella_vs_spear.txt": 15,
    "rep01_thunder_cleave.txt": 15,
    "rep02_ink_flame_sea.txt": 15,
    "rep03_jade_hammer_dragon.txt": 15,
    "rep04_v4_myriad_swords_cannon.txt": 15,
    "rep05_void_vs_peacock.txt": 15,
    "ult01_brush_seal_army.txt": 15,
    "ult02_lunar_prism_domain.txt": 15,
}

BAD_FILES = sorted(f for f in os.listdir(BAD) if f.endswith(".txt"))
# 需要時長才能觸發的規則（末鏡占比）在這裡標註
BAD_DURATIONS = {"07_last_shot_long.txt": 8}

ABSTRACT_MSG = "空泛打鬥句"
SPIN_MSG = "翻轉／旋轉詞"


def run(path, duration=None, *extra):
    cmd = [sys.executable, VALIDATOR, path]
    if duration:
        cmd += ["--duration", str(duration)]
    cmd += list(extra)
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=ENV)
    return p.returncode, p.stdout + p.stderr


def run_text(text, duration=None, *extra):
    """把合成提示詞寫進暫存檔再驗證（WARN-only 樣本不能放進 fixtures/bad）。"""
    fd, path = tempfile.mkstemp(suffix=".txt")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        return run(path, duration, *extra)
    finally:
        os.remove(path)


def t2va(shot1, shot2, shot3, t2="00:01.200", t3="00:02.400"):
    """三鏡 T2VA 骨架：Shot 1 無時間碼，Shot 2/3 依 t2/t3 切。"""
    return (
        f"integrated_multimodal_description: [Shot 1] 3D CG wuxia courtyard at dusk. {shot1}\n\n"
        f"[Shot 2] At {t2}, the camera cuts to a medium shot. {shot2}\n\n"
        f"[Shot 3] At {t3}, the camera cuts to a wide shot. {shot3}\n"
        "overall_soundscape: Steel clashes, boots on stone, sharp breaths.\n"
        "non_diegetic_music: Driving taiko.\n"
    )


PLAIN = "She plants her heel and drives a palm into his chest; his jaw tightens."


class TestGoodSamples(unittest.TestCase):
    def test_no_fail_and_warn_budget(self):
        for name, (duration, max_warn) in GOOD.items():
            with self.subTest(name=name):
                code, out = run(os.path.join(EXAMPLES, name), duration)
                self.assertEqual(code, 0, f"{name} 應該 FAIL 0 項\n{out}")
                warns = re.findall(r"^\s*\[WARN\]", out, re.M)
                self.assertLessEqual(len(warns), max_warn,
                                     f"{name} WARN {len(warns)} 個，超過預算 {max_warn}\n{out}")

    def test_v4_showcase_zero_fail(self):
        v4_dir = os.path.join(EXAMPLES, "v4-showcase")
        specs = {
            "blade-light-21x9-v4.txt": 8.0,
            "ultra-speed-drone-v4.txt": 8.0,
            "ink-wash-v4.txt": 5.2,
            "facial-performance-v4.txt": 6.6,
            "bloodmoon-ultimate-ref2va-v4.txt": 10.1,
            "jade-rift-summon-ref2va-v4.txt": 10.1,
        }
        for name, dur in specs.items():
            with self.subTest(name=name):
                code, out = run(os.path.join(v4_dir, name), dur)
                self.assertEqual(code, 0, f"v4-showcase/{name} 應該 FAIL 0 項\n{out}")


class TestBadSamples(unittest.TestCase):
    def test_each_bad_file_fails(self):
        self.assertGreaterEqual(len(BAD_FILES), 5, "壞樣本至少要 5 份")
        for name in BAD_FILES:
            with self.subTest(name=name):
                code, out = run(os.path.join(BAD, name), BAD_DURATIONS.get(name))
                self.assertEqual(code, 1, f"{name} 應該 FAIL ≥1 項\n{out}")
                self.assertIn("[FAIL]", out, f"{name} 沒有 FAIL 訊息\n{out}")


class TestProfiles(unittest.TestCase):
    def test_material_skips_face_warns(self):
        code, out = run(os.path.join(EXAMPLES, "impact-frame-source.txt"), 4)
        self.assertNotIn("表情肌肉", out)

    def test_ultra_skips_throw_sweep(self):
        code, out = run(os.path.join(EXAMPLES, "ultra-speed-drone.txt"), 8)
        self.assertNotIn("摔投", out)
        self.assertNotIn("下盤", out)

    def test_force_profile_restores_warns(self):
        # 明確指定 fight 時，ultra 本來被略過的警告要回來
        code, out = run(os.path.join(EXAMPLES, "ultra-speed-drone.txt"), 8, "--profile", "fight")
        self.assertIn("摔投", out)


class TestV2BilingualSync(unittest.TestCase):
    def test_v2_caseA_bilingual_sync_pass(self):
        code, out = run(os.path.join(EXAMPLES, "v2-demo", "caseA_duel.txt"), 15, "--check-sync")
        self.assertEqual(code, 0, out)
        # 舊 v2 caseA 含美型臉過激詞，應在 auto(aesthetic) 觸發 WARN
        self.assertIn("美型臉過激詞", out)

    def test_v2_caseB_bilingual_sync_pass(self):
        code, out = run(os.path.join(EXAMPLES, "v2-demo", "caseB_beast.txt"), 15, "--check-sync")
        self.assertEqual(code, 0, out)

    def test_v3_manju_aesthetic_zero_warn(self):
        for fname, dur in (("caseA_manju_duel.txt", 15), ("caseA_manju_8s.txt", 8)):
            with self.subTest(name=fname):
                code, out = run(os.path.join(V3, fname), dur, "--check-sync")
                self.assertEqual(code, 0, out)
                self.assertNotIn("[WARN]", out, out)

    def test_v3_flagships_strict_physics_pass(self):
        for fname, dur in V3_FLAGSHIPS.items():
            with self.subTest(name=fname):
                code, out = run(os.path.join(V3, fname), dur, "--check-sync", "--strict-physics")
                self.assertEqual(code, 0, out)
                self.assertNotIn("中英文切鏡時間碼不同步", out, out)
                self.assertNotIn("未偵測到中文導演母稿", out, out)


class TestAntiBreakupRules(unittest.TestCase):
    """v4.0 防動態破圖：抽象打鬥句與短鏡翻轉堆疊（只 WARN，不 FAIL）。"""

    def test_abstract_fight_without_body_mechanics_warns(self):
        text = t2va("The two warriors attack fiercely in an epic battle.", PLAIN, PLAIN)
        code, out = run_text(text, 3.4)
        self.assertEqual(code, 0, out)
        self.assertIn(ABSTRACT_MSG, out)
        self.assertIn("[Shot 1]", out)

    def test_abstract_fight_with_body_mechanics_passes(self):
        text = t2va("They trade blows: she pivots on her lead heel and drives an elbow into his ribs.",
                    PLAIN, PLAIN)
        code, out = run_text(text, 3.4)
        self.assertNotIn(ABSTRACT_MSG, out)

    def test_epic_camera_wording_is_not_abstract_fight(self):
        text = t2va("An epic ultra-wide low shot of the storm.", PLAIN, PLAIN)
        code, out = run_text(text, 3.4)
        self.assertNotIn(ABSTRACT_MSG, out)

    def test_spin_stack_in_short_shot_warns(self):
        spins = "She spins, flips, somersaults and whirls past his spear."
        text = t2va(PLAIN, spins, PLAIN)  # Shot 2 長 1.2s
        code, out = run_text(text, 3.4)
        self.assertEqual(code, 0, out)
        self.assertIn(SPIN_MSG, out)
        self.assertIn("[Shot 2]", out)

    def test_three_spins_in_short_shot_passes(self):
        text = t2va(PLAIN, "She spins, flips and whirls past his spear.", PLAIN)
        code, out = run_text(text, 3.4)
        self.assertNotIn(SPIN_MSG, out)

    def test_spin_stack_at_exact_threshold_passes(self):
        spins = "She spins, flips, somersaults and whirls past his spear."
        text = t2va(PLAIN, spins, PLAIN, t2="00:01.000", t3="00:02.500")  # Shot 2 恰 1.5s
        code, out = run_text(text, 3.5)
        self.assertNotIn(SPIN_MSG, out)

    def test_flagship_benchmarks_emit_no_anti_breakup_warn(self):
        for fname in ("orig01_v13_crimson_frost_blade_duel.txt", "rep04_v4_myriad_swords_cannon.txt"):
            with self.subTest(name=fname):
                code, out = run(os.path.join(V3, fname), 15, "--check-sync", "--strict-physics")
                self.assertEqual(code, 0, out)
                self.assertNotIn(ABSTRACT_MSG, out)
                self.assertNotIn(SPIN_MSG, out)


class TestScreenplayMode(unittest.TestCase):
    GOOD_SP = (
        "[參考鎖]\n<Picture 1>=庭院：只取石板地。\n\n"
        "[畫風]\n正常畫面：超精細 3DCG。不是二次元平塗。\n\n"
        "[本段]\n4 秒，兩個鏡頭，機位固定。\n"
        "0.0-2.0秒｜她後腳蹬地搶進半步，撩斬對方前膝。\n"
        "2.0-4.0秒｜他橫棍硬接，被震退一步。\n\n"
        "[聲音]\n雨聲；兵器撞擊一聲。沒有人說話，嘴唇閉著；沒有配樂。\n\n"
        "[連續性] 首態：兩人相隔半步 → 尾態：他退了一步。\n"
        "[硬約束] 無字幕、文字、水印；畫面裡只有這兩個人。\n"
    )

    def test_screenplay_example_passes(self):
        code, out = run(os.path.join(EXAMPLES, "impact-frame-screenplay.txt"), 7)
        self.assertEqual(code, 0, out)
        self.assertIn("mode=Screenplay", out)

    def test_minimal_screenplay_passes_clean(self):
        code, out = run_text(self.GOOD_SP, 4)
        self.assertEqual(code, 0, out)
        self.assertNotIn("[WARN]", out, out)

    def test_screenplay_missing_section_fails(self):
        code, out = run_text(self.GOOD_SP.replace("[硬約束]", "[備註]"), 4)
        self.assertEqual(code, 1, out)
        self.assertIn("[硬約束]", out)

    def test_screenplay_timeline_gap_fails(self):
        code, out = run_text(self.GOOD_SP.replace("2.0-4.0秒", "2.5-4.0秒"), 4)
        self.assertEqual(code, 1, out)
        self.assertIn("不連續", out)

    def test_screenplay_overrun_fails(self):
        code, out = run_text(self.GOOD_SP, 3)
        self.assertEqual(code, 1, out)
        self.assertIn("超出時長", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
