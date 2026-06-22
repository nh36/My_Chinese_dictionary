from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import render_integrated_dictionary  # noqa: E402


class RenderIntegratedDictionaryTests(unittest.TestCase):
    def test_collapse_hand_entry_strips_end_document(self) -> None:
        raw = "\\paragraph{X}\nbody\n\\end{document}\n"
        self.assertEqual(render_integrated_dictionary.sanitize_hand_entry(raw), "\\paragraph{X}\nbody")

    def test_render_semantic_section_omits_visible_provenance(self) -> None:
        semantic_data = {
            "items": [
                {
                    "graph_raw": "木",
                    "abbreviation": "arb",
                    "expanded_latin": "arb(or)",
                    "notes": None,
                    "comments": [],
                    "sources": [{"source": "current_main_tex"}, {"source": "earlier_pilot"}],
                }
            ]
        }
        rendered = "\n".join(render_integrated_dictionary.render_semantic_section(semantic_data))
        self.assertIn(r"\item 木 \textbf{arb} arb(or)", rendered)
        self.assertNotIn("current+pilot", rendered)


if __name__ == "__main__":
    unittest.main()
