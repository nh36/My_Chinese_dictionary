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

MAKEBOX_SAMPLE_TEX = r"""
\section{Semantic components}
\begin{multicols}{3}
\begin{itemize}[noitemsep]
\item 黃 \makebox[0pt][l]{galb(inus) (only in 黈?)}
\item 力 virt(us)
\end{itemize}
\end{multicols}
\section{The dictionary itself}
""".strip()

PAREN_LABEL_SAMPLE_TEX = r"""
\section{Semantic components}
\begin{itemize}[noitemsep]
\item 口 (os,) or(is)
\item 足 (pes,) ped(is)
\end{itemize}
\section{The dictionary itself}
""".strip()

SCOPED_DUPLICATE_SAMPLE_TEX = r"""
\section{Semantic components}
\begin{itemize}[noitemsep]
\item 田 forn(us) (only in 盧)
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

    def test_makebox_labels_and_structural_closers_parse_cleanly(self) -> None:
        inventory = extract_semantic_components.build_inventory(MAKEBOX_SAMPLE_TEX, "sample.tex")

        self.assertEqual(inventory["summary"]["item_count"], 2)
        self.assertEqual(inventory["items"][0]["graph_raw"], "黃")
        self.assertEqual(inventory["items"][0]["abbreviation"], "galb")
        self.assertEqual(inventory["items"][0]["label_token"], "galb(inus)")
        self.assertEqual(inventory["items"][0]["label_notes"], "(only in 黈?)")
        self.assertEqual(inventory["items"][1]["label_token"], "virt(us)")
        self.assertIsNone(inventory["items"][1]["label_notes"])
        self.assertNotIn(r"\end{itemize}", inventory["items"][1]["raw_latex"])

    def test_parenthetical_synonyms_use_later_label_stem_as_abbreviation(self) -> None:
        inventory = extract_semantic_components.build_inventory(PAREN_LABEL_SAMPLE_TEX, "sample.tex")

        self.assertEqual(inventory["items"][0]["abbreviation"], "or")
        self.assertEqual(inventory["items"][1]["abbreviation"], "ped")

    def test_scoped_duplicate_metadata_is_recorded(self) -> None:
        inventory = extract_semantic_components.build_inventory(SCOPED_DUPLICATE_SAMPLE_TEX, "sample.tex")

        self.assertEqual(inventory["items"][0]["scope"], "only_in")
        self.assertEqual(inventory["items"][0]["only_in"], ["盧"])
        self.assertEqual(inventory["items"][0]["duplicate_graph_status"], "intentional_scoped_duplicate")
        self.assertIn("Same visible graph as 田/ager", inventory["items"][0]["note"])


if __name__ == "__main__":
    unittest.main()
