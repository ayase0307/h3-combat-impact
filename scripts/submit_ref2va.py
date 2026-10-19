#!/usr/bin/env python3
"""上傳參考圖到本機 FreeVideo，並送出一支 Ref2VA 生成工作。

用法：
    python submit_ref2va.py --prompt F.txt \
        --image "C:/path/char1.png" --image "C:/path/char2.png" --image "C:/path/scene.png" \
        --label "F · 無人機運鏡" --seconds 8 --seed 20261019 --outdir analysis/drone
"""

import argparse
import base64
import json
import pathlib
import sys
import time
import urllib.request

BASE = "http://127.0.0.1:8189/freevideo/agent/v1"
ROOT = "http://127.0.0.1:8189"
TOKEN = pathlib.Path(r"E:\FreeVideo\agent\token")


class Client:
    def __init__(self, api=BASE, token_file=TOKEN):
        self.api = api.rstrip("/")
        self.root = self.api[:-len("/freevideo/agent/v1")] if self.api.endswith(
            "/freevideo/agent/v1") else self.api
        self.token = token_file.read_text(encoding="utf-8").strip()

    def call(self, method, path, body=None, raw=False):
        data = None
        headers = {"Authorization": "Bearer " + self.token}
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(self.api + path, data=data,
                                     method=method, headers=headers)
        op = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with op.open(req, timeout=300) as r:
            payload = r.read()
        if raw:
            return payload
        return json.loads(payload.decode("utf-8"))

    def upload(self, path):
        p = pathlib.Path(path)
        b64 = base64.b64encode(p.read_bytes()).decode("ascii")
        # 上傳的 name 必須帶副檔名，否則 API 判定「媒體無法辨識」回 422
        # （附件商店的檔名是純 hash，沒有副檔名）
        name = p.name
        if not pathlib.Path(name).suffix:
            head = p.read_bytes()[:12]
            if head.startswith(b"\x89PNG\r\n\x1a\n"):
                name += ".png"
            elif head.startswith(b"\xff\xd8\xff"):
                name += ".jpg"
            elif head[:4] == b"RIFF" and p.read_bytes()[8:12] == b"WEBP":
                name += ".webp"
            else:
                name += ".png"
        res = self.call("POST", "/media", {"name": name, "data_base64": b64})
        if isinstance(res, dict):
            f = res.get("file") or (res.get("media") or {}).get("file")
            if f:
                return f
            for k in ("path", "url", "id"):
                if res.get(k):
                    return res[k]
        return res

    def download(self, job, outdir, name):
        res = job.get("result") or {}
        url = (res.get("video") or {}).get("url")
        if not url:
            for b in (res.get("blocks") or []):
                if b.get("video"):
                    url = b["video"]["url"]
                    break
        if not url:
            return None
        if url.startswith("http"):
            full = url
        elif url.startswith("/freevideo/"):
            full = self.root + url
        else:
            full = self.api + url
        req = urllib.request.Request(full,
                                     headers={"Authorization": "Bearer " + self.token})
        op = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with op.open(req, timeout=600) as r:
            data = r.read()
        out = pathlib.Path(outdir) / name
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
        return str(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--image", action="append", default=[],
                    help="參考圖路徑，可重複（最多 9 張）")
    ap.add_argument("--label", default="generate")
    ap.add_argument("--width", type=int, default=960)
    ap.add_argument("--height", type=int, default=544)
    ap.add_argument("--seconds", type=float, default=8.0)
    ap.add_argument("--quality", default="light")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--wait", action="store_true")
    ap.add_argument("--outdir", default="analysis/drone")
    a = ap.parse_args()

    c = Client()
    refs = []
    for img in a.image:
        f = c.upload(img)
        print(f"上傳：{img} -> {f}", flush=True)
        refs.append({"file": f})

    prompt = pathlib.Path(a.prompt).read_text(encoding="utf-8").strip()
    # 注意：API 的 schema 沒有 top-level "task" 欄位（有 media.references 會自動
    # 推導成 ref2va），帶了會回 422 "must be absent (unknown field)"。
    spec = {
        "kind": "generate",
        "label": a.label,
        "prompt": prompt,
        "width": a.width,
        "height": a.height,
        "seconds": a.seconds,
        "quality": a.quality,
        "media": {"references": refs},
    }
    if a.seed is not None:
        spec["seed"] = a.seed

    res = c.call("POST", "/jobs", {"jobs": [spec]})
    created = res.get("jobs") or res.get("created") or []
    jid = created[0].get("id") if created else None
    print(f"已送出：{jid}  {a.label}", flush=True)

    outdir = pathlib.Path(a.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "jobs.json").write_text(
        json.dumps({"after": jid, "spec": spec}, ensure_ascii=False, indent=2),
        encoding="utf-8")

    if not a.wait:
        print("未等待完成。")
        return 0

    t0 = time.time()
    while time.time() - t0 < 7200:
        j = c.call("GET", f"/jobs/{jid}?wait=25")["job"]
        st = j.get("status")
        if st in ("succeeded", "failed", "cancelled", "interrupted"):
            print(f"狀態：{st}", flush=True)
            if st == "succeeded":
                p = c.download(j, outdir, "after.mp4")
                print(f"已下載：{p}", flush=True)
            return 0 if st == "succeeded" else 1
        pr = j.get("progress") or {}
        print(f"  {st} {pr.get('percent','')}", flush=True)
    return 1


if __name__ == "__main__":
    sys.exit(main())
