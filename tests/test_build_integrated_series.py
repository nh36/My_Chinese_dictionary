from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_integrated_series  # noqa: E402


class BuildIntegratedSeriesTests(unittest.TestCase):
    def test_normalize_raw_block_ignores_trailing_space(self) -> None:
        self.assertEqual(
            build_integrated_series.normalize_raw_block("a  \n b\t\n"),
            "a\n b",
        )

    def test_build_record_marks_generated_missing_series(self) -> None:
        record = build_integrated_series.build_record(
            "02-01",
            None,
            None,
            {"id": "02-01", "packet_kind": "missing_series", "status": "machine-curated-pilot"},
            ROOT / "key references/My_Chinese_dictionary/main.tex",
        )
        self.assertEqual(record["render_mode"], "generated_missing_series")
        self.assertIn("generated_candidate", record["status_flags"])
        self.assertIn("normalized_notes", record)
        self.assertIn("note_summary", record)


if __name__ == "__main__":
    unittest.main()
