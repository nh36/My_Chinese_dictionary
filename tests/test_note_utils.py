from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import note_utils  # noqa: E402


class NoteUtilsTests(unittest.TestCase):
    def test_extract_footnotes_from_hand_entry(self) -> None:
        raw_block = (
            "\\paragraph{X}\n"
            "野\\footnote{I need to look into this relationship more.}\n"
            "{\\large{la}},\n"
        )
        notes = note_utils.extract_footnotes_from_hand_entry("01-43", raw_block, 100)
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]["entry_id"], "01-43")
        self.assertEqual(notes[0]["source_layer"], "hand_footnote")
        self.assertEqual(notes[0]["anchor_kind"], "character")
        self.assertIn("look into this relationship", notes[0]["text"])
        self.assertEqual(notes[0]["recommended_rendering"], "footnote")

    def test_extract_visible_prose_notes_from_hand_entry(self) -> None:
        raw_block = (
            "\\paragraph{X}\n"
            "{\\large{tsa}},\n"
            "I do not see how ka and kua can mix in one XS series.\n"
            "Probably better to use y- to be agnostic.\n"
            "\\textit{ka};\n"
        )
        notes = note_utils.extract_visible_prose_notes_from_hand_entry("01-19", raw_block, 200)
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]["source_layer"], "hand_prose_note")
        self.assertEqual(notes[0]["anchor_kind"], "series")
        self.assertEqual(notes[0]["recommended_rendering"], "series_end_note")
        self.assertIn("ka and kua", notes[0]["text"])

    def test_collect_curation_notes_includes_internal_semantic_review(self) -> None:
        curated_entry = {
            "notes": ["Machine-promoted from a series packet; not yet hand-checked."],
            "resolved_series_root": {"division_note": "top-level series head left unmarked", "character": "蜀"},
            "proposed_additions": [
                {
                    "character": "磔",
                    "semantic_assignment_review": {
                        "status": "nonlatin_generated_semantic_suppressed",
                        "original_abbreviation": "桀",
                        "semantic_component": "桀",
                        "original_source": "ids_component_literal_fallback",
                    },
                    "semantic_assignment": {
                        "research_note": "Chinese sources support 言 semantic + 㠩 phonetic."
                    },
                    "mc_resolution": {"needs_investigation": True, "bs_not_in_mand2mc": ["triak"]},
                    "resolved_node_root": {"division_note": "top-level series head left unmarked"},
                }
            ],
        }
        notes = note_utils.collect_curation_notes(curated_entry, "02-17")
        source_layers = {note["source_layer"] for note in notes}
        self.assertIn("curation_entry_note", source_layers)
        self.assertIn("curation_semantic_review", source_layers)
        self.assertIn("curation_research_note", source_layers)
        self.assertIn("curation_mc_investigation", source_layers)
        self.assertIn("curation_division_note", source_layers)


if __name__ == "__main__":
    unittest.main()
