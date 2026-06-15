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
                {"mc_nwh": "kaek", "mc_bs": "kaek", "gsr": "0766d"},
                {"mc_nwh": "kak", "mc_bs": "kak", "gsr": "0766d"},
            ],
            "bs_gsr_rows": [
                {"mc_bs": "kaek", "gsr": "0766d"},
            ],
        }
        result = analyze_mc_disagreements.classify_candidate(candidate)
        self.assertIn("mand2mc-multiple", result["categories"])
        self.assertIn("mand2mc-extra-vs-bs", result["categories"])
        self.assertNotIn("bs-not-in-mand2mc", result["categories"])

    def test_render_report_explains_investigation_trigger(self) -> None:
        report = analyze_mc_disagreements.render_report(
            [
                {
                    "gsc_id": "02-01",
                    "character": "胳",
                    "categories": ["bs-not-in-mand2mc"],
                    "mand_forms": ["kaek", "kak"],
                    "bs_forms": ["kak", "kaep"],
                    "gsr_values": ["0766d"],
                    "mc_resolution": {
                        "bs_not_in_mand2mc": ["kaep"],
                        "mand2mc_not_in_bs_gsr": ["kaek"],
                    },
                }
            ]
        )
        self.assertIn("bs-not-in-mand2mc", report)
        self.assertIn("render Mand2MC-derived MC forms", report)


if __name__ == "__main__":
    unittest.main()
