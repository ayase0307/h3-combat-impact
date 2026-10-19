#!/usr/bin/env python3
"""量測「光影華麗度」：每鏡有沒有光影事件。

指標：
- light_event_rate：一鏡之內亮度（含飽和度）出現急遽變化的比例。
  閃光、能量爆發、放射線插入都會讓亮度在幾幀內拉高再回來。
- 每鏡的亮度擺幅（Y range）與飽和度擺幅（SAT range）。
- 「光事件鏡」佔比：這一鏡裡有沒有光影事件。

參考片的特色是幾乎每一鏡都有一個光影事件（能量浪、X 形爆、放射線漫畫格），
而不是只有「命中」的那幾鏡有。
"""

import argparse
import json
import os
import subprocess
import sys

import numpy as np


def raw_rgb(path, width=160, height=90):
    cmd = ["ffmpeg", "-v", "error", "-i", path, "-fps_mode", "passthrough",
           "-vf", f"scale={width}:{height}", "-f", "rawvideo",
           "-pix_fmt", "rgb24", "-"]
    out = subprocess.run(cmd, capture_output=True).stdout
    n = len(out) // (width * height * 3)
    if n == 0:
        return None
    arr = np.frombuffer(out[: n * width * height * 3], dtype=np.uint8)
    return arr.reshape(n, height, width, 3).astype(np.float32)


def cut_points(frames):
    if len(frames) < 8:
        return []
    g = frames.mean(axis=3)
    diff = np.abs(np.diff(g, axis=0)).mean(axis=(1, 2))
    med = np.median(diff)
    mad = np.median(np.abs(diff - med)) or 1e-6
    sharp = []
    for i in range(len(diff)):
        lo, hi = max(0, i - 3), min(len(diff), i + 4)
        neigh = np.concatenate([diff[lo:i], diff[i + 1:hi]])
        base = np.median(neigh) if len(neigh) else med
        sharp.append(diff[i] / (base + 1e-6))
    sharp = np.array(sharp)
    lum = g.mean(axis=(1, 2))
    sat = g.std(axis=(1, 2))
    is_insert = (sat < 12) | (lum < 14) | (lum > 240)
    cuts = []
    for i in range(len(diff)):
        if diff[i] < 8.0 and sharp[i] < 2.0:
            continue
        if diff[i] < med + 4 * mad:
            continue
        if is_insert[i] or (i + 1 < len(is_insert) and is_insert[i + 1]):
            continue
        cuts.append(i + 1)
    merged = []
    for c in cuts:
        if merged and c - merged[-1] < 3:
            continue
        merged.append(c)
    return cuts


def analyse(path, fps=24.0):
    frames = raw_rgb(path)
    if frames is None or len(frames) < 8:
        return None
    n = len(frames)
    g = frames.mean(axis=3)
    lum = g.mean(axis=(1, 2))
    sat = g.std(axis=(1, 2))
    cuts = [0] + cut_points(frames) + [n]
    rows = []
    for a, b in zip(cuts, cuts[1:]):
        if b - a < 2:
            continue
        L = lum[a:b]
        S = sat[a:b]
        if len(L) < 3:
            continue
        # 亮度軌跡的擺幅與最大跳躍
        d = np.abs(np.diff(L))
        jump = float(d.max()) if len(d) else 0.0
        # 光事件：鏡內亮度有明顯的「起→頂→落」形狀
        peak = int(np.argmax(L))
        has_event = bool(d.max() > max(4.0, 0.35 * (L.max() - L.min() + 1e-6)))
        rows.append(dict(start=a, end=b, dur=round((b - a) / fps, 3),
                         lum_rng=round(float(L.max() - L.min()), 1),
                         sat_rng=round(float(S.max() - S.min()), 1),
                         jump=round(jump, 1),
                         peak_at=round(peak / len(L), 2),
                         event=has_event))
    if not rows:
        return None
    ev = sum(1 for r in rows if r["event"])
    return dict(name=os.path.basename(path), shots=len(rows),
                event_pct=round(100 * ev / len(rows), 1),
                median_lum_rng=round(float(np.median([r["lum_rng"] for r in rows])), 1),
                median_sat_rng=round(float(np.median([r["sat_rng"] for r in rows])), 1),
                median_jump=round(float(np.median([r["jump"] for r in rows])), 1),
                rows=rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--fps", type=float, default=24.0)
    a = ap.parse_args()
    out = [r for r in (analyse(f, a.fps) for f in a.files) if r]
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 0
    hdr = (f"{'檔案':<24}{'鏡數':>6}{'有光事件鏡%':>12}{'亮度擺幅中位':>13}"
           f"{'飽和擺幅中位':>13}{'亮度跳躍中位':>13}")
    print(hdr)
    print("-" * 86)
    for r in out:
        print(f"{r['name'][:22]:<24}{r['shots']:>6}{r['event_pct']:>12.1f}"
              f"{r['median_lum_rng']:>13.1f}{r['median_sat_rng']:>13.1f}"
              f"{r['median_jump']:>13.1f}")
    print()
    for r in out:
        print(f"=== {r['name']} ===")
        for row in r["rows"][:24]:
            flag = "★" if row["event"] else " "
            print(f" {flag} {row['start']:>4}-{row['end']:<4} {row['dur']:>5.2f}s "
                  f"lumΔ={row['lum_rng']:>6.1f} satΔ={row['sat_rng']:>5.1f} "
                  f"jump={row['jump']:>5.1f} 峰在{row['peak_at']:.0%}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
