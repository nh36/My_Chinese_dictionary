from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import pilot_ab_subseries  # noqa: E402


class PilotAbSubseriesTests(unittest.TestCase):
    def test_mc_form_classifier_handles_clear_a_and_b_examples(self) -> None:
        self.assertEqual(pilot_ab_subseries.classify_mc_form("ka")["class"], "a")
        self.assertEqual(pilot_ab_subseries.classify_mc_form("puH")["class"], "a")
        self.assertEqual(pilot_ab_subseries.classify_mc_form("gie")["class"], "b")
        self.assertEqual(pilot_ab_subseries.classify_mc_form("phiu")["class"], "b")
        self.assertEqual(pilot_ab_subseries.classify_mc_form("ṅiəH")["class"], "b")

    def test_pilot_entries_match_handwritten_a_b_labels(self) -> None:
        entries = pilot_ab_subseries.load_entries(
            ROOT / "data/current_tex_entries.json",
            ROOT / "main.tex",
        )
        analysis = pilot_ab_subseries.build_analysis(entries, ["18-01", "01-67"])
        by_entry = {entry["id"]: entry for entry in analysis["entries"]}

        entry_1801 = {subgroup["head_character"]: subgroup for subgroup in by_entry["18-01"]["subgroups"]}
        self.assertEqual(entry_1801["何"]["predicted_class"], "a")
        self.assertEqual(entry_1801["哥"]["predicted_class"], "a")
        self.assertEqual(entry_1801["奇"]["predicted_class"], "b")

        entry_0167 = {subgroup["head_character"]: subgroup for subgroup in by_entry["01-67"]["subgroups"]}
        self.assertEqual(entry_0167["布"]["predicted_class"], "a")
        self.assertEqual(entry_0167["浦"]["predicted_class"], "a")
        self.assertEqual(entry_0167["捕"]["predicted_class"], "a")
        self.assertEqual(entry_0167["尃"]["predicted_class"], "b")
        self.assertEqual(entry_0167["旉"]["predicted_class"], "b")
        self.assertTrue(all(subgroup["matches_handwritten"] for subgroup in entry_1801.values()))
        self.assertTrue(all(subgroup["matches_handwritten"] for subgroup in entry_0167.values()))


if __name__ == "__main__":
    unittest.main()
