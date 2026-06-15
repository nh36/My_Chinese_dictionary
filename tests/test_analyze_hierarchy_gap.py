from __future__ import annotations

import sys
import unittest


ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import analyze_hierarchy_gap  # noqa: E402


class AnalyzeHierarchyGapTests(unittest.TestCase):
    def test_extract_intermediate_nodes(self) -> None:
        raw = r"""
\paragraph{\textoversetlarge{01-67}{\huge{父}}}
\begin{itemize}[noitemsep]
\item {\Large{布}}
{\large{pa{\textsuperscript{:lint}}}} = {\large{p\textoverset{a}{a}}},
\textit{puH};
\item {\Large{甫}}
{\large{pa{\textsuperscript{:ager}}}} = {\large{pa₂}},
\textit{piuX};
\end{itemize}
""".strip()
        nodes = analyze_hierarchy_gap.extract_intermediate_nodes(raw)
        self.assertEqual(len(nodes), 2)
        self.assertIn("布", nodes[0]["character_line"])
        self.assertIn("甫", nodes[1]["character_line"])

    def test_render_report_handles_missing_packet(self) -> None:
        entry = {
            "id": "18-01",
            "raw_block": r"\item {\Large{何}} = {\large{g\textoverset{a}{a}y}},",
            "itemize": {"max_depth": 1},
        }
        report = analyze_hierarchy_gap.render_report(
            ["18-01"],
            {"18-01": entry},
            {"18-01": None},
        )
        self.assertIn("Current packet available for direct comparison: no", report)
        self.assertIn("not yet represented by a packet file", report)

    def test_extract_intermediate_nodes_ignores_image_width_equals(self) -> None:
        raw = r"""
\item {\Large{布}}({\includegraphics[width=5mm]{布.png}})
{\large{pa{\textsuperscript{:lint}}}} = {\large{p\textoverset{a}{a}}},
\textit{puH};
""".strip()
        nodes = analyze_hierarchy_gap.extract_intermediate_nodes(raw)
        self.assertEqual(nodes[0]["rhs_snippet"], r"{\large{p\textoverset{a}{a}}},")


if __name__ == "__main__":
    unittest.main()
