from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import compare_sources  # noqa: E402


SAMPLE_ENTRIES = [
    {
        "id": "18-01",
        "head": {"characters": ["可"]},
        "chinese_characters": ["可", "柯"],
        "mc_forms": ["khaX", "ka"],
        "gsr_markers": ["0001a", "0001d"],
    },
    {
        "id": "01-67",
        "head": {"characters": ["父"]},
        "chinese_characters": ["父", "布"],
        "mc_forms": ["biuX", "puH"],
        "gsr_markers": ["0102a", "0102j"],
    },
]


class CompareSourcesTests(unittest.TestCase):
    def test_find_rows_not_in_tex(self) -> None:
        mand2mc = pd.DataFrame(
            [
                {"source_row_number": "2", "normalized_character": "可", "normalized_mc_nwh": "khaX", "normalized_gsr": "0001a"},
                {"source_row_number": "3", "normalized_character": "阿", "normalized_mc_nwh": "a", "normalized_gsr": "0001m"},
            ]
        )
        missing = compare_sources.find_rows_not_in_tex(
            mand2mc, compare_sources.build_tex_character_index(SAMPLE_ENTRIES)
        )
        self.assertEqual(len(missing), 1)
        self.assertEqual(missing[0]["normalized_character"], "阿")

    def test_find_candidate_mc_conflicts(self) -> None:
        mand2mc = pd.DataFrame(
            [
                {"source_row_number": "2", "normalized_character": "可", "normalized_mc_nwh": "khaX", "normalized_gsr": "0001a"},
                {"source_row_number": "3", "normalized_character": "可", "normalized_mc_nwh": "x", "normalized_gsr": "0001a"},
            ]
        )
        conflicts = compare_sources.find_candidate_mc_conflicts(
            mand2mc, compare_sources.build_tex_character_index(SAMPLE_ENTRIES)
        )
        self.assertEqual(len(conflicts), 1)
        self.assertTrue(conflicts[0]["matched_by_gsr"])

    def test_find_shengfu_groups_missing_from_tex(self) -> None:
        shengfu = pd.DataFrame(
            [
                {"normalized_character": "可", "normalized_phonetic_component": "可"},
                {"normalized_character": "丁", "normalized_phonetic_component": "丁"},
                {"normalized_character": "頂", "normalized_phonetic_component": "丁"},
            ]
        )
        missing = compare_sources.find_shengfu_groups_missing_from_tex(
            shengfu, compare_sources.build_tex_head_character_set(SAMPLE_ENTRIES)
        )
        self.assertEqual(len(missing), 1)
        self.assertEqual(missing[0]["component"], "丁")
        self.assertEqual(missing[0]["row_count"], 2)

    def test_write_reports(self) -> None:
        mand2mc = pd.DataFrame(
            [
                {
                    "source_row_number": "2",
                    "normalized_character": "阿",
                    "normalized_pinyin": "a1",
                    "normalized_mc_nwh": "a",
                    "normalized_gsr": "0001m",
                }
            ]
        )
        shengfu = pd.DataFrame(
            [
                {
                    "normalized_character": "丁",
                    "normalized_phonetic_component": "丁",
                }
            ]
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            reports_dir = Path(temp_dir) / "reports"
            compare_sources.write_reports(SAMPLE_ENTRIES, mand2mc, shengfu, reports_dir)

            self.assertTrue((reports_dir / "mand2mc_rows_not_in_tex.md").exists())
            self.assertTrue((reports_dir / "tex_forms_conflicting_with_mand2mc.md").exists())
            self.assertTrue((reports_dir / "shengfu_groups_missing_from_tex.md").exists())

    def test_load_entries(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "entries.json"
            path.write_text(json.dumps({"entries": SAMPLE_ENTRIES}), encoding="utf-8")
            loaded = compare_sources.load_entries(path)
            self.assertEqual(len(loaded), 2)


if __name__ == "__main__":
    unittest.main()
