from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import inventory_tex  # noqa: E402


SAMPLE_TEX = r"""
\section{Semantic components}
\section{The dictionary itself}
\subsection{-ay}
\paragraph{\textoversetlarge{18-01}{\huge{可}}}
%可	%ke3
{\Large{qay}},
\textit{khaX};	%0001a
\begin{itemize}[noitemsep]
\item {\Large{何}} {\large{\textsuperscript{hom·}qay}} = {\large{g\textoverset{a}{a}y}}, \textit{ḫa};	%0001f
\item {\includegraphics[width=5mm]{U+26760.png}}
\end{itemize}
\paragraph{\textoversetlarge{01-67}{\huge{父}}}{\huge{(}}{\includegraphics[width=6mm]{父.png}}{\huge{)}}
%父	%fu4
\textit{biuX};	%0102a
""".strip()


class InventoryTexTests(unittest.TestCase):
    def test_collect_inventory_from_sample(self) -> None:
        inventory = inventory_tex.collect_inventory(SAMPLE_TEX, source_path="sample.tex")

        self.assertEqual(inventory["summary"]["section_count"], 2)
        self.assertEqual(inventory["summary"]["subsection_count"], 1)
        self.assertEqual(inventory["summary"]["entry_count"], 2)
        self.assertEqual(inventory["summary"]["image_reference_count"], 2)
        self.assertEqual(inventory["summary"]["mc_form_count"], 3)
        self.assertEqual(inventory["summary"]["gsr_marker_count"], 3)
        self.assertEqual(inventory["summary"]["commented_pinyin_count"], 2)
        self.assertEqual(inventory["summary"]["entries_with_image_heads"], 1)

        first_entry = inventory["entries"][0]
        second_entry = inventory["entries"][1]

        self.assertEqual(first_entry["gsc_number"], "18-01")
        self.assertEqual(first_entry["subsection"], "-ay")
        self.assertEqual(first_entry["max_itemize_depth"], 1)
        self.assertIn("U+26760.png", first_entry["image_refs"])
        self.assertIn(chr(int("26760", 16)), first_entry["chinese_characters"])
        self.assertIn("khaX", first_entry["mc_forms"])
        self.assertIn("ke3", first_entry["commented_pinyin"])

        self.assertEqual(second_entry["gsc_number"], "01-67")
        self.assertTrue(second_entry["has_image_head"])
        self.assertIn("includegraphics", second_entry["heading_extra_raw"])
        self.assertIn("父.png", second_entry["image_refs"])

    def test_write_outputs(self) -> None:
        inventory = inventory_tex.collect_inventory(SAMPLE_TEX, source_path="sample.tex")

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            json_path = temp_path / "inventory.json"
            report_path = temp_path / "inventory.md"

            inventory_tex.write_outputs(inventory, json_path, report_path)

            written_inventory = json.loads(json_path.read_text(encoding="utf-8"))
            written_report = report_path.read_text(encoding="utf-8")

            self.assertEqual(written_inventory["source_path"], "sample.tex")
            self.assertIn("# Current TeX inventory", written_report)
            self.assertIn("| entry count | 2 |", written_report)


if __name__ == "__main__":
    unittest.main()
