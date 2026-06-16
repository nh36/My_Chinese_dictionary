from __future__ import annotations

import sys
import unittest
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import import_mand2mc  # noqa: E402


class ImportMand2MCTests(unittest.TestCase):
    def test_transform_mand2mc_adds_normalized_columns(self) -> None:
        frame = pd.DataFrame(
            {
                "source_row_number": [2, 3],
                "source_sheet_name": ["Feuil1", "Feuil1"],
                "character": [" 可 ", "阿"],
                "pinyin": ["ke3", None],
                "MC (NWH)": [" khaX ", "ʔa"],
                "MC (B&S)": ["khaX", None],
                "GSR": ["0001a", None],
                "漢語大字典": ["12", None],
                "廣韻": ["甲", "乙"],
                "": [None, "note"],
            }
        )

        transformed = import_mand2mc.transform_mand2mc(frame)

        self.assertEqual(transformed["normalized_character"].tolist(), ["可", "阿"])
        self.assertEqual(transformed["normalized_pinyin"].tolist(), ["ke3", None])
        self.assertEqual(transformed["normalized_mc_nwh"].tolist(), ["khaX", "ʔa"])
        self.assertEqual(transformed["normalized_mc_bs"].tolist(), ["khaX", None])
        self.assertEqual(transformed["normalized_gsr"].tolist(), ["0001a", None])
        self.assertEqual(transformed["normalized_hanyu_dazidian"].tolist(), ["12", None])
        self.assertEqual(transformed["normalized_guangyun"].tolist(), ["甲", "乙"])

    def test_transform_mand2mc_corrects_o_to_schwa_against_bs(self) -> None:
        frame = pd.DataFrame(
            {
                "source_row_number": [2],
                "source_sheet_name": ["Feuil1"],
                "character": ["圈"],
                "pinyin": ["juan4"],
                "MC (NWH)": ["qwonH"],
                "MC (B&S)": ["'wonH"],
                "GSR": ["0200a"],
                "漢語大字典": ["12"],
                "廣韻": ["甲"],
            }
        )
        transformed = import_mand2mc.transform_mand2mc(frame)
        self.assertEqual(transformed["normalized_mc_nwh"].tolist(), ["qwənH"])
        self.assertEqual(
            transformed.attrs["mc_orthography_summary"]["auto_corrected_count"],
            1,
        )

    def test_transform_mand2mc_uses_blank_character_column(self) -> None:
        frame = pd.DataFrame(
            {
                "source_row_number": [2],
                "source_sheet_name": ["Feuil1"],
                "": [" 可 "],
                "pinyin": ["ke3"],
                "MC (NWH)": ["khaX"],
                "MC (B&S)": ["khaX"],
                "GSR": ["0001a"],
                "漢語大字典": ["12"],
                "廣韻": ["甲"],
            }
        )

        transformed = import_mand2mc.transform_mand2mc(frame)
        self.assertEqual(transformed["normalized_character"].tolist(), ["可"])

    def test_render_report_mentions_sheets_and_columns(self) -> None:
        frame = pd.DataFrame(
            {
                "source_row_number": [2],
                "source_sheet_name": ["Feuil1"],
                "character": ["可"],
                "normalized_character": ["可"],
                "normalized_pinyin": ["ke3"],
                "normalized_mc_nwh": ["khaX"],
                "normalized_mc_bs": ["khaX"],
                "normalized_gsr": ["0001a"],
                "normalized_hanyu_dazidian": ["12"],
                "normalized_guangyun": ["甲"],
            }
        )
        report = import_mand2mc.render_report(
            source_path=Path("Mand2MC2009-06-08 copy.ods"),
            source_sheet_name="Feuil1",
            transformed_frame=frame,
            raw_columns=["character", "pinyin", "MC (NWH)", "MC (B&S)", "GSR", ""],
            sheet_summaries=[
                {"sheet_name": "Feuil1", "data_row_count": 1, "column_count": 6},
                {"sheet_name": "Feuil2", "data_row_count": 2, "column_count": 3},
            ],
        )

        self.assertIn("# Mand2MC import report", report)
        self.assertIn("`Feuil2`", report)
        self.assertIn("(blank column name)", report)
        self.assertIn("Auto-corrected NWH MC rows", report)


if __name__ == "__main__":
    unittest.main()
