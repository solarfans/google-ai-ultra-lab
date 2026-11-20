#!/usr/bin/env python3
"""
Generate 2 x 30s dark institutional documentary underscore stems via Vertex AI lyria-002
and crossfade them into a ~57.5s 48kHz stereo WAV bed at audio/lyria_score.wav.
Strictly pure instrumental prompts (no composer names or vocal/choir words per LL-012).
"""
from __future__ import annotations

import base64
import os
import subprocess
from pathlib import Path

import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

PROJECT = "project-665ac784-237e-4a71-ad0"
ROOT = Path(__file__).resolve().parent
AUDIO_DIR = ROOT / "audio"
STEM1 = AUDIO_DIR / "lyria_stem1.wav"
STEM2 = AUDIO_DIR / "lyria_stem2.wav"
OUT_WAV = AUDIO_DIR / "lyria_score.wav"


def get_token() -> str:
    legacy_path = os.path.expanduser("~/.config/colab-cli/token.json")
    if os.path.isfile(legacy_path):
        creds = Credentials.from_authorized_user_file(legacy_path)
        creds.refresh(Request())
        return str(creds.token)
    from colab_cli.auth import _get_google_auth_credentials

    oauth_cfg = os.path.expanduser(
        "~/.local/share/uv/tools/google-colab-cli/lib/python3.12/site-packages/colab_cli/oauth_config.json"
    )
    creds = _get_google_auth_credentials(oauth_cfg)
    if not creds.valid:
        creds.refresh(Request())
    return str(creds.token)


def generate_stem(token: str, prompt: str, negative_prompt: str, dst: Path) -> None:
    if dst.is_file() and dst.stat().st_size > 100_000:
        print(f"Reusing existing stem: {dst}")
        return
    url = f"https://us-central1-aiplatform.googleapis.com/v1/projects/{PROJECT}/locations/us-central1/publishers/google/models/lyria-002:predict"
    resp = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "x-goog-user-project": PROJECT,
            "Content-Type": "application/json",
        },
        json={
            "instances": [
                {
                    "prompt": prompt,
                    "negative_prompt": negative_prompt,
                }
            ],
            "parameters": {},
        },
        timeout=90,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"lyria-002 failed ({resp.status_code}): {resp.text[:800]}")
    preds = resp.json().get("predictions") or []
    if not preds:
        raise RuntimeError(f"lyria-002 returned empty predictions: {resp.text[:500]}")
    b64 = preds[0].get("bytesBase64Encoded") or preds[0].get("audioContent")
    if not b64:
        raise RuntimeError(f"lyria-002 missing audio payload keys: {list(preds[0].keys())}")
    dst.write_bytes(base64.b64decode(b64))
    print(f"Saved stem: {dst} ({dst.stat().st_size} bytes)")


def main() -> None:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    token = get_token()
    neg = "vocals, singing, choir, voice, cheerful, pop, upbeat, rock guitar, heavy edm"

    generate_stem(
        token,
        "Minimalist dark institutional finance documentary underscore in D minor, tense pulsing analog sub-bass, muted low cello ostinato, subtle ticking metallic percussion, sparse crystalline piano notes, restrained suspenseful atmosphere, 86 bpm",
        neg,
        STEM1,
    )
    generate_stem(
        token,
        "Dark modern investigative economic thriller instrumental underscore in D minor, deep atmospheric analog synth drone, deliberate low strings tension swell, soft muted piano motif, serious analytical mood, 86 bpm",
        neg,
        STEM2,
    )

    cmd = [
        "ffmpeg",
        "-y",
        "-v",
        "error",
        "-i",
        str(STEM1),
        "-i",
        str(STEM2),
        "-filter_complex",
        "[0:a][1:a]acrossfade=d=2.5:c1=tri:c2=tri,aformat=sample_rates=48000:channel_layouts=stereo[outa]",
        "-map",
        "[outa]",
        "-c:a",
        "pcm_s16le",
        str(OUT_WAV),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if res.returncode != 0:
        raise RuntimeError(f"ffmpeg crossfade failed: {res.stderr}")
    print(f"Created crossfaded score: {OUT_WAV} ({OUT_WAV.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
