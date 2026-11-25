#!/usr/bin/env python3
"""清晰度：每秒取 2 幀，算灰階拉普拉斯方差，報中位數與 P10（越高越銳）。

    python measure_sharpness.py a.mp4 b.mp4

只能拿「同解析度」的片互比；內容不同（水面、霧、墨爆）會拉動數值，所以看中位數、不看單幀。
"""
import statistics
import subprocess
import sys

import cv2
import numpy as np


def frames(path, fps=2):
    cmd = ["ffmpeg", "-loglevel", "error", "-i", path, "-vf", f"fps={fps}", "-f", "rawvideo", "-pix_fmt", "gray", "-"]
    w, h = [int(x) for x in subprocess.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
         "-of", "csv=p=0:s=x", path], text=True).strip().split("x")]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    n = len(raw) // (w * h)
    return np.frombuffer(raw, np.uint8)[: n * w * h].reshape(n, h, w)


def main():
    for p in sys.argv[1:]:
        v = sorted(float(cv2.Laplacian(f, cv2.CV_64F).var()) for f in frames(p))
        print(f"{p}\tmedian={statistics.median(v):.1f}\tp10={v[len(v) // 10]:.1f}\tn={len(v)}")


if __name__ == "__main__":
    main()
