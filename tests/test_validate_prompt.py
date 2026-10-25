"""validate_prompt.py 的回歸測試。

執行：python -m unittest discover -s tests -v   （不需要 pytest）
"""
import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "scripts", "validate_prompt.py")
FIX = os.path.join(ROOT, "tests", "fixtures")

sys.path.insert(0, os.path.join(ROOT, "scripts"))
import validate_prompt as vp  # noqa: E402


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def run(name, *args):
    r = subprocess.run([sys.executable, SCRIPT, os.path.join(FIX, name), *args],
                       capture_output=True, text=True)
    return r.returncode, r.stdout


class ImpactRules(unittest.TestCase):
    def test_ultimate_without_impact_warns(self):
        code, out = run("ult_no_impact.txt", "--duration", "8")
        self.assertEqual(code, 0)
        self.assertIn("[IMPACT] 有「ultimate」", out)

    def test_ultimate_with_plan_outside_block_passes(self):
        code, out = run("ult_with_plan.md", "--duration", "8")
        self.assertEqual(code, 0)
        self.assertNotIn("[IMPACT]", out)

    def test_ultimate_with_plan_flag_passes(self):
        code, out = run("ult_no_impact.txt", "--duration", "8", "--impact-plan", "P3")
        self.assertNotIn("沒有任何衝擊幀", out)

    def test_manga_inline_fails(self):
        code, out = run("manga_inline.txt", "--duration", "8")
        self.assertEqual(code, 1)
        self.assertIn("主片同段寫漫畫格", out)
        self.assertIn("then one frame of black", out)
        self.assertIn("寫了幀數控制", out)

    def test_manga_in_impact_clip_is_exempt(self):
        code, out = run("manga_inline.txt", "--duration", "8", "--impact-clip")
        self.assertEqual(code, 0)
        self.assertNotIn("主片同段寫漫畫格", out)

    def test_vague_flash_and_continuous_shake(self):
        code, out = run("flash_nocount.txt", "--duration", "8")
        self.assertIn("閃白用模糊時長", out)
        self.assertIn("閃白配持續震屏", out)

    def test_slow_words(self):
        code, out = run("slow_words.txt", "--duration", "6")
        self.assertEqual(code, 0)
        for w in ("near-freeze", "hangs poised", "like a meteor", "for half a second"):
            self.assertIn(w, out)
        self.assertIn("slowly／gradually", out)

    def test_good_p2_passes_clean(self):
        code, out = run("good_p2.txt", "--duration", "5")
        self.assertEqual(code, 0)
        self.assertIn("[PASS]", out)

    def test_impact_clip_passes(self):
        code, out = run("impact_clip.txt", "--duration", "4", "--impact-clip")
        self.assertEqual(code, 0)
        self.assertIn("[PASS]", out)

    def test_metronome_spacing_warns(self):
        code, out = run("metronome.txt", "--duration", "5.5")
        self.assertEqual(code, 0)
        self.assertIn("節拍器", out)


class WordBudget(unittest.TestCase):
    """字數預算要與 SKILL.md §5、output-format.md 同一張表。"""

    def test_table(self):
        self.assertEqual(vp.word_limit(8, False), 520)
        self.assertEqual(vp.word_limit(4, False), 520)
        self.assertEqual(vp.word_limit(15, False), 700)
        self.assertEqual(vp.word_limit(9, False), 700)
        self.assertEqual(vp.word_limit(8, True), 820)
        self.assertEqual(vp.word_limit(15, True), 1000)
        self.assertEqual(vp.word_limit(None, False), 520)

    def test_skill_md_states_same_numbers(self):
        skill = read(os.path.join(ROOT, "SKILL.md"))
        self.assertIn("4–8 秒 ≤520 字、9–15 秒 ≤700 字；Ref2VA 再 +300", skill)


class RepoExamples(unittest.TestCase):
    """repo 內的提示詞範例不得再出現被推翻的寫法。"""

    def test_examples_have_no_slow_words(self):
        ex = os.path.join(ROOT, "examples")
        for name in sorted(os.listdir(ex)):
            body = read(os.path.join(ex, name))
            self.assertIsNone(vp.SLOW.search(body), f"{name} 含 H3 慢詞")


if __name__ == "__main__":
    unittest.main()
