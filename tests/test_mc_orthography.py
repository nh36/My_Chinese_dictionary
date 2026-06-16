from __future__ import annotations

import csv
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import mc_orthography  # noqa: E402


class McOrthographyTests(unittest.TestCase):
    def test_normalize_nwh_mc_against_bs_auto_corrects_o_to_schwa(self) -> None:
        corrected, status = mc_orthography.normalize_nwh_mc_against_bs("qwonX", "'wonX")
        self.assertEqual(corrected, "qwənX")
        self.assertEqual(status, mc_orthography.AUTO_CORRECTION_STATUS)

    def test_normalize_nwh_mc_against_bs_flags_unexpected_o(self) -> None:
        corrected, status = mc_orthography.normalize_nwh_mc_against_bs("qwonX", "qwenX")
        self.assertEqual(corrected, "qwonX")
        self.assertEqual(status, mc_orthography.ANOMALY_STATUS)

    def test_current_derived_mand2mc_has_no_o_in_nwh_mc(self) -> None:
        path = ROOT / "data/derived/mand2mc.csv"
        with path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        offenders = [
            (row.get("source_row_number"), row.get("normalized_character"), row.get("normalized_mc_nwh"))
            for row in rows
            if "o" in (row.get("normalized_mc_nwh") or "")
        ]
        self.assertFalse(offenders)

    def test_current_curated_mand2mc_rows_have_no_o_but_old_chinese_can(self) -> None:
        curation_dir = ROOT / "data/entries/curation"
        mc_offenders = []
        oc_examples = []
        for path in curation_dir.glob("*.json"):
            entry = json.loads(path.read_text(encoding="utf-8"))
            for candidate in entry.get("proposed_additions", []):
                for row in candidate.get("mand2mc_rows", []):
                    if "o" in (row.get("mc_nwh") or ""):
                        mc_offenders.append((path.name, candidate["character"], row.get("mc_nwh")))
                for row in candidate.get("bs_gsr_rows", []):
                    if "o" in (row.get("oc_bs") or ""):
                        oc_examples.append((path.name, candidate["character"], row.get("oc_bs")))
        self.assertFalse(mc_offenders)
        self.assertTrue(oc_examples)


if __name__ == "__main__":
    unittest.main()
