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

    def make_integrated_record(self, entry_id: str, *, render_mode: str, preferred_hand_entry: dict | None = None) -> dict:
        left, right = entry_id.split("-")
        return {
            "id": entry_id,
            "render_mode": render_mode,
            "schuessler": {
                "rhyme_section": int(left),
                "series_number": int(right),
            },
            "preferred_hand_entry": preferred_hand_entry,
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

    def test_integrated_order_counts_hand_baseline_before_generated_duplicate(self) -> None:
        generated = self.make_entry("02-17", "tak")
        integrated_records = [
            self.make_integrated_record(
                "01-38",
                render_mode="hand_only",
                preferred_hand_entry={
                    "head": {"characters": ["著"]},
                    "raw_block": "\\paragraph{X}\n{\\large{ta}},\n\\begin{itemize}[noitemsep]\n\\item {\\Large{著}} = {\\large{tak}},\n\\textit{tśiok};\n\\end{itemize}\n",
                },
            ),
            self.make_integrated_record("02-17", render_mode="generated_missing_series"),
        ]

        summary = number_phonetic_transcriptions.apply_numbering(
            [generated],
            integrated_records=integrated_records,
        )

        self.assertEqual(generated["resolved_series_root"]["display_root"], "tak₂")
        self.assertEqual(summary["order_source"], "integrated_render_order")

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

    def test_mutable_subseries_root_occurrences_deduplicate_nested_head_children(self) -> None:
        entry = {
            "id": "13-01",
            "packet_kind": "missing_series",
            "proposed_additions": [
                {"character": "A"},
                {
                    "character": "B",
                    "hierarchy_assignment": {"status": "assigned-to-candidate-node", "parent_character": "A"},
                    "resolved_node_root": {"root": "ka", "display_root": "ka"},
                },
                {
                    "character": "C",
                    "hierarchy_assignment": {"status": "assigned-to-candidate-node", "parent_character": "B"},
                    "resolved_node_root": {"root": "ka", "display_root": "ka₂"},
                },
                {
                    "character": "D",
                    "hierarchy_assignment": {"status": "assigned-to-candidate-node", "parent_character": "A"},
                },
                {
                    "character": "E",
                    "hierarchy_assignment": {"status": "assigned-to-candidate-node", "parent_character": "C"},
                },
            ],
        }
        occurrences = number_phonetic_transcriptions.mutable_subseries_root_occurrences(entry)
        self.assertEqual(
            [occurrence["character"] for occurrence in occurrences],
            ["B", "C"],
        )

    def test_current_generated_root_labels_are_unique(self) -> None:
        entries = copy.deepcopy(number_phonetic_transcriptions.load_entries(ROOT / "data/entries/curation"))
        integrated_records = number_phonetic_transcriptions.load_integrated_records(
            ROOT / "data/entries/integrated_series"
        )
        summary = number_phonetic_transcriptions.apply_numbering(
            entries,
            integrated_records=integrated_records,
        )
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
        self.assertEqual(summary["order_source"], "integrated_render_order")

    def test_current_integrated_order_has_no_numbering_mismatches(self) -> None:
        entries = copy.deepcopy(number_phonetic_transcriptions.load_entries(ROOT / "data/entries/curation"))
        integrated_records = number_phonetic_transcriptions.load_integrated_records(
            ROOT / "data/entries/integrated_series"
        )
        number_phonetic_transcriptions.apply_numbering(entries, integrated_records=integrated_records)
        counters: dict[str, int] = {}
        mismatches = []
        for occurrence in number_phonetic_transcriptions.iter_integrated_document_root_occurrences(
            entries,
            integrated_records,
        ):
            base_root, existing_ordinal = number_phonetic_transcriptions.split_root_ordinal(
                occurrence["current_root"]
            )
            if not base_root:
                continue
            next_count = counters.get(base_root, 0) + 1
            if occurrence["mutable"]:
                current_display = occurrence["root_data"].get("display_root") or occurrence["root_data"].get("root")
                expected_display = number_phonetic_transcriptions.format_root_ordinal(base_root, next_count)
                counters[base_root] = next_count
                if current_display != expected_display:
                    mismatches.append((occurrence["entry_id"], occurrence["character"], current_display, expected_display))
            else:
                counters[base_root] = max(next_count, existing_ordinal)
        self.assertEqual(mismatches, [])


if __name__ == "__main__":
    unittest.main()
