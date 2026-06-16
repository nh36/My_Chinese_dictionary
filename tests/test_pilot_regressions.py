from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import evaluate_pilot_render  # noqa: E402
import analyze_hierarchy_gap  # noqa: E402
import render_curated_series  # noqa: E402


class PilotRegressionTests(unittest.TestCase):
    def load_active_entries(self) -> list[dict[str, object]]:
        active_ids = set(render_curated_series.DEFAULT_IDS)
        entries = evaluate_pilot_render.load_curated_entries(ROOT / "data/entries/curation")
        return [entry for entry in entries if entry["id"] in active_ids]

    def extract_entry_block(self, rendered: str, entry_id: str) -> str:
        block = evaluate_pilot_render.extract_entry_block(rendered, entry_id)
        assert block is not None
        return block

    def test_current_pilot_readiness_is_ready(self) -> None:
        entries = self.load_active_entries()
        rendered = (ROOT / "build/generated_curated_series_sample.tex").read_text(encoding="utf-8")
        metrics = evaluate_pilot_render.evaluate_entries(entries, rendered)
        self.assertEqual(metrics["overall_status"], "ready")

    def test_current_curated_entries_have_full_semantic_and_transliteration_coverage(self) -> None:
        entries = self.load_active_entries()
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
        self.assertIn(r"{\large{kym}},", rendered)
        self.assertNotIn("ŋrrar", rendered)
        self.assertRegex(
            rendered,
            re.compile(r"\{\\large\{\\textsuperscript\{bamb˸\}[^}]*\\textoverset\{a\}\{a\}k[₀₁₂₃₄₅₆₇₈₉]*\}\},"),
        )
        self.assertRegex(
            rendered,
            re.compile(r"\{\\large\{\\textsuperscript\{herb˸\}[^}]*\\textoverset\{a\}\{a\}k[₀₁₂₃₄₅₆₇₈₉]*\}\},"),
        )
        self.assertEqual(rendered.count(r"\begin{multicols*}{2}"), 1)
        self.assertEqual(rendered.count(r"\raggedcolumns"), 1)
        self.assertEqual(rendered.count(r"\pilotentry{%"), len(render_curated_series.DEFAULT_IDS))

    def test_generated_sample_orders_entries_by_schuessler_id(self) -> None:
        rendered = (ROOT / "build/generated_curated_series_sample.tex").read_text(encoding="utf-8")
        ordered_ids = [
            "02-01",
            "03-38",
            "03-57",
            "04-30",
            "04-61",
            "07-08",
            "09-25",
            "24-01",
            "38-03",
        ]
        positions = [rendered.index(rf"\paragraph{{\textoversetlarge{{{entry_id}}}") for entry_id in ordered_ids]
        self.assertEqual(positions, sorted(positions))

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

    def test_specific_hierarchy_cases_do_not_over_nest(self) -> None:
        entry_3803 = json.loads((ROOT / "data/entries/curation/38-03.json").read_text(encoding="utf-8"))
        by_character_3803 = {candidate["character"]: candidate for candidate in entry_3803["proposed_additions"]}
        self.assertEqual(by_character_3803["金"]["hierarchy_assignment"]["status"], "assigned-to-top-level")
        self.assertEqual(by_character_3803["金"]["hierarchy_assignment"]["parent_character"], "今")
        self.assertEqual(by_character_3803["㜝"]["hierarchy_assignment"]["parent_character"], "酓")

        entry_2614 = json.loads((ROOT / "data/entries/curation/26-14.json").read_text(encoding="utf-8"))
        by_character_2614 = {candidate["character"]: candidate for candidate in entry_2614["proposed_additions"]}
        self.assertIsNone(by_character_2614["眂"]["hierarchy_assignment"])
        self.assertEqual(by_character_2614["低"]["hierarchy_assignment"]["parent_character"], "氐")

        entry_1332 = json.loads((ROOT / "data/entries/curation/13-32.json").read_text(encoding="utf-8"))
        by_character_1332 = {candidate["character"]: candidate for candidate in entry_1332["proposed_additions"]}
        self.assertEqual(by_character_1332["修"]["hierarchy_assignment"]["status"], "assigned-to-top-level")
        self.assertEqual(by_character_1332["修"]["hierarchy_assignment"]["parent_character"], "攸")
        self.assertEqual(by_character_1332["䩦"]["hierarchy_assignment"]["parent_character"], "攸")

    def test_generated_sample_gathers_subseries_at_the_end_of_each_level(self) -> None:
        rendered = (ROOT / "build/generated_curated_series_sample.tex").read_text(encoding="utf-8")

        block_0201 = self.extract_entry_block(rendered, "02-01")
        self.assertLess(block_0201.index("格\t%"), block_0201.index(r"\begin{itemize}[noitemsep]"))
        self.assertIn(r"\item {\Large{客}}", block_0201)
        self.assertIn(r"\item {\Large{洛}}", block_0201)
        self.assertIn(r"\item {\Large{路}}", block_0201)

        block_0430 = self.extract_entry_block(rendered, "04-30")
        self.assertLess(block_0430.index("耜\t%"), block_0430.index(r"\item {\Large{以}}"))
        self.assertLess(block_0430.index("飴\t%"), block_0430.index(r"\item {\Large{枲}}"))
        self.assertLess(block_0430.index(r"\item {\Large{枲}}"), block_0430.index(r"\item {\Large{矣}}"))
        self.assertLess(block_0430.index(r"\item {\Large{矣}}"), block_0430.index(r"\item {\Large{台}}"))

        block_2805 = self.extract_entry_block(rendered, "28-05")
        self.assertLess(block_2805.index("諱\t%"), block_2805.index(r"\item {\Large{衛}}"))

        block_3240 = self.extract_entry_block(rendered, "32-40")
        self.assertLess(block_3240.index("愍\t%"), block_3240.index(r"\item {\Large{昬}}"))

        block_3521 = self.extract_entry_block(rendered, "35-21")
        self.assertLess(block_3521.index(r"\item {\Large{劫}}"), block_3521.index(r"\item {\Large{盇}}"))

        block_3803 = self.extract_entry_block(rendered, "38-03")
        self.assertLess(block_3803.index(r"\item {\Large{侌}}"), block_3803.index(r"\item {\Large{陰}}"))
        self.assertLess(block_3803.index(r"\item {\Large{酓}}"), block_3803.index(r"\item {\Large{金}}"))
        self.assertLess(block_3803.index(r"\item {\Large{金}}"), block_3803.index("錦\t%"))
        self.assertLess(block_3803.index(r"\item {\Large{欽}}"), block_3803.index("廞\t%"))

    def test_bad_subseries_roots_are_replaced_by_conservative_values(self) -> None:
        rendered = (ROOT / "build/generated_curated_series_sample.tex").read_text(encoding="utf-8")
        self.assertIn(r"\item {\Large{湯}}", rendered)
        self.assertRegex(rendered, re.compile(r"= \{\\large\{laṅ[₀₁₂₃₄₅₆₇₈₉]*\}\},"))
        self.assertIn(r"\item {\Large{台}}", rendered)
        self.assertRegex(rendered, re.compile(r"= \{\\large\{ly[₀₁₂₃₄₅₆₇₈₉]*\}\},"))
        self.assertIn(r"\item {\Large{咅}}", rendered)
        self.assertRegex(rendered, re.compile(r"= \{\\large\{py[₀₁₂₃₄₅₆₇₈₉]*\}\},"))
        self.assertIn(r"\item {\Large{星}}", rendered)
        self.assertRegex(rendered, re.compile(r"= \{\\large\{seṅ[₀₁₂₃₄₅₆₇₈₉]*\}\},"))
        self.assertNotIn(r"= {\large{khaṅ}},", rendered)
        self.assertNotIn(r"= {\large{khy}},", rendered)
        self.assertNotIn(r"= {\large{phy}},", rendered)
        self.assertNotIn(r"= {\large{theṅ}},", rendered)

    def test_active_curated_entries_have_no_candidate_parent_cycles(self) -> None:
        for entry in self.load_active_entries():
            cycles = build_parent_cycles(entry)
            self.assertFalse(cycles, msg=f"{entry['id']} has candidate-parent cycles: {cycles}")


def build_parent_cycles(entry: dict[str, object]) -> list[list[str]]:
    parent_map = {}
    for candidate in entry.get("proposed_additions", []):
        assignment = candidate.get("hierarchy_assignment") or {}
        if assignment.get("status") != "assigned-to-candidate-node":
            continue
        parent_character = assignment.get("parent_character")
        if parent_character and parent_character != candidate["character"]:
            parent_map[candidate["character"]] = parent_character

    cycles: list[list[str]] = []
    visited: set[str] = set()
    for start in parent_map:
        if start in visited:
            continue
        path: list[str] = []
        path_index: dict[str, int] = {}
        current = start
        while current in parent_map and current not in path_index and current not in visited:
            path_index[current] = len(path)
            path.append(current)
            current = parent_map[current]
        visited.update(path)
        if current in path_index:
            cycles.append(path[path_index[current] :])
    return cycles


if __name__ == "__main__":
    unittest.main()
