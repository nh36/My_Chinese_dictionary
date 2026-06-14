from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import extract_semantic_components  # noqa: E402


SAMPLE_TEX = r"""
\section{Semantic components}
\begin{itemize}[noitemsep]
\item 黹 acu(laria)
\item 尚
%(shàng) -
adhuc
%(still)
\item \symbol{"268DE}
barbil(ia)
\end{itemize}
\section{The dictionary itself}
""".strip()


class ExtractSemanticComponentsTests(unittest.TestCase):
    def test_build_inventory(self) -> None:
        inventory = extract_semantic_components.build_inventory(SAMPLE_TEX, "sample.tex")

        self.assertEqual(inventory["summary"]["item_count"], 3)
        self.assertEqual(inventory["items"][0]["abbreviation"], "acu")
        self.assertEqual(inventory["items"][1]["abbreviation"], "adhuc")
        self.assertEqual(inventory["items"][2]["graph_raw"], r'\symbol{"268DE}')
        self.assertEqual(inventory["summary"]["unresolved_item_count"], 0)

    def test_write_outputs(self) -> None:
        inventory = extract_semantic_components.build_inventory(SAMPLE_TEX, "sample.tex")
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            json_path = temp_path / "semantic.json"
            report_path = temp_path / "semantic.md"
            extract_semantic_components.write_outputs(inventory, json_path, report_path)
            written = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(written["summary"]["item_count"], 3)
            self.assertIn("# Semantic components inventory", report_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
