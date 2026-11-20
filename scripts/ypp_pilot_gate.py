#!/usr/bin/env python3
"""
Deterministic Pre-Production Compliance Gate for YouTube YPP (`Y0`) Original English Pilot (100% stdlib).

Enforces:
  - English-only (`language == "en"`)
  - 100% original IP (`original_ip == True`) and zero banned third-party franchise terms
  - Explicit audio source + mandatory YouTube AI disclosure flag
  - Zero GCP cash/trial burn (`gcp_usd_budget == 0`) & bounded Channel A Flow credits (`<= 2000`)
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any

BANNED_IP_TERMS: tuple[str, ...] = (
    "warcraft",
    "blizzard",
    "illidan",
    "arthas",
    "azeroth",
    "disney",
    "marvel",
    "nintendo",
    "chu shi chun qiu",
    "楚氏春秋",
)
_BANNED_RE = re.compile(
    "|".join(re.escape(term) for term in BANNED_IP_TERMS),
    re.IGNORECASE,
)


def validate_ypp_pilot_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    """Validate pilot manifest against YPP original-IP & Zero-Burn rules. Raises ValueError or returns ok dict."""
    if not isinstance(manifest, dict):
        raise ValueError("Manifest must be a JSON object")

    reasons: list[str] = []
    title = str(manifest.get("title") or "").strip()
    concept = str(manifest.get("concept") or "").strip()
    track = str(manifest.get("track") or "").strip()
    lang = str(manifest.get("language") or "").strip().lower()
    audio_source = str(manifest.get("audio_source") or "").strip()

    if len(title) < 4:
        reasons.append("missing_or_short_title")
    if not track:
        reasons.append("missing_track")
    if lang != "en":
        reasons.append(f"language_must_be_en_got:{lang or 'empty'}")
    if manifest.get("original_ip") is not True:
        reasons.append("original_ip_must_be_true")
    if manifest.get("ai_disclosure_required") is not True:
        reasons.append("ai_disclosure_required_must_be_true")
    if not audio_source:
        reasons.append("missing_audio_source")

    flow_credits = manifest.get("flow_credit_budget")
    if not isinstance(flow_credits, (int, float)) or flow_credits <= 0 or flow_credits > 2000:
        reasons.append(f"invalid_flow_credit_budget:{flow_credits}")

    gcp_budget = manifest.get("gcp_usd_budget", 0)
    if not isinstance(gcp_budget, (int, float)) or float(gcp_budget) != 0.0:
        reasons.append(f"gcp_usd_budget_must_be_zero:{gcp_budget}")

    hit = _BANNED_RE.search(f"{title}\n{concept}")
    if hit:
        reasons.append(f"banned_third_party_ip:{hit.group(0)}")

    return {
        "ok": len(reasons) == 0,
        "reasons": reasons,
        "track": track,
        "language": lang,
        "flow_credit_budget": flow_credits,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate YouTube YPP Y0 Original English Pilot Manifest")
    parser.add_argument("manifest_json", help="Path to pilot manifest JSON")
    args = parser.parse_args(argv)

    data = json.loads(Path(args.manifest_json).read_text(encoding="utf-8"))
    res = validate_ypp_pilot_manifest(data)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
