from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_coverage_model  # noqa: E402


SAMPLE_ENTRIES = [
    {
        "id": "18-01",
        "subsection": "-ay",
        "chinese_characters": ["可", "歌"],
        "gsr_markers": ["0001a", "0001q"],
        "mc_forms": ["khaX", "ka"],
        "head": {"characters": ["可"]},
    },
    {
        "id": "10-10",
        "subsection": "-a",
        "chinese_characters": ["區"],
        "gsr_markers": ["0122a"],
        "mc_forms": ["quw"],
        "head": {"characters": ["區"]},
    },
]

SAMPLE_HEADERS = [
    {"gsc_id": "18-01", "rhyme_section": 18, "series_number": 1, "k_tokens": ["1"], "source_page_number": 1, "source_line_number": 10, "source_line_raw": "18-01 = K. 1"},
    {"gsc_id": "10-10", "rhyme_section": 10, "series_number": 10, "k_tokens": ["122"], "source_page_number": 2, "source_line_number": 20, "source_line_raw": "10-10 = K. 122"},
    {"gsc_id": "01-99", "rhyme_section": 1, "series_number": 99, "k_tokens": ["139"], "source_page_number": 3, "source_line_number": 30, "source_line_raw": "01-99 = K. 139"},
]

MAND_ROWS = [
    {"normalized_character": "可", "normalized_gsr": "0001a", "source_row_number": "2", "normalized_pinyin": "ke3", "normalized_mc_nwh": "khaX"},
    {"normalized_character": "奇", "normalized_gsr": "0001s", "source_row_number": "3", "normalized_pinyin": "qi2", "normalized_mc_nwh": "gie"},
    {"normalized_character": "區", "normalized_gsr": "0122a", "source_row_number": "4", "normalized_pinyin": "qu1", "normalized_mc_nwh": "quw"},
    {"normalized_character": "干", "normalized_gsr": "0139a", "source_row_number": "5", "normalized_pinyin": "gan1", "normalized_mc_nwh": "kan"},
]

SHENGFU_ROWS = [
    {"normalized_character": "可", "normalized_phonetic_component": "可", "normalized_component_level": "1", "source_row_number": "2"},
    {"normalized_character": "頂", "normalized_phonetic_component": "丁", "normalized_component_level": "1", "source_row_number": "3"},
]

BS_ROWS = [
    {"character": "可", "normalized_gsr": "0001a", "pinyin": "kě", "mc_bs": "khaX", "oc_bs": "*kʰˤajʔ", "source_page_number": "2"},
    {"character": "歌", "normalized_gsr": "0001q", "pinyin": "gē", "mc_bs": "ka", "oc_bs": "*kˤaj", "source_page_number": "2"},
    {"character": "區", "normalized_gsr": "0122a", "pinyin": "qū", "mc_bs": "quw", "oc_bs": "*q", "source_page_number": "5"},
]


class BuildCoverageModelTests(unittest.TestCase):
    def test_normalize_schuessler_gsc_id_recovers_ocr_l(self) -> None:
        self.assertEqual(build_coverage_model.normalize_schuessler_gsc_id("33-l"), "33-01")
        self.assertEqual(build_coverage_model.normalize_schuessler_gsc_id("33-I"), "33-01")

    def test_gsr_matching(self) -> None:
        self.assertTrue(build_coverage_model.gsr_matches("0001a", "1"))
        self.assertTrue(build_coverage_model.gsr_matches("0001a'", "1a"))
        self.assertFalse(build_coverage_model.gsr_matches("0122a", "139"))

    def test_build_gsc_series_coverage(self) -> None:
        rows = build_coverage_model.build_gsc_series_coverage(
            SAMPLE_ENTRIES, SAMPLE_HEADERS, MAND_ROWS, BS_ROWS
        )
        self.assertEqual(len(rows), 3)
        first = rows[0]
        self.assertEqual(first["gsc_id"], "01-99")
        self.assertEqual(first["in_tex"], "no")
        second = rows[1]
        self.assertEqual(second["gsc_id"], "10-10")
        self.assertEqual(second["in_tex"], "yes")

    def test_build_existing_series_expansion_candidates(self) -> None:
        candidates = build_coverage_model.build_existing_series_expansion_candidates(
            SAMPLE_ENTRIES, MAND_ROWS, BS_ROWS
        )
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0]["gsc_id"], "18-01")
        self.assertIn("奇", candidates[0]["candidate_characters_sample"])

    def test_build_missing_shengfu_components(self) -> None:
        missing = build_coverage_model.build_missing_shengfu_components(
            SHENGFU_ROWS, SAMPLE_ENTRIES
        )
        self.assertEqual(len(missing), 1)
        self.assertEqual(missing[0]["component"], "丁")


if __name__ == "__main__":
    unittest.main()
