#!/usr/bin/env python3
"""Deterministic AI Manju Episode Workflow Compiler (v2.0).

Reads `character_vault.json` and an episode manifest (`ep01_beizhao_chushi_manifest.json`),
validates all canonical character IDs and asset files, and compiles speed-optimized
ComfyUI API workflow JSONs for each pending shot:
- Zero duplicate reference image tokens (`first_frame` injected ONLY via `MiniMaxH3AddGuide` frame_idx=0)
- 6-step Turbo schedule (`minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors` + `MiniMaxH3SigmasTail`)
- Zero photorealistic skin-pore LoRAs
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SHORT_DRAMA_DIR = BASE_DIR / "pipelines" / "short_drama"
VAULT_PATH = SHORT_DRAMA_DIR / "character_vault.json"
ASSETS_DIR = SHORT_DRAMA_DIR / "assets_manju_v2"
WORKFLOWS_DIR = SHORT_DRAMA_DIR / "workflows"


def build_prompt_text(vault: dict, shot: dict) -> str:
    chars = vault["characters"]
    c1 = chars[shot["subject_1"]]
    c2 = chars[shot["subject_2"]]
    style = vault["visual_style"]

    d1 = shot["dialogue_1"]
    d2 = shot["dialogue_2"]

    return (
        "subject_definitions:\n"
        f"<Subject 1> is {c1['visual_desc']}, depicted in <Picture 1>.\n"
        f"<Subject 2> is {c2['visual_desc']}, depicted in <Picture 2>.\n"
        f"<Audio 1> is the voice-timbre reference for <Subject 1> (S1, {c1['canonical_name']}), providing only their {c1['vocal_desc']}.\n"
        f"<Audio 2> is the voice-timbre reference for <Subject 2> (S2, {c2['canonical_name']}), providing only their {c2['vocal_desc']}.\n\n"
        "summary:\n"
        f"[reference generation + audio reference] {shot['scene_summary']}\n\n"
        "retention_analysis:\n"
        f"<Subject 1> (appears in [Shot 1]): fully_preserved - exact 3D Donghua CG facial modeling, hairstyle, and costume from <Picture 1> and Frame 0 are strictly preserved.\n"
        f"<Subject 2> (appears in [Shot 1]): fully_preserved - exact 3D Donghua CG facial modeling, hairstyle, and costume from <Picture 2> and Frame 0 are strictly preserved.\n"
        "<Audio 1>: reference - guides <Subject 1> (S1)'s Mandarin dialogue performance.\n"
        "<Audio 2>: reference - guides <Subject 2> (S2)'s Mandarin dialogue performance.\n\n"
        "detailed_description:\n"
        f"{style}.\n"
        f"[Shot 1] The camera holds a {shot['camera_motion']}. "
        f"During 00:00.000–{d1['window'].split('–')[0]}, both characters hold the opening composition naturally with closed lips. "
        f"During {d1['window']}, <Subject 1> (S1) {d1['action']} referenced from <Audio 1> with clear natural lip-sync: "
        f"<d>[Mandarin]{d1['line']}</d> While <Subject 1> speaks, <Subject 2> keeps their mouth closed. "
        f"During {d2['window']}, <Subject 1> closes their lips naturally while <Subject 2> (S2) {d2['action']} referenced from <Audio 2> with clear natural lip-sync: "
        f"<d>[Mandarin]{d2['line']}</d> "
        f"Immediately during {d2['window'].split('–')[1]}–00:10.125, both characters close their lips naturally and hold the expressive closing beat. "
        "No subtitles, no text overlays, no watermarks.\n\n"
        "overall_soundscape:\n"
        f"{shot['soundscape']}\n\n"
        "non_diegetic_music:\n"
        "N/A"
    )


def compile_shot_workflow(vault: dict, manifest: dict, shot: dict, seed: int) -> dict:
    chars = vault["characters"]
    c1 = chars[shot["subject_1"]]
    c2 = chars[shot["subject_2"]]

    for fname in (c1["sheet_image"], c2["sheet_image"], shot["first_frame"], c1["voice_seed"], c2["voice_seed"]):
        fpath = ASSETS_DIR / fname
        if not fpath.exists():
            raise FileNotFoundError(f"Missing required asset in {ASSETS_DIR}: {fname}")

    prompt_text = build_prompt_text(vault, shot)
    width, height = manifest.get("resolution", [1344, 768])
    length = shot.get("frames", manifest.get("default_frames", 243))
    steps = shot.get("steps", manifest.get("default_steps", 6))

    return {
        "1": {
            "class_type": "UNETLoader",
            "inputs": {
                "unet_name": "Minimax-h3_Singularity_ref2va_Pruned_v1.3_int8.safetensors",
                "weight_dtype": "default",
            },
        },
        "4": {
            "class_type": "LoraLoaderModelOnly",
            "inputs": {
                "model": ["1", 0],
                "lora_name": "minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors",
                "strength_model": 1.0,
            },
        },
        "5": {
            "class_type": "MiniMaxH3SigmaShift",
            "inputs": {"model": ["4", 0], "shift_video": 12.0, "shift_audio": 3.0},
        },
        "6": {
            "class_type": "CLIPLoader",
            "inputs": {
                "clip_name": "qwen3vl_32b_heretic_minimax_h3_nvfp4.safetensors",
                "type": "minimax",
                "device": "default",
            },
        },
        "7": {"class_type": "VAELoader", "inputs": {"vae_name": "minimax_h3_video_vae_fp16.safetensors"}},
        "8": {"class_type": "VAELoader", "inputs": {"vae_name": "minimax_h3_audio_vae_fp32.safetensors"}},
        "10": {"class_type": "LoadImage", "inputs": {"image": c1["sheet_image"]}},
        "11": {"class_type": "LoadImage", "inputs": {"image": c2["sheet_image"]}},
        "12": {"class_type": "LoadImage", "inputs": {"image": shot["first_frame"]}},
        "13": {"class_type": "LoadAudio", "inputs": {"audio": c1["voice_seed"]}},
        "14": {"class_type": "LoadAudio", "inputs": {"audio": c2["voice_seed"]}},
        "20": {
            "class_type": "MiniMaxH3ReferenceToVideo",
            "inputs": {
                "clip": ["6", 0],
                "vae": ["7", 0],
                "audio_vae": ["8", 0],
                "width": width,
                "height": height,
                "length": length,
                "ref_image_size": "match",
                "ref_images.ref_image_0": ["10", 0],
                "ref_images.ref_image_1": ["11", 0],
                "ref_audios.ref_audio_0": ["13", 0],
                "ref_audios.ref_audio_1": ["14", 0],
                "prompt": prompt_text,
            },
        },
        "201": {
            "class_type": "MiniMaxH3AddGuide",
            "inputs": {
                "positive": ["20", 0],
                "vae": ["7", 0],
                "latent": ["20", 1],
                "image": ["12", 0],
                "frame_idx": 0,
            },
        },
        "21": {
            "class_type": "BunnyH3ConditioningBridge",
            "inputs": {
                "conditioning": ["201", 0],
                "adapter": "BUNNY_H3_ActionLogic_Bridge_V2.safetensors",
                "alpha": 0.1,
                "magnitude_match": "per_token",
                "enabled": True,
            },
        },
        "22": {
            "class_type": "BasicScheduler",
            "inputs": {"model": ["5", 0], "scheduler": "simple", "steps": steps, "denoise": 1.0},
        },
        "23": {
            "class_type": "MiniMaxH3SigmasTail",
            "inputs": {"sigmas": ["22", 0], "tail_steps": 2, "strength": 0.5},
        },
        "24": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "res_multistep"}},
        "25": {"class_type": "RandomNoise", "inputs": {"noise_seed": seed}},
        "26": {"class_type": "BasicGuider", "inputs": {"model": ["5", 0], "conditioning": ["21", 0]}},
        "27": {
            "class_type": "SamplerCustomAdvanced",
            "inputs": {
                "noise": ["25", 0],
                "guider": ["26", 0],
                "sampler": ["24", 0],
                "sigmas": ["23", 0],
                "latent_image": ["20", 1],
            },
        },
        "30": {"class_type": "LTXVSeparateAVLatent", "inputs": {"av_latent": ["27", 0]}},
        "31": {"class_type": "VAEDecode", "inputs": {"samples": ["30", 0], "vae": ["7", 0]}},
        "32": {"class_type": "VAEDecodeAudio", "inputs": {"samples": ["30", 1], "vae": ["8", 0]}},
        "34": {"class_type": "CreateVideo", "inputs": {"images": ["31", 0], "audio": ["32", 0], "fps": 24.0}},
        "35": {
            "class_type": "SaveVideo",
            "inputs": {
                "video": ["34", 0],
                "filename_prefix": shot["output_prefix"],
                "format": "mp4",
                "codec": "h264",
            },
        },
    }


def main() -> None:
    manifest_path = Path(sys.argv[1]) if len(sys.argv) > 1 else SHORT_DRAMA_DIR / "ep01_beizhao_chushi_manifest.json"
    vault = json.loads(VAULT_PATH.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    WORKFLOWS_DIR.mkdir(parents=True, exist_ok=True)
    compiled = []
    for idx, shot in enumerate(manifest["shots"], start=1):
        if shot.get("status") == "completed":
            print(f"⏭️  Skipping completed {shot['shot_id']} ({shot.get('output_mp4')})")
            continue
        wf = compile_shot_workflow(vault, manifest, shot, seed=2026110900 + idx)
        out_wf = WORKFLOWS_DIR / f"compiled_{manifest['episode_id']}_{shot['shot_id'].lower()}.json"
        out_wf.write_text(json.dumps(wf, ensure_ascii=False, indent=2), encoding="utf-8")
        compiled.append(out_wf)
        print(f"✅ Compiled {shot['shot_id']} -> {out_wf.name} (steps={shot.get('steps', manifest['default_steps'])}, deduplicated ref_images=2)")

    print(f"🎯 Total compiled pending shots: {len(compiled)}")


if __name__ == "__main__":
    main()
