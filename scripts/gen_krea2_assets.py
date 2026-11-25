#!/usr/bin/env python3
"""使用本機 ComfyUI Krea 2（manju_pure: rayArtshoot V5 + krmj_epoch_4）生成 AI 漫劇風格武戲素材。

嚴格遵守：
- 角色：單主體純中性灰底棚拍全身立繪（絕不生四視圖／拼板，杜絕 H3 Ref2VA 拼板洩漏），
        採 8 步 er_sde/simple (848x1280) -> LatentUpscaleBy 1.5x -> 5 步 euler/simple (denoise=0.45) 實出 1272x1920。
- 場景：2.5D 國漫仙俠空鏡，0 人、中央寬闊雪石留白、零偽字（不提 plaque/banner/calligraphy），
        採 1280x720 雙采 1.5x -> Lanczos 2752x1536 -> SeedVR2-7b-int8 1 步重建 + ImageSmartSharpen+。
"""

import json
import os
import pathlib
import sys
import time
import urllib.parse
import urllib.request

COMFY = os.environ.get("COMFYUI_URL", "http://127.0.0.1:8188")
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))
OUT_DIR = pathlib.Path(__file__).resolve().parent.parent / "assets" / "v3-manju" / "caseA"

ASSETS = [
    {
        "name": "hero_feixue.png",
        "kind": "character",
        "seed": 2026112401,
        "lora_strength": 0.75,
        "prompt": (
            "krmj, High-end Chinese-Korean 2.5D semi-realistic AI manju guoman xianxia character illustration, "
            "studio full-body standing portrait centered on a clean solid seamless neutral mid-grey studio backdrop, "
            "even soft studio beauty lighting, full head-to-toe visibility with clear margin around boots and head. "
            "A strikingly beautiful slender young East Asian swordswoman in her early twenties, delicate refined oval face, "
            "sharp upswept dark eyes with a small crimson lotus mark between her brows, composed cool expression with softly closed lips, "
            "long silky jet-black hair tied in a high flowing ponytail secured by a gold hairpin and twin trailing crimson silk ribbons. "
            "Wearing a tailored crimson and ink-black layered xianxia combat robe with intricate gold-thread cloud trim, "
            "fitted dark leather vambraces, high-waisted sash, flowing layered skirt hem, and sleek black combat boots. "
            "Holding a slender ornate Chinese jian sword with a subtle warm crimson blade edge angled cleanly downward in her right hand, "
            "natural poised upright combat-ready stance facing three-quarter forward. "
            "Crisp painterly 2.5D manju rendering, luminous silky hair strands, refined cel-meets-painterly shading, clean fabric folds, "
            "single solo character only, completely plain grey backdrop."
        ),
    },
    {
        "name": "villain_shuangjue.png",
        "kind": "character",
        "seed": 2026112402,
        "lora_strength": 0.72,
        "prompt": (
            "krmj, High-end Chinese-Korean 2.5D semi-realistic AI manju guoman xianxia character illustration, "
            "studio full-body standing portrait centered on a clean solid seamless neutral mid-grey studio backdrop, "
            "even soft studio key lighting, full head-to-toe visibility with clear margin around boots and head. "
            "A tall broad-shouldered strikingly handsome young East Asian swordsman in his mid-twenties, clean masculine jawline, "
            "chiseled noble features with sharp ice-blue eyes and straight dark brows, calm cold aristocratic expression with closed lips, "
            "long flowing silver-white hair half-bound atop his head with a sleek dark steel-and-silver hairpin crown. "
            "Wearing a layered ivory-white and silver xianxia warrior robe with engraved silver-steel pauldrons, fitted dark metallic bracers, "
            "a long billowing ivory shoulder cape, wide silver-buckled belt, and tall armored dark boots. "
            "Holding a long heavy broad Chinese jian sword with a faint translucent ice-blue edge resting cleanly downward in his right hand, "
            "tall upright poised stance facing three-quarter forward. "
            "Crisp painterly 2.5D manju rendering, refined clean masculine shading with zero heavy makeup, silky silver hair strands, "
            "sharp metallic armor highlights, single solo character only, completely plain grey backdrop."
        ),
    },
    {
        "name": "scene_snow_peak.png",
        "kind": "scene",
        "seed": 2026112403,
        "lora_strength": 0.70,
        "prompt": (
            "krmj, Wide establishing Chinese 2.5D semi-realistic AI manju guoman xianxia background plate of an ancient snow-covered "
            "mountain peak sword-duel granite terrace high above a vast sea of silver clouds under cold pale blue-grey winter sky and crisp rim backlight. "
            "A broad unobstructed expanse of weathered cracked dark-grey granite flagstones dusted with fresh wind-blown snow extends cleanly across the entire center foreground for staging. "
            "Flanked on the left by a weathered stone lantern pedestal and on the far right and rear edges by broken carved granite columns with pure geometric fretwork and unadorned torn solid dark-crimson silk cloth strips fluttering in the wind. "
            "Distant jagged snow-capped peaks rising through swirling mist beyond the cliff edge. "
            "Completely empty uninhabited location with zero people, zero figures, zero animals, open wide clear stone floor in center. "
            "All stone surfaces and cloth strips are plain unadorned solid materials with geometric carvings only, crisp atmospheric perspective, luminous 2.5D manju background rendering."
        ),
    },
]


def build_character_graph(prompt: str, seed: int, lora_strength: float, prefix: str) -> dict:
    return {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": r"Krea2\rayArtshoot_krea2NSFWV5Int8c.safetensors", "weight_dtype": "default"}},
        "30": {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["1", 0], "lora_name": r"KREA2\krmj_epoch_4.safetensors", "strength_model": lora_strength}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen3vl_4b_uncensored_int8_convrot.safetensors", "type": "krea2", "device": "default"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": "qwen_image_vae.safetensors"}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": prompt}},
        "5": {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["4", 0]}},
        "6": {"class_type": "EmptySD3LatentImage", "inputs": {"width": 848, "height": 1280, "batch_size": 1}},
        "7": {"class_type": "KSampler", "inputs": {"model": ["30", 0], "positive": ["4", 0], "negative": ["5", 0], "latent_image": ["6", 0], "seed": seed, "steps": 8, "cfg": 1.0, "sampler_name": "er_sde", "scheduler": "simple", "denoise": 1.0}},
        "10": {"class_type": "LatentUpscaleBy", "inputs": {"samples": ["7", 0], "upscale_method": "bicubic", "scale_by": 1.5}},
        "11": {"class_type": "KSampler", "inputs": {"model": ["30", 0], "positive": ["4", 0], "negative": ["5", 0], "latent_image": ["10", 0], "seed": seed + 17, "steps": 5, "cfg": 1.0, "sampler_name": "euler", "scheduler": "simple", "denoise": 0.45}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["11", 0], "vae": ["3", 0]}},
        "19": {"class_type": "SaveImage", "inputs": {"filename_prefix": f"h3_manju/{prefix}", "images": ["8", 0]}},
    }


def build_scene_graph(prompt: str, seed: int, lora_strength: float, prefix: str) -> dict:
    return {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": r"Krea2\rayArtshoot_krea2NSFWV5Int8c.safetensors", "weight_dtype": "default"}},
        "30": {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["1", 0], "lora_name": r"KREA2\krmj_epoch_4.safetensors", "strength_model": lora_strength}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen3vl_4b_uncensored_int8_convrot.safetensors", "type": "krea2", "device": "default"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": "qwen_image_vae.safetensors"}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": prompt}},
        "5": {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["4", 0]}},
        "6": {"class_type": "EmptySD3LatentImage", "inputs": {"width": 1280, "height": 720, "batch_size": 1}},
        "7": {"class_type": "KSampler", "inputs": {"model": ["30", 0], "positive": ["4", 0], "negative": ["5", 0], "latent_image": ["6", 0], "seed": seed, "steps": 8, "cfg": 1.0, "sampler_name": "er_sde", "scheduler": "simple", "denoise": 1.0}},
        "10": {"class_type": "LatentUpscaleBy", "inputs": {"samples": ["7", 0], "upscale_method": "bicubic", "scale_by": 1.5}},
        "11": {"class_type": "KSampler", "inputs": {"model": ["30", 0], "positive": ["4", 0], "negative": ["5", 0], "latent_image": ["10", 0], "seed": seed + 17, "steps": 5, "cfg": 1.0, "sampler_name": "euler", "scheduler": "simple", "denoise": 0.45}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["11", 0], "vae": ["3", 0]}},
        "20": {"class_type": "ImageScale", "inputs": {"image": ["8", 0], "upscale_method": "lanczos", "width": 2752, "height": 1536, "crop": "disabled"}},
        "21": {"class_type": "SeedVR2Preprocess", "inputs": {"resized_images": ["20", 0]}},
        "22": {"class_type": "VAELoader", "inputs": {"vae_name": "seedvr2_ema_vae_fp16.safetensors"}},
        "23": {"class_type": "VAEEncodeTiled", "inputs": {"pixels": ["21", 0], "vae": ["22", 0], "tile_size": 512, "overlap": 128, "temporal_size": 4096, "temporal_overlap": 8}},
        "24": {"class_type": "UNETLoader", "inputs": {"unet_name": "seedvr2_7b_int8_convrot.safetensors", "weight_dtype": "default"}},
        "25": {"class_type": "SeedVR2Conditioning", "inputs": {"model": ["24", 0], "vae_conditioning": ["23", 0]}},
        "26": {"class_type": "KSampler", "inputs": {"model": ["24", 0], "positive": ["25", 0], "negative": ["25", 1], "latent_image": ["23", 0], "seed": seed, "steps": 1, "cfg": 1.0, "sampler_name": "euler", "scheduler": "simple", "denoise": 1.0}},
        "27": {"class_type": "VAEDecodeTiled", "inputs": {"samples": ["26", 0], "vae": ["22", 0], "tile_size": 512, "overlap": 128, "temporal_size": 4096, "temporal_overlap": 8}},
        "28": {"class_type": "SeedVR2PostProcessing", "inputs": {"images": ["27", 0], "original_resized_images": ["20", 0], "color_correction_method": "adain"}},
        "29": {"class_type": "ImageSmartSharpen+", "inputs": {"image": ["28", 0], "noise_radius": 7, "preserve_edges": 0.75, "sharpen": 5.0, "ratio": 0.5}},
        "19": {"class_type": "SaveImage", "inputs": {"filename_prefix": f"h3_manju/{prefix}", "images": ["29", 0]}},
    }


def run_graph(graph: dict, out_path: pathlib.Path) -> None:
    req = urllib.request.Request(
        COMFY + "/prompt",
        data=json.dumps({"prompt": graph}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        pid = json.loads(OPENER.open(req, timeout=60).read())["prompt_id"]
    except urllib.error.HTTPError as e:
        sys.exit(f"ComfyUI rejected ({e.code}): {e.read().decode('utf-8', errors='replace')[:1200]}")
    t0 = time.time()
    while True:
        h = json.loads(OPENER.open(f"{COMFY}/history/{pid}", timeout=60).read()).get(pid)
        if h and h.get("status", {}).get("completed") is not None:
            break
        time.sleep(2)
    elapsed = time.time() - t0
    if h["status"].get("status_str") != "success":
        sys.exit(f"failed ({elapsed:.1f}s): {json.dumps(h['status'])[:1000]}")
    img = h["outputs"]["19"]["images"][0]
    q = urllib.parse.urlencode({"filename": img["filename"], "subfolder": img.get("subfolder", ""), "type": img.get("type", "output")})
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(OPENER.open(f"{COMFY}/view?{q}", timeout=120).read())
    print(f"[OK] {out_path.name} ({elapsed:.1f}s) -> {out_path}", flush=True)


def main():
    only = set(sys.argv[1:])
    for item in ASSETS:
        if only and item["name"] not in only:
            continue
        prefix = pathlib.Path(item["name"]).stem
        if item["kind"] == "character":
            g = build_character_graph(item["prompt"], item["seed"], item["lora_strength"], prefix)
        else:
            g = build_scene_graph(item["prompt"], item["seed"], item["lora_strength"], prefix)
        run_graph(g, OUT_DIR / item["name"])


if __name__ == "__main__":
    main()
