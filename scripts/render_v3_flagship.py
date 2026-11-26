#!/usr/bin/env python3
"""以實測冠軍管線（PRISM_int8 + DMAD 0.8 + SelfLift 14s simple）批量渲染 9 套旗艦 15 秒 AI 漫劇成片。

v4.0：9 套全部走 P7/P8/P9 相位正負雙軌（--anchor / --burst / --hitstop / --closeup），
P7/P8 二採 --hires-dials phase-motion，P9 依左眼 5.0 實證維持 --hires-dials off。
每套 `beats` 列出劇本鏡內的相位轉折秒數（雙軌邊界若不在切點上，必須落在這裡）。

用法：
    python scripts/render_v3_flagship.py                  # 跑全部未完成套件
    python scripts/render_v3_flagship.py rep01 rep02      # 只跑指定套件
    python scripts/render_v3_flagship.py --force rep01    # 覆蓋已存在的 mp4 重跑
    python scripts/render_v3_flagship.py --dry            # 只建圖與印出 Dial 運動預算，不送 ComfyUI
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
        # v4.0：切點 0/3.2/6.2/9.0/10.6/12.6。P8 base_eff +0.30；地面清場 +0.65、騰空與天劍破空 +0.80；頓幀後末段續行 +0.65（不鎖尾，防末幀凍結）
        "preset": "P8",
        "bursts": ["0.0:2.9:0.65", "2.9:5.9:0.80", "8.7:10.5:0.80", "10.9:15.0:0.65"],
        "anchors": ["5.9:8.7:-0.65"],
        "hitstops": ["10.6:10.85:-1.8"],
        "hits": ["0.8:1.1"],
        "beats": [],
        "hires_dials": "phase-motion",
        "seed": 6101,
    },
    "rep02": {
        "prompt": "rep02_ink_flame_sea.txt",
        "refs": ["rep02/chichuan.png", "rep02/xuanlan.png", "rep02/bg_ink_sea.png"],
        # v4.0：切點 0/3.2/6.2/9.0/11.6。P9 實證五滑塊 base_eff +0.69（含 motion 0.50），正軌上限 +0.29 才守住 +0.98
        "preset": "P9",
        "closeups": ["6.0:9.0"],
        "anchors": ["5.9:8.7:-0.30"],
        "bursts": ["0.0:5.9:0.25", "11.3:15.0:0.25"],
        "hitstops": ["9.0:9.25:-1.8"],
        "hits": ["11.8:12.1"],
        "beats": [],
        "hires_dials": "off",
        "seed": 6201,
    },
    "rep03": {
        "prompt": "rep03_jade_hammer_dragon.txt",
        "refs": ["rep03/qinglan.png", "rep03/dragon_azure.png", "rep03/bg_fairy_gorge.png"],
        # v4.0：切點 0/2.8/6.0/9.0/12.2。P7 base_eff +0.32；踏浪奔襲 +0.65、騰空 +0.80；特寫段 10.2s 轉側面重錘（頓幀）後末段續行 +0.65，不鎖尾
        "preset": "P7",
        "bursts": ["0.0:5.7:0.65", "5.7:8.7:0.80", "10.5:15.0:0.65"],
        "anchors": ["8.7:10.2:-0.55"],
        "hitstops": ["0.35:0.6:-1.8", "10.2:10.45:-1.8"],
        "hits": [],
        "beats": [10.2],
        "hires_dials": "phase-motion",
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
        # v4.0：切點 0/3.2/6.2/9.1/12.0。P7；特寫 7.8s 轉紅絲彈射、12.8s 奪槍頓幀、13.3s 後單膝定樁
        "preset": "P7",
        "bursts": ["0.0:5.9:0.65", "8.8:12.8:0.65"],
        "anchors": ["5.9:7.8:-0.55", "13.3:15.0:-0.45"],
        "hitstops": ["12.8:13.05:-1.8"],
        "hits": ["3.6:3.9", "10.6:10.9"],
        "beats": [7.8, 12.8, 13.3],
        "hires_dials": "phase-motion",
        "seed": 7201,
    },
    "ult01": {
        "prompt": "ult01_brush_seal_army.txt",
        "refs": ["ult01/moli.png", "ult01/bg_fortress_pass.png"],
        # v4.0：切點 0/3.2/7.0/10.8。P8 取代 P5：P5 的 arcane_sigils 走固定正規化關鍵幀（45–65% 滿、80% 歸零），與本劇本切點無關且無 storm 可乘雙軌；
        # 代價是失去 sigils 滑塊，墨圈只靠 prompt（驗收看墨圈仍清楚可讀，糊掉就用 render_comfy --rack 補短 h3_arcane_sigils 脈衝 A/B）。
        # 特寫 5.0s 轉環繞揮毫；頓幀後末段續行 +0.65，不鎖尾
        "preset": "P8",
        "bursts": ["0.0:2.9:0.65", "6.7:10.5:0.80", "11.1:15.0:0.65"],
        "anchors": ["2.9:5.0:-0.55"],
        "hitstops": ["10.8:11.05:-1.8"],
        "hits": [],
        "beats": [5.0],
        "hires_dials": "phase-motion",
        "seed": 8101,
    },
    "ult02": {
        "prompt": "ult02_lunar_prism_domain.txt",
        "refs": ["ult02/wangshu.png", "ult02/bg_lunar_lake.png"],
        # v4.0：切點 0/4.0/7.8/11.0。P8 取代 P5（理由與代價同 ult01：失去 sigils 滑塊，驗收看冰陣仍清楚可讀，必要時 --rack 補脈衝）；
        # 點湖與結印定樁、冰柱破湖到冰蓮綻放直到末幀正軌 +0.55（不鎖尾）
        "preset": "P8",
        "anchors": ["0.0:3.7:-0.30", "3.7:7.5:-0.65"],
        "bursts": ["7.5:15.0:0.55"],
        "hits": [],
        "beats": [],
        "hires_dials": "phase-motion",
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
    ap.add_argument("--dry", action="store_true", help="只建圖並印出 Dial 運動預算，不送 ComfyUI、不出片")
    args = ap.parse_args()

    targets = args.suites if args.suites else list(JOBS.keys())
    OUT.mkdir(parents=True, exist_ok=True)
    rendered: list[str] = []

    for idx, key in enumerate(targets, 1):
        cfg = JOBS[key]
        out_mp4 = OUT / f"{key}_15s_prism14.mp4"
        if out_mp4.exists() and not args.force and not args.dry:
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
            if args.dry:
                cmd.append("--dry")
            print(f"\n=== [{idx}/{len(targets)}] RENDER {key} ({cfg['preset']}, hits={cfg['hits']}) ===", flush=True)
            res = subprocess.run(cmd)
            if res.returncode != 0:
                sys.exit(f"Render failed on {key} (exit {res.returncode})")
        if args.dry:
            continue
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
