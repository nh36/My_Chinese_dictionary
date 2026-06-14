from __future__ import annotations

import sys
import unittest
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import import_shengfu  # noqa: E402


class ImportShengfuTests(unittest.TestCase):
    def test_transform_shengfu_adds_normalized_columns(self) -> None:
        frame = pd.DataFrame(
            {
                "source_row_number": [2, 3],
                "source_sheet_name": ["Sheet1", "Sheet1"],
                "字": [" 可 ", "阿"],
                "声符": ["丁 ", "可"],
                "声符级别": ["A", "B"],
                "次級聲符": [None, "口"],
                "反切": ["苦我切", None],
                "来源": ["test", "source"],
                "上古声": ["k", None],
                "上古韵": ["a", None],
                "上古音节": ["ka", None],
            }
        )

        transformed = import_shengfu.transform_shengfu(frame)

        self.assertEqual(transformed["normalized_character"].tolist(), ["可", "阿"])
        self.assertEqual(transformed["normalized_phonetic_component"].tolist(), ["丁", "可"])
        self.assertEqual(transformed["normalized_component_level"].tolist(), ["A", "B"])
        self.assertEqual(transformed["normalized_secondary_component"].tolist(), [None, "口"])
        self.assertEqual(transformed["normalized_fanqie"].tolist(), ["苦我切", None])
        self.assertEqual(transformed["normalized_source"].tolist(), ["test", "source"])
        self.assertEqual(transformed["normalized_oc_initial"].tolist(), ["k", None])
        self.assertEqual(transformed["normalized_oc_rhyme"].tolist(), ["a", None])
        self.assertEqual(transformed["normalized_oc_syllable"].tolist(), ["ka", None])

    def test_render_report_mentions_sheet_summary(self) -> None:
        frame = pd.DataFrame(
            {
                "source_row_number": [2],
                "source_sheet_name": ["Sheet1"],
                "normalized_character": ["可"],
                "normalized_phonetic_component": ["丁"],
                "normalized_component_level": ["A"],
                "normalized_secondary_component": [None],
                "normalized_fanqie": ["苦我切"],
                "normalized_source": ["test"],
                "normalized_oc_initial": ["k"],
                "normalized_oc_rhyme": ["a"],
                "normalized_oc_syllable": ["ka"],
            }
        )
        report = import_shengfu.render_report(
            source_path=Path("声符级别-2022.06.07.xlsx"),
            source_sheet_name="Sheet1",
            transformed_frame=frame,
            raw_columns=["字", "声符", "声符级别"],
            sheet_summaries=[{"sheet_name": "Sheet1", "data_row_count": 1, "column_count": 3}],
        )

        self.assertIn("# Shengfu import report", report)
        self.assertIn("`Sheet1`", report)
        self.assertIn("normalized_phonetic_component", report)


if __name__ == "__main__":
    unittest.main()
