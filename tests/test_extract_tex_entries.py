from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import extract_tex_entries  # noqa: E402


SAMPLE_TEX = r"""
\section{The dictionary itself}
\subsection{-ay}
\paragraph{\textoversetlarge{18-01}{\huge{可}}}
{\Large{qay}},
\textit{khaX};	%0001a
\begin{itemize}[noitemsep]
\item {\Large{何}} \textit{ḫa};	%0001f
\item {\includegraphics[width=5mm]{U+26760.png}}
\end{itemize}
\paragraph{\textoversetlarge{01-67}{\huge{父}}}{\huge{(}}{\includegraphics[width=6mm]{父.png}}{\huge{)}}
{\large{pa}},
\textit{biuX};	%0102a
""".strip()


class ExtractTexEntriesTests(unittest.TestCase):
    def test_extract_entries_from_sample(self) -> None:
        entries_data = extract_tex_entries.extract_entries(SAMPLE_TEX, source_path="sample.tex")

        self.assertEqual(entries_data["entry_count"], 2)

        first_entry = entries_data["entries"][0]
        second_entry = entries_data["entries"][1]

        self.assertEqual(first_entry["id"], "18-01")
        self.assertEqual(first_entry["head"]["type"], "character")
        self.assertEqual(first_entry["itemize"]["max_depth"], 1)
        self.assertEqual(first_entry["itemize"]["events"][0]["kind"], "begin")
        self.assertIn("\\textit{khaX}", first_entry["raw_block"])
        self.assertIn("{\\Large{qay}},", first_entry["raw_body"])
        self.assertEqual(first_entry["context_environments"], [])
        self.assertIn(chr(int("26760", 16)), first_entry["chinese_characters"])

        self.assertEqual(second_entry["id"], "01-67")
        self.assertEqual(second_entry["head"]["type"], "character_with_image")
        self.assertIn("父.png", second_entry["head"]["image_refs"])
        self.assertTrue(second_entry["raw_body"].startswith("{\\huge{(}}"))

    def test_write_entries(self) -> None:
        entries_data = extract_tex_entries.extract_entries(SAMPLE_TEX, source_path="sample.tex")

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "entries.json"
            extract_tex_entries.write_entries(entries_data, output_path)

            written_data = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(written_data["entry_count"], 2)
            self.assertEqual(written_data["entries"][1]["head"]["type"], "character_with_image")

    def test_entry_does_not_absorb_following_subsection_lines(self) -> None:
        sample = r"""
\section{The dictionary itself}
\subsection{-ay}
\paragraph{\textoversetlarge{18-01}{\huge{可}}}
\textit{khaX};	%0001a
\subsection{-a}
\paragraph{\textoversetlarge{01-01}{\huge{古}}}
\textit{kuX};	%0049a
""".strip()
        entries_data = extract_tex_entries.extract_entries(sample, source_path="sample.tex")

        self.assertEqual(entries_data["entries"][0]["id"], "18-01")
        self.assertNotIn("\\subsection{-a}", entries_data["entries"][0]["raw_block"])
        self.assertEqual(entries_data["entries"][1]["subsection"], "-a")


if __name__ == "__main__":
    unittest.main()
