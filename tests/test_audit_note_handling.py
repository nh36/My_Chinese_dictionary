from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import audit_note_handling  # noqa: E402


class AuditNoteHandlingTests(unittest.TestCase):
    def test_current_note_inventory_keeps_real_notes_and_skips_mc_line_noise(self) -> None:
        inventory = json.loads((ROOT / "data/derived/note_inventory.json").read_text(encoding="utf-8"))
        notes = inventory["notes"]

        self.assertTrue(
            any(
                note["entry_id"] == "18-03"
                and note["source_layer"] == "hand_prose_note"
                and "Baxter" in note["text"]
                for note in notes
            )
        )
        self.assertTrue(
            any(
                note["entry_id"] == "01-28"
                and note["source_layer"] == "hand_footnote"
                and note["recommended_rendering"] == "footnote"
                for note in notes
            )
        )
        self.assertFalse(
            any(
                note["entry_id"] == "10-19"
                and note["source_layer"] == "hand_prose_note"
                for note in notes
            )
        )

    def test_build_inventory_has_only_supported_rendering_policies(self) -> None:
        records = audit_note_handling.load_integrated_records(ROOT / "data/entries/integrated_series")
        inventory = audit_note_handling.build_inventory(records)
        rendering_policies = {note["recommended_rendering"] for note in inventory["notes"]}
        self.assertEqual(rendering_policies - {"footnote", "series_end_note", "internal_only"}, set())


if __name__ == "__main__":
    unittest.main()
