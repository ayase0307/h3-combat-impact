#!/usr/bin/env python3
"""兩段接續的接縫驗收：量接縫那一格有沒有「死格」。

用法：
    python seam_check.py segA.mp4 segB.mp4 full.mp4

判讀：
    接縫格的逐幀差應該與前後 8 格的中位數接近。
    低於 50% = 接縫是死格（姿態跳、鏡頭跳或光線跳），觀眾會看到頓點。
"""

import argparse
import re
import subprocess
import sys

import numpy as np


def frame_diffs(path):
    out = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-vf",
         "tblend=all_mode=difference,signalstats,"
         "metadata=print:key=lavfi.signalstats.YAVG:file=-",
         "-f", "null", "-"],
        capture_output=True, text=True, errors="ignore").stdout
    t = None
    ts, ys = [], []
    for line in out.splitlines():
        line = line.strip()
        m = re.search(r"pts_time:([0-9.]+)", line)
        if m:
            t = float(m.group(1))
        elif line.startswith("lavfi.signalstats.YAVG=") and t is not None:
            ts.append(t)
            ys.append(float(line.split("=")[1]))
    return np.array(ts), np.array(ys)


def info(path):
    o = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=nb_frames",
                        "-of", "csv=p=0", path],
                       capture_output=True, text=True).stdout.strip()
    try:
        return int(o)
    except ValueError:
        return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sega")
    ap.add_argument("segb")
    ap.add_argument("full")
    a = ap.parse_args()

    nA = info(a.sega)
    nB = info(a.segb)
    ts, ys = frame_diffs(a.full)
    if len(ys) == 0:
        print("無法量測", file=sys.stderr)
        return 1

    print(f"段 A：{nA} 幀　段 B：{nB} 幀　合計：{len(ys)} 個差值樣本")
    print()

    # 接縫格 = 段 A 最後一幀之後的那一格
    seam = nA
    if seam >= len(ys):
        print("接縫超出量測範圍")
        return 1

    lo, hi = max(0, seam - 8), min(len(ys), seam + 9)
    win = ys[lo:hi]
    neigh = np.concatenate([ys[lo:seam], ys[seam + 1:hi]])
    med = float(np.median(neigh)) if len(neigh) else 0.0
    val = float(ys[seam])
    ratio = val / med if med else 0.0

    print(f"接縫格（第 {seam} 格）YAVG 差 = {val:.2f}")
    print(f"前後 8 格中位數        = {med:.2f}")
    print(f"比值                  = {ratio * 100:.0f}%")
    print()
    if ratio < 0.5:
        print("[FAIL] 接縫是死格 → 兩段在這一格對不上（姿態/鏡頭/光線跳）")
        print("       修法：第 1 段結尾寫成動作中；第 2 段首鏡 0.5 秒內打破")
        return 1
    if ratio < 0.7:
        print("[WARN] 接縫偏弱，觀眾可能察覺一個小頓點")
        return 0
    print("[PASS] 接縫銜接正常")
    return 0


if __name__ == "__main__":
    sys.exit(main())
