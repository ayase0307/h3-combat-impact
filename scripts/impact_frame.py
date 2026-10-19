#!/usr/bin/env python3
"""分開生成衝擊幀，再後製合成到主片上。

用途：H3 在同一段提示詞裡很難同時產出「高速動作」與「精準的 2 幀衝擊幀」。
解法是拆成兩條：
  1. 主片：只做高速動作與運鏡，**完全不寫衝擊幀**。
  2. 衝擊幀片：單獨生成一兩幀的爆發／漫畫格。
  3. 合成：把衝擊幀片的那幾幀，用 ffmpeg 的 overlay 蓋到主片的指定時間點。

用法：
    # 產生衝擊幀片（短、有明確爆發描述）
    python impact_frame.py gen --prompt impact.txt --out impact.mp4 --width 960 --height 544

    # 合成：把 impact.mp4 的第 N 幀蓋到 main.mp4 的 t 秒
    python impact_frame.py composite --main main.mp4 --impact impact.mp4 \
        --at 6.5 --frame 12 --out final.mp4
"""

import argparse
import json
import pathlib
import subprocess
import sys

BASE = "http://127.0.0.1:8189/freevideo/agent/v1"
ROOT = "http://127.0.0.1:8189"
TOKEN = pathlib.Path(r"E:\FreeVideo\agent\token")


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def gen(args):
    import base64
    import urllib.request
    import urllib.error

    tok = TOKEN.read_text(encoding="utf-8").strip()

    def call(method, path, body=None):
        data = None
        headers = {"Authorization": "Bearer " + tok}
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(BASE + path, data=data, method=method,
                                     headers=headers)
        op = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        try:
            with op.open(req, timeout=300) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            sys.stderr.write(e.read().decode("utf-8", "replace") + "\n")
            raise

    prompt = pathlib.Path(args.prompt).read_text(encoding="utf-8").strip()
    spec = {
        "kind": "generate", "label": args.label, "prompt": prompt,
        "width": args.width, "height": args.height,
        "seconds": args.seconds, "quality": args.quality,
    }
    if args.seed is not None:
        spec["seed"] = args.seed
    res = call("POST", "/jobs", {"jobs": [spec]})
    jid = (res.get("jobs") or res.get("created"))[0]["id"]
    print(f"已送出衝擊幀工作：{jid}", flush=True)

    import time
    t0 = time.time()
    while time.time() - t0 < 7200:
        j = call("GET", f"/jobs/{jid}?wait=25")["job"]
        st = j.get("status")
        if st in ("succeeded", "failed", "cancelled", "interrupted"):
            if st != "succeeded":
                print(f"狀態：{st}")
                return 1
            url = (j.get("result") or {}).get("video", {}).get("url")
            if not url:
                return 1
            full = ROOT + url if url.startswith("/") else url
            req = urllib.request.Request(full, headers={"Authorization": "Bearer " + tok})
            op = urllib.request.build_opener(urllib.request.ProxyHandler({}))
            with op.open(req, timeout=300) as r:
                data = r.read()
            out = pathlib.Path(args.out)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)
            print(f"已下載：{out}")
            return 0
        print(f"  {st}", flush=True)
    return 1


def composite(args):
    """把 impact 的第 --frame 幀蓋在 main 的 --at 秒處，長度 --hold 秒。"""
    # 1. 抽出衝擊幀那一幀成 PNG
    #    注意：ffmpeg 9 已移除 -vsync，改用 -fps_mode passthrough
    png = pathlib.Path(args.out).with_suffix(".impact_frame.png")
    r = run(["ffmpeg", "-v", "error", "-y", "-i", args.impact,
             "-vf", f"select=eq(n\\,{args.frame})", "-fps_mode", "passthrough",
             "-frames:v", "1", str(png)])
    if r.returncode != 0:
        sys.stderr.write(r.stderr + "\n")
        return 1

    # 2. 算出衝擊幀要覆蓋的時間區間
    nframes = int(run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                       "-count_frames", "-show_entries",
                       "stream=nb_read_frames", "-of", "csv=p=0",
                       args.main]).stdout.strip() or 0)
    fps = 24.0
    start = args.at
    dur = args.hold
    # 3. overlay：衝擊幀圖在 [start, start+dur] 區間出現在主片最上層
    fc = (f"[1:v]format=rgba,scale=iw:ih[if];"
          f"[0:v][if]overlay=enable='between(t,{start},{start + dur})':"
          f"eof_action=pass[ov];"
          f"[ov]fps={fps},format=yuv420p[v]")
    r = run(["ffmpeg", "-v", "error", "-y", "-i", args.main, "-loop", "1",
             "-i", str(png), "-filter_complex", fc, "-map", "[v]",
             "-c:v", "libx264", "-crf", "18", "-preset", "medium",
             "-pix_fmt", "yuv420p", args.out])
    if r.returncode != 0:
        sys.stderr.write(r.stderr + "\n")
        return 1
    png.unlink(missing_ok=True)
    print(f"已合成：{args.out}  （衝擊幀疊在 {start:.2f}s，長 {dur:.2f}s）")
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("gen", help="生成衝擊幀片")
    g.add_argument("--prompt", required=True)
    g.add_argument("--out", required=True)
    g.add_argument("--label", default="impact frame")
    g.add_argument("--width", type=int, default=960)
    g.add_argument("--height", type=int, default=544)
    g.add_argument("--seconds", type=float, default=4.0)
    g.add_argument("--quality", default="light")
    g.add_argument("--seed", type=int, default=None)
    g.set_defaults(func=gen)

    c = sub.add_parser("composite", help="把衝擊幀合成到主片")
    c.add_argument("--main", required=True)
    c.add_argument("--impact", required=True)
    c.add_argument("--at", type=float, required=True, help="合成開始秒數")
    c.add_argument("--frame", type=int, default=0, help="取衝擊幀片的第幾幀")
    c.add_argument("--hold", type=float, default=0.08, help="覆蓋長度（秒）")
    c.add_argument("--out", required=True)
    c.set_defaults(func=composite)

    a = ap.parse_args()
    return a.func(a)


if __name__ == "__main__":
    sys.exit(main())
