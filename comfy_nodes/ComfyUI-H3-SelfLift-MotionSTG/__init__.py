"""H3 Motion/STG 引導的 SelfLift 相容轉接節點（MODEL 進、MODEL 出）。

Sulphur-3 開發者的 H3MotionGuider（見 ComfyUI-H3-Corrector-Advanced/guidance.py）輸出 GUIDER，只能接
SamplerCustomAdvanced；SelfLiftH3Sampler 內部每段各自呼叫 comfy.samplers.sample 並自建 CFGGuider，
沒有 guider 輸入口。本節點把同一套數學改掛成 PREDICT_NOISE wrapper，讓它能在 SelfLift 內部生效：

    STG    ：guided = v + stg_scale * (v - v_skip)        v_skip = 指定 H3 區塊被跳過的同提示預測
    Motion ：guided = guided + motion_scale * (guided - v_still)   v_still = 「靜止版」提示的預測

「靜止版」條件取自取樣器的 negative 槽（SelfLift 在 cfg=1 時不會評估 negative，故可安全借用）。
音訊切片保留正提示預測；最後以 CFG 1 呼叫 cfg_function，post-CFG 鉤子（H3 Corrector）照常執行。
until 以「該段取樣的 sample_sigmas」計算（SelfLift 一採/二採各自從 0 起算）。
"""
from __future__ import annotations

import math
import re

import torch

import comfy.model_patcher
import comfy.patcher_extension
import comfy.samplers
from comfy.patcher_extension import copy_nested_dicts

WRAPPER_KEY = "h3_selflift_motion_stg"


def _skip_block(args, extra_args):
    """STG 弱分支：直接回傳區塊輸入，等同跳過該 H3 雙流區塊。"""
    return args


def parse_layers(value: str) -> list[int]:
    value = (value or "").strip()
    if not value:
        return []
    if re.fullmatch(r"[0-9]+(?:\s*,\s*[0-9]+|\s+[0-9]+)*", value) is None:
        raise ValueError("stg_layers 格式錯誤：請用逗號或空白分隔的非負整數，例如 '20,21,22'")
    return list(dict.fromkeys(int(p) for p in re.split(r"[,\s]+", value)))


def active_interval(sample_sigmas, timestep, until: float) -> bool:
    """與開發者 guidance.py 相同：僅前 round(steps*until) 個雜訊區間啟用引導。"""
    if sample_sigmas is None or sample_sigmas.numel() < 2 or timestep.numel() == 0 or until <= 0:
        return False
    steps = sample_sigmas.numel() - 1
    active_steps = round(steps * until)
    if active_steps <= 0:
        return False
    sigmas = sample_sigmas.to(device="cpu").double().flatten()
    value = float(timestep.flatten()[0])
    index = min(max(int((sigmas[:-1] >= value - 1e-6).sum()) - 1, 0), steps - 1)
    return index < active_steps


def make_wrapper(motion_scale: float, stg_scale: float, stg_layers: list[int], until: float):
    def wrapper(executor, x, timestep, model_options={}, seed=None):
        guider = executor.class_obj
        positive = guider.conds.get("positive")
        still = guider.conds.get("negative")
        use_motion = motion_scale > 0 and still is not None
        use_stg = stg_scale > 0 and bool(stg_layers)
        sigmas = model_options.get("transformer_options", {}).get("sample_sigmas")
        if not (use_motion or use_stg) or not active_interval(sigmas, timestep, until):
            return executor(x, timestep, model_options, seed)
        model = guider.inner_model
        if use_motion:
            cond_pred, still_pred = comfy.samplers.calc_cond_batch(model, [positive, still], x, timestep, model_options)
        else:
            (cond_pred,) = comfy.samplers.calc_cond_batch(model, [positive], x, timestep, model_options)
        guided = cond_pred
        if use_stg:
            skip_options = copy_nested_dicts(model_options)
            for layer in stg_layers:
                skip_options = comfy.model_patcher.set_model_options_patch_replace(
                    skip_options, _skip_block, "dit", "double_block", layer)
            (weak_pred,) = comfy.samplers.calc_cond_batch(model, [positive], x, timestep, skip_options)
            guided = guided + stg_scale * (cond_pred - weak_pred)
        if use_motion:
            guided = guided + motion_scale * (guided - still_pred)
        shapes = getattr(model, "latent_shapes", None)
        if shapes and len(shapes) >= 2:
            # 打包潛空間為「影片在前、音訊在後」；音訊保留正提示預測
            video = math.prod(shapes[0][1:])
            guided = torch.cat((guided[..., :video], cond_pred[..., video:]), dim=-1)
        return comfy.samplers.cfg_function(model, guided, guided, 1.0, x, timestep, model_options=model_options,
                                           cond=positive, uncond=None)
    return wrapper


class H3SelfLiftMotionSTG:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "model": ("MODEL",),
            "motion_scale": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 6.0, "step": 0.1,
                                       "tooltip": "推離 negative 槽「靜止版提示」的強度；0=只用 STG。開發者 RL 工作流用 1。"}),
            "stg_scale": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.1,
                                    "tooltip": "跳區塊結構引導強度；有效係數會再乘 (1+motion_scale)。"}),
            "stg_layers": ("STRING", {"default": "20,21,22"}),
            "until": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.05,
                                "tooltip": "本段取樣前多少比例的區間啟用引導（以該段 sample_sigmas 計）。"}),
        }}

    RETURN_TYPES = ("MODEL",)
    FUNCTION = "patch"
    CATEGORY = "MiniMax H3/guidance"
    DESCRIPTION = "把 Sulphur-3 Motion/STG 引導改為 PREDICT_NOISE wrapper，可用於 SelfLiftH3Sampler（negative 槽放靜止版提示，cfg=1）。"

    def patch(self, model, motion_scale, stg_scale, stg_layers, until):
        layers = parse_layers(stg_layers)
        patched = model.clone()
        patched.add_wrapper_with_key(comfy.patcher_extension.WrappersMP.PREDICT_NOISE, WRAPPER_KEY,
                                     make_wrapper(motion_scale, stg_scale, layers, until))
        return (patched,)


NODE_CLASS_MAPPINGS = {"H3SelfLiftMotionSTG": H3SelfLiftMotionSTG}
NODE_DISPLAY_NAME_MAPPINGS = {"H3SelfLiftMotionSTG": "H3 Motion/STG for SelfLift (MODEL patch)"}
