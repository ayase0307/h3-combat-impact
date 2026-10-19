#!/usr/bin/env python3
"""量測「運鏡感」的兩個核心指標：

1. 取景變化（staging variation）：每一鏡主體在畫面裡的位置與大小，
   相鄰鏡之間改變多少。主體永遠在同一位置 = 觀眾感覺「同一個鏡頭」。
2. 節奏交替（rhythm alternation）：鏡長是否呈「長鏡承載動作、短鏡承載衝擊」
   的雙峰分布。單一分布 = 節奏單調。

用法：
    python staging_variation.py clip.mp4 [clip2.mp4 ...]
"""

import argparse
import json
import os
import subprocess
import sys

import numpy as np


def raw_rgb(path, width=192, height=108):
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


def subject_bbox(frame):
    """主體＝最暗的連續區塊（剪影）。回傳 (cx, cy, area_pct, h_pct)。"""
    g = frame.mean(axis=2)
    th = np.percentile(g, 22)
    mask = g < th
    if mask.sum() < 20:
        return None
    # 取密度最高的水平帶作為主體帶
    rows = mask.sum(axis=1)
    best = 0
    bi = 0
    for i in range(len(rows)):
        s = rows[max(0, i - 3):i + 4].sum()
        if s > best:
            best = s
            bi = i
    band = mask[max(0, bi - 6):bi + 7]
    if band.sum() < 20:
        return None
    cols = band.sum(axis=0)
    nz = np.nonzero(cols > 0)[0]
    if len(nz) == 0:
        return None
    h, w = mask.shape
    x0, x1 = nz[0], nz[-1]
    return (float((x0 + x1) / 2 / w), float(bi / h),
            float(mask.mean() * 100), float((x1 - x0) / w * 100))


def analyse(path, fps=24.0):
    frames = raw_rgb(path)
    if frames is None or len(frames) < 8:
        return None
    n = len(frames)
    cuts = [0] + cut_points(frames) + [n]
    rows = []
    for a, b in zip(cuts, cuts[1:]):
        if b - a < 2:
            continue
        mid = frames[(a + b) // 2]
        bb = subject_bbox(mid)
        rows.append(dict(start=a, end=b, frames=b - a,
                         dur=round((b - a) / fps, 3),
                         cx=None if not bb else round(bb[0], 3),
                         cy=None if not bb else round(bb[1], 3),
                         area=None if not bb else round(bb[2], 1),
                         width=None if not bb else round(bb[3], 1)))
    if len(rows) < 2:
        return None
    # 相鄰鏡的取景變化
    dcx, darea = [], []
    for p, q in zip(rows, rows[1:]):
        if p["cx"] is None or q["cx"] is None:
            continue
        dcx.append(abs(q["cx"] - p["cx"]))
        darea.append(abs(q["width"] - p["width"]))
    durs = [r["dur"] for r in rows]
    # 節奏雙峰：短鏡(<=0.5s)與長鏡(>=1.0s)的比例
    short = sum(1 for d in durs if d <= 0.5)
    long = sum(1 for d in durs if d >= 1.0)
    return dict(name=os.path.basename(path), frames=n, shots=len(rows),
                dur=round(n / fps, 2),
                median_shot=round(float(np.median(durs)), 3),
                short_pct=round(100 * short / len(durs), 1),
                long_pct=round(100 * long / len(durs), 1),
                mean_dcx=round(float(np.mean(dcx)), 3) if dcx else 0.0,
                max_dcx=round(float(np.max(dcx)), 3) if dcx else 0.0,
                mean_dwidth=round(float(np.mean(darea)), 1) if darea else 0.0,
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
    hdr = (f"{'檔案':<24}{'鏡數':>6}{'中位鏡長':>9}{'短鏡%':>8}{'長鏡%':>8}"
           f"{'Δ水平位置':>10}{'Δ主體寬':>9}")
    print(hdr)
    print("-" * 78)
    for r in out:
        print(f"{r['name'][:22]:<24}{r['shots']:>6}{r['median_shot']:>9.3f}"
              f"{r['short_pct']:>8.1f}{r['long_pct']:>8.1f}"
              f"{r['mean_dcx']:>10.3f}{r['mean_dwidth']:>9.1f}")
    print()
    for r in out:
        print(f"=== {r['name']} 逐鏡 ===")
        for row in r["rows"][:22]:
            print(f"  {row['start']:>4}-{row['end']:<4} {row['dur']:>5.2f}s "
                  f"cx={row['cx']} cy={row['cy']} 寬={row['width']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
