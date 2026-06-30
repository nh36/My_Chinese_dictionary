from __future__ import annotations

import os
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import open_review_pdf  # noqa: E402


class OpenReviewPdfTests(unittest.TestCase):
    def test_resolve_review_pdf_paths_uses_build_outputs(self) -> None:
        curated_tex, curated_pdf = open_review_pdf.resolve_review_pdf_paths(ROOT, "curated")
        integrated_tex, integrated_pdf = open_review_pdf.resolve_review_pdf_paths(ROOT, "integrated")

        self.assertEqual(curated_tex, ROOT / "build" / "generated_curated_series_sample.tex")
        self.assertEqual(curated_pdf, ROOT / "build" / "generated_curated_series_sample.pdf")
        self.assertEqual(integrated_tex, ROOT / "build" / "generated_integrated_dictionary.tex")
        self.assertEqual(integrated_pdf, ROOT / "build" / "generated_integrated_dictionary.pdf")

    def test_review_pdf_is_stale_only_when_pdf_is_missing_or_older(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            tex_path = tmp_path / "generated.tex"
            pdf_path = tmp_path / "generated.pdf"

            tex_path.write_text("tex", encoding="utf-8")
            now = time.time()
            os.utime(tex_path, (now, now))

            self.assertTrue(open_review_pdf.review_pdf_is_stale(tex_path, pdf_path))

            pdf_path.write_text("pdf", encoding="utf-8")
            os.utime(pdf_path, (now + 10, now + 10))
            self.assertFalse(open_review_pdf.review_pdf_is_stale(tex_path, pdf_path))

            os.utime(tex_path, (now + 20, now + 20))
            self.assertTrue(open_review_pdf.review_pdf_is_stale(tex_path, pdf_path))

    @patch("open_review_pdf.subprocess.run")
    def test_refresh_review_pdf_invokes_build_helper(self, run_mock: object) -> None:
        tex_path = ROOT / "build" / "generated_curated_series_sample.tex"

        open_review_pdf.refresh_review_pdf(ROOT, tex_path)

        run_mock.assert_called_once_with(
            [
                sys.executable,
                str(ROOT / "scripts" / "build_review_pdfs.py"),
                "--tex",
                "build/generated_curated_series_sample.tex",
            ],
            cwd=ROOT,
            check=True,
        )


if __name__ == "__main__":
    unittest.main()
