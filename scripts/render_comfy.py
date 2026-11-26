#!/usr/bin/env python3
"""本機 ComfyUI 出片管線（支援 Pika 6 步 LCM 與 PRISM/YZ金魚 SelfLiftH3Sampler 一採二採＋Dials＋De-rope＋ReCaVSR 2x）。

用法範例：
    # 1. PRISM + YZ金魚 SelfLiftH3Sampler（euler + simple 12/14 步，0.6x->1.0x 潛空間一採二採，大幅降動態模糊）
    python scripts/render_comfy.py --engine selflift \
        --unet Minimax-h3_Singularity_x_10Eros-Max_PRISM_int8.safetensors --dmad 0.8 \
        --scheduler simple --steps 12 --transition 6 --lowres-scale 0.6 --chunks 4 --hires-dials off \
        --prompt examples/v3-manju/caseA_manju_8s.txt \
        --ref assets/v3-manju/caseA/hero_feixue.png --ref assets/v3-manju/caseA/villain_shuangjue.png --ref assets/v3-manju/caseA/scene_snow_peak.png \
        --seconds 8 --seed 5002 --stage final --preset P3 --hit 2.2:2.6 --hit 6.6:7.0 \
        --job v3_prism_selflift --out analysis/v3-manju/v3_prism_selflift.mp4

    # 2. PRISM_DMAD_PDMD_int8（已內融 DMAD/PDMD，務必設 --dmad 0 勿重複疊掛 DMAD LoRA）
    python scripts/render_comfy.py --engine selflift \
        --unet PRISM_DMAD_PDMD_int8.safetensors --dmad 0 \
        --scheduler simple --steps 10 --transition 5 --lowres-scale 0.6 --chunks 4 --hires-dials off \
        --prompt examples/v3-manju/caseA_manju_8s.txt --ref ... --seconds 8 --seed 5002 --stage final --preset P3 \
        --job v3_prism_pdmd --out analysis/v3-manju/v3_prism_pdmd.mp4

    # 3. 傳統 Pika 6 步 LCM（快速抽卡／相容舊管線）
    python scripts/render_comfy.py --engine pika --prompt ... --ref ... --seconds 15 --seed 5001 --stage final --preset P3 --job test --out out/test.mp4

    # 3b. Sulphur-3 組件（實驗性，見 docs/research/2026-11-26-sulphur3-anti-artifact-study.md）
    #     --corrector 需像素寬高皆為 32 的倍數（768p 可，draft480 不可）。16GB 卡上 fp32 修正器掛二採會溢出顯存，
    #     兩段都掛時請加 --corrector-precision bf16。
    python scripts/render_comfy.py --engine selflift ...（同範例 1）... \
        --corrector s3_corrector.safetensors --corrector-stage low
    #     Motion/STG（只作用於一採骨架期；--still-prompt 為「全部動作凍結」的靜止版劇本）
    python scripts/render_comfy.py --engine selflift ...（同範例 1）... \
        --motion-stg --still-prompt examples/v3-manju/caseA_manju_8s_still.txt --stg-until 0.5

    # 4. 三採 ReCaVSR 2x 超分（768p -> 2K）
    python scripts/render_comfy.py --stage upscale --input-video analysis/v3-manju/v3_prism_selflift.mp4 \
        --job v3_prism_2k --out analysis/v3-manju/v3_prism_2k.mp4
"""

import argparse
import copy
import json
import os
import pathlib
import re
import shutil
import sys
import time
import urllib.parse
import urllib.request
import uuid

COMFY = os.environ.get("COMFYUI_URL", "http://127.0.0.1:8188")
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))

DEFAULT_SELFLIFT_UNET = "Minimax-h3_Singularity_x_10Eros-Max_PRISM_int8.safetensors"
DEFAULT_PIKA_UNET = "minimax_h3_ref2va_pruned_int8_convrot.safetensors"
DEFAULT_PIKA_LORA = "pika_h3_flex_ref2va_v1_bf16.safetensors"
DEFAULT_PIKA_SIGMAS = "1.0, 0.972973, 0.923077, 0.8, 0.571429, 0.333333, 0.0"
DEFAULT_DMAD_LORA = "minimax_h3_dmad_full_dareties_v4_step600_comfy_fro.safetensors"
DEFAULT_H3_UPSCALER = "h3_upscaler_lms_v0.1.safetensors"
DEFAULT_CLIP = "qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors"
DEFAULT_VIDEO_VAE = "minimax_h3_video_vae_int8_convrot.safetensors"
DEFAULT_AUDIO_VAE = "minimax_h3_audio_vae_fp32.safetensors"
DEFAULT_RECAVSR_MODEL = "transformer_int8_convrot.safetensors"

# ComfyUI-H3-Corrector-Advanced（Sulphur-3 experimental）Controls 節點預設值（profiles.DEFAULT_SETTINGS）
CORRECTOR_ADV_DEFAULTS = {
    "strength": 1.0, "budget_fraction": 0.5, "velocity_floor": 0.001, "start_step": 0, "end_step": -1,
    "enable_layer_controls": False, "block_strength": 1.0, "self_attention_strength": 1.0,
    "cross_attention_strength": 1.0, "mlp_strength": 1.0, "layer_overrides": "{}", "enable_cache": False,
    "enable_directional": False, "backward_limit": 0.25, "forward_limit": 0.25, "turn_limit": 0.20,
    "enable_local_budget": False, "local_budget": 0.25, "local_window": 5, "enable_frequency_budget": False,
    "low_budget": 0.15, "high_budget": 0.35, "frequency_cutoff": 0.25, "enable_sparse_correction": False,
    "correction_interval": 2, "always_correct_last": True, "enable_timing": False, "enable_compile": False,
    "compile_mode": "default", "attention_backend": "auto", "enable_diagnostics": False, "cache_limit_mb": 256,
}


def h3_frames(seconds: float) -> int:
    """MiniMax H3 24fps 合法幀數對齊公式（n ≡ 5 mod 17）。"""
    n = max(5, round(float(seconds) * 24))
    return n + (5 - n % 17) % 17


def build_pika_graph(prompt: str, seconds: float, seed: int, width: int, height: int,
                     picture_files: list[str], rack: list[dict], job: str) -> dict:
    """建構獨立自含的 Pika H3 Flex 6 步 LCM ComfyUI 節點圖（無外部私有套件依賴）。"""
    ref_inputs: dict = {
        "clip": ["3", 0],
        "vae": ["4", 0],
        "audio_vae": ["5", 0],
        "prompt": prompt,
        "width": width,
        "height": height,
        "length": h3_frames(seconds),
        "ref_image_size": "match",
    }
    graph: dict = {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": DEFAULT_PIKA_UNET, "weight_dtype": "default"}},
        "2": {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["1", 0], "lora_name": DEFAULT_PIKA_LORA, "strength_model": 1.0}},
        "3": {"class_type": "CLIPLoader", "inputs": {"clip_name": DEFAULT_CLIP, "type": "minimax", "device": "default"}},
        "4": {"class_type": "VAELoader", "inputs": {"vae_name": DEFAULT_VIDEO_VAE}},
        "5": {"class_type": "VAELoader", "inputs": {"vae_name": DEFAULT_AUDIO_VAE}},
        "7": {"class_type": "MiniMaxH3ReferenceToVideo", "inputs": ref_inputs},
        "8": {"class_type": "BasicGuider", "inputs": {"model": ["61", 0], "conditioning": ["7", 0]}},
        "9": {"class_type": "RandomNoise", "inputs": {"noise_seed": seed}},
        "10": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "lcm"}},
        "11": {"class_type": "ManualSigmas", "inputs": {"sigmas": DEFAULT_PIKA_SIGMAS}},
        "12": {
            "class_type": "SamplerCustomAdvanced",
            "inputs": {
                "noise": ["9", 0], "guider": ["8", 0], "sampler": ["10", 0],
                "sigmas": ["11", 0], "latent_image": ["7", 1],
            },
        },
        "13": {"class_type": "VAEDecode", "inputs": {"samples": ["12", 0], "vae": ["4", 0]}},
        "14": {"class_type": "VAEDecodeAudio", "inputs": {"samples": ["12", 0], "vae": ["5", 0]}},
        "15": {
            "class_type": "VHS_VideoCombine",
            "inputs": {
                "images": ["13", 0], "audio": ["14", 0], "frame_rate": 24, "loop_count": 0,
                "filename_prefix": f"h3_combat/{job}", "format": "video/h264-mp4", "pix_fmt": "yuv420p",
                "crf": 18, "save_metadata": True, "trim_to_audio": False, "pingpong": False, "save_output": True,
            },
        },
    }
    for i, name in enumerate(picture_files):
        graph[str(30 + i)] = {"class_type": "LoadImage", "inputs": {"image": name}}
        ref_inputs[f"ref_images.ref_image_{i}"] = [str(30 + i), 0]
    base = "2"
    if rack:
        graph["dr"] = {"class_type": "MAIDialRack", "inputs": {"model": [base, 0], "rack": json.dumps(rack, ensure_ascii=False)}}
        base = "dr"
    graph["60"] = {"class_type": "ModelAttentionBackend", "inputs": {"model": [base, 0], "attention": "comfy kitchen attention"}}
    graph["61"] = {
        "class_type": "BlockSparseAttention",
        "inputs": {
            "model": ["60", 0], "selection": "sol-attn", "selection.tau": 1.3,
            "start_percent": 0.2, "end_percent": 1.0, "dense_blocks": "",
            "min_tokens": 12288, "extra_tokens": 256, "sink_conditioning": "exact_kv_and_rows", "verbose": False,
        },
    }
    return graph


def build_recavsr_graph(input_filename: str, job: str) -> dict:
    """建構獨立自含的 ReCaVSR 2x 影片超分節點圖。"""
    return {
        "1": {"class_type": "LoadVideo", "inputs": {"file": input_filename}},
        "2": {"class_type": "ReCaVSRLoader", "inputs": {"transformer": DEFAULT_RECAVSR_MODEL}},
        "3": {
            "class_type": "ReCaVSRUpscale",
            "inputs": {
                "model": ["2", 0], "video": ["1", 0], "scale": 2.0, "color_fix": "wavelet",
                "seed": 42, "decoder": "flashdecoder", "kernels": "fast",
                "kv_offload": False, "encoder": "h264 nvenc",
            },
        },
        "4": {
            "class_type": "SaveVideo",
            "inputs": {"video": ["3", 0], "filename_prefix": f"h3_combat/{job}_2k", "format": "mp4", "codec": "auto"},
        },
    }

# 八組即用型武戲 Dial Rack 配方（對應 references/comfyui-dials-guide.md v3.0）
# 5376 維 token_refiner 實測內積運動洩漏係數：dot(v_dial, u_motion) / ||v_motion||
MOTION_LEAKAGE = {
    "h3_storm.safetensors": 0.375,          # cos=+0.460, ||storm||=53.05 vs ||motion||=65.03
    "h3_evil_unhinged.safetensors": 0.221,  # cos=+0.242, ||unhinged||=59.36
    "h3_space_warp.safetensors": 0.199,     # cos=+0.247, ||warp||=52.37
    "h3_aura.safetensors": 0.172,           # cos=+0.260, ||aura||=42.92
    "h3_evil_cold.safetensors": -0.125,     # cos=-0.195, ||cold||=41.59 (抑制運動)
}

DIAL_PRESETS = {
    "none": [],
    "P1": [
        {"dial": "dials/h3_motion.safetensors", "strength": 0.50, "on": True},
        {"dial": "dials/h3_dramatic_light.safetensors", "strength": 1.00, "on": True},
    ],
    "P2": [
        # v3.0 校準：考量 storm(+1.00) 自帶 +0.375 運動洩漏，motion 由 0.80 下修至 0.55，使總等效 M_eff = 0.925 不破構圖紅線
        {"dial": "dials/h3_motion.safetensors", "strength": 0.55, "on": True},
        {"dial": "dials/h3_storm.safetensors", "strength": 1.00, "on": True},
        {"dial": "dials/h3_dramatic_light.safetensors", "strength": 1.10, "on": True},
    ],
    "P3": [
        {"dial": "dials/h3_motion.safetensors", "strength": 0.45, "on": True},
        {"dial": "dials/h3_dramatic_light.safetensors", "strength": 1.60, "on": True},
        {"dial": "dials/h3_storm.safetensors", "strength": 1.00, "on": True},
    ],
    "P4": [
        {"dial": "dials/h3_motion.safetensors", "strength": -0.35, "on": True},
        {"dial": "dials/h3_dramatic_light.safetensors", "strength": 1.80, "on": True},
        {"dial": "dials/h3_evil_dread.safetensors", "strength": 0.80, "on": True},
    ],
    "P5": [
        {
            "dial": "dials/h3_arcane_sigils.safetensors",
            "strength": 1.40,
            "on": True,
            "time": {
                "type": "keys",
                "points": [[0.0, 0.0], [0.15, 0.0], [0.45, 1.0], [0.65, 1.0], [0.80, 0.0], [1.0, 0.0]],
                "unit": "normalized",
                "interp": "linear",
                "steps": 6,
                "audio": "protect",
            },
        },
        {"dial": "dials/h3_dramatic_light.safetensors", "strength": 1.20, "on": True},
        {"dial": "dials/h3_evil_dread.safetensors", "strength": 0.60, "on": True},
    ],
    "P6": [
        {
            "dial": "dials/h3_space_warp.safetensors",
            "strength": 1.50,
            "on": True,
            "time": {
                "type": "keys",
                "points": [[0.0, 0.0], [0.20, 0.0], [0.55, 1.0], [0.75, 0.0], [1.0, 0.0]],
                "unit": "normalized",
                "interp": "linear",
                "steps": 6,
                "audio": "protect",
            },
        },
        {"dial": "dials/h3_dramatic_light.safetensors", "strength": 1.40, "on": True},
        {"dial": "dials/h3_evil_dread.safetensors", "strength": 0.60, "on": True},
    ],
    # P7：相位雙軌近身實戰主力（常駐戲劇硬光＋適度風壓，運動完全由 --anchor / --burst / --hitstop 雙軌 0..1 曲線精準接管）
    "P7": [
        {"dial": "dials/h3_dramatic_light.safetensors", "strength": 1.35, "on": True},
        {"dial": "dials/h3_storm.safetensors", "strength": 0.85, "on": True},
        {"dial": "dials/h3_evil_dread.safetensors", "strength": 0.45, "on": True},
    ],
    # P8：定樁蓄勢→破空大招主力（專治跪地/站樁展開萬劍或集氣接超高速毀滅主砲，零法陣爬臉、零斜坡滑行）
    "P8": [
        {"dial": "dials/h3_dramatic_light.safetensors", "strength": 1.40, "on": True},
        {"dial": "dials/h3_storm.safetensors", "strength": 0.80, "on": True},
        {"dial": "dials/h3_evil_dread.safetensors", "strength": 0.55, "on": True},
    ],
    # P9：左眼 5.0 實證武戲五滑塊配方（水墨筆觸強化紅藍刀弧軌跡 + 冷暖高反差光影，禁用極端負向 blur_hook 防鬼畜閃切）
    "P9": [
        {"dial": "dials/h3_motion.safetensors", "strength": 0.50, "on": True},
        {"dial": "dials/h3_ink_wash.safetensors", "strength": 0.50, "on": True},
        {"dial": "dials/h3_storm.safetensors", "strength": 0.50, "on": True},
        {"dial": "dials/h3_dramatic_light.safetensors", "strength": 0.90, "on": True},
        {"dial": "dials/experimental/h3_x_silentfilm_cyberpunk.safetensors", "strength": 0.40, "on": True},
        {"dial": "dials/h3_impact_frame.safetensors", "strength": 0.35, "on": True},
    ],
}

STAGE_DIMS = {
    "draft": (1088, 640),
    "draft480": (854, 480),
    "final": (1344, 768),
    "derope": (1344, 768),
    "hd": (1504, 832),
    "fhd": (1664, 928),
}


def extract_h3_prompt(raw: str) -> str:
    """從純英文檔或雙語檔（中文母稿 + 英文 code block）自動擷取 H3 提示詞本體。"""
    cleaned = "\n".join(ln for ln in raw.splitlines() if not ln.lstrip().startswith("#!"))
    blocks = re.findall(r"```(?:text)?\s*\n(.*?)\n```", cleaned, re.S)
    for b in blocks:
        if re.search(r"^\s*(?:subject_definitions|integrated_multimodal_description)\s*:", b, re.M):
            return b.strip()
    m = re.search(r"^\s*(?:subject_definitions|integrated_multimodal_description)\s*:", cleaned, re.M)
    if m:
        return cleaned[m.start():].strip()
    return cleaned.strip()


def _clamp(t: float) -> float:
    return min(1.0, max(0.0, t))


def build_impact_curve(hits: list[tuple[float, float]], seconds: float,
                       min_pulse: float = 0.25, lead: float = 0.02, tail: float = 0.03) -> list[list[float]]:
    """將多個 (t0, t1) 命中秒數轉為正規化 [0..1] 的 0/1 曲線（實際強度由 row.strength 控制）。"""
    pulses = []
    for t0, t1 in sorted(hits):
        a = _clamp(t0 / seconds)
        b = _clamp(max(t1, t0 + min_pulse) / seconds)
        pulses.append([_clamp(a - lead), a, b, _clamp(b + tail)])
    merged = []
    for p in pulses:
        if merged and merged[-1][3] >= p[0]:
            merged[-1][2] = max(merged[-1][2], p[2])
            merged[-1][3] = max(merged[-1][3], p[3])
        else:
            merged.append(p)
    best: dict[float, float] = {}
    for lo, a, b, hi in merged:
        for t, v in ((lo, 0.0), (a, 1.0), (b, 1.0), (hi, 0.0)):
            tr = round(t, 3)
            best[tr] = max(best.get(tr, 0.0), v)
    pts: list[list[float]] = []
    for t, v in sorted(best.items()):
        if pts and t <= pts[-1][0]:
            t = round(pts[-1][0] + 0.001, 3)
        pts.append([min(1.0, t), v])
    if not pts or pts[0][0] > 0.0:
        pts.insert(0, [0.0, 0.0])
    if pts[-1][0] < 1.0:
        pts.append([1.0, 0.0])
    return pts


def resolve_pika_lora(preferred: str) -> str:
    """查詢運行中的 ComfyUI，確保 Pika LoRA 檔名與實際安裝一致。"""
    try:
        info = json.loads(OPENER.open(f"{COMFY}/object_info/LoraLoaderModelOnly", timeout=10).read())
        avail = info["LoraLoaderModelOnly"]["input"]["required"]["lora_name"][0]
        if preferred in avail:
            return preferred
        for name in avail:
            low = name.lower()
            if "pika_h3_flex_ref2va" in low:
                return name
        for name in avail:
            if "pika_h3_flex" in name.lower():
                return name
    except Exception:
        pass
    return preferred


def upload(path: str, mime: str = "image/png") -> str:
    p = pathlib.Path(path)
    name = f"{uuid.uuid4().hex[:8]}_{p.name}"
    b = uuid.uuid4().hex
    body = (
        f"--{b}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"{name}\"\r\n"
        f"Content-Type: {mime}\r\n\r\n"
    ).encode() + p.read_bytes() + f"\r\n--{b}--\r\n".encode()
    req = urllib.request.Request(
        COMFY + "/upload/image",
        data=body,
        method="POST",
        headers={"Content-Type": f"multipart/form-data; boundary={b}"},
    )
    return json.loads(OPENER.open(req, timeout=180).read())["name"]


def _attach_h3_model_tail(graph: dict, prefix: str, model_node: str,
                          shift_video: float, shift_audio: float, chunks: int) -> str:
    """為 H3 模型掛接 AttentionBackend -> BlockSparseAttention -> SigmaShift -> ChunkFeedForward。"""
    n_attn = f"{prefix}_attn"
    n_bsa = f"{prefix}_bsa"
    n_shift = f"{prefix}_shift"
    n_chunk = f"{prefix}_chunk"
    graph[n_attn] = {
        "class_type": "ModelAttentionBackend",
        "inputs": {"model": [model_node, 0], "attention": "comfy kitchen attention"},
    }
    graph[n_bsa] = {
        "class_type": "BlockSparseAttention",
        "inputs": {
            "model": [n_attn, 0],
            "selection": "sol-attn",
            "selection.tau": 1.3,
            "start_percent": 0.2,
            "end_percent": 1.0,
            "dense_blocks": "",
            "min_tokens": 12288,
            "extra_tokens": 256,
            "sink_conditioning": "exact_kv_and_rows",
            "verbose": False,
        },
    }
    graph[n_shift] = {
        "class_type": "MiniMaxH3SigmaShift",
        "inputs": {"model": [n_bsa, 0], "shift_video": shift_video, "shift_audio": shift_audio},
    }
    graph[n_chunk] = {
        "class_type": "MiniMaxChunkFeedForward",
        "inputs": {"model": [n_shift, 0], "chunks": chunks, "seq_threshold": 4096},
    }
    return n_chunk


def _scale_rack(rack: list[dict], factor: float) -> list[dict]:
    out = []
    for row in rack:
        r = copy.deepcopy(row)
        r["strength"] = round(float(r.get("strength", 0.0)) * factor, 3)
        out.append(r)
    return out


def build_weighted_span_curve(
    spans: list[tuple[float, float, float]],
    seconds: float,
    ramp: float = 0.02,
) -> tuple[float, list[list[float]]]:
    """將同號多段 (t0, t1, signed_strength) 編譯為單列 strength + 精確 [0..1] 時間曲線。

    依據 ComfyUI-MAINodes timecurve.py 實測：單列 M 必須落在 [0, 1] 才是精確雙分支混合，
    因此正值（Burst）與負值（Anchor/Hit-Stop）必須拆成獨立兩列，同號多段則以最大絕對值為
    row strength、各段高度正規化為 |s_i| / max_abs ∈ [0, 1]，共用單一分支零額外算力損耗。
    """
    if not spans:
        return 0.0, [[0.0, 0.0], [1.0, 0.0]]
    sign = -1.0 if spans[0][2] < 0 else 1.0
    max_abs = max(abs(s) for _, _, s in spans)
    if max_abs < 1e-6:
        return 0.0, [[0.0, 0.0], [1.0, 0.0]]

    # 在高密度時間網格 (0.005) 上取各區段梯形包絡的最大值，再簡化為嚴格遞增折線點
    n_grid = 200
    grid = [0.0] * (n_grid + 1)
    for t0, t1, s in spans:
        lvl = min(1.0, abs(s) / max_abs)
        a = _clamp(t0 / seconds)
        b = _clamp(max(t1, t0 + 0.18) / seconds)
        lo = _clamp(a - ramp)
        hi = _clamp(b + ramp)
        for idx in range(n_grid + 1):
            u = idx / n_grid
            val = 0.0
            if a <= u <= b:
                val = lvl
            elif lo < u < a and a > lo:
                val = lvl * (u - lo) / (a - lo)
            elif b < u < hi and hi > b:
                val = lvl * (hi - u) / (hi - b)
            if val > grid[idx]:
                grid[idx] = val

    pts: list[list[float]] = []
    for idx, val in enumerate(grid):
        u = round(idx / n_grid, 3)
        v = round(val, 3)
        if len(pts) >= 2 and abs(pts[-1][1] - v) < 1e-6 and abs(pts[-2][1] - v) < 1e-6:
            pts[-1][0] = u
        else:
            if pts and u <= pts[-1][0]:
                continue
            pts.append([u, v])
    if pts[0][0] > 0.0:
        pts.insert(0, [0.0, pts[0][1]])
    if pts[-1][0] < 1.0:
        pts.append([1.0, pts[-1][1]])
    return round(sign * max_abs, 3), pts


def summarize_motion_budget(rack: list[dict]) -> dict[str, float]:
    """依據 5376 維向量內積計算常駐運動洩漏、最深錨定值與最高爆發值。"""
    const_motion = 0.0
    leak_const = 0.0
    burst_peak = 0.0
    anchor_dip = 0.0
    for row in rack:
        if not row.get("on", True):
            continue
        dname = pathlib.Path(str(row.get("dial", ""))).name
        s = float(row.get("strength", 0.0))
        has_time = isinstance(row.get("time"), dict)
        if dname == "h3_motion.safetensors":
            if not has_time:
                const_motion += s
            elif s > 0:
                burst_peak += s
            elif s < 0:
                anchor_dip += s
        elif dname in MOTION_LEAKAGE and not has_time:
            leak_const += s * MOTION_LEAKAGE[dname]
    base_eff = const_motion + leak_const
    return {
        "const_motion": round(const_motion, 3),
        "leak_const": round(leak_const, 3),
        "base_eff": round(base_eff, 3),
        "anchor_eff": round(base_eff + anchor_dip, 3),
        "burst_eff": round(base_eff + burst_peak, 3),
    }


def build_anti_closeup_curve(closeups: list[tuple[float, float]], seconds: float,
                             margin: float = 0.02) -> list[list[float]]:
    """建立「打鬥段=1.0、臉部特寫段=0.0」的反相時間曲線，讓特寫保穩保顏值、打鬥全速爆發。"""
    dips = []
    for t0, t1 in sorted(closeups):
        a = _clamp(t0 / seconds)
        b = _clamp(max(t1, t0 + 0.25) / seconds)
        dips.append([_clamp(a - margin), a, b, _clamp(b + margin)])
    merged = []
    for d in dips:
        if merged and merged[-1][3] >= d[0]:
            merged[-1][2] = max(merged[-1][2], d[2])
            merged[-1][3] = max(merged[-1][3], d[3])
        else:
            merged.append(d)
    pts: list[list[float]] = [[0.0, 1.0]]
    for lo, a, b, hi in merged:
        for t, v in ((lo, 1.0), (a, 0.0), (b, 0.0), (hi, 1.0)):
            tr = round(t, 3)
            if tr <= pts[-1][0]:
                if abs(tr - pts[-1][0]) < 1e-6:
                    pts[-1][1] = min(pts[-1][1], v)
                    continue
                tr = round(pts[-1][0] + 0.001, 3)
            pts.append([min(1.0, tr), v])
    if pts[-1][0] < 1.0:
        pts.append([1.0, 1.0])
    return pts


def build_selflift_graph(
    prompt: str,
    seconds: float,
    seed: int,
    width: int,
    height: int,
    picture_files: list[str],
    rack: list[dict],
    job: str,
    *,
    unet_name: str,
    clip_name: str,
    dmad_lora: str,
    dmad_strength: float,
    extra_loras: list[str],
    lowres_loras: list[str] | None = None,
    scheduler: str = "simple",
    steps: int,
    transition_step: int,
    lowres_scale: float,
    cfg: float,
    shift_video: float,
    shift_audio: float,
    chunks: int,
    upscaler_model: str,
    hires_dials: str,
    corrector: str | None = None,
    corrector_strength: float = 1.0,
    corrector_budget: float = 0.5,
    corrector_stage: str = "both",
    corrector_precision: str = "fp32",
    motion_stg: dict | None = None,
) -> dict:
    """建構 PRISM / YZ金魚 SelfLiftH3Sampler 一採二採完整圖，並整合 MAIDialRack 雙模型口。

    corrector 非空時，於模型尾端（AttentionBackend/BSA/SigmaShift/ChunkFF 之後）掛 Sulphur-3
    ApplyH3Corrector（post-CFG 速度殘差修正）；corrector_stage 決定掛在一採、二採或兩者。
    """
    length = h3_frames(seconds)
    graph: dict = {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": unet_name, "weight_dtype": "default"}},
        "3": {"class_type": "CLIPLoader", "inputs": {"clip_name": clip_name, "type": "minimax", "device": "default"}},
        "4": {"class_type": "VAELoader", "inputs": {"vae_name": "minimax_h3_video_vae_int8_convrot.safetensors"}},
        "5": {"class_type": "VAELoader", "inputs": {"vae_name": "minimax_h3_audio_vae_fp32.safetensors"}},
    }

    # 主幹模型鏈：UNET -> 可選 DMAD LoRA -> 可選額外 LoRA
    cur = "1"
    if dmad_strength > 0.0 and dmad_lora:
        graph["2"] = {
            "class_type": "LoraLoaderModelOnly",
            "inputs": {"model": [cur, 0], "lora_name": dmad_lora, "strength_model": dmad_strength},
        }
        cur = "2"
    for i, spec in enumerate(extra_loras):
        lname, _, strength = spec.rpartition(":")
        nid = f"7{i}"
        graph[nid] = {
            "class_type": "LoraLoaderModelOnly",
            "inputs": {"model": [cur, 0], "lora_name": lname, "strength_model": float(strength)},
        }
        cur = nid
    clean_base = cur

    # 僅掛載於低解析一採的動作/武術骨架 LoRA（避免舊底模 LoRA 污染二採 1080p PRISM 銳利度）
    low_lora_base = clean_base
    for j, spec in enumerate(lowres_loras or []):
        lname, _, strength = spec.rpartition(":")
        nid = f"7L{j}"
        graph[nid] = {
            "class_type": "LoraLoaderModelOnly",
            "inputs": {"model": [low_lora_base, 0], "lora_name": lname, "strength_model": float(strength)},
        }
        low_lora_base = nid

    # 低解析一採模型（掛全量 MAIDialRack；一採僅執行前 transition_step 步）
    low_base = low_lora_base
    if rack:
        rack_adj = copy.deepcopy(rack)
        for row in rack_adj:
            if isinstance(row.get("time"), dict):
                row["time"]["steps"] = transition_step
        graph["dr"] = {
            "class_type": "MAIDialRack",
            "inputs": {"model": [low_lora_base, 0], "rack": json.dumps(rack_adj, ensure_ascii=False)},
        }
        low_base = "dr"
    model_low = _attach_h3_model_tail(graph, "low", low_base, shift_video, shift_audio, chunks)

    # 高解析二採模型（依 hires_dials 決定 keep / half / motion-only / phase-motion / off；永遠基於無 lowres_loras 的 clean_base）
    model_hires = None
    if rack and hires_dials == "off":
        model_hires = _attach_h3_model_tail(graph, "hi", clean_base, shift_video, shift_audio, chunks)
    elif rack and hires_dials == "half":
        rack_half = _scale_rack(rack_adj, 0.5)
        for row in rack_half:
            if isinstance(row.get("time"), dict):
                row["time"]["steps"] = 2
        graph["dr_hi"] = {
            "class_type": "MAIDialRack",
            "inputs": {"model": [clean_base, 0], "rack": json.dumps(rack_half, ensure_ascii=False)},
        }
        model_hires = _attach_h3_model_tail(graph, "hi", "dr_hi", shift_video, shift_audio, chunks)
    elif rack and hires_dials in ("motion-only", "phase-motion"):
        # SelfLift 將 sigmas[transition_step:] 切片傳入 model_hires；二採僅需前 2 步維持雙軌錨定/爆發，後 6 步單分支極速精修（立省 8 分鐘）
        rack_motion = [copy.deepcopy(r) for r in rack_adj if "h3_motion" in str(r.get("dial", ""))]
        for row in rack_motion:
            if isinstance(row.get("time"), dict):
                row["time"]["steps"] = 2
        if rack_motion:
            graph["dr_hi"] = {
                "class_type": "MAIDialRack",
                "inputs": {"model": [clean_base, 0], "rack": json.dumps(rack_motion, ensure_ascii=False)},
            }
            model_hires = _attach_h3_model_tail(graph, "hi", "dr_hi", shift_video, shift_audio, chunks)
        else:
            model_hires = _attach_h3_model_tail(graph, "hi", clean_base, shift_video, shift_audio, chunks)
    elif lowres_loras:
        if rack:
            rack_keep = copy.deepcopy(rack)
            for row in rack_keep:
                if isinstance(row.get("time"), dict):
                    row["time"]["steps"] = max(1, steps - transition_step)
            graph["dr_hi"] = {
                "class_type": "MAIDialRack",
                "inputs": {"model": [clean_base, 0], "rack": json.dumps(rack_keep, ensure_ascii=False)},
            }
            model_hires = _attach_h3_model_tail(graph, "hi", "dr_hi", shift_video, shift_audio, chunks)
        else:
            model_hires = _attach_h3_model_tail(graph, "hi", clean_base, shift_video, shift_audio, chunks)

    # Sulphur-3 H3 Corrector（選用）：SelfLift 每段各自呼叫 comfy.samplers.sample，
    # post-CFG 鉤子與分段 sample_sigmas 都會正確傳入，故只需在對應段的 MODEL 上掛 Apply。
    sampler_model_low = model_low
    if corrector and corrector_stage not in ("low", "hires", "both"):
        raise ValueError(f"corrector_stage 必須是 low/hires/both，收到 {corrector_stage!r}")
    needs_split = (corrector and corrector_stage != "both") or motion_stg is not None
    if model_hires is None and needs_split:
        # 原本二採沿用一採模型；為了只在單段掛修正器／引導，另建一條與一採完全相同的二採尾端
        model_hires = _attach_h3_model_tail(graph, "hi", low_base, shift_video, shift_audio, chunks)
    if corrector and corrector_precision == "bf16":
        # Advanced 節點：Linear/Conv3d 以 BF16 存放（約 4GB），LayerNorm 保持 FP32；其餘控制全用預設（不開 compile/sparse/實驗模式）
        graph["cr_load"] = {
            "class_type": "H3CorrectorAdvancedLoad",
            "inputs": {"corrector": corrector, "enable_bf16_compute_weights": True, "use_saved_precision": True},
        }
        ctl = dict(CORRECTOR_ADV_DEFAULTS, strength=corrector_strength, budget_fraction=corrector_budget)
        graph["cr_ctl"] = {"class_type": "H3CorrectorAdvancedControls", "inputs": {"corrector": ["cr_load", 0], **ctl}}

        def _apply_corrector(node_id: str, src: str) -> str:
            graph[node_id] = {
                "class_type": "H3CorrectorAdvancedApply",
                "inputs": {"model": [src, 0], "corrector": ["cr_load", 0], "controls": ["cr_ctl", 0]},
            }
            return node_id
    elif corrector:
        graph["cr_load"] = {"class_type": "LoadH3Corrector", "inputs": {"corrector": corrector}}

        def _apply_corrector(node_id: str, src: str) -> str:
            graph[node_id] = {
                "class_type": "ApplyH3Corrector",
                "inputs": {
                    "model": [src, 0], "corrector": ["cr_load", 0], "strength": corrector_strength,
                    "budget_fraction": corrector_budget, "velocity_floor": 0.001,
                    "start_step": 0, "end_step": -1,
                },
            }
            return node_id
    if corrector:

        if corrector_stage in ("low", "both"):
            sampler_model_low = _apply_corrector("cr_low", model_low)
        if corrector_stage in ("hires", "both") and model_hires is not None:
            model_hires = _apply_corrector("cr_hi", model_hires)

    # Sulphur-3 Motion/STG 引導（選用，僅掛一採骨架期）：靜止版提示放 negative 槽，cfg=1 時只有本 wrapper 會評估它
    if motion_stg is not None:
        graph["stg_low"] = {
            "class_type": "H3SelfLiftMotionSTG",
            "inputs": {
                "model": [sampler_model_low, 0],
                "motion_scale": motion_stg["motion"], "stg_scale": motion_stg["stg"],
                "stg_layers": motion_stg["layers"], "until": motion_stg["until"],
            },
        }
        sampler_model_low = "stg_low"

    # Ref2VA conditioning + 參考圖
    ref_inputs: dict = {
        "clip": ["3", 0],
        "vae": ["4", 0],
        "audio_vae": ["5", 0],
        "prompt": prompt,
        "width": width,
        "height": height,
        "length": length,
        "ref_image_size": "match",
    }
    for i, name in enumerate(picture_files):
        graph[str(30 + i)] = {"class_type": "LoadImage", "inputs": {"image": name}}
        ref_inputs[f"ref_images.ref_image_{i}"] = [str(30 + i), 0]
    graph["7"] = {"class_type": "MiniMaxH3ReferenceToVideo", "inputs": ref_inputs}
    graph["8"] = {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["7", 0]}}
    negative = ["8", 0]
    if motion_stg is not None and motion_stg.get("still_prompt"):
        still_inputs = dict(ref_inputs)
        still_inputs["prompt"] = motion_stg["still_prompt"]
        graph["7s"] = {"class_type": "MiniMaxH3ReferenceToVideo", "inputs": still_inputs}
        negative = ["7s", 0]

    # Euler + BasicScheduler + SelfLiftH3Sampler（武戲嚴禁 highres_tiling）
    graph["10"] = {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "euler"}}
    graph["11"] = {
        "class_type": "BasicScheduler",
        "inputs": {"model": [model_low, 0], "scheduler": scheduler, "steps": steps, "denoise": 1.0},
    }
    sampler_inputs: dict = {
        "model": [sampler_model_low, 0],
        "positive": ["7", 0],
        "negative": negative,
        "vae": ["4", 0],
        "latent_image": ["7", 1],
        "sampler": ["10", 0],
        "sigmas": ["11", 0],
        "seed": seed,
        "cfg": cfg,
        "transition_step": transition_step,
        "lowres_scale": lowres_scale,
        "rho": 0.0,
        "w_min": 0.5,
        "w_max": 1.0,
        "upscaler_model": upscaler_model,
        "highres_tiling": False,
        "upscaler_unload": True,
    }
    if model_hires is not None:
        sampler_inputs["model_hires"] = [model_hires, 0]
    graph["12"] = {"class_type": "SelfLiftH3Sampler", "inputs": sampler_inputs}

    graph["13"] = {"class_type": "VAEDecode", "inputs": {"samples": ["12", 0], "vae": ["4", 0]}}
    graph["14"] = {"class_type": "VAEDecodeAudio", "inputs": {"samples": ["12", 0], "vae": ["5", 0]}}
    graph["15"] = {
        "class_type": "VHS_VideoCombine",
        "inputs": {
            "images": ["13", 0],
            "audio": ["14", 0],
            "frame_rate": 24,
            "loop_count": 0,
            "filename_prefix": f"h3_combat/{job}",
            "format": "video/h264-mp4",
            "pix_fmt": "yuv420p",
            "crf": 18,
            "save_metadata": True,
            "trim_to_audio": False,
            "pingpong": False,
            "save_output": True,
        },
    }
    return graph


def attach_derope(graph: dict, seed: int, width: int, height: int, job: str,
                  inject: float = 0.48, d_max: int = 4, has_rack: bool = False) -> dict:
    """在既有 Pika Pass 1 graph 後串接 De-rope（含 MAIDialHoldMap 同步時間曲線與 Pass 1 音訊保留）。"""
    length = graph["7"]["inputs"]["length"]
    pre_attn_model = graph["60"]["inputs"]["model"][0]
    graph["15"]["inputs"]["filename_prefix"] = f"h3_combat/{job}_pass1"

    graph["201"] = {
        "class_type": "H3JerkOracle",
        "inputs": {"samples": ["12", 0], "length": length, "q": 0.75, "d_max": d_max, "ramp": True, "bridge": 8},
    }
    graph["202"] = {
        "class_type": "H3ClockRemap",
        "inputs": {"hold_map": ["201", 0], "model_profile": "minimax-h3"},
    }
    graph["203"] = {
        "class_type": "H3TimeSmear",
        "inputs": {"images": ["13", 0], "dilation": d_max, "hold_map": ["202", 0]},
    }
    graph["204"] = {
        "class_type": "H3AudioSmear",
        "inputs": {"audio": ["14", 0], "hold_map": ["203", 1], "fps": 24},
    }
    graph["205"] = {"class_type": "VAEEncode", "inputs": {"pixels": ["203", 0], "vae": ["4", 0]}}
    graph["206"] = {"class_type": "VAEEncodeAudio", "inputs": {"audio": ["204", 0], "vae": ["5", 0]}}
    graph["207"] = {
        "class_type": "H3V2VInit",
        "inputs": {
            "samples": ["205", 0],
            "audio_latent": ["206", 0],
            "audio_mode": "follow the original performance (0.5)",
            "audio_strength": 0.5,
        },
    }

    s2_base = pre_attn_model
    if has_rack:
        graph["208"] = {
            "class_type": "MAIDialHoldMap",
            "inputs": {"model": [pre_attn_model, 0], "hold_map": ["203", 1]},
        }
        s2_base = "208"

    graph["209"] = {
        "class_type": "ModelAttentionBackend",
        "inputs": {"model": [s2_base, 0], "attention": "comfy kitchen attention"},
    }
    graph["210"] = {
        "class_type": "BlockSparseAttention",
        "inputs": {
            "model": ["209", 0],
            "selection": "sol-attn",
            "selection.tau": 1.3,
            "start_percent": 0.2,
            "end_percent": 1.0,
            "dense_blocks": "",
            "min_tokens": 12288,
            "extra_tokens": 256,
            "sink_conditioning": "exact_kv_and_rows",
            "verbose": False,
        },
    }

    cond2_inputs = copy.deepcopy(graph["7"]["inputs"])
    cond2_inputs["width"] = width
    cond2_inputs["height"] = height
    cond2_inputs["length"] = ["203", 2]
    graph["211"] = {"class_type": "MiniMaxH3ReferenceToVideo", "inputs": cond2_inputs}

    graph["212"] = {"class_type": "RandomNoise", "inputs": {"noise_seed": seed + 1}}
    graph["213"] = {"class_type": "BasicGuider", "inputs": {"model": ["210", 0], "conditioning": ["211", 0]}}
    graph["214"] = {
        "class_type": "H3DeropeSigmas",
        "inputs": {"model": ["210", 0], "sigmas": ["11", 0], "inject": inject, "steps": 0},
    }
    graph["215"] = {
        "class_type": "SamplerCustomAdvanced",
        "inputs": {
            "noise": ["212", 0],
            "guider": ["213", 0],
            "sampler": ["10", 0],
            "sigmas": ["214", 0],
            "latent_image": ["207", 0],
        },
    }
    graph["216"] = {"class_type": "VAEDecode", "inputs": {"samples": ["215", 0], "vae": ["4", 0]}}
    graph["217"] = {"class_type": "VAEDecodeAudio", "inputs": {"samples": ["215", 0], "vae": ["5", 0]}}
    graph["218"] = {"class_type": "H3ExactRecover", "inputs": {"images": ["216", 0], "hold_map": ["203", 1]}}
    graph["219"] = {
        "class_type": "H3AudioRecover",
        "inputs": {
            "audio": ["217", 0],
            "hold_map": ["203", 1],
            "fps": 24,
            "reference": ["14", 0],
            "reference_mix": 1.0,
            "audio_source": "keep the original performance (safe default)",
        },
    }
    graph["220"] = {
        "class_type": "VHS_VideoCombine",
        "inputs": {
            "images": ["218", 0],
            "audio": ["219", 0],
            "frame_rate": 24,
            "loop_count": 0,
            "filename_prefix": f"h3_combat/{job}_derope",
            "format": "video/h264-mp4",
            "pix_fmt": "yuv420p",
            "crf": 18,
            "save_metadata": True,
            "trim_to_audio": False,
            "pingpong": False,
            "save_output": True,
        },
    }
    return graph


def queue_and_download(graph: dict, out_path: pathlib.Path, preferred_node: str | None = None) -> None:
    req = urllib.request.Request(
        COMFY + "/prompt",
        data=json.dumps({"prompt": graph}).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        pid = json.loads(OPENER.open(req, timeout=60).read())["prompt_id"]
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        sys.exit(f"ComfyUI rejected workflow ({e.code}): {err_body[:1500]}")
    print("queued", pid, flush=True)
    t0 = time.time()
    while True:
        h = json.loads(OPENER.open(f"{COMFY}/history/{pid}", timeout=60).read()).get(pid)
        if h and h.get("status", {}).get("completed") is not None:
            break
        time.sleep(10)
    elapsed = time.time() - t0
    if h["status"].get("status_str") != "success":
        sys.exit(f"render failed ({elapsed:.0f}s): {json.dumps(h['status'])[:1000]}")

    outputs = h.get("outputs", {})
    file_entry = None
    if preferred_node and preferred_node in outputs:
        node_out = outputs[preferred_node]
        for key in ("gifs", "videos", "images"):
            if node_out.get(key):
                file_entry = node_out[key][0]
                break
    if not file_entry:
        for node_out in outputs.values():
            for key in ("gifs", "videos"):
                if node_out.get(key):
                    file_entry = node_out[key][0]
                    break
            if file_entry:
                break
    if not file_entry:
        sys.exit(f"no video output found in history: {json.dumps(outputs)[:600]}")

    q = urllib.parse.urlencode(
        {"filename": file_entry["filename"], "subfolder": file_entry.get("subfolder", ""), "type": file_entry.get("type", "output")}
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(OPENER.open(f"{COMFY}/view?{q}", timeout=300).read())
    print(f"saved {out_path} ({elapsed:.1f}s)", flush=True)


def run_upscale(args) -> None:
    if not args.input_video:
        sys.exit("--stage upscale 需要提供 --input-video <mp4>")
    src = pathlib.Path(args.input_video)
    if not src.exists():
        sys.exit(f"找不到輸入影片：{src}")
    comfy_in_name = f"h3_recavsr_{args.job}.mp4"
    if not args.dry:
        env_input = os.environ.get("COMFYUI_INPUT_DIR")
        shared_input = pathlib.Path(env_input) if env_input else None
        if shared_input and shared_input.exists():
            shutil.copy2(src, shared_input / comfy_in_name)
        else:
            comfy_in_name = upload(str(src), mime="video/mp4")
    graph = build_recavsr_graph(comfy_in_name, args.job)
    if args.dry:
        est = 10 + 6.6 * args.seconds
        print(f"dry ok (upscale): {len(graph)} nodes, input={comfy_in_name}, est={est:.0f}s")
        return
    queue_and_download(graph, pathlib.Path(args.out), preferred_node="4")


def main():
    ap = argparse.ArgumentParser(description="本機 ComfyUI H3（SelfLiftH3Sampler / Pika + Dials + De-rope + ReCaVSR）出片工具")
    ap.add_argument("--engine", default="pika", choices=["pika", "selflift"],
                    help="pika=6步LCM快採；selflift=PRISM+YZ金魚 SelfLiftH3Sampler 潛空間一採二採降動態模糊")
    ap.add_argument("--prompt", help="提示詞檔（支援純英文或雙語檔，自動抽英文 H3 區塊）")
    ap.add_argument("--ref", action="append", default=[], help="參考圖路徑（最多 9 張）")
    ap.add_argument("--seconds", type=float, default=8.0)
    ap.add_argument("--seed", type=int, default=1001)
    ap.add_argument("--width", type=int, default=None, help="覆寫寬度（預設依 stage 決定）")
    ap.add_argument("--height", type=int, default=None, help="覆寫高度（預設依 stage 決定）")
    ap.add_argument("--stage", default="final", choices=["draft", "draft480", "final", "derope", "hd", "fhd", "upscale"],
                    help="draft=640p, draft480=480p, final=768p, derope=768p+De-rope(pika), hd=1504x832, fhd=1664x928, upscale=ReCaVSR 2x")
    ap.add_argument("--preset", default="none", choices=list(DIAL_PRESETS), help="武戲 Dial Rack 預設配方 (P1..P6)")
    ap.add_argument("--rack", default=None, help="自訂 MAIDialRack JSON 字串或 .json 檔案路徑（會附加在 preset 後）")
    ap.add_argument("--hit", action="append", default=[], help="衝擊定幀命中秒數區間 t0:t1（可重複，例 --hit 5.2:5.6）")
    ap.add_argument("--hitstop", action="append", default=[], help="重擊頓幀區間 t0:t1[:brake]（同時打入負向 h3_motion 制動與衝擊幀，預設 brake=-1.8）")
    ap.add_argument("--anchor", action="append", default=[], help="定樁錨定區間 t0:t1[:strength]（負向 h3_motion 防地面滑行與鎖特寫，預設 -0.65）")
    ap.add_argument("--burst", action="append", default=[], help="爆發推進區間 t0:t1[:strength]（正向 h3_motion 釋放高速突進與破空，預設 +0.65）")
    ap.add_argument("--closeup", action="append", default=[], help="臉部特寫秒數區間 t0:t1（自動於該區間將常駐 h3_motion 降為 0 保穩保顏值）")
    ap.add_argument("--motion", type=float, default=None, help="覆寫常駐 h3_motion 強度")
    ap.add_argument("--impact-strength", type=float, default=None, help="覆寫衝擊定幀強度（預設 Ref2VA=4.8, T2VA=4.5）")
    # SelfLift 專用參數
    ap.add_argument("--unet", default=DEFAULT_SELFLIFT_UNET, help="[selflift] UNet 底模檔名")
    ap.add_argument("--clip", default=DEFAULT_CLIP, help="[selflift] Qwen3-VL H3 文本編碼器")
    ap.add_argument("--dmad", type=float, default=0.8, help="[selflift] DMAD LoRA 強度（PRISM_DMAD_PDMD 請設 0）")
    ap.add_argument("--dmad-lora", default=DEFAULT_DMAD_LORA, help="[selflift] DMAD LoRA 檔名")
    ap.add_argument("--scheduler", default="simple", choices=["simple", "beta", "sgm_uniform", "normal"], help="[selflift] BasicScheduler")
    ap.add_argument("--steps", type=int, default=12, help="[selflift] 總採樣步數（推薦 12，高動態虛影試 14）")
    ap.add_argument("--transition", type=int, default=6, help="[selflift] 低解析轉高解析步數（預設 6）")
    ap.add_argument("--lowres-scale", type=float, default=0.6, help="[selflift] 一採低解析倍率（預設 0.6）")
    ap.add_argument("--cfg", type=float, default=1.0, help="[selflift] CFG（DMAD 預設 1.0）")
    ap.add_argument("--shift-video", type=float, default=12.0, help="[selflift] MiniMaxH3SigmaShift shift_video")
    ap.add_argument("--shift-audio", type=float, default=3.0, help="[selflift] MiniMaxH3SigmaShift shift_audio")
    ap.add_argument("--chunks", type=int, default=4, help="[selflift] MiniMaxChunkFeedForward chunks（16GB 顯卡推薦 4）")
    ap.add_argument("--upscaler", default=DEFAULT_H3_UPSCALER, help="[selflift] 潛空間超分模型")
    ap.add_argument("--hires-dials", default="keep", choices=["keep", "half", "motion-only", "phase-motion", "off"],
                    help="[selflift] 二採 model_hires 策略：phase-motion/motion-only=僅保留正負雙軌h3_motion兼顧釘樁防滑、爆發力與鎖臉, off=全關")
    # Pika / De-rope 專用參數
    ap.add_argument("--derope-inject", type=float, default=0.48, help="De-rope inject 強度（預設 0.48）")
    ap.add_argument("--derope-dmax", type=int, default=4, help="De-rope 最大 hold 倍率（預設 4）")
    ap.add_argument("--input-video", default=None, help="--stage upscale 專用輸入 mp4 路徑")
    ap.add_argument("--lora", action="append", default=[], help="額外 LoRA（一採與二採共用），名稱:強度")
    ap.add_argument("--lowres-lora", action="append", default=[], help="[selflift] 僅掛載於低解析一採的動作骨架 LoRA，二採保持純淨 PRISM 高銳度，名稱:強度")
    # Sulphur-3 H3 Corrector（選用；預設關閉，不影響既有行為）
    ap.add_argument("--corrector", default=None,
                    help="[selflift] models/h3_correctors 內的修正器檔名（例 s3_corrector.safetensors）；不給=關閉")
    ap.add_argument("--corrector-strength", type=float, default=1.0, help="[selflift] 修正器殘差倍率（1=訓練原值）")
    ap.add_argument("--corrector-budget", type=float, default=0.5,
                    help="[selflift] 殘差 RMS 上限＝budget×速度 RMS（S3 訓練值 0.5）")
    ap.add_argument("--corrector-stage", default="both", choices=["low", "hires", "both"],
                    help="[selflift] 修正器掛載段：low=一採骨架期、hires=二採精修期、both=兩段")
    ap.add_argument("--corrector-precision", default="fp32", choices=["fp32", "bf16"],
                    help="[selflift] fp32=官方基本節點（8GB，數值為訓練原狀）；bf16=Advanced 節點 BF16 計算權重（約 4GB，"
                         "16GB 卡二採用；官方註明 BF16 會改變輸出）")
    # Sulphur-3 Motion/STG 引導（選用；需部署 comfy_nodes/ComfyUI-H3-SelfLift-MotionSTG）
    ap.add_argument("--motion-stg", action="store_true", help="[selflift] 一採骨架期啟用 Motion/STG 引導")
    ap.add_argument("--stg-motion", type=float, default=1.0, help="[selflift] 推離靜止版提示強度（>0 需 --still-prompt）")
    ap.add_argument("--stg-scale", type=float, default=1.0, help="[selflift] 跳區塊結構引導強度")
    ap.add_argument("--stg-layers", default="20,21,22", help="[selflift] STG 跳過的 H3 區塊索引")
    ap.add_argument("--stg-until", type=float, default=0.5,
                    help="[selflift] 一採前多少比例區間啟用（14步/t=6 時 0.5≈前3步≈全程前21%%）")
    ap.add_argument("--still-prompt", default=None, help="[selflift] 靜止版提示詞檔（同角色同場景、所有動作凍結）")
    ap.add_argument("--job", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--dry", action="store_true", help="只建圖與印出設定，不送出 ComfyUI")
    args = ap.parse_args()

    if args.stage == "upscale":
        run_upscale(args)
        return

    if not args.prompt:
        sys.exit(f"--stage {args.stage} 需要提供 --prompt")

    raw_text = pathlib.Path(args.prompt).read_text(encoding="utf-8")
    text = extract_h3_prompt(raw_text)
    names = [upload(r) for r in args.ref] if not args.dry else [pathlib.Path(r).name for r in args.ref]

    # 組裝 MAIDialRack
    rack: list[dict] = copy.deepcopy(DIAL_PRESETS[args.preset])
    if args.motion is not None:
        found_m = False
        for row in rack:
            if "h3_motion" in str(row.get("dial", "")):
                row["strength"] = args.motion
                found_m = True
        if not found_m:
            rack.insert(0, {"dial": "dials/h3_motion.safetensors", "strength": args.motion, "on": True})
    if args.closeup:
        parsed_cu = []
        for c in args.closeup:
            t0_s, _, t1_s = c.partition(":")
            t0 = float(t0_s)
            t1 = float(t1_s) if t1_s else t0 + 1.2
            parsed_cu.append((t0, t1))
        anti_pts = build_anti_closeup_curve(parsed_cu, args.seconds)
        for row in rack:
            if "h3_motion" in str(row.get("dial", "")):
                row["time"] = {
                    "type": "keys",
                    "points": anti_pts,
                    "unit": "normalized",
                    "interp": "linear",
                    "steps": args.steps if args.engine == "selflift" else 6,
                    "audio": "protect",
                }
    def _parse_span_spec(spec_str: str, default_str: float, default_len: float) -> tuple[float, float, float]:
        parts = spec_str.split(":")
        t0 = float(parts[0])
        t1 = float(parts[1]) if len(parts) >= 2 and parts[1] != "" else t0 + default_len
        s = float(parts[2]) if len(parts) >= 3 and parts[2] != "" else default_str
        return t0, t1, s

    neg_spans: list[tuple[float, float, float]] = []
    pos_spans: list[tuple[float, float, float]] = []
    extra_hits: list[tuple[float, float]] = []

    for a_spec in args.anchor:
        t0, t1, s = _parse_span_spec(a_spec, -0.65, 1.5)
        neg_spans.append((t0, t1, -abs(s)))
    for b_spec in args.burst:
        t0, t1, s = _parse_span_spec(b_spec, 0.65, 2.0)
        pos_spans.append((t0, t1, abs(s)))
    for hs_spec in args.hitstop:
        t0, t1, s = _parse_span_spec(hs_spec, -1.80, 0.25)
        neg_spans.append((t0, t1, -abs(s)))
        extra_hits.append((t0, t1))

    curve_steps = args.transition if args.engine == "selflift" else 6
    if neg_spans:
        neg_str, neg_pts = build_weighted_span_curve(neg_spans, args.seconds, ramp=0.018)
        if abs(neg_str) > 1e-6:
            rack.append({
                "dial": "dials/h3_motion.safetensors",
                "strength": neg_str,
                "on": True,
                "time": {
                    "type": "keys",
                    "points": neg_pts,
                    "unit": "normalized",
                    "interp": "linear",
                    "steps": curve_steps,
                    "audio": "protect",
                },
            })
    if pos_spans:
        pos_str, pos_pts = build_weighted_span_curve(pos_spans, args.seconds, ramp=0.020)
        if abs(pos_str) > 1e-6:
            rack.append({
                "dial": "dials/h3_motion.safetensors",
                "strength": pos_str,
                "on": True,
                "time": {
                    "type": "keys",
                    "points": pos_pts,
                    "unit": "normalized",
                    "interp": "linear",
                    "steps": curve_steps,
                    "audio": "protect",
                },
            })

    all_hits: list[tuple[float, float]] = list(extra_hits)
    for h in args.hit:
        t0_s, _, t1_s = h.partition(":")
        t0 = float(t0_s)
        t1 = float(t1_s) if t1_s else t0 + 0.28
        all_hits.append((t0, t1))
    if all_hits:
        imp_str = args.impact_strength if args.impact_strength is not None else (4.8 if names else 4.5)
        rack.append({
            "dial": "dials/h3_impact_frame.safetensors",
            "strength": imp_str,
            "on": True,
            "time": {
                "type": "keys",
                "points": build_impact_curve(all_hits, args.seconds),
                "unit": "normalized",
                "interp": "linear",
                "steps": curve_steps,
                "audio": "protect",
            },
        })
    if args.rack:
        rp = pathlib.Path(args.rack)
        extra = json.loads(rp.read_text(encoding="utf-8-sig")) if rp.exists() else json.loads(args.rack)
        if not isinstance(extra, list):
            sys.exit("--rack 必須是 JSON array")
        rack.extend(extra)

    budget = summarize_motion_budget(rack)
    print(
        f"[dial-physics] const_motion={budget['const_motion']:+.2f}, storm/fx_leak={budget['leak_const']:+.2f} "
        f"=> base_eff={budget['base_eff']:+.2f}, anchor_eff={budget['anchor_eff']:+.2f}, burst_eff={budget['burst_eff']:+.2f}",
        flush=True,
    )
    if budget["base_eff"] > 1.05:
        print(
            f"[WARN] 常駐等效運動 base_eff={budget['base_eff']:+.2f} > +1.05！高風險觸發場景重排與角色貼地滑行，建議改用 P7/P8 搭配 --anchor/--burst。",
            flush=True,
        )

    w, h = STAGE_DIMS[args.stage]
    if args.width:
        w = args.width
    if args.height:
        h = args.height

    if args.engine == "selflift" and args.corrector and (w % 32 or h % 32):
        # 修正器以 2x2 patch 切 H3 潛空間（像素 /16），潛空間寬高須為偶數，即像素寬高須為 32 的倍數
        sys.exit(f"--corrector 需要寬高皆為 32 的倍數（目前 {w}x{h}）；請改用 final/hd/fhd 或以 --width/--height 對齊")

    motion_stg = None
    if args.engine == "selflift" and args.motion_stg:
        still_text = None
        if args.stg_motion > 0:
            if not args.still_prompt:
                sys.exit("--motion-stg 且 --stg-motion>0 時必須提供 --still-prompt（或設 --stg-motion 0 只用 STG）")
            still_text = extract_h3_prompt(pathlib.Path(args.still_prompt).read_text(encoding="utf-8"))
        motion_stg = {"motion": args.stg_motion, "stg": args.stg_scale, "layers": args.stg_layers,
                      "until": args.stg_until, "still_prompt": still_text}

    if args.engine == "selflift":
        graph = build_selflift_graph(
            text, args.seconds, args.seed, w, h, names, rack, args.job,
            unet_name=args.unet, clip_name=args.clip, dmad_lora=args.dmad_lora,
            dmad_strength=args.dmad, extra_loras=args.lora, lowres_loras=args.lowres_lora,
            scheduler=args.scheduler, steps=args.steps, transition_step=args.transition,
            lowres_scale=args.lowres_scale, cfg=args.cfg, shift_video=args.shift_video,
            shift_audio=args.shift_audio, chunks=args.chunks, upscaler_model=args.upscaler,
            hires_dials=args.hires_dials, corrector=args.corrector,
            corrector_strength=args.corrector_strength, corrector_budget=args.corrector_budget,
            corrector_stage=args.corrector_stage, corrector_precision=args.corrector_precision,
            motion_stg=motion_stg,
        )
        if args.dry:
            cr_info = (f", corrector={args.corrector}(s={args.corrector_strength},b={args.corrector_budget},"
                       f"stage={args.corrector_stage},{args.corrector_precision})" if args.corrector else "")
            if motion_stg:
                cr_info += (f", motion_stg(motion={args.stg_motion},stg={args.stg_scale},layers={args.stg_layers},"
                            f"until={args.stg_until},still={'yes' if motion_stg['still_prompt'] else 'no'})")
            print(
                f"dry ok [selflift]: {len(graph)} nodes, {w}x{h}, {graph['7']['inputs']['length']} frames, "
                f"unet={args.unet}, dmad={args.dmad}, sched={args.scheduler}/{args.steps}(t={args.transition},s={args.lowres_scale}), "
                f"chunks={args.chunks}, hires_dials={args.hires_dials}, dials={len(rack)}{cr_info}"
            )
            if rack:
                print("rack:", json.dumps(rack, ensure_ascii=False))
            return
        queue_and_download(graph, pathlib.Path(args.out), preferred_node="15")
        return

    # 傳統 Pika 6 步 LCM 路徑
    graph = build_pika_graph(text, args.seconds, args.seed, w, h, names, rack, args.job)
    graph["2"]["inputs"]["lora_name"] = resolve_pika_lora(graph["2"]["inputs"]["lora_name"])

    prev = graph["60"]["inputs"]["model"][0]
    for i, spec in enumerate(args.lora):
        lname, _, strength = spec.rpartition(":")
        nid = f"7{i}"
        graph[nid] = {
            "class_type": "LoraLoaderModelOnly",
            "inputs": {"model": [prev, 0], "lora_name": lname, "strength_model": float(strength)},
        }
        prev = nid
    graph["60"]["inputs"]["model"] = [prev, 0]

    preferred_node = "15"
    if args.stage == "derope":
        attach_derope(graph, args.seed, w, h, args.job, inject=args.derope_inject, d_max=args.derope_dmax, has_rack=bool(rack))
        preferred_node = "220"

    if args.dry:
        print(
            f"dry ok [pika]: stage={args.stage}, {len(graph)} nodes, {w}x{h}, "
            f"{graph['7']['inputs']['length']} frames, lora={graph['2']['inputs']['lora_name']}, "
            f"refs={names}, dials={len(rack)}"
        )
        if rack:
            print("rack:", json.dumps(rack, ensure_ascii=False))
        return

    queue_and_download(graph, pathlib.Path(args.out), preferred_node=preferred_node)


if __name__ == "__main__":
    main()
