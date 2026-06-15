from __future__ import annotations

import sys
import unittest


ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import analyze_mc_disagreements  # noqa: E402


class AnalyzeMcDisagreementsTests(unittest.TestCase):
    def test_classify_candidate(self) -> None:
        candidate = {
            "character": "胳",
            "mand2mc_rows": [
                {"mc_nwh": "kaek", "gsr": "0766d"},
                {"mc_nwh": "kak", "gsr": "0766d"},
            ],
            "bs_gsr_rows": [
                {"mc_bs": "kaek", "gsr": "0766d"},
            ],
        }
        result = analyze_mc_disagreements.classify_candidate(candidate)
        self.assertIn("mand2mc-multiple", result["categories"])
        self.assertIn("cross-source-mismatch", result["categories"])

    def test_render_report_explains_current_warning_trigger(self) -> None:
        report = analyze_mc_disagreements.render_report(
            [
                {
                    "gsc_id": "02-01",
                    "character": "胳",
                    "categories": ["cross-source-mismatch"],
                    "mand_forms": ["kaek", "kak"],
                    "bs_forms": ["kak"],
                    "gsr_values": ["0766d"],
                }
            ]
        )
        self.assertIn("mand_bs_mc_disagreement", report)
        self.assertIn("[MC disagreement among imported sources]", report)


if __name__ == "__main__":
    unittest.main()
