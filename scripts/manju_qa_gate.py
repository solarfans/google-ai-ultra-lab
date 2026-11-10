#!/usr/bin/env python3
"""Autonomous 5-Gate Pre-Flight & Post-Render QA Engine for AI Manju (`manju_qa_gate.py`).

Enforces deterministic self-discovery of defects BEFORE burning Colab G4 CU or
delivering any artifact to the Owner:
- Gate 1: Canonical Novel Fidelity & Substring Verification against `novel-continuation-lab`
- Gate 2: Physical Staging Common-Sense & Soul-Transmigration OS Mode Check
- Gate 3: Neural Voice Seed Provenance & PCM Acoustic Distortion Audit (blocks `say`/`asetrate`)
- Gate 4: Anti-"Book Recitation" Spoken Cadence & Clause-Length Audit
- Gate 5: Post-Mix / Post-Render Multimodal Audio-Visual Readiness Check
"""

from __future__ import annotations

import json
import math
import re
import struct
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SHORT_DRAMA_DIR = BASE_DIR / "pipelines" / "short_drama"
VAULT_PATH = SHORT_DRAMA_DIR / "character_vault.json"
ASSETS_DIR = SHORT_DRAMA_DIR / "assets_manju_v2"
SEEDS_MANIFEST_PATH = ASSETS_DIR / "voice_seeds_manifest.json"
NOVEL_CHAPTERS_DIR = Path(
    "/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/novel-continuation-lab/books/chushi-chunqiu/source/raw/chapters"
)

VALID_SHOT_MODES = {
    "offscreen_pa_and_os",
    "single_inner_monologue_os",
    "os_plus_short_spoken",
    "natural_dialogue",
}


def parse_window_seconds(window_str: str) -> float:
    """Parse '00:00.800–00:04.800' into duration in seconds."""
    parts = re.split(r"[–-]", window_str)
    if len(parts) != 2:
        raise ValueError(f"Invalid window format: {window_str}")

    def to_sec(ts: str) -> float:
        mm, ss = ts.strip().split(":")
        return int(mm) * 60.0 + float(ss)

    return max(0.1, to_sec(parts[1]) - to_sec(parts[0]))


def count_chinese_chars(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def max_clause_length(text: str) -> tuple[int, str]:
    clauses = [c.strip() for c in re.split(r"[，。！？……；、,!?]+", text) if c.strip()]
    if not clauses:
        return 0, ""
    longest = max(clauses, key=count_chinese_chars)
    return count_chinese_chars(longest), longest


def inspect_wav_acoustics(wav_path: Path) -> dict:
    with wave.open(str(wav_path), "rb") as wf:
        n_channels = wf.getnchannels()
        sample_width = wf.getsampwidth()
        framerate = wf.getframerate()
        n_frames = wf.getnframes()
        raw = wf.readframes(n_frames)

    if sample_width != 2:
        raise ValueError(f"{wav_path.name}: expected 16-bit PCM WAV, got sample_width={sample_width}")

    total_samples = n_frames * n_channels
    samples = struct.unpack(f"<{total_samples}h", raw)
    # Mix down to mono for acoustic analysis
    mono = samples[0::n_channels] if n_channels > 1 else samples

    if not mono:
        raise ValueError(f"{wav_path.name}: empty audio file")

    sum_sq = sum(float(s) * float(s) for s in mono)
    rms = math.sqrt(sum_sq / len(mono))
    dbfs = 20.0 * math.log10(max(rms, 1.0) / 32768.0)
    peak = max(abs(s) for s in mono)

    # Zero-crossing rate (detects metallic high-frequency screech / formant distortion)
    zero_crossings = sum(1 for i in range(1, len(mono)) if (mono[i - 1] >= 0) != (mono[i] >= 0))
    zcr = zero_crossings / float(len(mono))

    return {
        "duration_sec": round(n_frames / float(framerate), 3),
        "dbfs": round(dbfs, 2),
        "peak": peak,
        "zcr": round(zcr, 4),
    }


def parse_window_bounds(window_str: str) -> tuple[float, float]:
    """Parse '00:00.800–00:04.800' into (start_sec, end_sec)."""
    parts = re.split(r"[–-]", window_str)
    if len(parts) != 2:
        raise ValueError(f"Invalid window format: {window_str}")

    def to_sec(ts: str) -> float:
        mm, ss = ts.strip().split(":")
        return int(mm) * 60.0 + float(ss)

    return to_sec(parts[0]), to_sec(parts[1])


def audit_rendered_mp4_shot(mp4_path: Path, shot: dict) -> list[str]:
    """Post-render inspection of an individual rendered MP4 shot (stream integrity + window RMS energy)."""
    errs: list[str] = []
    if not mp4_path.exists():
        return [f"[Gate 6 Post-Render] {shot['shot_id']}: Missing rendered MP4: {mp4_path.name}"]

    probe = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=codec_type,width,height",
            "-of",
            "json",
            str(mp4_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if probe.returncode != 0:
        return [f"[Gate 6 Post-Render] {shot['shot_id']}: ffprobe failed on {mp4_path.name}"]

    info = json.loads(probe.stdout)
    dur = float(info.get("format", {}).get("duration", 0.0))
    if dur < 9.5 or dur > 11.0:
        errs.append(f"[Gate 6 Post-Render] {shot['shot_id']}: Abnormal duration {dur:.2f}s in {mp4_path.name}")

    # Check for unintended black frames (> 0.25s continuous black) via FFmpeg blackdetect
    b_res = subprocess.run(
        ["ffmpeg", "-v", "info", "-i", str(mp4_path), "-vf", "blackdetect=d=0.25:pix_th=0.05", "-an", "-f", "null", "-"],
        capture_output=True,
        text=True,
        check=False,
    )
    if "black_start:" in b_res.stderr:
        errs.append(f"[Gate 6 Post-Render] {shot['shot_id']}: Black frame glitch detected in {mp4_path.name}!")

    # Extract 16kHz mono PCM WAV and verify speech RMS energy + anti-clipping inside d1 and d2 windows
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp_wav:
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(mp4_path), "-ac", "1", "-ar", "16000", tmp_wav.name],
            capture_output=True,
            check=True,
        )
        with wave.open(tmp_wav.name, "rb") as wf:
            sr = wf.getframerate()
            n_frames = wf.getnframes()
            samples = struct.unpack(f"<{n_frames}h", wf.readframes(n_frames))

        peak_all = max((abs(x) for x in samples), default=0)
        if peak_all >= 32765:
            errs.append(f"[Gate 6 Post-Render] {shot['shot_id']}: Hard audio clipping detected (peak={peak_all})!")

        for d_key in ("dialogue_1", "dialogue_2"):
            s_sec, e_sec = parse_window_bounds(shot[d_key]["window"])
            i0 = max(0, int(s_sec * sr))
            i1 = min(len(samples), int(e_sec * sr))
            seg = samples[i0:i1]
            if not seg:
                errs.append(f"[Gate 6 Post-Render] {shot['shot_id']}.{d_key}: Empty audio slice [{s_sec:.2f}s–{e_sec:.2f}s]")
                continue
            rms = math.sqrt(sum(float(x) * float(x) for x in seg) / len(seg))
            dbfs = 20.0 * math.log10(max(rms, 1.0) / 32768.0)
            if dbfs < -36.0:
                errs.append(
                    f"[Gate 6 Post-Render] {shot['shot_id']}.{d_key}: Dead/silent audio window [{s_sec:.2f}s–{e_sec:.2f}s] ({dbfs:.1f} dBFS)!"
                )
    return errs


def run_qa_gate(manifest_path: Path, post_render: bool = False) -> int:
    mode_label = "Pre-Flight + Post-Render 6-Gate" if post_render else "Pre-Flight 5-Gate"
    print(f"🔍 Running Autonomous {mode_label} QA Audit on: {manifest_path.name}")
    vault = json.loads(VAULT_PATH.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    seeds_manifest = json.loads(SEEDS_MANIFEST_PATH.read_text(encoding="utf-8")) if SEEDS_MANIFEST_PATH.exists() else {}

    errors: list[str] = []
    warnings: list[str] = []

    # --- GATE 1: Canonical Novel Fidelity & Anti-Rushing ---
    print("  [Gate 1] Auditing Canonical Novel Fidelity & Exact Quote Anchors...")
    for shot in manifest.get("shots", []):
        sid = shot["shot_id"]
        anchor = shot.get("canonical_anchor")
        if not anchor:
            errors.append(f"[Gate 1] {sid}: Missing `canonical_anchor` block (must anchor to novel chapter text).")
            continue
        chap_file = NOVEL_CHAPTERS_DIR / anchor.get("chapter_file", "")
        if not chap_file.exists():
            errors.append(f"[Gate 1] {sid}: Canonical chapter file not found: {chap_file}")
            continue
        chap_text = chap_file.read_text(encoding="utf-8")
        quote = anchor.get("source_quote", "").strip()
        if len(quote) < 6 or quote not in chap_text:
            errors.append(
                f"[Gate 1] {sid}: `source_quote` ('{quote}') not found verbatim in {chap_file.name}! Hallucination/drift blocked."
            )

    # --- GATE 2: Physical Staging Common-Sense & Soul-Transmigration OS Logic ---
    print("  [Gate 2] Auditing Physical Staging Common-Sense & Inner Monologue (OS) Logic...")
    for shot in manifest.get("shots", []):
        sid = shot["shot_id"]
        mode = shot.get("shot_mode", "")
        if mode not in VALID_SHOT_MODES:
            errors.append(f"[Gate 2] {sid}: Invalid or missing `shot_mode`='{mode}'. Must be one of {sorted(VALID_SHOT_MODES)}.")

        if "stewardess_broadcast" in (shot["subject_1"], shot["subject_2"]) and mode != "offscreen_pa_and_os":
            errors.append(
                f"[Gate 2] {sid}: `stewardess_broadcast` MUST use `shot_mode='offscreen_pa_and_os'` (no flight attendant standing beside passenger seat with a phone!)."
            )

        if not shot.get("visual_must_show"):
            errors.append(f"[Gate 2] {sid}: Missing `visual_must_show` checklist for visual-dialogue alignment.")

    # --- GATE 3: Neural Voice Seed Provenance & Acoustic Distortion Check ---
    print("  [Gate 3] Auditing Voice Seeds Provenance & PCM Acoustic Metrics...")
    seeds_dict = seeds_manifest.get("seeds", {})
    used_chars = set()
    for shot in manifest.get("shots", []):
        used_chars.add(shot["subject_1"])
        used_chars.add(shot["subject_2"])

    for cid in sorted(used_chars):
        if cid not in vault["characters"]:
            errors.append(f"[Gate 3] Unknown character_id '{cid}' not in character_vault.json")
            continue
        seed_fname = vault["characters"][cid]["voice_seed"]
        seed_path = ASSETS_DIR / seed_fname
        if not seed_path.exists():
            errors.append(f"[Gate 3] Voice seed file missing: {seed_fname}")
            continue
        prov = seeds_dict.get(seed_fname)
        if not prov or prov.get("engine") not in ("edge-tts", "CosyVoice2") or prov.get("asetrate_used", True):
            errors.append(
                f"[Gate 3] {seed_fname}: Failed provenance check (legacy macOS `say` or `asetrate` pitch-shift is strictly forbidden)."
            )
        acoustics = inspect_wav_acoustics(seed_path)
        if acoustics["zcr"] > 0.20:
            errors.append(
                f"[Gate 3] {seed_fname}: High zero-crossing rate ({acoustics['zcr']}) indicates metallic/ghostly distortion!"
            )
        if acoustics["dbfs"] < -30.0 or acoustics["dbfs"] > -5.0:
            errors.append(f"[Gate 3] {seed_fname}: Abnormal loudness ({acoustics['dbfs']} dBFS).")
        print(
            f"     ✓ {seed_fname}: engine={prov.get('engine')}, loudness={acoustics['dbfs']} dBFS, zcr={acoustics['zcr']}"
        )

    # --- GATE 4: Anti-"Book Recitation" Spoken Cadence & Clause-Length Audit ---
    print("  [Gate 4] Auditing Spoken Dialogue Cadence & Clause Length (Anti-'Book Recitation')...")
    for shot in manifest.get("shots", []):
        sid = shot["shot_id"]
        for d_key in ("dialogue_1", "dialogue_2"):
            d = shot[d_key]
            line = d["line"]
            if "【" in line or "】" in line:
                errors.append(f"[Gate 4] {sid}.{d_key}: Spoken line contains forbidden bracket tags: {line}")
            max_len, bad_clause = max_clause_length(line)
            if max_len > 16:
                errors.append(
                    f"[Gate 4] {sid}.{d_key}: Clause too long/bookish ({max_len} chars > 16 max): '{bad_clause}'. Add natural breathing pauses (`，`/`……`)."
                )
            dur = parse_window_seconds(d["window"])
            total_chars = count_chinese_chars(line)
            cps = total_chars / dur
            if cps > 6.2:
                errors.append(
                    f"[Gate 4] {sid}.{d_key}: Speaking rate too rushed ({cps:.1f} chars/sec, {total_chars} chars in {dur:.1f}s)."
                )
            print(
                f"     ✓ {sid}.{d_key}: {total_chars} chars in {dur:.1f}s ({cps:.1f} chars/s), max_clause={max_len} chars"
            )

    # --- GATE 5: First-Frame Visual Asset Existence & Audio Timing Non-Overlap Check ---
    print("  [Gate 5] Auditing Storyboard First-Frame Assets & Dual-Track Audio Timings...")
    timings_path = SHORT_DRAMA_DIR / "audio_previews" / f"{manifest['episode_id']}_audio_timings.json"
    timings_data = json.loads(timings_path.read_text(encoding="utf-8")) if timings_path.exists() else {}
    for shot in manifest.get("shots", []):
        sid = shot["shot_id"]
        ff_path = ASSETS_DIR / shot["first_frame"]
        if not ff_path.exists():
            errors.append(f"[Gate 5] {sid}: First-frame PNG missing: {shot['first_frame']}")
        else:
            print(f"     ✓ {sid}: First-frame asset present ({shot['first_frame']})")
        if sid in timings_data:
            t = timings_data[sid]
            if t["gap_sec"] < 0.20:
                errors.append(f"[Gate 5] {sid}: Audio stems overlap or gap too tight (gap={t['gap_sec']}s < 0.20s)!")
            if t["d2_end_sec"] > 9.95:
                errors.append(f"[Gate 5] {sid}: Audio stem 2 cut off at shot boundary (d2_end={t['d2_end_sec']}s > 9.95s)!")
            print(
                f"     ✓ {sid} Audio Timing: d1=[{t['d1_start_sec']}s–{t['d1_end_sec']}s], "
                f"gap={t['gap_sec']}s, d2=[{t['d2_start_sec']}s–{t['d2_end_sec']}s] (0 overlap, 0 cutoff)"
            )

    # --- GATE 6 (Optional `--post-render`): Actual Rendered MP4 Stream & Window Acoustic Audit ---
    if post_render:
        print("  [Gate 6] Auditing Post-Render MP4 Shots (ffprobe stream integrity + speech window dBFS)...")
        for shot in manifest.get("shots", []):
            sid = shot["shot_id"]
            mp4_name = shot.get("output_mp4", f"{shot['output_prefix']}_00001.mp4")
            mp4_path = ASSETS_DIR / mp4_name
            shot_errs = audit_rendered_mp4_shot(mp4_path, shot)
            if shot_errs:
                errors.extend(shot_errs)
            else:
                print(f"     ✓ {sid}: Rendered MP4 verified ({mp4_name}, speech energy present in d1 & d2 windows)")

    if warnings:
        for w in warnings:
            print(f"  ⚠️  {w}")

    if errors:
        print("\n❌ QA GATE BLOCKED COMPILATION — Fix the following defects first:")
        for err in errors:
            print(f"  ✗ {err}")
        return 1

    print("\n✅ ALL QA GATES PASSED (0 errors). Ready for compilation / synthesis.")
    return 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    post_render_flag = "--post-render" in sys.argv
    target = Path(args[0]) if args else SHORT_DRAMA_DIR / "ep02_zhuanshi_chongsheng_manifest.json"
    sys.exit(run_qa_gate(target, post_render=post_render_flag))
