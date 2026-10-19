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


def detect_fps(path):
    """偵測實際帧率（含 2:3 pulldown 的偽 60fps）。

    回傳 (fps, is_pulldown, frame_count)。
    容器宣告的 r_frame_rate 可能是假的：一支標 60fps 的片實測只有 24fps
    （幀間隔在 0.050s 與 0.0333s 之間交替 = 24fps 母版的 2:3 pulldown）。
    """
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "packet=pts_time", "-of", "csv=p=0", path],
        capture_output=True, text=True, errors="ignore").stdout
    ts = []
    for line in out.splitlines():
        line = line.strip().rstrip(",")
        if not line:
            continue
        try:
            ts.append(float(line))
        except ValueError:
            pass
    if len(ts) < 8:
        return 0.0, False, len(ts)
    ts.sort()
    span = ts[-1] - ts[0]
    if span <= 0:
        return 0.0, False, len(ts)
    fps = len(ts) / span
    # 檢查是否有兩種交替的間隔（pulldown 的特徵）
    deltas = [round(ts[i] - ts[i - 1], 4) for i in range(1, len(ts))]
    common = {}
    for d in deltas:
        common[d] = common.get(d, 0) + 1
    # 把相近的間隔合併（浮點誤差）
    merged = {}
    for d, c in common.items():
        key = min((k for k in merged if abs(k - d) < 0.002), default=d)
        merged[key] = merged.get(key, 0) + c
    top2 = sorted(merged.values(), reverse=True)[:2]
    pulldown = len(top2) == 2 and top2[1] > len(ts) * 0.15
    return fps, pulldown, len(ts)


def normalise_to_24(value, fps):
    """把「每幀平均差異」換算回 24fps 等效值。

    30fps 素材的每幀差異只有 24fps 的 0.8 倍，60fps 只有 0.5 倍。
    不換算就不能跟以 24fps 校準的門檻比較。

    換算係數是 fps/24（不是 24/fps）：幀率越高 → 每幀位移越小 → 分數越低，
    所以要「乘回來」而不是「乘下去」。
    實測：30fps 的 24.52 → 24fps 等效 30.67；30fps 的 14.06 → 17.59。
    """
    if fps <= 0 or abs(fps - 24.0) < 0.5:
        return value
    return value * (fps / 24.0)


def analyse(path):
    ts, ys = measure(path)
    if len(ys) < 8:
        return None
    fps, pulldown, nframes = detect_fps(path)
    dur = ts[-1] + 1 / 24
    overall = st.mean(ys)
    opening = seg(ts, ys, 0.0, 0.8)
    mid = seg(ts, ys, 0.8, max(1.0, dur - 2.0))
    ending = seg(ts, ys, dur - 2.0, dur)
    ratio = ending / mid if mid else 0.0
    low, low_at = longest_low(ts, ys, overall * 0.35)
    peaks = sum(1 for y in ys if y > overall * 1.8)

    # 折回 24fps 等效值，讓不同幀率的素材可以比較
    overall24 = normalise_to_24(overall, fps)
    opening24 = normalise_to_24(opening, fps)
    mid24 = normalise_to_24(mid, fps)
    ending24 = normalise_to_24(ending, fps)
    # 峰值格是「幀數」，幀率越高格數越多 → 折回 24fps
    peaks24 = int(round(peaks * (24.0 / fps))) if fps > 0 else peaks

    flags = []
    if mid and opening < 0.5 * mid:
        flags.append("開場過靜")
    if ratio < 0.6:
        flags.append("尾端停滯")
    if low > 0.8:
        flags.append(f"低潮{low:.2f}s")
    if peaks24 < 4:
        flags.append("節拍過少")
    if overall24 < 14:
        flags.append("整體過靜(比例可能失真)")
    if pulldown:
        flags.append(f"pulldown(實{nframes}幀/{fps:.0f}fps,幀間隔交替)")

    return dict(name=os.path.basename(path), dur=dur, overall=overall,
                opening=opening, mid=mid, ending=ending, ratio=ratio,
                low=low, low_at=low_at, peaks=peaks,
                overall24=overall24, opening24=opening24, mid24=mid24,
                ending24=ending24, peaks24=peaks24,
                fps=fps, pulldown=pulldown, nframes=nframes, flags=flags)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--dir", help="掃描目錄下所有 mp4")
    ap.add_argument("--symmetry", action="store_true",
                    help="額外檢查「靜止對稱段」（遊戲技能展示式的姿勢）")
    ap.add_argument("--fps24", action="store_true",
                    help="顯示折回 24fps 等效值（跨幀率比較用）")
    a = ap.parse_args()

    files = list(a.files)
    if a.dir:
        files += sorted(glob.glob(os.path.join(a.dir, "*.mp4")))
    if not files:
        ap.print_help()
        return 1

    rows = [r for r in (analyse(f) for f in files) if r]
    if a.fps24:
        hdr = (f"{'檔案':<26}{'時長':>6}{'實際fps':>8}{'幀數':>6}{'全程24':>8}"
               f"{'開場24':>8}{'末2s24':>8}{'末/中':>7}{'峰值24':>7}  旗標")
        print(hdr)
        print("-" * 122)
        for r, f in zip(rows, files):
            flags = list(r["flags"])
            if a.symmetry:
                hits = static_symmetric(f)
                if hits:
                    flags.append("靜止對稱 " + ",".join(f"{s}-{s+1}s" for s in hits))
            print(f"{r['name'][:24]:<26}{r['dur']:>6.2f}{r['fps']:>8.2f}{r['nframes']:>6}"
                  f"{r['overall24']:>8.2f}{r['opening24']:>8.2f}{r['ending24']:>8.2f}"
                  f"{r['ratio'] * 100:>6.0f}%{r['peaks24']:>7}  "
                  f"{'、'.join(flags) or '—'}")
        return 0

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
