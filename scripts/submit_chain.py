#!/usr/bin/env python3
"""兩段 15 秒的 FL2VA 接續：第 1 段 T2VA/Ref2VA 生成 → 抽末幀 → 第 2 段以末幀續接。

用法：
    python submit_chain.py --prompt-a segA.txt --prompt-b segB.txt \
        --seconds 15 --width 960 --height 544 --seed 20261019 \
        --reference "ref1.png" --reference "ref2.png" --reference "ref3.png" \
        --outdir analysis/chain

流程：
    1. 第 1 段以 media.references 送 Ref2VA（有給 --reference 時）否則 T2VA
    2. 等第 1 段完成 → 下載 → ffmpeg 抽最後一幀成 PNG → 上傳
    3. 第 2 段以該末幀為 media.first 送 FL2VA
    4. 等第 2 段完成 → 下載
    5. 用 ffmpeg concat 接成一支 30 秒
"""

import argparse
import base64
import json
import pathlib
import subprocess
import sys
import time
import urllib.request

BASE = "http://127.0.0.1:8189/freevideo/agent/v1"
ROOT = "http://127.0.0.1:8189"
TOKEN = pathlib.Path(r"E:\FreeVideo\agent\token")


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


class Client:
    def __init__(self):
        self.token = TOKEN.read_text(encoding="utf-8").strip()

    def call(self, method, path, body=None, raw=False):
        data = None
        headers = {"Authorization": "Bearer " + self.token}
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(BASE + path, data=data, method=method,
                                     headers=headers)
        op = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with op.open(req, timeout=300) as r:
            payload = r.read()
        if raw:
            return payload
        return json.loads(payload.decode("utf-8"))

    def upload(self, path):
        p = pathlib.Path(path)
        b64 = base64.b64encode(p.read_bytes()).decode("ascii")
        name = p.name
        if not pathlib.Path(name).suffix:
            head = p.read_bytes()[:12]
            if head.startswith(b"\x89PNG\r\n\x1a\n"):
                name += ".png"
            elif head.startswith(b"\xff\xd8\xff"):
                name += ".jpg"
            else:
                name += ".png"
        res = self.call("POST", "/media", {"name": name, "data_base64": b64})
        f = res.get("file") or (res.get("media") or {}).get("file")
        if not f:
            raise RuntimeError(f"upload failed: {res}")
        return f

    def download(self, job, out, ):
        url = (job.get("result") or {}).get("video", {}).get("url")
        if not url:
            for b in (job.get("result") or {}).get("blocks") or []:
                if b.get("video"):
                    url = b["video"]["url"]
                    break
        if not url:
            raise RuntimeError("no video url")
        full = ROOT + url if url.startswith("/freevideo/") else (
            url if url.startswith("http") else BASE + url)
        req = urllib.request.Request(full,
                                     headers={"Authorization": "Bearer " + self.token})
        op = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with op.open(req, timeout=600) as r:
            data = r.read()
        out = pathlib.Path(out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
        return str(out)

    def wait(self, jid, label, timeout=10800):
        t0 = time.time()
        while time.time() - t0 < timeout:
            j = self.call("GET", f"/jobs/{jid}?wait=25")["job"]
            st = j.get("status")
            if st in ("succeeded", "failed", "cancelled", "interrupted"):
                print(f"  [{label}] {st}", flush=True)
                return j if st == "succeeded" else None
            pr = j.get("progress") or {}
            print(f"  [{label}] {st} {pr.get('percent','')}", flush=True)
        return None


def last_frame(video, out):
    """抽最後一幀。用 -sseof 倒退 0.5 秒再取最後一格，比 -frames:v 1 穩。"""
    dur = float(run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                     "-show_entries", "stream=duration", "-of", "csv=p=0",
                     video]).stdout.strip() or 0)
    if not dur:
        dur = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                         "-of", "csv=p=0", video]).stdout.strip() or 1)
    ss = max(0.0, dur - 0.5)
    r = run(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.5", "-i", video,
             "-update", "1", "-q:v", "2", out])
    if r.returncode != 0 or not pathlib.Path(out).exists():
        # 退路：直接取最後一格
        r2 = run(["ffmpeg", "-v", "error", "-y", "-i", video,
                  "-vf", f"select='eq(n\\,{int(dur*24)-1})'",
                  "-fps_mode", "passthrough", "-frames:v", "1", out])
        if r2.returncode != 0:
            sys.stderr.write(r.stderr + r2.stderr + "\n")
            return None
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt-a", required=True)
    ap.add_argument("--prompt-b", required=True)
    ap.add_argument("--reference", action="append", default=[])
    ap.add_argument("--seconds", type=float, default=15.0)
    ap.add_argument("--width", type=int, default=960)
    ap.add_argument("--height", type=int, default=544)
    ap.add_argument("--quality", default="light")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--outdir", default="analysis/chain")
    ap.add_argument("--resume", action="store_true",
                    help="若 segA.mp4 已存在就跳過第 1 段")
    a = ap.parse_args()

    c = Client()
    outdir = pathlib.Path(a.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    segA = outdir / "segA.mp4"
    segB = outdir / "segB.mp4"
    state_p = outdir / "chain.json"
    state = json.loads(state_p.read_text(encoding="utf-8")) if state_p.exists() else {}

    # ---------- 段 A ----------
    if a.resume and segA.exists() and segA.stat().st_size > 200_000:
        print(f"段 A 已存在，跳過：{segA}")
    else:
        refs = [{"file": c.upload(p)} for p in a.reference]
        for p, r in zip(a.reference, refs):
            print(f"上傳參考：{p} -> {r['file']}")
        spec = {
            "kind": "generate", "label": "A · 第1段 15s",
            "prompt": pathlib.Path(a.prompt_a).read_text(encoding="utf-8").strip(),
            "width": a.width, "height": a.height,
            "seconds": a.seconds, "quality": a.quality,
        }
        if refs:
            spec["media"] = {"references": refs}
        if a.seed is not None:
            spec["seed"] = a.seed
        res = c.call("POST", "/jobs", {"jobs": [spec]})
        jid = (res.get("jobs") or res.get("created"))[0]["id"]
        print(f"段 A 已送出：{jid}", flush=True)
        state["segA_job"] = jid
        state_p.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
        job = c.wait(jid, "A")
        if not job:
            print("段 A 失敗")
            return 1
        print("段 A 下載：", c.download(job, segA))

    # ---------- 抽末幀 ----------
    lf = outdir / "segA_last.png"
    if not last_frame(str(segA), str(lf)):
        print("抽末幀失敗")
        return 1
    print(f"段 A 末幀：{lf}")

    # ---------- 段 B ----------
    if a.resume and segB.exists() and segB.stat().st_size > 200_000:
        print(f"段 B 已存在，跳過：{segB}")
    else:
        first = c.upload(str(lf))
        print(f"上傳段 A 末幀 -> {first}")
        spec = {
            "kind": "generate", "label": "B · 第2段 15s 續接",
            "prompt": pathlib.Path(a.prompt_b).read_text(encoding="utf-8").strip(),
            "width": a.width, "height": a.height,
            "seconds": a.seconds, "quality": a.quality,
            "media": {"first": {"file": first}},
        }
        if a.seed is not None:
            spec["seed"] = a.seed
        res = c.call("POST", "/jobs", {"jobs": [spec]})
        jid = (res.get("jobs") or res.get("created"))[0]["id"]
        print(f"段 B 已送出：{jid}", flush=True)
        state["segB_job"] = jid
        state_p.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
        job = c.wait(jid, "B")
        if not job:
            print("段 B 失敗")
            return 1
        print("段 B 下載：", c.download(job, segB))

    # ---------- concat ----------
    lst = outdir / "concat.txt"
    lst.write_text(f"file '{segA.resolve().as_posix()}'\nfile '{segB.resolve().as_posix()}'\n",
                   encoding="utf-8")
    full = outdir / "full_30s.mp4"
    r = run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
             "-i", str(lst), "-c", "copy", str(full)])
    if r.returncode != 0:
        sys.stderr.write(r.stderr + "\n")
        return 1
    print(f"已接成：{full}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
