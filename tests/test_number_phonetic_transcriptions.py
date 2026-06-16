from __future__ import annotations

import copy
import copy
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import number_phonetic_transcriptions  # noqa: E402


class NumberPhoneticTranscriptionsTests(unittest.TestCase):
    def make_entry(self, entry_id: str, root: str) -> dict:
        return {
            "id": entry_id,
            "packet_kind": "missing_series",
            "schuessler": {
                "rhyme_section": int(entry_id.split("-")[0]),
                "series_number": int(entry_id.split("-")[1]),
            },
            "resolved_series_root": {
                "root": root,
                "display_root": root,
                "character": entry_id,
            },
            "proposed_additions": [
                {
                    "character": entry_id,
                    "semantic_assignment": {
                        "abbreviation": None,
                        "position": "none",
                    },
                    "mc_resolution": {"display_forms": ["ka"]},
                    "mand2mc_rows": [],
                    "bs_gsr_rows": [],
                    "render_latex": None,
                    "transliteration_latex": None,
                    "hierarchy_assignment": {"status": "assigned-to-top-level", "parent_character": entry_id},
                }
            ],
        }

    def test_split_and_format_root_ordinals(self) -> None:
        self.assertEqual(number_phonetic_transcriptions.split_root_ordinal("ka"), ("ka", 1))
        self.assertEqual(
            number_phonetic_transcriptions.split_root_ordinal(r"k\textoverset{a}{a}₂"),
            (r"k\textoverset{a}{a}", 2),
        )
        self.assertEqual(number_phonetic_transcriptions.format_root_ordinal("ka", 1), "ka")
        self.assertEqual(number_phonetic_transcriptions.format_root_ordinal("ka", 4), "ka₄")

    def test_document_wide_numbering_assigns_consecutive_duplicates(self) -> None:
        entries = [
            self.make_entry("02-01", "ka"),
            self.make_entry("03-01", "ko"),
            self.make_entry("04-01", "ka"),
        ]
        summary = number_phonetic_transcriptions.apply_numbering(entries)
        self.assertEqual(entries[0]["resolved_series_root"]["display_root"], "ka")
        self.assertEqual(entries[1]["resolved_series_root"]["display_root"], "ko")
        self.assertEqual(entries[2]["resolved_series_root"]["display_root"], "ka₂")
        self.assertEqual(summary["duplicate_roots"]["ka"], 2)

    def test_numbering_recalculates_when_earlier_duplicate_is_inserted(self) -> None:
        base_entries = [
            self.make_entry("02-01", "ka"),
            self.make_entry("04-01", "ka"),
        ]
        number_phonetic_transcriptions.apply_numbering(base_entries)
        self.assertEqual(base_entries[1]["resolved_series_root"]["display_root"], "ka₂")

        inserted_entries = [
            self.make_entry("01-01", "ka"),
            self.make_entry("02-01", "ka"),
            self.make_entry("04-01", "ka"),
        ]
        number_phonetic_transcriptions.apply_numbering(inserted_entries)
        self.assertEqual(inserted_entries[0]["resolved_series_root"]["display_root"], "ka")
        self.assertEqual(inserted_entries[1]["resolved_series_root"]["display_root"], "ka₂")
        self.assertEqual(inserted_entries[2]["resolved_series_root"]["display_root"], "ka₃")

    def test_numbering_updates_descendant_transliteration_from_numbered_parent(self) -> None:
        entry = self.make_entry("02-01", "ka")
        child = {
            "character": "客",
            "semantic_assignment": {"abbreviation": "tect", "position": "prefix-colon"},
            "mc_resolution": {"display_forms": ["khaek"]},
            "mand2mc_rows": [],
            "bs_gsr_rows": [],
            "render_latex": None,
            "transliteration_latex": None,
            "hierarchy_assignment": {"status": "assigned-to-top-level", "parent_character": "02-01"},
            "resolved_node_root": {"root": "ka", "display_root": "ka"},
        }
        later_entry = self.make_entry("03-01", "ka")
        later_entry["proposed_additions"].append(child)
        number_phonetic_transcriptions.apply_numbering([entry, later_entry])
        self.assertEqual(later_entry["resolved_series_root"]["display_root"], "ka₂")
        self.assertIn("ka₂", child["transliteration_latex"])

    def test_current_generated_root_labels_are_unique(self) -> None:
        entries = copy.deepcopy(number_phonetic_transcriptions.load_entries(ROOT / "data/entries/curation"))
        number_phonetic_transcriptions.apply_numbering(entries)
        seen: set[str] = set()
        duplicates: set[str] = set()
        for occurrence in number_phonetic_transcriptions.iter_document_root_occurrences(entries):
            if not occurrence["mutable"]:
                continue
            root = occurrence["root_data"].get("display_root") or occurrence["root_data"].get("root")
            if root in seen:
                duplicates.add(root)
            seen.add(root)
        self.assertFalse(duplicates)


if __name__ == "__main__":
    unittest.main()
