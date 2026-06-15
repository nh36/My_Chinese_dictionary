from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import evaluate_pilot_render  # noqa: E402
import analyze_hierarchy_gap  # noqa: E402


class PilotRegressionTests(unittest.TestCase):
    def extract_entry_block(self, rendered: str, entry_id: str) -> str:
        marker = rf"\paragraph{{\textoversetlarge{{{entry_id}}}"
        start = rendered.index(marker)
        next_start = rendered.find(r"\paragraph{\textoversetlarge{", start + 1)
        return rendered[start : next_start if next_start != -1 else len(rendered)]

    def test_current_pilot_readiness_is_ready(self) -> None:
        entries = evaluate_pilot_render.load_curated_entries(ROOT / "data/entries/curation")
        rendered = (ROOT / "build/generated_curated_series_sample.tex").read_text(encoding="utf-8")
        metrics = evaluate_pilot_render.evaluate_entries(entries, rendered)
        self.assertEqual(metrics["overall_status"], "ready")

    def test_current_curated_entries_have_full_semantic_and_transliteration_coverage(self) -> None:
        entries = evaluate_pilot_render.load_curated_entries(ROOT / "data/entries/curation")
        proposed = [c for e in entries for c in e.get("proposed_additions", [])]
        self.assertTrue(proposed)
        self.assertTrue(all(c.get("semantic_assignment") for c in proposed))
        self.assertTrue(all(c.get("transliteration_latex") for c in proposed))
        self.assertTrue(all(c.get("render_latex") for c in proposed))
        self.assertTrue(all(c.get("mc_resolution") for c in proposed))

    def test_generated_sample_retains_semantic_superscripts_without_visible_mc_warning(self) -> None:
        rendered = (ROOT / "build/generated_curated_series_sample.tex").read_text(encoding="utf-8")
        self.assertNotIn(r"{\footnotesize[MC disagreement among imported sources]}", rendered)
        self.assertIn(r"{\large{\textsuperscript{oryz·}ka}},", rendered)

    def test_hand_done_01_01_hierarchy_snapshot(self) -> None:
        entries = json.loads((ROOT / "data/current_tex_entries.json").read_text(encoding="utf-8"))["entries"]
        entry = next(item for item in entries if item["id"] == "01-01")
        nodes = analyze_hierarchy_gap.extract_intermediate_nodes(entry["raw_block"])
        self.assertEqual(len(nodes), 5)
        for character in ["固", "胡", "居", "辜", "苦"]:
            self.assertTrue(any(character in node["character_line"] for node in nodes))

    def test_current_01_01_additions_use_inherited_hierarchy(self) -> None:
        entry = json.loads((ROOT / "data/entries/curation/01-01.json").read_text(encoding="utf-8"))
        by_character = {candidate["character"]: candidate for candidate in entry["proposed_additions"]}
        self.assertEqual(by_character["痼"]["hierarchy_assignment"]["parent_character"], "固")
        self.assertEqual(by_character["個"]["hierarchy_assignment"]["parent_character"], "固")

    def test_missing_series_additions_use_generated_hierarchy(self) -> None:
        entry_0201 = json.loads((ROOT / "data/entries/curation/02-01.json").read_text(encoding="utf-8"))
        by_character_0201 = {candidate["character"]: candidate for candidate in entry_0201["proposed_additions"]}
        self.assertEqual(by_character_0201["喀"]["hierarchy_assignment"]["parent_character"], "客")
        self.assertEqual(by_character_0201["露"]["hierarchy_assignment"]["parent_character"], "路")

        entry_3803 = json.loads((ROOT / "data/entries/curation/38-03.json").read_text(encoding="utf-8"))
        by_character_3803 = {candidate["character"]: candidate for candidate in entry_3803["proposed_additions"]}
        self.assertEqual(by_character_3803["飲"]["hierarchy_assignment"]["parent_character"], "酓")
        self.assertEqual(by_character_3803["錦"]["hierarchy_assignment"]["parent_character"], "金")

    def test_generated_sample_gathers_subseries_at_the_end_of_each_level(self) -> None:
        rendered = (ROOT / "build/generated_curated_series_sample.tex").read_text(encoding="utf-8")

        block_0201 = self.extract_entry_block(rendered, "02-01")
        self.assertLess(block_0201.index("格\t%"), block_0201.index(r"\begin{itemize}[noitemsep]"))
        self.assertIn(r"\item {\Large{客}}", block_0201)
        self.assertIn(r"\item {\Large{洛}}", block_0201)
        self.assertIn(r"\item {\Large{路}}", block_0201)

        block_0430 = self.extract_entry_block(rendered, "04-30")
        self.assertLess(block_0430.index("𨽿\t%"), block_0430.index(r"\begin{itemize}[noitemsep]"))
        self.assertLess(block_0430.index("飴\t%"), block_0430.index(r"\item {\Large{矣}}"))
        self.assertLess(block_0430.index(r"\item {\Large{矣}}"), block_0430.index(r"\item {\Large{台}}"))

        block_3803 = self.extract_entry_block(rendered, "38-03")
        self.assertLess(block_3803.index("廞\t%"), block_3803.index(r"\begin{itemize}[noitemsep]"))
        self.assertLess(block_3803.index(r"\item {\Large{侌}}"), block_3803.index(r"\item {\Large{陰}}"))
        self.assertLess(block_3803.index(r"\item {\Large{金}}"), block_3803.index("錦\t%"))


if __name__ == "__main__":
    unittest.main()
