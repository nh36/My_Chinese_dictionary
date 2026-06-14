from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_tex_reports  # noqa: E402


SAMPLE_ENTRIES = {
    "entries": [
        {
            "id": "18-01",
            "subsection": "-ay",
            "start_line": 10,
            "end_line": 20,
            "head": {"raw": "\\huge{可}", "image_refs": []},
            "raw_body": "{\\large{\\textsuperscript{hom·}qay}} {\\large{qay\\textsuperscript{·dehab}}}",
            "gsr_markers": ["0001a", "0001f"],
            "mc_forms": ["khaX"],
            "commented_pinyin": ["ke3"],
            "image_refs": [],
        },
        {
            "id": "01-67",
            "subsection": "-a",
            "start_line": 30,
            "end_line": 40,
            "head": {"raw": "\\huge{父}", "image_refs": ["父.png"]},
            "raw_body": "{\\huge{(}}{\\includegraphics[width=6mm]{父.png}}{\\huge{)}} {\\large{pa\\textsuperscript{:met}}}",
            "gsr_markers": [],
            "mc_forms": ["biuX"],
            "commented_pinyin": ["fu4"],
            "image_refs": ["父.png"],
        },
    ]
}


class BuildTexReportsTests(unittest.TestCase):
    def test_classify_label(self) -> None:
        self.assertEqual(build_tex_reports.classify_label("hom·"), "prefix-dot")
        self.assertEqual(build_tex_reports.classify_label("bamb:"), "prefix-colon")
        self.assertEqual(build_tex_reports.classify_label("·dehab"), "suffix-dot")
        self.assertEqual(build_tex_reports.classify_label(":met"), "suffix-colon")
        self.assertEqual(build_tex_reports.classify_label("claχ"), "bare")

    def test_render_reports(self) -> None:
        by_gsr = build_tex_reports.render_tex_entries_by_gsr(SAMPLE_ENTRIES)
        without_gsr = build_tex_reports.render_tex_entries_without_gsr(SAMPLE_ENTRIES)
        rare = build_tex_reports.render_rare_glyphs_report(
            SAMPLE_ENTRIES, Path("/tmp/nonexistent-assets")
        )
        labels = build_tex_reports.render_semantic_labels_report(SAMPLE_ENTRIES)

        self.assertIn("# TeX entries by GSR", by_gsr)
        self.assertIn("`0001a`", by_gsr)
        self.assertIn("`01-67`", without_gsr)
        self.assertIn("`父.png`", rare)
        self.assertIn("`hom·`", labels)
        self.assertIn("`·dehab`", labels)
        self.assertIn("`:met`", labels)

    def test_build_reports_writes_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            reports_dir = temp_path / "reports"
            assets_dir = temp_path / "assets"
            assets_dir.mkdir()
            (assets_dir / "父.png").write_bytes(b"")
            (assets_dir / "unused.png").write_bytes(b"")

            build_tex_reports.build_reports(SAMPLE_ENTRIES, reports_dir, assets_dir)

            self.assertTrue((reports_dir / "tex_entries_by_gsr.md").exists())
            self.assertTrue((reports_dir / "tex_entries_without_gsr.md").exists())
            self.assertTrue((reports_dir / "rare_glyphs_and_images.md").exists())
            self.assertTrue((reports_dir / "semantic_labels_used_in_tex.md").exists())


if __name__ == "__main__":
    unittest.main()
