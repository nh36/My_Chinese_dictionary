from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import render_ab_visual_mockup  # noqa: E402


class RenderAbVisualMockupTests(unittest.TestCase):
    def test_render_document_uses_requested_variant_and_snippets(self) -> None:
        source_text = (ROOT / "main.tex").read_text(encoding="utf-8")
        rendered = render_ab_visual_mockup.render_document(source_text, "overlay-balanced")

        self.assertIn(r"\renewcommand{\textoverset}[2]", rendered)
        self.assertIn(r"\texttt{18-01}", rendered)
        self.assertIn(r"\texttt{01-67}", rendered)
        self.assertIn(r"\paragraph{\textoversetlarge{18-01}{\huge{可}}}", rendered)
        self.assertIn(r"\paragraph{\textoversetlarge{01-67}{\huge{父}}}", rendered)
        self.assertIn(r"Variant under review: \texttt{overlay-balanced}.", rendered)


if __name__ == "__main__":
    unittest.main()
