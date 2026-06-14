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
        self.assertIn("\\begin{multicols}{2}", rendered)
        self.assertIn("\\textsuperscript{arb·}kay", rendered)
        self.assertIn("\\textit{kak};", rendered)

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
            self.assertIn("\\section*{Curated pilot series in comparable format}", doc)
            self.assertIn("\\end{document}", doc)


if __name__ == "__main__":
    unittest.main()
