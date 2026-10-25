#!/usr/bin/env python3
"""衝擊幀組裝工具：找衝擊幀、分段變速（P2）、疊衝擊幀（P3）、生成衝擊片。

H3 不遵守幀數（`for two frames` 的白閃實際亮 11–45 幀），所以衝擊幀的長度與速度一律在組裝決定：

  find-peak  找出影片裡最像衝擊幀的格（亮度峰／壓暗／去飽和）與連續變化段（衝擊幀串）
  ramp       P2：把衝擊幀串段加速（例 5×）、主特效段 1.5×，其餘原速；音軌一起變速
  composite  P3：把衝擊片的某一格疊到主片指定幀（自動縮放到主片解析度、保留主片音軌、
             一次可疊多組、可插純黑幀），結束時印出驗收數值
  gen        送本機 FreeVideo／H3 生成衝擊片（需本機服務；Hark 雲端跑不了）

需要 ffmpeg／ffprobe。詳細流程見 references/impact-frame/burst-strip.md（P2）與 post.md（P3）。
"""

import argparse
import json
import os
import pathlib
import re
import statistics
import subprocess
import sys
import time
from urllib.parse import urlsplit

DEFAULT_API = "http://127.0.0.1:8189/freevideo/agent/v1"
WINDOWS_TOKEN = r"E:\FreeVideo\agent\token"

EPILOG = """範例：
  # 衝擊幀實際落在哪幾格？
  python scripts/impact_frame.py find-peak --in S04a.mp4

  # P2：衝擊幀段 5×、主特效 1.5×（只保留 0.8–4.0 秒）
  python scripts/impact_frame.py ramp --in S04a.mp4 --seg 1.40-2.21:5 --seg 2.21-3.96:1.5 \\
      --keep 0.8-4.0 --out S04a.ramped.mp4

  # P3：衝擊片自動挑最亮／最去飽和的一格，疊到主片第 163 幀起、停 2 幀
  python scripts/impact_frame.py composite --main main.mp4 --impact impact.mp4 \\
      --insert 163:auto:2 --out final.mp4

  # P3 多階段序列＋3 幀黑尾，一次完成
  python scripts/impact_frame.py composite --main main.mp4 --impact B.mp4 \\
      --insert 163:3:2 --insert 165:9:2 --insert 167:15:2 --black 169:3 --out final.mp4

  # 生成衝擊片（本機 FreeVideo）
  H3_API_BASE=http://127.0.0.1:8189/freevideo/agent/v1 H3_TOKEN_FILE=~/token \\
  python scripts/impact_frame.py gen --prompt impact.txt --out impact.mp4
"""


# ---------------------------------------------------------------- 共用

def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def die(msg, code=1):
    sys.stderr.write(msg.rstrip() + "\n")
    sys.exit(code)


def need_ffmpeg():
    for exe in ("ffmpeg", "ffprobe"):
        if run([exe, "-version"]).returncode != 0:
            die(f"找不到 {exe}，請先安裝 ffmpeg。", 2)


def probe(path):
    """回傳 dict：width, height, fps, duration, has_audio, nframes。"""
    if not os.path.exists(path):
        die(f"找不到檔案：{path}", 2)
    r = run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path])
    if r.returncode != 0:
        die(f"ffprobe 讀不了 {path}：\n{r.stderr}", 2)
    info = json.loads(r.stdout)
    v = next((s for s in info["streams"] if s.get("codec_type") == "video"), None)
    if v is None:
        die(f"{path} 沒有影像串流", 2)
    num, _, den = (v.get("avg_frame_rate") or v.get("r_frame_rate") or "24/1").partition("/")
    fps = float(num) / float(den or 1) if float(num or 0) else 24.0
    dur = float(v.get("duration") or info.get("format", {}).get("duration") or 0)
    has_audio = any(s.get("codec_type") == "audio" for s in info["streams"])
    nframes = int(v["nb_frames"]) if str(v.get("nb_frames", "")).isdigit() else round(dur * fps)
    return {"width": int(v["width"]), "height": int(v["height"]), "fps": fps,
            "duration": dur, "has_audio": has_audio, "nframes": nframes}


def frame_stats(path):
    """逐幀 YAVG／SATAVG／YDIF（signalstats）。回傳 list[dict(n, t, y, s, d)]。"""
    r = run(["ffmpeg", "-v", "error", "-i", path, "-vf",
             "signalstats,metadata=print:file=-", "-an", "-f", "null", "-"])
    if r.returncode != 0:
        die(f"ffmpeg 量測失敗：\n{r.stderr}", 2)
    rows, cur = [], None
    for line in r.stdout.splitlines():
        m = re.match(r"frame:(\d+)\s+pts:\S+\s+pts_time:([\d.]+)", line)
        if m:
            cur = {"n": int(m.group(1)), "t": float(m.group(2)), "y": 0.0, "s": 0.0, "d": 0.0}
            rows.append(cur)
            continue
        if cur is None:
            continue
        for key, field in (("YAVG", "y"), ("SATAVG", "s"), ("YDIF", "d")):
            if line.startswith(f"lavfi.signalstats.{key}="):
                cur[field] = float(line.split("=", 1)[1])
    return rows


def local_median(vals, i, half=8):
    lo, hi = max(0, i - half), min(len(vals), i + half + 1)
    window = vals[lo:i] + vals[i + 1:hi]
    return statistics.median(window) if window else vals[i]


def score_frames(rows):
    """每幀的衝擊分數：亮度偏離鄰近中位數，或飽和度掉到鄰近以下。"""
    ys = [r["y"] for r in rows]
    ss = [r["s"] for r in rows]
    out = []
    for i, r in enumerate(rows):
        dy = r["y"] - local_median(ys, i)
        ds = local_median(ss, i) - r["s"]
        kind = "white" if dy >= 25 else ("dark" if dy <= -25 else ("desat" if ds >= 15 else ""))
        out.append({**r, "dy": dy, "ds": ds, "score": max(abs(dy), ds * 1.5), "kind": kind})
    return out


def candidates(scored, top=5, gap=6):
    picked = []
    for r in sorted(scored, key=lambda x: -x["score"]):
        if all(abs(r["n"] - p["n"]) >= gap for p in picked):
            picked.append(r)
        if len(picked) >= top:
            break
    return picked


def burst_runs(scored, min_len=3):
    """連續每格都在大幅變化的段（衝擊幀串的特徵）。"""
    ds = [r["d"] for r in scored]
    if not ds:
        return [], 0.0
    med = statistics.median(ds)
    thr = max(15.0, med * 3 + 6)
    runs, start, last = [], None, None
    for r in scored:
        hot = r["d"] >= thr or r["kind"]
        if hot:
            if start is None:
                start = r
            last = r
        elif start is not None and r["n"] - last["n"] > 2:
            if last["n"] - start["n"] + 1 >= min_len:
                runs.append((start, last))
            start = None
    if start is not None and last["n"] - start["n"] + 1 >= min_len:
        runs.append((start, last))
    return runs, thr


# ---------------------------------------------------------------- find-peak

def cmd_find_peak(a):
    need_ffmpeg()
    info = probe(a.inp)
    scored = score_frames(frame_stats(a.inp))
    if not scored:
        die("讀不到任何幀", 2)
    print(f"{a.inp}  {info['width']}×{info['height']}  {info['fps']:.3f} fps  "
          f"{info['duration']:.2f}s  音軌={'有' if info['has_audio'] else '無'}")
    print("\n最像衝擊幀的格（composite 的 --insert 幀號:這裡的 n:hold）：")
    print("   n      秒     YAVG   SATAVG   ΔY(鄰近)  ΔS(鄰近)  類型")
    for r in candidates(scored, a.top):
        print(f"{r['n']:5d}  {r['t']:6.3f}  {r['y']:6.1f}  {r['s']:6.1f}  {r['dy']:+8.1f}  "
              f"{r['ds']:+8.1f}  {r['kind'] or '-'}")
    runs, thr = burst_runs(scored)
    print(f"\n連續變化段（可能是衝擊幀串；YDIF 門檻 {thr:.1f}）——填 ramp 的 --seg：")
    if not runs:
        print("  （沒有）")
    for s, e in runs:
        print(f"  幀 {s['n']}–{e['n']}  ≈ {s['t']:.2f}–{e['t'] + 1 / info['fps']:.2f}s  "
              f"（{e['n'] - s['n'] + 1} 幀）  建議 --seg {s['t']:.2f}-{e['t'] + 1 / info['fps']:.2f}:5")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(scored, ensure_ascii=False, indent=1),
                                        encoding="utf-8")
        print(f"\n逐幀資料已寫入 {a.json}")
    return 0


# ---------------------------------------------------------------- ramp

def parse_range(text, what):
    m = re.fullmatch(r"\s*([\d.]+)\s*-\s*([\d.]+)\s*", text)
    if not m:
        die(f"{what} 格式錯誤：{text}（要 起-迄，單位秒）", 2)
    a, b = float(m.group(1)), float(m.group(2))
    if b <= a:
        die(f"{what} 迄點要大於起點：{text}", 2)
    return a, b


def atempo_chain(x):
    """把任意倍率拆成 0.5–2.0 的 atempo 串（相容舊版 ffmpeg）。"""
    parts = []
    while x > 2.0:
        parts.append(2.0)
        x /= 2.0
    while x < 0.5:
        parts.append(0.5)
        x /= 0.5
    parts.append(x)
    return ",".join(f"atempo={p:.6f}" for p in parts)


def cmd_ramp(a):
    need_ffmpeg()
    info = probe(a.inp)
    k0, k1 = parse_range(a.keep, "--keep") if a.keep else (0.0, info["duration"])
    k1 = min(k1, info["duration"])
    segs = []
    for s in a.seg:
        rng, _, x = s.rpartition(":")
        if not rng:
            die(f"--seg 格式錯誤：{s}（要 起-迄:倍率，例 1.40-2.21:5）", 2)
        lo, hi = parse_range(rng, "--seg")
        try:
            speed = float(x)
        except ValueError:
            die(f"--seg 倍率不是數字：{s}", 2)
        if speed <= 0:
            die(f"--seg 倍率要 >0：{s}", 2)
        segs.append((max(lo, k0), min(hi, k1), speed))
    segs = sorted(s for s in segs if s[1] > s[0])
    for (a0, a1, _), (b0, _, _) in zip(segs, segs[1:]):
        if b0 < a1 - 1e-6:
            die(f"--seg 區間重疊：{a0}-{a1} 與 {b0}-…", 2)

    pieces, t = [], k0
    for lo, hi, speed in segs:
        if lo > t + 1e-6:
            pieces.append((t, lo, 1.0))
        pieces.append((lo, hi, speed))
        t = hi
    if k1 > t + 1e-6:
        pieces.append((t, k1, 1.0))

    audio = info["has_audio"] and not a.no_audio
    fc, labels = [], []
    for i, (lo, hi, speed) in enumerate(pieces):
        fc.append(f"[0:v]trim=start={lo:.4f}:end={hi:.4f},setpts=(PTS-STARTPTS)/{speed:.6f}[v{i}]")
        labels.append(f"[v{i}]")
        if audio:
            fc.append(f"[0:a]atrim=start={lo:.4f}:end={hi:.4f},asetpts=PTS-STARTPTS,"
                      f"{atempo_chain(speed)}[a{i}]")
            labels.append(f"[a{i}]")
    n = len(pieces)
    fc.append("".join(labels) + f"concat=n={n}:v=1:a={1 if audio else 0}"
              + ("[vc][ac]" if audio else "[vc]"))
    out_fps = a.fps or info["fps"]
    fc.append(f"[vc]fps={out_fps:.6f},format=yuv420p[v]")
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", a.inp, "-filter_complex", ";".join(fc),
           "-map", "[v]"]
    if audio:
        cmd += ["-map", "[ac]", "-c:a", "aac", "-b:a", "192k"]
    cmd += ["-c:v", "libx264", "-crf", str(a.crf), "-preset", "medium", a.out]
    r = run(cmd)
    if r.returncode != 0:
        die(f"ffmpeg 變速失敗：\n{r.stderr}")
    out = probe(a.out)
    print(f"已變速：{a.out}")
    for lo, hi, speed in pieces:
        print(f"  {lo:6.2f}–{hi:6.2f}s  ×{speed:g}  → {(hi - lo) / speed:5.2f}s")
    print(f"  總長 {k1 - k0:.2f}s → {out['duration']:.2f}s，{out_fps:g} fps，"
          f"音軌={'有' if out['has_audio'] else '無'}")
    if info["has_audio"] and not out["has_audio"] and not a.no_audio:
        print("  [WARN] 原片有音軌但輸出沒有")
    return 0


# ---------------------------------------------------------------- composite

def parse_insert(text, main_fps):
    parts = text.split(":")
    if len(parts) != 3:
        die(f"--insert 格式錯誤：{text}（要 主片幀號:衝擊片幀號或auto:停幾幀，例 163:auto:2）", 2)
    at, frame, hold = parts
    at = round(float(at[:-1]) * main_fps) if at.endswith("s") else int(at)
    hold = int(hold)
    if hold < 1:
        die(f"--insert 停留幀數要 ≥1：{text}", 2)
    return at, frame.strip().lower(), hold


def extract_frame(src, idx, w, h, dst):
    vf = (f"select=eq(n\\,{idx}),scale={w}:{h}:force_original_aspect_ratio=increase,"
          f"crop={w}:{h},setsar=1")
    r = run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", vf, "-fps_mode", "passthrough",
             "-frames:v", "1", dst])
    if r.returncode != 0 or not os.path.exists(dst):
        die(f"抽不出衝擊片第 {idx} 幀（是否超出長度？）：\n{r.stderr}")


def cmd_composite(a):
    need_ffmpeg()
    main, imp = probe(a.main), probe(a.impact)
    W, H, fps = main["width"], main["height"], main["fps"]

    inserts = [parse_insert(x, fps) for x in (a.insert or [])]
    if a.at is not None or a.at_frame is not None:   # 舊語法
        at = a.at_frame if a.at_frame is not None else round(a.at * fps)
        inserts.append((at, str(a.frame), max(1, round(a.hold * fps))))
    blacks = []
    for b in a.black or []:
        at, _, n = b.partition(":")
        blacks.append((int(at), int(n or 1)))
    if not inserts and not blacks:
        die("沒有任何 --insert／--black（或舊語法 --at／--at-frame）", 2)

    cands = None
    if any(f.startswith("auto") for _, f, _ in inserts):
        cands = candidates(score_frames(frame_stats(a.impact)), top=10)
        print("衝擊片候選格：" + "、".join(f"#{c['n']}({c['kind'] or '-'} ΔY{c['dy']:+.0f})"
                                         for c in cands[:5]))

    tmp = pathlib.Path(a.out).with_suffix("")
    pngs, resolved = {}, []
    for at, f, hold in inserts:
        if f.startswith("auto"):
            k = int(f[4:] or 1) - 1
            if not cands or k >= len(cands):
                die(f"找不到第 {k + 1} 個候選格", 2)
            idx = cands[k]["n"]
        else:
            idx = int(f)
        if idx >= imp["nframes"] + 2:
            die(f"衝擊片只有約 {imp['nframes']} 幀，要求第 {idx} 幀", 2)
        if idx not in pngs:
            pngs[idx] = f"{tmp}.impact_{idx}.png"
            extract_frame(a.impact, idx, W, H, pngs[idx])
        if at + hold > main["nframes"] + 1:
            die(f"插入點 {at}+{hold} 超出主片長度（約 {main['nframes']} 幀）", 2)
        resolved.append((at, idx, hold))

    order = list(pngs)
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", a.main]
    for idx in order:
        cmd += ["-loop", "1", "-framerate", f"{fps:.6f}", "-i", pngs[idx]]
    fc, last = [], "[0:v]"
    for j, (at, idx, hold) in enumerate(resolved):
        src = order.index(idx) + 1
        lab = f"[o{j}]"
        fc.append(f"{last}[{src}:v]overlay=enable='between(n,{at},{at + hold - 1})':"
                  f"eof_action=pass:shortest=1{lab}")
        last = lab
    for j, (at, n) in enumerate(blacks):
        lab = f"[b{j}]"
        fc.append(f"{last}drawbox=x=0:y=0:w=iw:h=ih:color=black:t=fill:"
                  f"enable='between(n,{at},{at + n - 1})'{lab}")
        last = lab
    fc.append(f"{last}format=yuv420p[v]")
    cmd += ["-filter_complex", ";".join(fc), "-map", "[v]"]
    if main["has_audio"]:
        cmd += ["-map", "0:a?", "-c:a", "copy"]
    cmd += ["-c:v", "libx264", "-crf", str(a.crf), "-preset", "medium", "-r", f"{fps:.6f}",
            a.out]
    r = run(cmd)
    for p in pngs.values():
        if not a.keep_png:
            pathlib.Path(p).unlink(missing_ok=True)
    if r.returncode != 0:
        die(f"ffmpeg 合成失敗：\n{r.stderr}")

    out = probe(a.out)
    print(f"已合成：{a.out}  {out['width']}×{out['height']}  {out['fps']:.3f} fps  "
          f"音軌={'有' if out['has_audio'] else '無'}")
    if imp["width"] != W or imp["height"] != H:
        print(f"  衝擊片 {imp['width']}×{imp['height']} 已縮放裁切到主片 {W}×{H}")
    if main["has_audio"] and not out["has_audio"]:
        print("  [WARN] 主片有音軌但輸出沒有")
    verify(a.out, resolved, blacks)
    return 0


def verify(path, resolved, blacks):
    """兩段式驗收：插入幀看得見（ΔY≥40 或 S<15）；插入區以外接得順（前後 3 幀 ΔY<8）。"""
    rows = {r["n"]: r for r in frame_stats(path)}
    spans = sorted([(at, at + hold - 1) for at, _, hold in resolved] +
                   [(at, at + n - 1) for at, n in blacks])
    merged = []
    for s, e in spans:
        if merged and s <= merged[-1][1] + 1:
            merged[-1] = (merged[-1][0], max(e, merged[-1][1]))
        else:
            merged.append((s, e))
    print("  驗收（references/impact-frame/post.md §3）：")
    for s, e in merged:
        before = [rows[n]["y"] for n in range(s - 3, s) if n in rows]
        after = [rows[n]["y"] for n in range(e + 1, e + 4) if n in rows]
        inside = [rows[n] for n in range(s, e + 1) if n in rows]
        if not inside:
            print(f"    幀 {s}–{e}：量不到")
            continue
        ref = statistics.mean(before + after) if (before or after) else inside[0]["y"]
        dy = max(abs(r["y"] - ref) for r in inside)
        smin = min(r["s"] for r in inside)
        seam = abs(statistics.mean(before) - statistics.mean(after)) if before and after else 0
        ok1 = dy >= 40 or smin < 15
        ok2 = seam < 8
        ystr = "/".join("%.0f" % r["y"] for r in inside)
        sstr = "/".join("%.0f" % r["s"] for r in inside)
        print(f"    幀 {s}–{e}：插入 Y={ystr} S={sstr}  鄰幀 Y≈{ref:.0f}  "
              f"ΔY={dy:.0f}  [{'OK' if ok1 else 'WARN 插入幀不夠顯眼（換一格或改衝擊片）'}]  "
              f"前後接縫 ΔY={seam:.1f}  [{'OK' if ok2 else 'WARN 主片本身在此跳亮度或環境光對不上'}]")


# ---------------------------------------------------------------- gen

def resolve_token(a):
    if a.token:
        return a.token.strip()
    env_tok = os.environ.get("H3_TOKEN") or os.environ.get("FREEVIDEO_TOKEN")
    if env_tok:
        return env_tok.strip()
    paths = [a.token_file, os.environ.get("H3_TOKEN_FILE"), os.environ.get("FREEVIDEO_TOKEN_FILE")]
    if os.name == "nt":
        paths.append(WINDOWS_TOKEN)
    for p in paths:
        if p and os.path.exists(os.path.expanduser(p)):
            return pathlib.Path(os.path.expanduser(p)).read_text(encoding="utf-8").strip()
    die("找不到生成端 token。請用 --token-file／--token，或設環境變數 H3_TOKEN_FILE／H3_TOKEN"
        "（舊名 FREEVIDEO_TOKEN_FILE／FREEVIDEO_TOKEN）。\n"
        "本機 FreeVideo 不可用時，請在家機跑 gen，或用其他後端生成衝擊片再跑 composite。", 2)


def cmd_gen(a):
    import urllib.error
    import urllib.request

    base = (a.api or os.environ.get("H3_API_BASE") or os.environ.get("FREEVIDEO_API")
            or DEFAULT_API).rstrip("/")
    parts = urlsplit(base)
    root = f"{parts.scheme}://{parts.netloc}"
    tok = resolve_token(a)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

    def call(method, path, body=None):
        data, headers = None, {"Authorization": "Bearer " + tok}
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(base + path, data=data, method=method, headers=headers)
        try:
            with opener.open(req, timeout=300) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            die(f"生成端回應 HTTP {e.code}：{e.read().decode('utf-8', 'replace')}", 1)
        except (urllib.error.URLError, OSError) as e:
            die(f"連不到生成端 {base}：{e}\n本機 FreeVideo 沒開，或這台機器不是家機。", 2)

    if not os.path.exists(a.prompt):
        die(f"找不到提示詞檔：{a.prompt}", 2)
    prompt = pathlib.Path(a.prompt).read_text(encoding="utf-8").strip()
    spec = {"kind": "generate", "label": a.label, "prompt": prompt, "width": a.width,
            "height": a.height, "seconds": a.seconds, "quality": a.quality}
    if a.seed is not None:
        spec["seed"] = a.seed
    res = call("POST", "/jobs", {"jobs": [spec]})
    jid = (res.get("jobs") or res.get("created"))[0]["id"]
    print(f"已送出衝擊片工作：{jid}", flush=True)
    t0 = time.time()
    while time.time() - t0 < a.timeout:
        j = call("GET", f"/jobs/{jid}?wait=25")["job"]
        st = j.get("status")
        if st in ("succeeded", "failed", "cancelled", "interrupted"):
            if st != "succeeded":
                die(f"狀態：{st}", 1)
            url = (j.get("result") or {}).get("video", {}).get("url")
            if not url:
                die("工作成功但沒有影片網址", 1)
            full = root + url if url.startswith("/") else url
            req = urllib.request.Request(full, headers={"Authorization": "Bearer " + tok})
            with opener.open(req, timeout=300) as r:
                data = r.read()
            out = pathlib.Path(a.out)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)
            print(f"已下載：{out}")
            return 0
        print(f"  {st}", flush=True)
    die("等待逾時", 1)


# ---------------------------------------------------------------- CLI

def main():
    fmt = argparse.RawDescriptionHelpFormatter
    ap = argparse.ArgumentParser(description=__doc__, epilog=EPILOG, formatter_class=fmt)
    sub = ap.add_subparsers(dest="cmd", required=True, metavar="{find-peak,ramp,composite,gen}")

    f = sub.add_parser("find-peak", formatter_class=fmt,
                       help="找出最像衝擊幀的格與連續變化段（衝擊幀串）",
                       description="逐幀量 YAVG／SATAVG／YDIF，列出亮度峰、壓暗、去飽和的候選格，"
                                   "以及每格都在大幅變化的連續段（P2 衝擊幀串的位置，填 ramp --seg）。")
    f.add_argument("--in", dest="inp", required=True, help="要分析的影片")
    f.add_argument("--top", type=int, default=5, help="列出幾個候選格（預設 5）")
    f.add_argument("--json", help="把逐幀資料寫成 JSON")
    f.set_defaults(func=cmd_find_peak)

    r = sub.add_parser("ramp", formatter_class=fmt, help="P2：分段變速（音軌一起變速）",
                       description="把指定區間加速／減速，其餘原速，接成一支。音軌用 atempo 同步變速。\n"
                                   "例：--seg 1.40-2.21:5 --seg 2.21-3.96:1.5",
                       epilog="教學片做法：衝擊幀段生成時每張約 0.2 秒 → 5× 後每張約 1 幀；主特效 1.5×；"
                              "開場空等 1.5–2×。區間先用 find-peak 校正。")
    r.add_argument("--in", dest="inp", required=True, help="生成片")
    r.add_argument("--seg", action="append", default=[], metavar="起-迄:倍率",
                   help="變速區間（秒）與倍率，可重複；>1 加速、<1 減速（升格）")
    r.add_argument("--keep", metavar="起-迄", help="只保留這段（秒），其餘裁掉；預設整支")
    r.add_argument("--fps", type=float, default=None, help="輸出幀率（預設同原片，H3 為 24）")
    r.add_argument("--crf", type=int, default=18, help="x264 品質（預設 18）")
    r.add_argument("--no-audio", action="store_true", help="輸出不帶音軌")
    r.add_argument("--out", required=True, help="輸出檔")
    r.set_defaults(func=cmd_ramp)

    c = sub.add_parser("composite", formatter_class=fmt, help="P3：把衝擊片的格疊到主片",
                       description="把衝擊片某一格疊到主片指定幀。衝擊片自動縮放＋置中裁切到主片解析度，"
                                   "主片音軌原樣保留，多組 --insert 一次完成，結束時印出驗收數值。")
    c.add_argument("--main", required=True, help="主片（不含衝擊幀）")
    c.add_argument("--impact", required=True, help="衝擊片")
    c.add_argument("--insert", action="append", metavar="主片幀號:衝擊片幀號:停幾幀",
                   help="可重複。衝擊片幀號可寫 auto（最像衝擊幀的那格）、auto2、auto3…；"
                        "主片位置也可寫秒數加 s（例 6.8s:auto:2）")
    c.add_argument("--black", action="append", metavar="主片幀號:幀數",
                   help="插純黑幀（多階段序列的黑尾），可重複，例 172:3")
    c.add_argument("--at", type=float, help="（舊語法）合成開始秒數")
    c.add_argument("--at-frame", type=int, help="（舊語法）合成開始的主片幀號")
    c.add_argument("--frame", default="0", help="（舊語法）取衝擊片第幾幀，可寫 auto")
    c.add_argument("--hold", type=float, default=0.083, help="（舊語法）停留秒數，預設 0.083＝24fps 的 2 幀")
    c.add_argument("--crf", type=int, default=18, help="x264 品質（預設 18）")
    c.add_argument("--keep-png", action="store_true", help="保留抽出的衝擊幀 PNG")
    c.add_argument("--out", required=True, help="輸出檔")
    c.set_defaults(func=cmd_composite)

    g = sub.add_parser("gen", formatter_class=fmt, help="送本機 FreeVideo／H3 生成衝擊片",
                       description="需要本機生成服務。位址：--api 或環境變數 H3_API_BASE（舊名 FREEVIDEO_API），"
                                   f"預設 {DEFAULT_API}。\ntoken：--token／--token-file，或環境變數 "
                                   "H3_TOKEN／H3_TOKEN_FILE（舊名 FREEVIDEO_TOKEN／FREEVIDEO_TOKEN_FILE）；"
                                   f"Windows 另會找 {WINDOWS_TOKEN}。")
    g.add_argument("--prompt", required=True, help="衝擊片提示詞檔（先用 validate_prompt.py --impact-clip 檢查）")
    g.add_argument("--out", required=True, help="下載到哪")
    g.add_argument("--api", help="生成端 API 基底位址")
    g.add_argument("--token-file", help="token 檔路徑")
    g.add_argument("--token", help="token 字串（不建議寫進指令歷史，優先用 --token-file）")
    g.add_argument("--label", default="impact frame", help="工作標籤")
    g.add_argument("--width", type=int, default=960)
    g.add_argument("--height", type=int, default=544)
    g.add_argument("--seconds", type=float, default=4.0, help="衝擊片長度（預設 4 秒）")
    g.add_argument("--quality", default="light")
    g.add_argument("--seed", type=int, default=None)
    g.add_argument("--timeout", type=int, default=7200, help="最多等幾秒（預設 7200）")
    g.set_defaults(func=cmd_gen)

    a = ap.parse_args()
    return a.func(a)


if __name__ == "__main__":
    sys.exit(main())
