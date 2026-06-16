from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import ab_division  # noqa: E402
import render_curated_series  # noqa: E402


class AbDivisionTests(unittest.TestCase):
    def test_uniform_ambiguous_group_gets_marker(self) -> None:
        resolution = ab_division.resolve_root_display("pa", ["puH", "phuH"])
        self.assertEqual(resolution["division_class"], "a")
        self.assertTrue(resolution["mark_required"])
        self.assertEqual(resolution["display_root"], r"p\textoverset{a}{a}")

    def test_mixed_group_stays_unmarked(self) -> None:
        resolution = ab_division.resolve_root_display("pa₂", ["phuX", "phiu"])
        self.assertEqual(resolution["division_class"], "mixed")
        self.assertFalse(resolution["mark_required"])
        self.assertEqual(resolution["display_root"], "pa₂")

    def test_explicit_root_stays_unmarked(self) -> None:
        resolution = ab_division.resolve_root_display("phiu", ["phiu", "biuH"])
        self.assertEqual(resolution["division_class"], "b")
        self.assertFalse(resolution["mark_required"])
        self.assertEqual(resolution["display_root"], "phiu")

    def test_render_candidate_node_prefers_display_root(self) -> None:
        candidate = {
            "character": "布",
            "render_latex": "布\t%bu4\n{\\large{pa\\textsuperscript{˸lint}}},\n\\textit{puH};",
            "mand2mc_rows": [{"pinyin": "bu4"}],
            "bs_gsr_rows": [],
            "resolved_node_root": {
                "root": "pa",
                "display_root": r"p\textoverset{a}{a}",
            },
        }
        rendered = "\n".join(render_curated_series.render_candidate_node(candidate, {}))
        self.assertIn(r"= {\large{p\textoverset{a}{a}}},", rendered)


if __name__ == "__main__":
    unittest.main()
