#!/usr/bin/env python3
"""等待 A/B 兩支生成完成並下載。

用法：
    python scripts/poll_ab.py --jobs analysis/ab/jobs.json
    python scripts/poll_ab.py --once        # 只查一次狀態

支援續跑：已下載且檔案大小合理的影片會直接跳過，不重複等待。
"""

import argparse
import json
import os
import pathlib
import sys
import time
import urllib.request

DEFAULT_API = "http://127.0.0.1:8189/freevideo/agent/v1"
DEFAULT_TOKEN = r"E:\FreeVideo\agent\token"
MIN_SIZE = 100_000  # 小於這個大小視為下載失敗


def resolve_token(explicit=None):
    if explicit:
        return pathlib.Path(explicit)
    env = os.environ.get("FREEVIDEO_TOKEN")
    if env:
        return pathlib.Path(env)
    return pathlib.Path(DEFAULT_TOKEN)


class Client:
    def __init__(self, api, token_file):
        self.api = api.rstrip("/")
        self.root = self.api[: -len("/freevideo/agent/v1")] if self.api.endswith(
            "/freevideo/agent/v1") else self.api
        self.token = token_file.read_text(encoding="utf-8").strip()

    def call(self, path):
        req = urllib.request.Request(self.api + path,
                                     headers={"Authorization": "Bearer " + self.token})
        op = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with op.open(req, timeout=180) as r:
            return json.load(r)

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
        # result.video.url 已含完整路徑前綴，必須接在主機根目錄，不能疊 API 前綴
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", default="analysis/ab/jobs.json")
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--timeout", type=int, default=21600)
    ap.add_argument("--api", default=DEFAULT_API)
    ap.add_argument("--token-file", default=None)
    a = ap.parse_args()

    jobs_path = pathlib.Path(a.jobs)
    if not jobs_path.exists():
        print(f"找不到 {jobs_path}", file=sys.stderr)
        return 2
    token_file = resolve_token(a.token_file)
    if not token_file.exists():
        print(f"找不到 token 檔：{token_file}", file=sys.stderr)
        return 2
    client = Client(a.api, token_file)

    meta = json.loads(jobs_path.read_text(encoding="utf-8"))
    outdir = jobs_path.parent
    targets = [("before", meta.get("before"), "before.mp4"),
               ("after", meta.get("after"), "after.mp4")]
    t0 = time.time()
    done = {}

    # 續跑：已下載且檔案合理的直接標完成
    for key, jid, name in targets:
        p = outdir / name
        if jid and p.exists() and p.stat().st_size > MIN_SIZE:
            done[key] = "succeeded(downloaded)"
            print(f"[{key}] already downloaded -> {p}", flush=True)
    if len(done) == len(targets):
        print("ALL DONE", json.dumps(done), flush=True)
        return 0

    while True:
        for key, jid, name in targets:
            if key in done or not jid:
                continue
            try:
                j = client.call(f"/jobs/{jid}?wait=25")["job"]
            except Exception as e:
                print(f"  poll error {key}: {e}", flush=True)
                continue
            st = j.get("status")
            pr = j.get("progress") or {}
            if st in ("succeeded", "failed", "cancelled", "interrupted"):
                done[key] = st
                print(f"[{key}] {st}", flush=True)
                if st == "succeeded":
                    try:
                        p = client.download(j, outdir, name)
                        print(f"  -> {p}", flush=True)
                    except Exception as e:
                        # 下載失敗不能讓整個輪詢死掉，標記後續重試
                        print(f"  download error {key}: {e}", flush=True)
                        done.pop(key, None)
            else:
                print(f"[{key}] {st} {pr.get('percent','')} "
                      f"queue_pos={pr.get('queue_position','')}", flush=True)

        if len(done) == len(targets):
            print("ALL DONE", json.dumps(done), flush=True)
            return 0
        if a.once:
            return 0
        if time.time() - t0 > a.timeout:
            print("TIMEOUT", json.dumps(done), flush=True)
            return 1
        time.sleep(3)


if __name__ == "__main__":
    sys.exit(main())
