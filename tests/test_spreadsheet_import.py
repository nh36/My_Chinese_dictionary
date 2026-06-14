from __future__ import annotations

import sys
import unittest
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import spreadsheet_import  # noqa: E402


class FakeExcelFile:
    sheet_names = ["Feuil1", "Feuil3"]

    def parse(self, sheet_name, header=None, dtype=object):
        if sheet_name == "Feuil1":
            return pd.DataFrame([["character", "pinyin"], ["可", "ke3"]], dtype=object)
        if sheet_name == "Feuil3":
            return pd.DataFrame([], dtype=object)
        raise KeyError(sheet_name)


class SpreadsheetImportTests(unittest.TestCase):
    def test_collect_sheet_summaries_tolerates_empty_sheet(self) -> None:
        summaries = spreadsheet_import.collect_sheet_summaries(FakeExcelFile())

        self.assertEqual(summaries[0]["sheet_name"], "Feuil1")
        self.assertEqual(summaries[0]["data_row_count"], 1)
        self.assertEqual(summaries[1]["sheet_name"], "Feuil3")
        self.assertEqual(summaries[1]["data_row_count"], 0)
        self.assertEqual(summaries[1]["column_count"], 0)


if __name__ == "__main__":
    unittest.main()
