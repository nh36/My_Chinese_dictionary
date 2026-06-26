from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import render_curated_series  # noqa: E402


class RenderCuratedSeriesTests(unittest.TestCase):
    def test_render_curated_entry(self) -> None:
        entry = {
            "id": "02-01",
            "packet_kind": "missing_series",
            "candidate_source_strategy": "schuessler_k_tokens",
            "candidate_source_tokens": ["766"],
            "coverage": {"schuessler_k_tokens": "766", "combined_source_character_count": 37},
            "tex_entry": None,
            "proposed_additions": [{
                "character": "各",
                "mand2mc_count": 2,
                "bs_gsr_count": 1,
                "shengfu_character_count": 0,
                "transliteration_latex": r"{\large{\textsuperscript{arb·}kay}},",
                "mand2mc_rows": [{"pinyin": "ge4", "mc_nwh": "kak", "gsr": "0766a"}],
                "bs_gsr_rows": [{"pinyin": "gè", "mc_bs": "kak", "gsr": "0766a"}],
                "mand_bs_mc_disagreement": False,
            }],
        }
        rendered = render_curated_series.render_curated_entry(entry)
        self.assertIn("\\paragraph{\\textoversetlarge{02-01}{\\huge{各}}}", rendered)
        self.assertNotIn("\\begin{multicols}{2}", rendered)
        self.assertIn("\\textit{kak};", rendered)

    def test_render_existing_addendum_entry_does_not_repeat_heading(self) -> None:
        entry = {
            "id": "01-42",
            "packet_kind": "existing_addendum",
            "tex_entry": {
                "head": {"raw": r"\huge{余}"},
                "raw_block": "\\paragraph{\\textoversetlarge{01-42}{\\huge{余}}}\n{\\large{la}},\n\\textit{yiə};\n",
            },
            "entry_hierarchy": {"nodes": []},
            "proposed_additions": [
                {
                    "character": "敘",
                    "mand2mc_rows": [{"pinyin": "xu4", "gsr": "0082o"}],
                    "bs_gsr_rows": [],
                    "mc_resolution": {"display_forms": ["ziəX"]},
                    "transliteration_latex": r"{\large{la\textsuperscript{·fer}}},",
                    "hierarchy_assignment": {"status": "assigned-to-top-level"},
                }
            ],
        }

        rendered = render_curated_series.render_curated_entry(entry)

        self.assertEqual(rendered.count(r"\paragraph{\textoversetlarge{01-42}{\huge{余}}}"), 1)
        self.assertIn("% Proposed additions from imported sources for 01-42", rendered)
        self.assertIn("敘\t%xu4", rendered)

    def test_render_document(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            main_tex = Path(temp_dir) / "main.tex"
            main_tex.write_text("\\documentclass{article}\n\\begin{document}\n\\end{document}\n", encoding="utf-8")
            semantic_data = {
                "items": [
                    {
                        "graph_raw": "木",
                        "abbreviation": "arb",
                        "expanded_latin": "arb(or)",
                        "notes": "(only in test)",
                        "comments": ["(mù)", "(tree)"],
                        "used_abbreviation_aliases": ["arb"],
                    }
                ]
            }
            doc = render_curated_series.render_document(
                [
                    {
                        "id": "02-01",
                        "packet_kind": "missing_series",
                        "candidate_source_strategy": "schuessler_k_tokens",
                        "candidate_source_tokens": ["766"],
                        "coverage": {"schuessler_k_tokens": "766", "combined_source_character_count": 37},
                        "tex_entry": None,
                        "proposed_additions": [],
                    }
                ],
                main_tex,
                semantic_data,
            )
            self.assertIn("\\section*{Integrated semantic components}", doc)
            self.assertIn(r"\item 木 \textbf{arb} arb(or) --- (only in test)", doc)
            self.assertNotIn("(mù)", doc)
            self.assertNotIn("(tree)", doc)
            self.assertNotIn("entry aliases", doc)
            self.assertIn("\\section*{Curated pilot series in comparable format}", doc)
            self.assertIn("\\end{document}", doc)

    def test_default_ids_are_unique(self) -> None:
        self.assertEqual(len(render_curated_series.DEFAULT_IDS), len(set(render_curated_series.DEFAULT_IDS)))


if __name__ == "__main__":
    unittest.main()
