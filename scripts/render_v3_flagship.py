#!/usr/bin/env python3
"""以實測冠軍管線（PRISM_int8 + DMAD 0.8 + SelfLift 14s simple + hires-dials off）批量渲染 9 套旗艦 15 秒 AI 漫劇成片。

用法：
    python scripts/render_v3_flagship.py                  # 跑全部未完成套件
    python scripts/render_v3_flagship.py rep01 rep02      # 只跑指定套件
    python scripts/render_v3_flagship.py --upscale rep01  # 連同 ReCaVSR 2x 一起跑
"""

import argparse
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
COMFY = os.environ.get("COMFYUI_URL", "http://127.0.0.1:8188")
ASSETS = ROOT / "assets" / "v3-manju"
PROMPTS = ROOT / "examples" / "v3-manju"
OUT = ROOT / "analysis" / "v3-manju" / "flagship"

JOBS = {
    "rep01": {
        "prompt": "rep01_thunder_cleave.txt",
        "refs": ["rep01/leijin.png", "rep01/bg_volcano.png"],
        "preset": "P3",
        "hits": ["0.8:1.2", "10.6:11.0"],
        "seed": 6101,
    },
    "rep02": {
        "prompt": "rep02_ink_flame_sea.txt",
        "refs": ["rep02/chichuan.png", "rep02/xuanlan.png", "rep02/bg_ink_sea.png"],
        "preset": "P3",
        "hits": ["9.0:9.4", "11.8:12.2"],
        "seed": 6201,
    },
    "rep03": {
        "prompt": "rep03_jade_hammer_dragon.txt",
        "refs": ["rep03/qinglan.png", "rep03/dragon_azure.png", "rep03/bg_fairy_gorge.png"],
        "preset": "P3",
        "hits": ["0.3:0.7", "10.2:10.6"],
        "seed": 6301,
    },
    "rep04": {
        "prompt": "rep04_v4_myriad_swords_cannon.txt",
        "refs": ["rep04/taixuan.png", "rep04/bg_pine_cliff.png"],
        "preset": "P8",
        "anchors": ["0.0:4.2:-0.65", "4.2:9.0:-0.30"],
        "bursts": ["9.2:12.0:0.65", "12.0:15.0:0.80"],
        "hits": ["9.0:9.3", "12.8:13.1"],
        "hires_dials": "phase-motion",
        "seed": 6401,
    },
    "rep05": {
        "prompt": "rep05_void_vs_peacock.txt",
        "refs": ["rep05/yeshi.png", "rep05/lihuang.png", "rep05/bg_sunset_meadow.png"],
        "preset": "P7",
        "bursts": ["0.0:3.3:0.65", "3.8:15.0:0.60"],
        "hitstops": ["3.4:3.7:-1.8"],
        "hits": [],
        "hires_dials": "phase-motion",
        "seed": 6501,
    },
    "orig01": {
        "prompt": "orig01_v13_crimson_frost_blade_duel.txt",
        "refs": ["orig01_v5/jinyuan_katana.png", "orig01_v5/heming_broadsword.png", "orig01_v5/bg_rooftop_terrace.png"],
        "preset": "P9",
        "closeups": ["6.2:8.8"],
        "hits": ["12.2:12.5"],
        "hires_dials": "off",
        "seed": 7201,
    },
    "orig02": {
        "prompt": "orig02_bamboo_lantern_umbrella_vs_spear.txt",
        "refs": ["orig02/feiyu.png", "orig02/hanji.png", "orig02/bg_bamboo_lanterns.png"],
        "preset": "P3",
        "hits": ["3.6:4.0", "12.8:13.2"],
        "seed": 7201,
    },
    "ult01": {
        "prompt": "ult01_brush_seal_army.txt",
        "refs": ["ult01/moli.png", "ult01/bg_fortress_pass.png"],
        "preset": "P5",
        "hits": ["10.8:11.2"],
        "seed": 8101,
    },
    "ult02": {
        "prompt": "ult02_lunar_prism_domain.txt",
        "refs": ["ult02/wangshu.png", "ult02/bg_lunar_lake.png"],
        "preset": "P5",
        "hits": [],
        "seed": 8201,
    },
}


def free_comfy_memory() -> None:
    """主動通知 ComfyUI 卸載模型與釋放 VRAM/RAM，避免長批次連跑累積 OOM。"""
    import json
    import urllib.request
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        req = urllib.request.Request(
            f"{COMFY}/free",
            data=json.dumps({"unload_models": True, "free_memory": True}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        opener.open(req, timeout=15).read()
    except Exception:
        pass


def make_sheet(mp4: pathlib.Path, jpg: pathlib.Path) -> None:
    cmd = [
        "ffmpeg", "-y", "-v", "error", "-i", str(mp4),
        "-vf", "fps=0.45,scale=640:-2,tile=3x2", "-frames:v", "1", "-q:v", "2", str(jpg),
    ]
    subprocess.run(cmd, check=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("suites", nargs="*", help="指定套件名稱（留空則跑全部 9 套）")
    ap.add_argument("--upscale", action="store_true", help="每支成片跑完再接 ReCaVSR 2x 超分到 2K")
    ap.add_argument("--seconds", type=float, default=15.0)
    ap.add_argument("--force", action="store_true", help="強制覆蓋已存在的 mp4")
    args = ap.parse_args()

    targets = args.suites if args.suites else list(JOBS.keys())
    OUT.mkdir(parents=True, exist_ok=True)
    rendered: list[str] = []

    for idx, key in enumerate(targets, 1):
        cfg = JOBS[key]
        out_mp4 = OUT / f"{key}_15s_prism14.mp4"
        if out_mp4.exists() and not args.force:
            print(f"[{idx}/{len(targets)}] SKIP existing {out_mp4.name}", flush=True)
        else:
            cmd = [
                sys.executable, str(ROOT / "scripts" / "render_comfy.py"),
                "--engine", "selflift",
                "--unet", "Minimax-h3_Singularity_x_10Eros-Max_PRISM_int8.safetensors",
                "--dmad", "0.8",
                "--scheduler", "simple",
                "--steps", "14",
                "--transition", "6",
                "--lowres-scale", "0.6",
                "--chunks", "4",
                "--hires-dials", cfg.get("hires_dials", "off"),
                "--prompt", str(PROMPTS / cfg["prompt"]),
                "--seconds", str(args.seconds),
                "--seed", str(cfg["seed"]),
                "--stage", "final",
                "--preset", cfg["preset"],
                "--job", f"v3_{key}_15s",
                "--out", str(out_mp4),
            ]
            for r in cfg["refs"]:
                cmd += ["--ref", str(ASSETS / r)]
            if "motion" in cfg:
                cmd += ["--motion", str(cfg["motion"])]
            for lr in cfg.get("loras", []):
                cmd += ["--lora", lr]
            for llr in cfg.get("lowres_loras", []):
                cmd += ["--lowres-lora", llr]
            for a in cfg.get("anchors", []):
                cmd += ["--anchor", a]
            for b in cfg.get("bursts", []):
                cmd += ["--burst", b]
            for hs in cfg.get("hitstops", []):
                cmd += ["--hitstop", hs]
            for cu in cfg.get("closeups", []):
                cmd += ["--closeup", cu]
            for h in cfg.get("hits", []):
                cmd += ["--hit", h]
            print(f"\n=== [{idx}/{len(targets)}] RENDER {key} ({cfg['preset']}, hits={cfg['hits']}) ===", flush=True)
            res = subprocess.run(cmd)
            if res.returncode != 0:
                sys.exit(f"Render failed on {key} (exit {res.returncode})")
        make_sheet(out_mp4, OUT / f"{key}_sheet.jpg")
        rendered.append(str(out_mp4))

        if args.upscale:
            out_2k = OUT / f"{key}_15s_2k.mp4"
            if not (out_2k.exists() and not args.force):
                ucmd = [
                    sys.executable, str(ROOT / "scripts" / "render_comfy.py"),
                    "--stage", "upscale",
                    "--seconds", str(args.seconds),
                    "--input-video", str(out_mp4),
                    "--job", f"v3_{key}_2k",
                    "--out", str(out_2k),
                ]
                print(f"=== [{idx}/{len(targets)}] UPSCALE 2K {key} ===", flush=True)
                res = subprocess.run(ucmd)
                if res.returncode != 0:
                    sys.exit(f"Upscale failed on {key}")
        free_comfy_memory()

    if rendered:
        print("\n=== Quantitative QA (Motion & Sharpness) ===", flush=True)
        subprocess.run([sys.executable, str(ROOT / "scripts" / "measure_motion.py"), "--fps24"] + rendered)
        subprocess.run([sys.executable, str(ROOT / "scripts" / "measure_sharpness.py")] + rendered)


if __name__ == "__main__":
    main()
