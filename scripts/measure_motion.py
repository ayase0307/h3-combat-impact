#!/usr/bin/env python3
"""量測生成影片的運動曲線，用數據檢查「開場過靜」與「尾端停滯」。

用法：
    python measure_motion.py video1.mp4 [video2.mp4 ...]
    python measure_motion.py --dir ./outputs

原理：
    逐格計算前後張差異（tblend difference）的平均亮度 → 運動能量。
    數值越高代表畫面變化越大（主體移動、鏡頭運動、特效變化都算）。

指標：
    全程      全片平均運動量
    開場0.8s  開頭 0.8 秒的平均（檢查「有效開場」）
    中段      0.8s 到倒數 2 秒的平均（基準線）
    末2s      最後 2 秒的平均（檢查「動態結尾」）
    末/中     末2s ÷ 中段，<60% 視為尾端停滯
    最長低潮  連續低於全程 35% 的最長時間
    峰值格    高於全程 1.8 倍的行數（動作節拍數）

注意：這是「畫面變化」而非「主體運動」。特效/背景大幅運動會拉高分數，
      即使角色站著不動。要判斷主體是否靜止，仍須目視。
"""

import argparse
import glob
import os
import statistics as st
import subprocess
import sys


def measure(path):
    cmd = [
        "ffmpeg", "-v", "error", "-i", path,
        "-vf", "tblend=all_mode=difference,signalstats,"
               "metadata=print:key=lavfi.signalstats.YAVG:file=-",
        "-f", "null", "-",
    ]
    out = subprocess.run(cmd, capture_output=True, text=True, errors="ignore").stdout
    ts, ys = [], []
    t = None
    for line in out.splitlines():
        line = line.strip()
        if line.startswith("frame:"):
            for q in line.split():
                if q.startswith("pts_time:"):
                    try:
                        t = float(q.split(":")[1])
                    except ValueError:
                        t = None
        elif line.startswith("lavfi.signalstats.YAVG=") and t is not None:
            try:
                ys.append(float(line.split("=")[1]))
                ts.append(t)
            except ValueError:
                pass
    return ts, ys


def seg(ts, ys, a, b):
    v = [y for t, y in zip(ts, ys) if a <= t < b]
    return st.mean(v) if v else 0.0


def longest_low(ts, ys, thresh):
    best = cur = 0.0
    start = None
    best_at = 0.0
    for t, y in zip(ts, ys):
        if y < thresh:
            if start is None:
                start = t
            cur = t - start
            if cur > best:
                best, best_at = cur, start
        else:
            start = None
            cur = 0.0
    return best, best_at


def measure_symmetry(path):
    """左右對稱殘差：把畫面水平翻轉後與原圖相減，值越低越對稱。

    對稱 + 低運動 = 遊戲技能展示式的靜止姿勢，是最該避免的構圖。
    """
    cmd = [
        "ffmpeg", "-v", "error", "-i", path, "-filter_complex",
        "[0:v]split[a][b];[b]hflip[c];[a][c]blend=all_mode=difference,"
        "signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-",
        "-f", "null", "-",
    ]
    out = subprocess.run(cmd, capture_output=True, text=True, errors="ignore").stdout
    ts, ys = [], []
    t = None
    for line in out.splitlines():
        line = line.strip()
        if line.startswith("frame:"):
            for q in line.split():
                if q.startswith("pts_time:"):
                    try:
                        t = float(q.split(":")[1])
                    except ValueError:
                        t = None
        elif line.startswith("lavfi.signalstats.YAVG=") and t is not None:
            try:
                ys.append(float(line.split("=")[1]))
                ts.append(t)
            except ValueError:
                pass
    return ts, ys


def static_symmetric(path):
    """找出「低運動 + 高對稱」的秒數，這是遊戲技能展示的典型特徵。"""
    ts_m, y_m = measure(path)
    ts_s, y_s = measure_symmetry(path)
    if not y_m or not y_s:
        return []
    motion_all = st.mean(y_m)
    sym_all = st.mean(y_s)
    dur = int(ts_m[-1]) + 1
    hits = []
    for sec in range(dur):
        m = [y for t, y in zip(ts_m, y_m) if sec <= t < sec + 1]
        s = [y for t, y in zip(ts_s, y_s) if sec <= t < sec + 1]
        if not m or not s:
            continue
        if st.mean(m) < 0.60 * motion_all and st.mean(s) < 0.80 * sym_all:
            hits.append(sec)
    return hits


def analyse(path):
    ts, ys = measure(path)
    if len(ys) < 8:
        return None
    dur = ts[-1] + 1 / 24
    overall = st.mean(ys)
    opening = seg(ts, ys, 0.0, 0.8)
    mid = seg(ts, ys, 0.8, max(1.0, dur - 2.0))
    ending = seg(ts, ys, dur - 2.0, dur)
    ratio = ending / mid if mid else 0.0
    low, low_at = longest_low(ts, ys, overall * 0.35)
    peaks = sum(1 for y in ys if y > overall * 1.8)

    flags = []
    if mid and opening < 0.5 * mid:
        flags.append("開場過靜")
    if ratio < 0.6:
        flags.append("尾端停滯")
    if low > 0.8:
        flags.append(f"低潮{low:.2f}s")
    if peaks < 4:
        flags.append("節拍過少")
    if overall < 14:
        flags.append("整體過靜(比例可能失真)")

    return dict(name=os.path.basename(path), dur=dur, overall=overall,
                opening=opening, mid=mid, ending=ending, ratio=ratio,
                low=low, low_at=low_at, peaks=peaks, flags=flags)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--dir", help="掃描目錄下所有 mp4")
    ap.add_argument("--symmetry", action="store_true",
                    help="額外檢查「靜止對稱段」（遊戲技能展示式的姿勢）")
    a = ap.parse_args()

    files = list(a.files)
    if a.dir:
        files += sorted(glob.glob(os.path.join(a.dir, "*.mp4")))
    if not files:
        ap.print_help()
        return 1

    rows = [r for r in (analyse(f) for f in files) if r]
    hdr = (f"{'檔案':<26}{'時長':>6}{'全程':>7}{'開場':>7}{'中段':>7}"
           f"{'末2s':>7}{'末/中':>7}{'最長低潮':>9}{'峰值':>5}  旗標")
    print(hdr)
    print("-" * 118)
    for r, f in zip(rows, files):
        flags = list(r["flags"])
        if a.symmetry:
            hits = static_symmetric(f)
            if hits:
                flags.append("靜止對稱 " + ",".join(f"{s}-{s+1}s" for s in hits))
        print(f"{r['name'][:24]:<26}{r['dur']:>6.2f}{r['overall']:>7.2f}"
              f"{r['opening']:>7.2f}{r['mid']:>7.2f}{r['ending']:>7.2f}"
              f"{r['ratio'] * 100:>6.0f}%{r['low']:>9.2f}{r['peaks']:>5}  "
              f"{'、'.join(flags) or '—'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
