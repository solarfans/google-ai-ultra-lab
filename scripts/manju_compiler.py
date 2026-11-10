#!/usr/bin/env python3
"""Deterministic AI Manju Episode Workflow Compiler (v3.2 — Fingerprint-Verified Resume + Hybrid Model Routing).

Core Engineering Rules in v3.2:
1. Strict Lip-Sync vs. Closed-Mouth OS Separation:
   - In `MiniMax-H3`, `<d>[Mandarin]...</d>` is a hard lip-movement trigger.
   - `<d>[Mandarin]...</d>` MUST ONLY be emitted for `onscreen_spoken` segments (or the spoken tail of `os_then_spoken`).
   - For `offscreen_pa` and `inner_monologue_os` segments, `<d>` tags are strictly OMITTED so the character keeps their lips 100% closed on screen while the studio-grade neural PA/OS stem is mastered in post-production.
2. Fingerprint-Verified Checkpoint Resume:
   - `status == "completed"` alone is NEVER trusted to skip compilation.
   - A shot is skipped ONLY if: (a) `status == "completed"`, (b) `output_mp4` exists on disk and size > 100 KB, and (c) `shot.get("input_fingerprint")` matches the live SHA-256 of `(shot_mode, subject_1, subject_2, dialogue_1, dialogue_2, first_frame_sha256)`.
3. Hybrid Backend Adapter Metadata (`model_backend`):
   - Supports `"h3_comfyui"` (default for character dialogue/acting), `"flow_veo_3_1_lite"` (0-credit Ultra 20x lower-priority B-roll/transitions), and `"flow_omni_1_2"` (high-impact environment/establishing shots).
"""

from __future__ import annotations

import hashlib
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
    shot_mode = shot.get("shot_mode", "natural_dialogue")

    d1 = shot["dialogue_1"]
    d2 = shot["dialogue_2"]

    if shot_mode == "offscreen_pa_and_os":
        # Shot 01: Both d1 (cabin PA) and d2 (adult inner monologue) are OFF-SCREEN / OS.
        # Emit ZERO <d> tags so the modern protagonist keeps his mouth clenched shut!
        return (
            "subject_definitions:\n"
            f"<Subject 1> is {c1['visual_desc']}, depicted in <Picture 1>.\n\n"
            "summary:\n"
            f"[reference generation] {shot['scene_summary']}\n\n"
            "retention_analysis:\n"
            f"<Subject 1> (appears in [Shot 1]): fully_preserved - exact 3D Donghua CG facial modeling, hairstyle, and costume from <Picture 1> and Frame 0 are strictly preserved.\n\n"
            "detailed_description:\n"
            f"{style}.\n"
            f"[Shot 1] The camera holds an {shot['camera_motion']}. "
            f"Only <Subject 1> appears on screen strapped into his window seat inside the violently shaking airliner cabin; no flight attendant is present. "
            f"<Subject 1> keeps his lips tightly closed and jaw clenched throughout the entire 10-second shot, never speaking out loud. "
            f"During {d1['window']}, as red emergency lights flash and yellow oxygen masks swing overhead, <Subject 1> {d1['action']} with his mouth firmly closed. "
            f"During {d2['window']}, lightning illuminates the storm clouds outside the window as <Subject 1> {d2['action']} with his lips closed in tragic resolve. "
            "No subtitles, no text overlays, no watermarks.\n\n"
            "overall_soundscape:\n"
            f"{shot['soundscape']}\n\n"
            "non_diegetic_music:\n"
            "Tense cinematic disaster strings and low sub-bass rumble."
        )

    if shot_mode == "single_inner_monologue_os":
        # Shot 02: 6-year-old Chu Zheng on screen thinking in his 28yo adult soul voice (OS).
        # Emit ZERO <d> tags so 6yo Chu Zheng keeps his mouth 100% closed!
        return (
            "subject_definitions:\n"
            f"<Subject 1> is {c1['visual_desc']}, depicted in <Picture 1>.\n\n"
            "summary:\n"
            f"[reference generation] {shot['scene_summary']}\n\n"
            "retention_analysis:\n"
            f"<Subject 1> (appears in [Shot 1]): fully_preserved - exact 3D Donghua CG child facial modeling, white forehead bandage, hairstyle, and costume from <Picture 1> and Frame 0 are strictly preserved.\n\n"
            "detailed_description:\n"
            f"{style}.\n"
            f"[Shot 1] The camera holds a {shot['camera_motion']}. "
            f"<Subject 1> keeps his mouth and lips completely closed in mute silence throughout the entire 10-second shot, never moving his lips to speak, acting purely through mature, shocked eyes and hand movements. "
            f"During {d1['window']}, <Subject 1> {d1['action']} with his mouth strictly closed. "
            f"During {d2['window']}, <Subject 1> {d2['action']} with his lips still tightly closed in silent psychological resistance. "
            "No subtitles, no text overlays, no watermarks.\n\n"
            "overall_soundscape:\n"
            f"{shot['soundscape']}\n\n"
            "non_diegetic_music:\n"
            "Subtle melancholic guqin and quiet ancient room ambience."
        )

    if shot_mode == "os_plus_short_spoken":
        # Shot 03: Mother Wang Xiuhe speaks in d1; in d2, Chu Zheng first weeps silently (OS) during 05.0s–07.1s,
        # then opens his mouth ONLY during 07.1s–09.0s to call "娘，小五儿在这儿。"
        spoken_tail = d2["line"].split("……", 1)[1] if "……" in d2["line"] else d2["line"]
        return (
            "subject_definitions:\n"
            f"<Subject 1> is {c1['visual_desc']}, depicted in <Picture 1>.\n"
            f"<Subject 2> is {c2['visual_desc']}, depicted in <Picture 2>.\n"
            f"<Audio 1> is the voice-timbre reference for <Subject 1> (S1, {c1['canonical_name']}), providing only their {c1['vocal_desc']}.\n"
            f"<Audio 2> is the voice-timbre reference for <Subject 2> (S2, {c2['canonical_name']}), providing only their {c2['vocal_desc']}.\n\n"
            "summary:\n"
            f"[reference generation + audio reference] {shot['scene_summary']}\n\n"
            "retention_analysis:\n"
            f"<Subject 1> (appears in [Shot 1]): fully_preserved - exact 3D Donghua CG facial modeling, bleeding forehead bruise from kowtowing, hairstyle, and costume from <Picture 1> and Frame 0 are strictly preserved.\n"
            f"<Subject 2> (appears in [Shot 1]): fully_preserved - exact 3D Donghua CG child facial modeling, white forehead bandage, and costume from <Picture 2> and Frame 0 are strictly preserved.\n"
            "<Audio 1>: reference - guides <Subject 1> (S1)'s emotional weeping Mandarin delivery.\n"
            "<Audio 2>: reference - guides <Subject 2> (S2)'s brief final spoken call.\n\n"
            "detailed_description:\n"
            f"{style}.\n"
            f"[Shot 1] The camera holds an {shot['camera_motion']}. "
            f"During {d1['window']}, <Subject 1> (S1) {d1['action']} referenced from <Audio 1> with natural emotional lip-sync: "
            f"<d>[Mandarin]{d1['line']}</d> While <Subject 1> speaks, <Subject 2> keeps his mouth closed as warm tears roll down his cheeks. "
            f"During 00:04.600–00:07.100, both characters keep their lips closed as <Subject 1>'s forehead blood touches <Subject 2>'s cheek and <Subject 2> weeps silently in deep inner emotion. "
            f"During 00:07.100–00:09.200, <Subject 2> (S2) gently touches his mother's face and opens his mouth to softly call out referenced from <Audio 2>: "
            f"<d>[Mandarin]{spoken_tail}</d> "
            "Immediately during 00:09.200–00:10.125, both hold the tearful embrace with closed lips. "
            "No subtitles, no text overlays, no watermarks.\n\n"
            "overall_soundscape:\n"
            f"{shot['soundscape']}\n\n"
            "non_diegetic_music:\n"
            "Warm, deeply moving xiao flute and gentle strings."
        )

    # `natural_dialogue`: check if d2 is `inner_monologue_os` (as in Shot 05 & Shot 06!)
    d2_is_os = d2.get("voice_mode") == "inner_monologue_os"
    if d2_is_os:
        # Subject 1 (Wu Anran) speaks out loud on screen in d1; Subject 2 (6yo Chu Zheng) keeps mouth CLOSED in d2 (inner monologue OS)!
        c_boy = chars["chu_zheng_6yo"]
        return (
            "subject_definitions:\n"
            f"<Subject 1> is {c1['visual_desc']}, depicted in <Picture 1>.\n"
            f"<Subject 2> is {c_boy['visual_desc']}, depicted in <Picture 2>.\n"
            f"<Audio 1> is the voice-timbre reference for <Subject 1> (S1, {c1['canonical_name']}), providing only their {c1['vocal_desc']}.\n\n"
            "summary:\n"
            f"[reference generation + audio reference] {shot['scene_summary']}\n\n"
            "retention_analysis:\n"
            f"<Subject 1> (appears in [Shot 1]): fully_preserved - exact 3D Donghua CG facial modeling, hairstyle, and costume from <Picture 1> and Frame 0 are strictly preserved.\n"
            f"<Subject 2> (appears in [Shot 1]): fully_preserved - exact 3D Donghua CG child facial modeling, white forehead bandage, and costume from <Picture 2> and Frame 0 are strictly preserved.\n"
            "<Audio 1>: reference - guides <Subject 1> (S1)'s spoken Mandarin performance.\n\n"
            "detailed_description:\n"
            f"{style}.\n"
            f"[Shot 1] The camera holds a {shot['camera_motion']}. "
            f"During {d1['window']}, <Subject 1> (S1) {d1['action']} referenced from <Audio 1> with expressive natural lip-sync: "
            f"<d>[Mandarin]{d1['line']}</d> While <Subject 1> speaks, <Subject 2> keeps his mouth strictly closed. "
            f"During {d2['window']}, <Subject 1> closes his lips and holds his dramatic posture while <Subject 2> {d2['action']} with his lips completely closed (reacting purely with his eyes and facial expression in silent inner thought). "
            "No subtitles, no text overlays, no watermarks.\n\n"
            "overall_soundscape:\n"
            f"{shot['soundscape']}\n\n"
            "non_diegetic_music:\n"
            "N/A"
        )

    # Both d1 and d2 are on-screen spoken dialogue (e.g. Shot 04 in Huiwei Tofu Shop)
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
        "<Audio 1>: reference - guides <Subject 1> (S1)'s natural spoken Mandarin performance.\n"
        "<Audio 2>: reference - guides <Subject 2> (S2)'s natural spoken Mandarin performance.\n\n"
        "detailed_description:\n"
        f"{style}.\n"
        f"[Shot 1] The camera holds a {shot['camera_motion']}. "
        f"During 00:00.000–{d1['window'].split('–')[0]}, the characters perform dynamic physical staging rather than standing still. "
        f"During {d1['window']}, <Subject 1> (S1) {d1['action']} referenced from <Audio 1> with expressive natural lip-sync: "
        f"<d>[Mandarin]{d1['line']}</d> While <Subject 1> speaks, <Subject 2> reacts visibly with closed lips. "
        f"During {d2['window']}, <Subject 1> closes their lips while <Subject 2> (S2) {d2['action']} referenced from <Audio 2> with natural lip-sync: "
        f"<d>[Mandarin]{d2['line']}</d> "
        f"Immediately during {d2['window'].split('–')[1]}–00:10.125, both characters close their lips and hold the dramatic reaction beat. "
        "No subtitles, no text overlays, no watermarks.\n\n"
        "overall_soundscape:\n"
        f"{shot['soundscape']}\n\n"
        "non_diegetic_music:\n"
        "N/A"
    )


def compile_shot_workflow(vault: dict, manifest: dict, shot: dict, seed: int) -> dict:
    chars = vault["characters"]
    c1 = chars[shot["subject_1"]]
    # If d2 is inner_monologue_os in a two-shot with Wu Anran, the visual ref_image_1 should be chu_zheng_6yo!
    visual_s2_key = "chu_zheng_6yo" if (shot["subject_1"] == "wu_anran" and shot["subject_2"] == "modern_protagonist") else shot["subject_2"]
    c2_vis = chars[visual_s2_key]
    c2_aud = chars[shot["subject_2"]]

    for fname in (c1["sheet_image"], c2_vis["sheet_image"], shot["first_frame"], c1["voice_seed"], c2_aud["voice_seed"]):
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
        "11": {"class_type": "LoadImage", "inputs": {"image": c2_vis["sheet_image"]}},
        "12": {"class_type": "LoadImage", "inputs": {"image": shot["first_frame"]}},
        "13": {"class_type": "LoadAudio", "inputs": {"audio": c1["voice_seed"]}},
        "14": {"class_type": "LoadAudio", "inputs": {"audio": c2_aud["voice_seed"]}},
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


def compute_shot_fingerprint(shot: dict) -> str:
    """Compute deterministic SHA-256 fingerprint of shot inputs and first-frame asset."""
    ff_path = ASSETS_DIR / shot["first_frame"]
    ff_hash = hashlib.sha256(ff_path.read_bytes()).hexdigest()[:16] if ff_path.exists() else "missing"
    payload = {
        "shot_mode": shot.get("shot_mode", "natural_dialogue"),
        "model_backend": shot.get("model_backend", "h3_comfyui"),
        "subject_1": shot["subject_1"],
        "subject_2": shot["subject_2"],
        "first_frame": shot["first_frame"],
        "first_frame_sha16": ff_hash,
        "dialogue_1": shot["dialogue_1"],
        "dialogue_2": shot["dialogue_2"],
        "camera_motion": shot.get("camera_motion", ""),
        "scene_summary": shot.get("scene_summary", ""),
    }
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16]


def main() -> None:
    manifest_path = Path(sys.argv[1]) if len(sys.argv) > 1 else SHORT_DRAMA_DIR / "ep02_zhuanshi_chongsheng_manifest.json"
    force_compile = "--force" in sys.argv
    vault = json.loads(VAULT_PATH.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    WORKFLOWS_DIR.mkdir(parents=True, exist_ok=True)
    compiled = []
    manifest_dirty = False

    for idx, shot in enumerate(manifest["shots"], start=1):
        live_fp = compute_shot_fingerprint(shot)
        stored_fp = shot.get("input_fingerprint")
        out_mp4_name = shot.get("output_mp4", f"{shot['output_prefix']}_00001.mp4")
        out_mp4_path = ASSETS_DIR / out_mp4_name
        mp4_valid = out_mp4_path.exists() and out_mp4_path.stat().st_size > 100_000

        if not force_compile and shot.get("status") == "completed" and mp4_valid and stored_fp == live_fp:
            print(f"⏭️  Skipping verified completed {shot['shot_id']} ({out_mp4_name}, fp={live_fp})")
            continue

        if shot.get("status") == "completed" and (not mp4_valid or stored_fp != live_fp):
            print(
                f"🔄 Re-compiling {shot['shot_id']}: status='completed' but "
                f"mp4_valid={mp4_valid}, stored_fp={stored_fp} vs live_fp={live_fp}"
            )

        wf = compile_shot_workflow(vault, manifest, shot, seed=2026111000 + idx)
        out_wf = WORKFLOWS_DIR / f"compiled_{manifest['episode_id']}_{shot['shot_id'].lower()}.json"
        out_wf.write_text(json.dumps(wf, ensure_ascii=False, indent=2), encoding="utf-8")
        shot["input_fingerprint"] = live_fp
        manifest_dirty = True
        compiled.append(out_wf)
        print(
            f"✅ Compiled {shot['shot_id']} [{shot.get('shot_mode', 'natural_dialogue')} | "
            f"backend={shot.get('model_backend', 'h3_comfyui')}] -> {out_wf.name} (fp={live_fp})"
        )

    if manifest_dirty:
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"🎯 Total compiled shots: {len(compiled)}")


if __name__ == "__main__":
    main()
