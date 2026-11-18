#!/usr/bin/env python3
"""validate_prompt.py 的回歸測試。

規則（來自 2026-11-18 的 T5 校準）：
  1. 好樣本（examples/）FAIL 必須是 0 —— 檢查器不能把自家出過片的提示詞判死。
  2. 壞樣本（tests/fixtures/bad/）FAIL 必須 ≥1 —— 每個都是已知會壞的寫法。
  3. 好樣本的 WARN 數量固定；多一個少一個都要在這裡看到，避免規則漂移。

跑法：python tests/test_validate.py
"""

import os
import re
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VALIDATOR = os.path.join(ROOT, "scripts", "validate_prompt.py")
EXAMPLES = os.path.join(ROOT, "examples")
BAD = os.path.join(ROOT, "tests", "fixtures", "bad")

# 檔名 -> (標註時長, 允許的 WARN 數量)
GOOD = {
    "six-beat-single-hit.txt": (8, 0),
    "continuous-brawl.txt": (8, 1),
    "ultra-speed-drone.txt": (8, 0),
    "blade-light-21x9.txt": (8, 0),
    "force-field-explosion.txt": (5, 0),
    "ink-wash.txt": (5, 0),
    "facial-performance.txt": (5, 0),
    "impact-frame-source.txt": (4, 1),
    "anime-ref2va-part1.txt": (15, 0),
    "anime-ref2va-part2.txt": (15, 1),
}

BAD_FILES = sorted(f for f in os.listdir(BAD) if f.endswith(".txt"))
# 需要時長才能觸發的規則（末鏡占比）在這裡標註
BAD_DURATIONS = {"07_last_shot_long.txt": 8}


def run(path, duration=None):
    cmd = [sys.executable, VALIDATOR, path]
    if duration:
        cmd += ["--duration", str(duration)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, p.stdout + p.stderr


class TestGoodSamples(unittest.TestCase):
    def test_no_fail_and_warn_budget(self):
        for name, (duration, max_warn) in GOOD.items():
            with self.subTest(name=name):
                code, out = run(os.path.join(EXAMPLES, name), duration)
                self.assertEqual(code, 0, f"{name} 應該 FAIL 0 項\n{out}")
                warns = re.findall(r"^\s*\[WARN\]", out, re.M)
                self.assertLessEqual(len(warns), max_warn,
                                     f"{name} WARN {len(warns)} 個，超過預算 {max_warn}\n{out}")


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
        cmd = [sys.executable, VALIDATOR, os.path.join(EXAMPLES, "ultra-speed-drone.txt"),
               "--duration", "8", "--profile", "fight"]
        p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        self.assertIn("摔投", p.stdout + p.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
