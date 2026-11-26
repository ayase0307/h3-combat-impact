#!/usr/bin/env python3
"""render_v3_flagship.py 的 JOBS 配置回歸測試：讓「雙軌秒數精準對齊劇本切點」成為可檢查的事實。

規則：
  1. 9 套全部是 P7/P8/P9；P9 二採 off（左眼 5.0 實證），P7/P8 二採 phase-motion。
  2. 所有區段都落在 0–15 秒、t0 < t1；慢變力場軌（anchor/burst/closeup）長度 ≥ 0.5s，
     快切軌（hitstop/hit）長度 ≤ 0.4s。
  3. v4.0 升級的 6 套：慢變力場軌邊界必須在劇本切點（或 `beats` 鏡內相位點）±0.4s 內。
  4. 每個臉部特寫鏡至少被一條負軌（anchor / hitstop / closeup）覆蓋。
  5. P9 正軌上限 +0.29（P9 常駐 motion 0.50 + storm 洩漏 0.19，總等效不得破 +0.98）。

跑法：python -m unittest discover -s tests -v
"""

import importlib.util
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = importlib.util.spec_from_file_location(
    "render_v3_flagship", os.path.join(ROOT, "scripts", "render_v3_flagship.py"))
FLAGSHIP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FLAGSHIP)
JOBS = FLAGSHIP.JOBS
PROMPTS = os.path.join(ROOT, "examples", "v3-manju")

SECONDS = 15.0
EDGE_TOL = 0.4
UPGRADED = ("rep01", "rep02", "rep03", "orig02", "ult01", "ult02")
SLOW_KEYS = ("anchors", "bursts", "closeups")
FAST_KEYS = ("hitstops", "hits")
NEG_KEYS = ("anchors", "hitstops", "closeups")
P9_BURST_CAP = 0.29

TS = re.compile(r"At\s+(\d{2}):(\d{2}\.\d{2,3})")
SHOT = re.compile(r"\[Shot (\d+)\](.*?)(?=\[Shot \d+\]|overall_soundscape:|\Z)", re.S)


def spans(cfg, key):
    out = []
    for spec in cfg.get(key, []):
        parts = spec.split(":")
        out.append((float(parts[0]), float(parts[1]), float(parts[2]) if len(parts) > 2 else None))
    return out


def prompt_text(cfg):
    with open(os.path.join(PROMPTS, cfg["prompt"]), encoding="utf-8") as fh:
        return fh.read()


def cuts(cfg):
    return [int(m.group(1)) * 60 + float(m.group(2)) for m in TS.finditer(prompt_text(cfg))]


def shot_windows(cfg):
    """回傳 [(t0, t1, shot_text)]，只取英文 H3 區塊的 detailed_description。"""
    text = prompt_text(cfg)
    desc = text[text.find("detailed_description:"):]
    blocks = [m.group(2) for m in SHOT.finditer(desc)]
    starts = [0.0] + cuts(cfg)
    ends = starts[1:] + [SECONDS]
    return list(zip(starts, ends, blocks))


class TestFlagshipJobs(unittest.TestCase):
    def test_all_suites_use_dual_rail_presets(self):
        for key, cfg in JOBS.items():
            with self.subTest(suite=key):
                if key in ("ult01", "ult02"):
                    # 純結印圓陣類經 GPU 實測維持 P5（80% 歸零防萬花筒）+ hires-dials off 保住符陣清晰度
                    self.assertEqual(cfg["preset"], "P5")
                    self.assertEqual(cfg.get("hires_dials"), "off")
                else:
                    self.assertIn(cfg["preset"], ("P7", "P8", "P9"))
                    want = "off" if cfg["preset"] == "P9" else "phase-motion"
                    self.assertEqual(cfg.get("hires_dials"), want)
                self.assertIn("hits", cfg, "print 行會讀 cfg['hits']")
                self.assertTrue(os.path.exists(os.path.join(PROMPTS, cfg["prompt"])))

    def test_span_ranges_and_lengths(self):
        for key, cfg in JOBS.items():
            for k in SLOW_KEYS + FAST_KEYS:
                for t0, t1, _ in spans(cfg, k):
                    with self.subTest(suite=key, rail=k, span=(t0, t1)):
                        self.assertTrue(0.0 <= t0 < t1 <= SECONDS)
                        if k in SLOW_KEYS:
                            self.assertGreaterEqual(t1 - t0, 0.5, "慢變力場盤嚴禁 <0.5s 碎拍")
                        else:
                            self.assertLessEqual(t1 - t0, 0.4, "頓幀／閃幀只畫窄脈衝")

    def test_upgraded_slow_rail_edges_align_to_cuts_or_beats(self):
        for key in UPGRADED:
            cfg = JOBS[key]
            marks = [0.0, SECONDS] + cuts(cfg) + list(cfg.get("beats", []))
            for k in SLOW_KEYS:
                for t0, t1, _ in spans(cfg, k):
                    for edge in (t0, t1):
                        with self.subTest(suite=key, rail=k, edge=edge):
                            gap = min(abs(edge - m) for m in marks)
                            self.assertLessEqual(gap, EDGE_TOL,
                                                 f"{key} {k} 邊界 {edge}s 距最近切點／相位點 {gap:.2f}s")

    def test_upgraded_beats_fall_inside_shots(self):
        for key in UPGRADED:
            cfg = JOBS[key]
            cut_list = cuts(cfg)
            for b in cfg.get("beats", []):
                with self.subTest(suite=key, beat=b):
                    self.assertTrue(0.0 < b < SECONDS)
                    self.assertGreater(min(abs(b - c) for c in [0.0] + cut_list), EDGE_TOL,
                                       "beat 應是鏡內相位點；貼著切點就直接用切點")

    def test_face_closeups_have_negative_rail(self):
        for key in UPGRADED:
            cfg = JOBS[key]
            neg = [s for k in NEG_KEYS for s in spans(cfg, k)]
            for t0, t1, txt in shot_windows(cfg):
                if not (re.search(r"close-up", txt) and re.search(r"\b(face|expression|brows)\b", txt)):
                    continue
                with self.subTest(suite=key, shot=(t0, t1)):
                    self.assertTrue(any(a < t1 and b > t0 for a, b, _ in neg),
                                    f"{key} 臉部特寫 {t0}-{t1}s 沒有任何負軌鎖臉")

    def test_p9_burst_within_ground_budget(self):
        for key, cfg in JOBS.items():
            if cfg["preset"] != "P9":
                continue
            for t0, t1, s in spans(cfg, "bursts"):
                with self.subTest(suite=key, span=(t0, t1)):
                    self.assertLessEqual(abs(s if s is not None else 0.65), P9_BURST_CAP)


if __name__ == "__main__":
    unittest.main(verbosity=2)
