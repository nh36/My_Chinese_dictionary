from __future__ import annotations

import sys
import unittest


ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import promote_series_packets  # noqa: E402


class PromoteSeriesPacketsTests(unittest.TestCase):
    def test_promote_packet_keeps_only_non_tex_additions(self) -> None:
        packet = {
            "gsc_id": "18-18",
            "packet_kind": "existing_addendum",
            "candidate_source_strategy": "tex_gsr_prefixes",
            "candidate_source_tokens": ["15", "17"],
            "schuessler": {},
            "coverage": {"combined_source_character_count": 9},
            "tex_entry": {"id": "18-18", "raw_block": "\\paragraph{...}", "context_environments": []},
            "candidate_characters": [
                {"character": "麻", "in_tex": True, "mand2mc_rows": [], "bs_gsr_rows": [], "shengfu_character_rows": [], "shengfu_component_rows": [], "mand_bs_mc_disagreement": False},
                {"character": "加", "in_tex": False, "mand2mc_rows": [{"character": "加"}], "bs_gsr_rows": [], "shengfu_character_rows": [], "shengfu_component_rows": [], "mand_bs_mc_disagreement": False},
            ],
        }
        promoted = promote_series_packets.promote_packet(packet)
        self.assertEqual(promoted["id"], "18-18")
        self.assertEqual(len(promoted["proposed_additions"]), 1)
        self.assertEqual(promoted["proposed_additions"][0]["character"], "加")
        self.assertEqual(promoted["candidate_source_strategy"], "tex_gsr_prefixes")


if __name__ == "__main__":
    unittest.main()
