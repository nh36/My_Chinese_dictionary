from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import import_bs_gsr_pdf  # noqa: E402


class ImportBsGsrPdfTests(unittest.TestCase):
    def test_parse_bs_gsr_line_with_regular_gsr(self) -> None:
        line = "可 kě       khaX      (kh- + -a B)     *kʰˤajʔ {*[k]ʰˤa[j]ʔ}                                 may; acceptable        0001a    U+53EF"
        parsed = import_bs_gsr_pdf.parse_bs_gsr_line(line)

        self.assertIsNotNone(parsed)
        assert parsed is not None
        self.assertEqual(parsed["character"], "可")
        self.assertEqual(parsed["pinyin"], "kě")
        self.assertEqual(parsed["mc_bs"], "khaX")
        self.assertEqual(parsed["gloss"], "may; acceptable")
        self.assertEqual(parsed["normalized_gsr"], "0001a")
        self.assertEqual(parsed["unicode_utf16"], "U+53EF")

    def test_parse_bs_gsr_line_without_gsr(self) -> None:
        line = "夒 náo      naw       (n- + -aw A)     *nˤu                                                  a kind of monkey       --       U+5912"
        parsed = import_bs_gsr_pdf.parse_bs_gsr_line(line)

        self.assertIsNotNone(parsed)
        assert parsed is not None
        self.assertIsNone(parsed["normalized_gsr"])
        self.assertEqual(parsed["gsr_raw"], "--")

    def test_parse_bs_gsr_line_with_extended_gsr_and_missing_gloss(self) -> None:
        line = "穄 jì    tsjejH    (ts- + -jej C)    *tset-s {*[ts][e][t]-s}                                                                    0337e   U+7A44"
        parsed = import_bs_gsr_pdf.parse_bs_gsr_line(line)

        self.assertIsNotNone(parsed)
        assert parsed is not None
        self.assertEqual(parsed["normalized_gsr"], "0337e")
        self.assertEqual(parsed["oc_bs"], "*tset-s {*[ts][e][t]-s}")
        self.assertIsNone(parsed["gloss"])


if __name__ == "__main__":
    unittest.main()
