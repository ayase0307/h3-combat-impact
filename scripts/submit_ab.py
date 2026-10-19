#!/usr/bin/env python3
"""向本機 FreeVideo 提交兩支 A/B 生成工作（技能使用前 / 使用後）。

這是「改版後要拿出證據」流程的第一步。兩版提示詞用**同一個 seed** 送出，
唯一的變因就是提示詞本身——這樣出來的對照才是嚴格的單變因實驗。

用法：
    python scripts/submit_ab.py --before before.txt --after after.txt \
        --label-before "A · 未套用技能" --label-after "B · 套用技能後" \
        --width 960 --height 544 --seconds 8 --quality light --seed 20261019

選項：
    --width  --height     目標解析度（預設 960x544，16:9）
    --seconds             生成時長（預設 8.0）
    --quality             light | medium | high | max（預設 light）
    --seed                固定亂數種子，讓 A/B 只差在提示詞（**一定要固定**）
    --image               首幀圖片路徑（走 I2VA）；省略則走 T2VA
    --wait                等待完成並下載（否則只送出並回報 job id）
    --outdir              下載輸出目錄（預設 analysis/ab）
    --api                 API 位址（預設 http://127.0.0.1:8189/freevideo/agent/v1）
    --token-file          token 檔案（預設 $FREEVIDEO_TOKEN，或 E:\\FreeVideo\\agent\\token）

回傳：兩個 job id，存成 <outdir>/jobs.json。

後續：
    python scripts/compare_clips.py --before <outdir>/before.mp4 \
        --after <outdir>/after.mp4 --out compare.gif \
        --label-before "A · 未套用技能" --label-after "B · 套用技能後" \
        --width 240 --fps 8 --colors 64 --dither-scale 3
"""

import argparse
import base64
import json
import os
import pathlib
import sys
import time
import urllib.request

DEFAULT_API = "http://127.0.0.1:8189/freevideo/agent/v1"
DEFAULT_TOKEN = r"E:\FreeVideo\agent\token"


def resolve_token(explicit=None):
    """token 來源的優先序：--token-file → 環境變數 → 預設路徑。"""
    if explicit:
        return pathlib.Path(explicit)
    env = os.environ.get("FREEVIDEO_TOKEN")
    if env:
        return pathlib.Path(env)
    return pathlib.Path(DEFAULT_TOKEN)


class Client:
    def __init__(self, api, token_file):
        self.api = api.rstrip("/")
        # API 位址去掉尾端 /freevideo/agent/v1 就是主機根目錄，
        # 媒體下載網址本身已含完整路徑前綴，必須接在根目錄而不是 API 前綴上。
        self.root = self.api[: -len("/freevideo/agent/v1")] if self.api.endswith(
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
        with op.open(req, timeout=180) as r:
            payload = r.read()
        if raw:
            return payload
        return json.loads(payload.decode("utf-8"))

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
        # result.video.url 已含完整路徑前綴（/freevideo/agent/v1/library/...），
        # 必須接在主機根目錄，不能再疊 API 前綴，否則會 404。
        if url.startswith("http://") or url.startswith("https://"):
            full = url
        elif url.startswith("/freevideo/"):
            full = self.root + url
        else:
            full = self.api + url
        req = urllib.request.Request(full,
                                     headers={"Authorization": "Bearer " + self.token})
        op = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with op.open(req, timeout=300) as r:
            data = r.read()
        out = pathlib.Path(outdir) / name
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
        return str(out)


def upload(client, path):
    """上傳圖片到 FreeVideo 的 media 區，回傳可用的 file 路徑。"""
    p = pathlib.Path(path)
    b64 = base64.b64encode(p.read_bytes()).decode("ascii")
    res = client.call("POST", "/media", {"name": p.name, "data_base64": b64})
    if isinstance(res, dict):
        f = res.get("file") or (res.get("media") or {}).get("file")
        if f:
            return f
        for k in ("path", "url", "id"):
            if res.get(k):
                return res[k]
    return res


def build_job(label, prompt, args, image_file):
    spec = {
        "kind": "generate",
        "label": label,
        "prompt": prompt,
        "width": args.width,
        "height": args.height,
        "seconds": args.seconds,
        "quality": args.quality,
    }
    if args.seed is not None:
        spec["seed"] = args.seed
    if image_file:
        spec["media"] = {"first": {"file": image_file}}
    return spec


def wait_for(client, jid, timeout=21600):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            j = client.call("GET", f"/jobs/{jid}?wait=25")["job"]
        except Exception as e:
            print(f"  poll error: {e}", flush=True)
            continue
        st = j.get("status")
        if st in ("succeeded", "failed", "cancelled", "interrupted"):
            return j
        pr = j.get("progress") or {}
        print(f"  [{(j.get('label') or '?')[:24]}] {st} {pr.get('percent', '')}",
              flush=True)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--before", required=True)
    ap.add_argument("--after", required=True)
    ap.add_argument("--label-before", default="BEFORE")
    ap.add_argument("--label-after", default="AFTER")
    ap.add_argument("--width", type=int, default=960)
    ap.add_argument("--height", type=int, default=544)
    ap.add_argument("--seconds", type=float, default=8.0)
    ap.add_argument("--quality", default="light")
    ap.add_argument("--seed", type=int, default=None,
                    help="固定種子。A/B 必須固定，否則不是單變因實驗。")
    ap.add_argument("--image", default=None)
    ap.add_argument("--wait", action="store_true")
    ap.add_argument("--outdir", default="analysis/ab")
    ap.add_argument("--api", default=DEFAULT_API)
    ap.add_argument("--token-file", default=None)
    a = ap.parse_args()

    if a.seed is None:
        print("提示：未指定 --seed。A/B 對照建議固定種子，"
              "否則兩版會用不同隨機種子，比較就不嚴格了。", file=sys.stderr)

    before_prompt = pathlib.Path(a.before).read_text(encoding="utf-8").strip()
    after_prompt = pathlib.Path(a.after).read_text(encoding="utf-8").strip()

    token_file = resolve_token(a.token_file)
    if not token_file.exists():
        print(f"找不到 token 檔：{token_file}\n"
              f"請用 --token-file 指定，或設定環境變數 FREEVIDEO_TOKEN。",
              file=sys.stderr)
        return 2
    client = Client(a.api, token_file)

    image_file = None
    if a.image:
        image_file = upload(client, a.image)
        print(f"首幀已上傳：{image_file}", flush=True)

    jobs = [
        build_job(a.label_before, before_prompt, a, image_file),
        build_job(a.label_after, after_prompt, a, image_file),
    ]
    res = client.call("POST", "/jobs", {"jobs": jobs})
    created = res.get("jobs") or res.get("created") or []
    ids = []
    for j in created:
        if isinstance(j, dict):
            ids.append((j.get("id"), j.get("label")))
    print("已送出：")
    for jid, lbl in ids:
        print(f"  {jid}  {lbl}")

    outdir = pathlib.Path(a.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "jobs.json").write_text(
        json.dumps({"before": ids[0][0] if ids else None,
                    "after": ids[1][0] if len(ids) > 1 else None,
                    "spec_before": jobs[0], "spec_after": jobs[1]},
                   ensure_ascii=False, indent=2), encoding="utf-8")

    if not a.wait:
        print("\n未等待完成。稍後用 poll_ab.py 查詢並下載。")
        return 0

    for (jid, lbl), name in ((ids[0], "before.mp4"), (ids[1], "after.mp4")):
        print(f"\n等待 {lbl} ({jid}) ...", flush=True)
        job = wait_for(client, jid)
        if not job:
            print(f"  {lbl} 逾時", flush=True)
            continue
        print(f"  {lbl} → {job.get('status')}", flush=True)
        if job.get("status") == "succeeded":
            try:
                p = client.download(job, outdir, name)
                print(f"  已下載：{p}", flush=True)
            except Exception as e:
                print(f"  下載失敗：{e}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
