from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import render_entries  # noqa: E402


SAMPLE_PAYLOAD = {
    "entries": [
        {"id": "18-01", "raw_latex": "\\paragraph{\\textoversetlarge{18-01}{\\huge{可}}}\n{\\Large{qay}},", "head": {"characters": ["可"]}, "context_environments": []},
        {"id": "19-18", "raw_latex": "\\paragraph{\\textoversetlarge{19-18}{\\includegraphics[width=9mm]{U+26760.png}}}", "head": {"characters": []}, "context_environments": [{"name":"multicols","arg":"2"},{"name":"spacing","arg":"0.7"}]},
    ]
}


class RenderEntriesTests(unittest.TestCase):
    def test_render_entries_tex_adds_warning_header(self) -> None:
        rendered = render_entries.render_entries_tex(SAMPLE_PAYLOAD["entries"])
        self.assertIn("% GENERATED FILE - DO NOT EDIT BY HAND.", rendered)
        self.assertIn("% Entry 18-01", rendered)
        self.assertIn("\\paragraph{\\textoversetlarge{19-18}", rendered)
        self.assertIn("\\begin{multicols}{2}", rendered)
        self.assertIn("\\end{spacing}", rendered)

    def test_render_main_sample_uses_preamble(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            main_tex = Path(temp_dir) / "main.tex"
            main_tex.write_text(
                "\\documentclass{article}\n\\newcommand{\\foo}{bar}\n\\begin{document}\nOriginal\n\\end{document}\n",
                encoding="utf-8",
            )
            rendered = render_entries.render_main_sample(SAMPLE_PAYLOAD["entries"], main_tex)

            self.assertTrue(rendered.startswith("\\documentclass{article}"))
            self.assertIn("\\section*{Generated sample entries}", rendered)
            self.assertIn("\\end{document}", rendered)

    def test_load_and_write_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            sample_path = temp_path / "sample_entries.json"
            sample_path.write_text(json.dumps(SAMPLE_PAYLOAD), encoding="utf-8")
            entries = render_entries.load_sample_entries(sample_path)

            output_path = temp_path / "generated_entries_sample.tex"
            main_output_path = temp_path / "generated_main_sample.tex"
            render_entries.write_output(output_path, render_entries.render_entries_tex(entries))
            main_tex = temp_path / "main.tex"
            main_tex.write_text("\\documentclass{article}\n\\begin{document}\n\\end{document}\n", encoding="utf-8")
            render_entries.write_output(
                main_output_path,
                render_entries.render_main_sample(entries, main_tex),
            )

            self.assertTrue(output_path.exists())
            self.assertTrue(main_output_path.exists())

    def test_render_comparison_report(self) -> None:
        entries = [
            {
                "id": "18-01",
                "section": "The dictionary itself",
                "subsection": "-ay",
                "source": {"tex_start_line": 10, "tex_end_line": 20},
                "head": {"type": "character"},
                "raw_latex": "x",
            }
        ]
        report = render_entries.render_comparison_report(
            entries,
            Path("data/entries/sample_entries.json"),
            Path("build/generated_entries_sample.tex"),
            Path("build/generated_main_sample.tex"),
        )
        self.assertIn("# Generated sample comparison", report)
        self.assertIn("outer environment wrappers", report)
        self.assertIn("`18-01`", report)


if __name__ == "__main__":
    unittest.main()
