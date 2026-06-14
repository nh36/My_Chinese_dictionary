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
            "proposed_additions": [{"character": "各", "mand2mc_count": 2, "bs_gsr_count": 1, "shengfu_character_count": 0}],
        }
        rendered = render_curated_series.render_curated_entry(entry)
        self.assertIn("\\section*{02-01 candidate packet}", rendered)
        self.assertIn("\\item 各", rendered)

    def test_render_document(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            main_tex = Path(temp_dir) / "main.tex"
            main_tex.write_text("\\documentclass{article}\n\\begin{document}\n\\end{document}\n", encoding="utf-8")
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
            )
            self.assertIn("\\section*{Curated pilot series packets}", doc)
            self.assertIn("\\end{document}", doc)


if __name__ == "__main__":
    unittest.main()
