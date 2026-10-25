"""impact_frame.py 的端到端測試（用 ffmpeg 合成的測試片，不需要 H3）。

執行：python -m unittest discover -s tests -v
沒有 ffmpeg 時自動略過。
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "scripts", "impact_frame.py")
HAS_FFMPEG = shutil.which("ffmpeg") and shutil.which("ffprobe")


def sh(*cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise AssertionError(f"{' '.join(cmd)}\n{r.stdout}\n{r.stderr}")
    return r.stdout


def streams(path):
    info = json.loads(sh("ffprobe", "-v", "error", "-count_frames", "-show_streams",
                         "-of", "json", path))
    return {s["codec_type"]: s for s in info["streams"]}


def yavg(path):
    out = sh("ffmpeg", "-v", "error", "-i", path, "-vf",
             "signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-", "-an", "-f", "null", "-")
    return [float(l.split("=")[1]) for l in out.splitlines() if "YAVG=" in l]


@unittest.skipUnless(HAS_FFMPEG, "需要 ffmpeg")
class ImpactFrameTool(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="impact_test_")
        d = cls.tmp
        # 主片：4 秒 960×544＋音軌；1.00–1.83 s 有 4 張「衝擊幀」各 5 幀（模擬 P2 生成片）
        cls.main = os.path.join(d, "main.mp4")
        sh("ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=s=960x544:r=24:d=4",
           "-f", "lavfi", "-i", "sine=f=440:d=4", "-filter_complex",
           "[0:v]drawbox=c=white:t=fill:enable='between(n,24,28)',"
           "drawbox=c=black:t=fill:enable='between(n,29,33)',"
           "drawbox=c=0xFF4400:t=fill:enable='between(n,34,38)',"
           "drawbox=c=0x202020:t=fill:enable='between(n,39,43)',format=yuv420p[v]",
           "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-c:a", "aac", "-shortest", cls.main)
        # 衝擊片：解析度比主片小（640×360），中間一格全白
        cls.small = os.path.join(d, "small.mp4")
        sh("ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=s=640x360:r=24:d=1",
           "-vf", "drawbox=c=white:t=fill:enable='eq(n,12)',format=yuv420p",
           "-c:v", "libx264", cls.small)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_help(self):
        out = sh(sys.executable, SCRIPT, "--help")
        for word in ("find-peak", "ramp", "composite", "gen"):
            self.assertIn(word, out)

    def test_find_peak_locates_burst(self):
        out = sh(sys.executable, SCRIPT, "find-peak", "--in", self.main)
        self.assertIn("幀 24–", out)

    def test_ramp_speeds_burst_and_keeps_audio(self):
        out = os.path.join(self.tmp, "ramped.mp4")
        sh(sys.executable, SCRIPT, "ramp", "--in", self.main, "--seg", "1.00-1.84:5",
           "--seg", "1.84-3.00:1.5", "--out", out)
        st = streams(out)
        self.assertIn("audio", st)
        self.assertAlmostEqual(float(st["video"]["duration"]), 2.96, delta=0.1)
        ys = yavg(out)
        # 4 張衝擊幀各 5 幀 → 5× 後各 1 幀：白、黑、橘、深灰
        self.assertGreater(ys[24], 200)
        self.assertLess(ys[25], 30)
        self.assertLess(abs(ys[28] - ys[30]), 5)   # 已回到正常畫面

    def test_composite_scales_keeps_audio_and_black_tail(self):
        out = os.path.join(self.tmp, "comp.mp4")
        log = sh(sys.executable, SCRIPT, "composite", "--main", self.main, "--impact", self.small,
                 "--insert", "60:auto:2", "--black", "62:3", "--out", out)
        self.assertIn("已縮放裁切", log)
        st = streams(out)
        self.assertIn("audio", st)
        self.assertEqual(int(st["video"]["nb_read_frames"]), 96)
        self.assertEqual((st["video"]["width"], st["video"]["height"]), (960, 544))
        ys = yavg(out)
        self.assertGreater(ys[60], 200)   # 整幀變白＝有縮放蓋滿，不是只蓋左上角
        self.assertGreater(ys[61], 200)
        self.assertLess(ys[62], 30)
        self.assertLess(ys[64], 30)
        self.assertGreater(ys[65], 60)

    def test_gen_without_token_exits_cleanly(self):
        env = {k: v for k, v in os.environ.items()
               if k not in ("H3_TOKEN", "FREEVIDEO_TOKEN", "H3_TOKEN_FILE", "FREEVIDEO_TOKEN_FILE")}
        prompt = os.path.join(self.tmp, "p.txt")
        with open(prompt, "w", encoding="utf-8") as fh:
            fh.write("x")
        r = subprocess.run([sys.executable, SCRIPT, "gen", "--prompt", prompt, "--out",
                            os.path.join(self.tmp, "x.mp4")], capture_output=True, text=True, env=env)
        self.assertEqual(r.returncode, 2)
        self.assertIn("token", r.stderr)
        self.assertNotIn("Traceback", r.stderr)


if __name__ == "__main__":
    unittest.main()
