from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import export_series_packets  # noqa: E402


class ExportSeriesPacketsTests(unittest.TestCase):
    def test_render_packet_report_mentions_candidates(self) -> None:
        packet = {
            "gsc_id": "02-01",
            "packet_kind": "missing_series",
            "candidate_source_strategy": "schuessler_k_tokens",
            "candidate_source_tokens": ["766"],
            "coverage": {
                "schuessler_k_tokens": "766",
                "schuessler_source_page": "90",
                "in_tex": "no",
                "mand2mc_character_count": "37",
                "bs_gsr_character_count": "12",
                "combined_source_character_count": "37",
            },
            "tex_entry": None,
            "candidate_characters": [
                {
                    "character": "各",
                    "in_tex": False,
                    "mand2mc_rows": [{"character": "各"}],
                    "bs_gsr_rows": [{"character": "各"}],
                    "shengfu_character_rows": [],
                    "shengfu_component_rows": [],
                    "mand_bs_mc_disagreement": False,
                }
            ],
        }
        report = export_series_packets.render_packet_report(packet)
        self.assertIn("# Series packet 02-01", report)
        self.assertIn("各", report)
        self.assertIn("Candidate characters not already in TeX", report)


if __name__ == "__main__":
    unittest.main()
