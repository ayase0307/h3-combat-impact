#!/usr/bin/env python3
"""把兩支影片做成並排動態圖（GIF），用來比較「技能使用前 / 使用後」的提示詞成果。

用法：
    python compare_clips.py --before old.mp4 --after new.mp4 --out compare.gif
    python compare_clips.py --before old.mp4 --after new.mp4 --out compare.gif \
        --label-before "V01 · 未套用技能" --label-after "V09 · 套用技能後"

產出：
    1. 一支並排動態圖（GIF），左＝before、右＝after，兩片都有標籤
    2. 標準輸出列出兩片的運動量指標（沿用 measure_motion.py 的算法）

依賴：ffmpeg（需在 PATH）。字型預設找 Windows 的 arial.ttf，
      可用 --font 指定其他字型檔路徑。
"""

import argparse
import json
import os
import re
import shutil
import statistics as st
import subprocess
import sys
import tempfile

# 依序嘗試。第一順位要能顯示繁體中文，否則標籤會變成空白方框。
FONT_CANDIDATES = [
    r"C:\Windows\Fonts\NotoSansTC-VF.ttf",
    r"C:\Windows\Fonts\msjh.ttc",
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\mingliu.ttc",
    r"C:\Windows\Fonts\NotoSansJP-VF.ttf",
    r"C:\Windows\Fonts\arial.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
]


def find_font(explicit=None):
    if explicit:
        return explicit
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            return p
    return None


def ff_path(path):
    """Windows 路徑在 ffmpeg 濾鏡字串裡要用正斜線，並把冒號轉義。"""
    p = path.replace("\\", "/")
    if len(p) > 1 and p[1] == ":":
        p = p[0] + "\\:" + p[2:]
    return p


def measure(path):
    """逐格差異 → 運動量。與 measure_motion.py 同一套算法。"""
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


def stats(path):
    ts, ys = measure(path)
    if len(ys) < 8:
        return None
    dur = ts[-1] + 1 / 24
    overall = st.mean(ys)
    opening = seg(ts, ys, 0.0, 0.8)
    mid = seg(ts, ys, 0.8, max(1.0, dur - 2.0))
    ending = seg(ts, ys, dur - 2.0, dur)
    peaks = sum(1 for y in ys if y > overall * 1.8)
    # 最長低潮
    best = cur = 0.0
    start = None
    for t, y in zip(ts, ys):
        if y < overall * 0.35:
            if start is None:
                start = t
            cur = t - start
            best = max(best, cur)
        else:
            start = None
            cur = 0.0
    return dict(dur=dur, overall=overall, opening=opening, mid=mid,
                ending=ending, ratio=(ending / mid if mid else 0.0),
                low=best, peaks=peaks)


def escape(text):
    """drawtext 需要跳過的字符。"""
    return (text.replace("\\", r"\\").replace(":", r"\:")
                .replace("'", "").replace("%", r"\%"))


def build_gif(before, after, out, label_before, label_after,
              fps, width, font, height=None, colors=128, dither_scale=3):
    """並排 GIF。左 = before，右 = after。"""
    tmp = tempfile.mkdtemp(prefix="cmpgif_")
    try:
        # 兩片各自縮放到同寬、同高（以 before 的比例為準），補黑邊
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height", "-of", "csv=p=0", before],
            capture_output=True, text=True, errors="ignore").stdout.strip()
        try:
            bw, bh = [int(x) for x in probe.split(",")[:2]]
        except Exception:
            bw, bh = 1280, 720
        if height is None:
            height = max(2, int(round(width * bh / bw)))
        # 高度要 2 的倍數，GIF 編碼器友善
        height += height % 2

        common = (f"fps={fps},scale={width}:{height}:force_original_aspect_ratio=decrease,"
                  f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black,"
                  f"setsar=1,format=rgb24")

        parts = []
        if font:
            fpath = ff_path(font)
            for i, (lbl, src) in enumerate(((label_before, "0:v"), (label_after, "1:v"))):
                if not lbl:
                    continue
                # 標籤寫成檔案再由 textfile 讀取，避免 shell 編碼破壞中文字元
                lf = os.path.join(tmp, f"label{i}.txt")
                with open(lf, "w", encoding="utf-8") as fh:
                    fh.write(lbl)
                parts.append(
                    f"[{src}]drawtext=fontfile='{fpath}':textfile='{ff_path(lf)}':"
                    f"fontcolor=white:fontsize={max(14, width // 26)}:"
                    f"box=1:boxcolor=black@0.65:boxborderw=6:"
                    f"x=(w-text_w)/2:y=h-th-8[v{i}]"
                )
                parts.append(f"[v{i}]fps={fps},scale={width}:{height}:"
                             f"force_original_aspect_ratio=decrease,"
                             f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black,"
                             f"setsar=1,format=rgb24[s{i}]")
            chain = ";".join(parts)
            layout = "[s0][s1]hstack=inputs=2[st]"
        else:
            layout = (f"[0:v]{common}[s0];[1:v]{common}[s1];[s0][s1]hstack=inputs=2[st]")

        pal = os.path.join(tmp, "pal.png")
        # 第一段：並排 → 產生調色盤（palettegen 只需要單一輸入）
        g1 = ["ffmpeg", "-v", "error", "-y",
              "-i", before, "-i", after,
              "-filter_complex", chain + ";" + layout +
              f";[st]palettegen=stats_mode=diff:max_colors={colors}[pal]",
              "-map", "[pal]", pal]
        r = subprocess.run(g1, capture_output=True, text=True, errors="ignore")
        if r.returncode != 0:
            raise RuntimeError("palettegen failed:\n" + r.stderr[-2000:])

        # 第二段：用調色盤輸出 GIF（paletteuse 需要「影片 + 調色盤」兩個輸入）
        g2 = ["ffmpeg", "-v", "error", "-y",
              "-i", before, "-i", after, "-i", pal,
              "-filter_complex", chain + ";" + layout +
              f";[st][2:v]paletteuse=dither=bayer:bayer_scale={dither_scale}:"
              f"diff_mode=rectangle[out]",
              "-map", "[out]", "-loop", "0", out]
        r = subprocess.run(g2, capture_output=True, text=True, errors="ignore")
        if r.returncode != 0:
            raise RuntimeError("paletteuse failed:\n" + r.stderr[-2000:])
        return dict(width=width * 2, height=height, fps=fps)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--before", required=True, help="技能使用前的影片")
    ap.add_argument("--after", required=True, help="技能使用後的影片")
    ap.add_argument("--out", required=True, help="輸出 GIF 路徑")
    ap.add_argument("--label-before", default="BEFORE")
    ap.add_argument("--label-after", default="AFTER")
    ap.add_argument("--fps", type=int, default=10)
    ap.add_argument("--width", type=int, default=420,
                    help="單片寬度（並排後為兩倍）")
    ap.add_argument("--height", type=int, default=None)
    ap.add_argument("--font", default=None)
    ap.add_argument("--colors", type=int, default=128,
                    help="調色盤顏色數（越少檔案越小）")
    ap.add_argument("--dither-scale", type=int, default=3,
                    help="Bayer 抖動強度（越大越省空間）")
    ap.add_argument("--json", action="store_true", help="只輸出 JSON 指標")
    a = ap.parse_args()

    for p in (a.before, a.after):
        if not os.path.exists(p):
            print(f"找不到檔案：{p}", file=sys.stderr)
            return 2

    font = find_font(a.font)
    if not font:
        print("警告：找不到字型，標籤將不會繪製。", file=sys.stderr)

    info = build_gif(a.before, a.after, a.out,
                     a.label_before, a.label_after,
                     a.fps, a.width, font, a.height,
                     a.colors, a.dither_scale)

    sb = stats(a.before)
    sa = stats(a.after)
    result = {
        "out": a.out,
        "gif": info,
        "before": sb,
        "after": sa,
    }
    if a.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    print(f"\n並排動態圖：{a.out}  "
          f"({info['width']}x{info['height']} @{info['fps']}fps, "
          f"{os.path.getsize(a.out) / 1024:.0f} KB)")

    hdr = f"{'指標':<16}{'BEFORE':>12}{'AFTER':>12}"
    print(hdr)
    print("-" * len(hdr))
    if sb and sa:
        rows = [
            ("時長(s)", f"{sb['dur']:.2f}", f"{sa['dur']:.2f}"),
            ("全程運動", f"{sb['overall']:.2f}", f"{sa['overall']:.2f}"),
            ("開場0.8s", f"{sb['opening']:.2f}", f"{sa['opening']:.2f}"),
            ("中段", f"{sb['mid']:.2f}", f"{sa['mid']:.2f}"),
            ("末2s", f"{sb['ending']:.2f}", f"{sa['ending']:.2f}"),
            ("末/中", f"{sb['ratio']*100:.0f}%", f"{sa['ratio']*100:.0f}%"),
            ("最長低潮", f"{sb['low']:.2f}s", f"{sa['low']:.2f}s"),
            ("峰值格", f"{sb['peaks']}", f"{sa['peaks']}"),
        ]
        for name, b, c in rows:
            print(f"{name:<16}{b:>12}{c:>12}")
    else:
        print("（其中一支影片太短，無法量測）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
