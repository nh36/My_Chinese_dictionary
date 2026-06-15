from __future__ import annotations

import sys
import unittest


ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import resolve_series_roots  # noqa: E402


class ResolveSeriesRootsTests(unittest.TestCase):
    def test_strip_tone(self) -> None:
        self.assertEqual(resolve_series_roots.strip_tone("qimX"), "qim")
        self.assertEqual(resolve_series_roots.strip_tone("kak"), "kak")

    def test_resolve_root_single_candidate(self) -> None:
        entry = {
            "packet_kind": "missing_series",
            "schuessler": {"k_tokens": ["766"]},
            "proposed_additions": [
                {
                    "character": "各",
                    "mand2mc_rows": [{"gsr": "0766a", "mc_nwh": "kak"}],
                    "bs_gsr_rows": [],
                }
            ],
        }
        resolved = resolve_series_roots.resolve_root(entry)
        self.assertEqual(resolved["root"], "kak")
        self.assertEqual(resolved["character"], "各")

    def test_resolve_root_multiple_candidates_unresolved(self) -> None:
        entry = {
            "packet_kind": "missing_series",
            "schuessler": {"k_tokens": ["651", "652"]},
            "proposed_additions": [
                {
                    "character": "今",
                    "mand2mc_rows": [{"gsr": "0651a", "mc_nwh": "kim"}],
                    "bs_gsr_rows": [],
                },
                {
                    "character": "甲",
                    "mand2mc_rows": [{"gsr": "0652a", "mc_nwh": "kam"}],
                    "bs_gsr_rows": [],
                },
            ],
        }
        self.assertIsNone(resolve_series_roots.resolve_root(entry))


if __name__ == "__main__":
    unittest.main()
