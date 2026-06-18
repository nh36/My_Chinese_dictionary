from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import resolve_series_roots  # noqa: E402


class ResolveSeriesRootsTests(unittest.TestCase):
    def test_derive_oc_root_examples(self) -> None:
        self.assertEqual(resolve_series_roots.derive_oc_root("*kˤak"), "kak")
        self.assertEqual(resolve_series_roots.derive_oc_root("*krəm {*[k]r[ə]m}"), "kym")
        self.assertEqual(resolve_series_roots.derive_oc_root("*ləʔ"), "ly")
        self.assertEqual(resolve_series_roots.derive_oc_root("*ŋrar", mode="node"), "ŋrar")
        self.assertEqual(resolve_series_roots.derive_oc_root("*kap {*k(r)ap}"), "kap")
        self.assertEqual(resolve_series_roots.derive_oc_root("*tsraŋ {*[ts]raŋ}", mode="node"), "tsraṅ")
        self.assertEqual(resolve_series_roots.derive_oc_root("*s.tʰˤiwk", mode="node"), "tsik")
        self.assertEqual(resolve_series_roots.derive_oc_root("*ɡ‧laɡ"), "lak")
        self.assertEqual(resolve_series_roots.derive_oc_root("*ɡ‧leb"), "lep")

    def test_resolve_root_single_oc_candidate(self) -> None:
        entry = {
            "packet_kind": "missing_series",
            "schuessler": {"k_tokens": ["766"]},
            "proposed_additions": [
                {
                    "character": "各",
                    "mand2mc_rows": [],
                    "bs_gsr_rows": [{"gsr": "0766a", "oc_bs": "*kˤak"}],
                }
            ],
        }
        resolved = resolve_series_roots.resolve_root(entry)
        self.assertEqual(resolved["root"], "kak")
        self.assertEqual(resolved["character"], "各")
        self.assertEqual(resolved["source"], "head_graph_oc_bs")

    def test_current_missing_series_roots_are_oc_driven(self) -> None:
        expectations = {
            "02-01": "kak",
            "04-30": "ly",
            "38-03": "kym",
        }
        for entry_id, expected_root in expectations.items():
            entry = json.loads((ROOT / "data/entries/curation" / f"{entry_id}.json").read_text(encoding="utf-8"))
            resolved = resolve_series_roots.apply_root_resolution(entry)["resolved_series_root"]
            self.assertEqual(resolved["root"], expected_root)
            self.assertEqual(resolved["source"], "head_graph_oc_bs")

    def test_packet_root_majority_fallback(self) -> None:
        entry = {
            "packet_kind": "missing_series",
            "proposed_additions": [
                {"character": "A", "bs_gsr_rows": [{"oc_bs": "*kap"}]},
                {"character": "B", "bs_gsr_rows": [{"oc_bs": "*kap"}]},
                {"character": "C", "bs_gsr_rows": [{"oc_bs": "*pap"}]},
            ],
        }
        resolved = resolve_series_roots.derive_packet_root_consensus(entry)
        self.assertEqual(resolved["root"], "kap")
        self.assertEqual(resolved["source"], "packet_bs_majority")

    def test_resolve_root_shengfu_head_fallback(self) -> None:
        entry = {
            "packet_kind": "missing_series",
            "schuessler": {"k_tokens": ["1182"]},
            "proposed_additions": [
                {
                    "character": "廾",
                    "mand2mc_rows": [{"gsr": "1182a"}],
                    "bs_gsr_rows": [],
                    "shengfu_character_rows": [{"oc_syllable": "koŋ"}],
                }
            ],
        }
        resolved = resolve_series_roots.resolve_root(entry)
        self.assertEqual(resolved["root"], "koṅ")
        self.assertEqual(resolved["character"], "廾")
        self.assertEqual(resolved["source"], "head_graph_oc_shengfu")

    def test_packet_shengfu_majority_fallback(self) -> None:
        entry = {
            "packet_kind": "missing_series",
            "schuessler": {"k_tokens": ["226"]},
            "proposed_additions": [
                {"character": "卷", "shengfu_character_rows": [{"oc_syllable": "ɡon"}, {"oc_syllable": "kʳonʔ"}]},
                {"character": "眷", "shengfu_character_rows": [{"oc_syllable": "kʳonʔ"}]},
                {"character": "拳", "shengfu_character_rows": [{"oc_syllable": "kʳonʔ"}]},
            ],
        }
        resolved = resolve_series_roots.resolve_root(entry)
        self.assertEqual(resolved["root"], "kon")
        self.assertEqual(resolved["source"], "packet_shengfu_majority")


if __name__ == "__main__":
    unittest.main()
