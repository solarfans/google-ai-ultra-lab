import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import hmb_episode_factory as f  # noqa: E402
from ypp_pilot_gate import validate_ypp_pilot_manifest  # noqa: E402


class TestHmbEpisodeFactory(unittest.TestCase):
    def test_normalize_cues_splits_sentences_and_merges_us_abbr(self) -> None:
        raw = [
            {"start": 0.0, "end": 1.2, "text": "Look behind the curtain."},
            {"start": 1.4, "end": 3.3, "text": "Ten-year U.S."},
            {"start": 3.3, "end": 5.6, "text": "Treasury yields pierced five percent."},
            {"start": 5.6, "end": 7.1, "text": "The U.S."},
            {"start": 7.1, "end": 9.1, "text": "dollar surged past one hundred and four."},
        ]
        out = f.normalize_cues(raw)
        self.assertEqual(
            [c["text"] for c in out],
            [
                "Look behind the curtain.",
                "Ten-year U.S. Treasury yields pierced five percent.",
                "The U.S. dollar surged past one hundred and four.",
            ],
        )

    def test_wrap_lines_handles_long_phrases_within_limit(self) -> None:
        txt = "Signals that separate a violent flush from a true structural bear market."
        lines = f.wrap_lines(txt, max_line=28)
        self.assertGreaterEqual(len(lines), 2)
        for ln in lines:
            self.assertLessEqual(len(ln), 38)

    def test_compute_vix_ratio_series_aligned_and_spot(self) -> None:
        vix = [{"date": "2026-11-18", "close": 24.0}, {"date": "2026-11-19", "close": 29.0}, {"date": "2026-11-20", "close": 29.79}]
        vix3m = [{"date": "2026-11-18", "close": 25.0}, {"date": "2026-11-19", "close": 27.03}]
        res = f.compute_vix_ratio_series(vix, vix3m)
        self.assertEqual(len(res["aligned_points"]), 2)
        self.assertEqual(res["latest_aligned_date"], "2026-11-19")
        self.assertAlmostEqual(res["spot_over_3m_ratio"], 1.10, places=2)

    def test_resolve_music_segments_requires_zero_gcp_spend(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            lib = root / "lib"
            lib.mkdir()
            (lib / "a.wav").write_bytes(b"RIFF0000")
            cat = {
                "gcp_spend_usd": 0.0,
                "tracks": [{"id": "t1", "file": "a.wav"}],
            }
            (lib / "CATALOG.json").write_text(json.dumps(cat), encoding="utf-8")
            spec = {
                "music_library_catalog": "lib/CATALOG.json",
                "music_segments": [{"track_id": "t1", "start_sec": 0, "duration_sec": 20}],
            }
            segs = f.resolve_music_segments(spec, repo_root=root)
            self.assertEqual(len(segs), 1)
            self.assertEqual(segs[0]["wav_path"], lib / "a.wav")

            cat["gcp_spend_usd"] = 0.12
            (lib / "CATALOG.json").write_text(json.dumps(cat), encoding="utf-8")
            with self.assertRaises(ValueError):
                f.resolve_music_segments(spec, repo_root=root)

    def test_ep01_manifest_passes_ypp_gate(self) -> None:
        ep01_manifest = REPO_ROOT / "pipelines" / "how_markets_break_ep01" / "manifest.json"
        data = json.loads(ep01_manifest.read_text(encoding="utf-8"))
        res = validate_ypp_pilot_manifest(data)
        self.assertTrue(res["ok"], f"Unexpected gate failure: {res}")
        self.assertEqual(res["language"], "en")


if __name__ == "__main__":
    unittest.main()
