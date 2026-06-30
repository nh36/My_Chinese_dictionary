from __future__ import annotations

import re
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import number_phonetic_transcriptions  # noqa: E402
import render_curated_series  # noqa: E402


class RenderCuratedSeriesTests(unittest.TestCase):
    def make_missing_entry(
        self,
        entry_id: str,
        *,
        heading_character: str,
        subsection: str | None = None,
        root: str = "ka",
        display_root: str | None = None,
    ) -> dict:
        left, right = entry_id.split("-", 1)
        entry = {
            "id": entry_id,
            "packet_kind": "missing_series",
            "schuessler": {
                "rhyme_section": int(left),
                "series_number": int(right),
            },
            "coverage": {
                "rhyme_section": left,
            },
            "tex_entry": {"subsection": subsection} if subsection is not None else None,
            "resolved_series_root": {
                "root": root,
                "display_root": display_root or root,
                "character": heading_character,
                "source": "head_graph_supplement",
            },
            "proposed_additions": [],
        }
        return entry

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
        self.assertNotIn("\\begin{multicols}{2}", rendered)
        self.assertIn("\\textit{kak};", rendered)

    def test_render_existing_addendum_entry_does_not_repeat_heading(self) -> None:
        entry = {
            "id": "01-42",
            "packet_kind": "existing_addendum",
            "tex_entry": {
                "head": {"raw": r"\huge{余}"},
                "raw_block": "\\paragraph{\\textoversetlarge{01-42}{\\huge{余}}}\n{\\large{la}},\n\\textit{yiə};\n",
            },
            "entry_hierarchy": {"nodes": []},
            "proposed_additions": [
                {
                    "character": "敘",
                    "mand2mc_rows": [{"pinyin": "xu4", "gsr": "0082o"}],
                    "bs_gsr_rows": [],
                    "mc_resolution": {"display_forms": ["ziəX"]},
                    "transliteration_latex": r"{\large{la\textsuperscript{·fer}}},",
                    "hierarchy_assignment": {"status": "assigned-to-top-level"},
                }
            ],
        }

        rendered = render_curated_series.render_curated_entry(entry)

        self.assertEqual(rendered.count(r"\paragraph{\textoversetlarge{01-42}{\huge{余}}}"), 1)
        self.assertIn("% Proposed additions from imported sources for 01-42", rendered)
        self.assertIn("敘\t%xu4", rendered)

    def test_group_entries_by_rhyme_section_follows_schuessler_order(self) -> None:
        entries = [
            self.make_missing_entry("02-03", heading_character="乙"),
            self.make_missing_entry("01-02", heading_character="甲"),
            self.make_missing_entry("02-01", heading_character="丙"),
        ]
        groups = render_curated_series.group_entries_by_rhyme_section(entries)

        self.assertEqual([group[0] for group in groups], [1, 2])
        self.assertEqual([entry["id"] for entry in groups[0][1]], ["01-02"])
        self.assertEqual([entry["id"] for entry in groups[1][1]], ["02-01", "02-03"])

    def test_format_rhyme_section_heading_prefers_subsection_hint(self) -> None:
        heading = render_curated_series.format_rhyme_section_heading(
            1,
            [
                self.make_missing_entry("01-01", heading_character="甲", subsection="-a"),
                self.make_missing_entry("01-02", heading_character="乙", subsection="-a"),
                self.make_missing_entry("01-03", heading_character="丙", subsection="-ay"),
            ],
        )
        self.assertEqual(heading, "01. -a")
        section_two_heading = render_curated_series.format_rhyme_section_heading(
            2,
            [self.make_missing_entry("02-01", heading_character="丁")],
        )
        self.assertRegex(section_two_heading, r"^02\. .+")
        self.assertNotEqual(section_two_heading, "02")

    def test_render_document(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            main_tex = Path(temp_dir) / "main.tex"
            main_tex.write_text("\\documentclass{article}\n\\begin{document}\n\\end{document}\n", encoding="utf-8")
            semantic_data = {
                "items": [
                    {
                        "graph_raw": "木",
                        "abbreviation": "arb",
                        "expanded_latin": "arb(or)",
                        "notes": "(only in test)",
                        "comments": ["(mù)", "(tree)"],
                        "used_abbreviation_aliases": ["arb"],
                    }
                ]
            }
            entries = [
                self.make_missing_entry("02-01", heading_character="乙"),
                self.make_missing_entry("01-01", heading_character="甲", subsection="-a"),
            ]
            doc = render_curated_series.render_document(
                entries,
                main_tex,
                semantic_data,
            )
            self.assertIn(r"\item 木 \textbf{arb} arb(or) --- (only in test)", doc)
            self.assertNotIn("(mù)", doc)
            self.assertNotIn("(tree)", doc)
            self.assertNotIn("entry aliases", doc)
            self.assertIn(r"\begin{titlepage}", doc)
            self.assertIn("A Chinese Historical Phonology Dictionary", doc)
            self.assertIn("Curated Schuessler Series with Old Chinese Reconstructions", doc)
            self.assertIn(r"\section*{\centering Introduction}", doc)
            self.assertIn(r"\section*{\centering Semantic Component Abbreviations}", doc)
            self.assertIn(r"\section*{\centering Schuessler Series}", doc)
            self.assertIn(r"\section*{\centering 01. -a}", doc)
            self.assertRegex(doc, r"\\section\*\{\\centering 02\. .+\}")
            self.assertNotIn("Chapter", doc)
            self.assertNotIn(r"\chapter", doc)
            self.assertNotIn(r"\section*{Curated pilot series in comparable format}", doc)
            self.assertIn(r"\lehead{\small Chinese Historical Phonology Dictionary}", doc)
            self.assertIn(r"\rohead{\small \rightmark}", doc)
            self.assertEqual(doc.count(r"\ifodd\value{page}\else"), 2)
            self.assertEqual(doc.count(r"\begin{multicols*}{2}"), 3)
            self.assertEqual(doc.count(r"\end{multicols*}"), 3)
            self.assertRegex(
                doc,
                re.compile(
                    r"\\ifodd\\value\{page\}\\else\s+\\thispagestyle\{empty\}\s+\\null\s+\\clearpage\s+\\fi\s+\\section\*\{\\centering 01\. -a\}",
                    re.MULTILINE,
                ),
            )
            self.assertRegex(
                doc,
                re.compile(
                    r"\\ifodd\\value\{page\}\\else\s+\\thispagestyle\{empty\}\s+\\null\s+\\clearpage\s+\\fi\s+\\section\*\{\\centering 02\. .+\}",
                    re.MULTILINE,
                ),
            )
            self.assertLess(doc.index(r"\section*{\centering 01. -a}"), doc.index(r"\section*{\centering 02. "))
            self.assertNotRegex(doc, r"\\section\*\{\\centering \d{2}\}")
            self.assertIn("\\end{document}", doc)

    def test_render_document_preserves_global_root_numbering_across_sections(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            main_tex = Path(temp_dir) / "main.tex"
            main_tex.write_text("\\documentclass{article}\n\\begin{document}\n\\end{document}\n", encoding="utf-8")
            entries = [
                self.make_missing_entry("01-01", heading_character="甲", root="ka"),
                self.make_missing_entry("02-01", heading_character="乙", root="ka"),
            ]
            number_phonetic_transcriptions.apply_numbering(entries)
            doc = render_curated_series.render_document(
                entries,
                main_tex,
                semantic_data=None,
            )

            self.assertRegex(
                doc,
                re.compile(r"\\paragraph\{\\textoversetlarge\{01-01\}\{\\huge\{甲\}\}\}\n\{\\large\{ka\}\},"),
            )
            self.assertRegex(
                doc,
                re.compile(r"\\paragraph\{\\textoversetlarge\{02-01\}\{\\huge\{乙\}\}\}\n\{\\large\{ka₂\}\},"),
            )

    def test_render_report_documents_rhyme_heading_policy(self) -> None:
        entries = [
            self.make_missing_entry("01-01", heading_character="甲", subsection="-a"),
            self.make_missing_entry("02-01", heading_character="乙"),
        ]
        report = render_curated_series.render_report(entries, Path("build/generated_curated_series_sample.tex"))
        self.assertIn("Sections with direct `tex_entry.subsection` hints", report)
        self.assertIn("| `01` | `01. -a` | 1 | `-a` | `tex_subsection` |", report)
        self.assertRegex(report, r"\| `02` \| `02\. .+` \| 1 \| `.+` \| `schuessler_heading_hint` \|")

    def test_default_ids_are_unique(self) -> None:
        self.assertEqual(len(render_curated_series.DEFAULT_IDS), len(set(render_curated_series.DEFAULT_IDS)))


if __name__ == "__main__":
    unittest.main()
