#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from ypp_pilot_gate import main as gate_main, validate_ypp_pilot_manifest  # noqa: E402


class TestYppPilotGate(unittest.TestCase):
    def test_valid_original_english_manifest_passes(self) -> None:
        manifest = {
            "track": "A",
            "title": "Why 94% of Retail Trading Bots Fail in Microstructure Regimes",
            "concept": "Original dark-tech quantitative documentary with self-created diagrams.",
            "language": "en",
            "original_ip": True,
            "audio_source": "self_recorded_en_narration + Flow Music",
            "flow_credit_budget": 1200,
            "gcp_usd_budget": 0,
            "ai_disclosure_required": True,
        }
        res = validate_ypp_pilot_manifest(manifest)
        self.assertTrue(res["ok"])
        self.assertEqual(res["reasons"], [])

        with tempfile.TemporaryDirectory() as tmp:
            fp = Path(tmp) / "pilot.json"
            fp.write_text(json.dumps(manifest), encoding="utf-8")
            self.assertEqual(gate_main([str(fp)]), 0)

    def test_rejects_banned_ip_non_en_missing_disclosure_and_gcp_burn(self) -> None:
        bad = {
            "track": "B",
            "title": "Illidan Arthas Warcraft Lore",
            "concept": "Fan trailer",
            "language": "zh",
            "original_ip": False,
            "audio_source": "",
            "flow_credit_budget": 4500,
            "gcp_usd_budget": 12.5,
            "ai_disclosure_required": False,
        }
        res = validate_ypp_pilot_manifest(bad)
        self.assertFalse(res["ok"])
        joined = ",".join(res["reasons"])
        self.assertIn("language_must_be_en_got:zh", joined)
        self.assertIn("original_ip_must_be_true", joined)
        self.assertIn("ai_disclosure_required_must_be_true", joined)
        self.assertIn("missing_audio_source", joined)
        self.assertIn("invalid_flow_credit_budget", joined)
        self.assertIn("gcp_usd_budget_must_be_zero", joined)
        self.assertIn("banned_third_party_ip", joined)


if __name__ == "__main__":
    unittest.main()
