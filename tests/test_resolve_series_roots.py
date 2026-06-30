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
        self.assertEqual(resolve_series_roots.derive_oc_root("*qʷʰo̠ɡʷ"), "quok")
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

    def test_26_28_head_supplement_supplies_resolved_root(self) -> None:
        supplement = resolve_series_roots.load_head_supplement(
            ROOT / "data/series_root_head_supplement.json"
        )
        entry = json.loads((ROOT / "data/entries/curation/26-28.json").read_text(encoding="utf-8"))
        entry = resolve_series_roots.apply_root_resolution(entry, head_supplement=supplement)

        resolved = entry.get("resolved_series_root") or {}
        self.assertEqual(resolved.get("character"), "𠂔")
        self.assertEqual(resolved.get("root"), "sy")
        self.assertEqual(resolved.get("source"), "head_graph_supplement")

    def test_01_47_head_shengfu_support_breaks_tied_head_roots(self) -> None:
        entry = json.loads((ROOT / "data/entries/curation/01-47.json").read_text(encoding="utf-8"))
        entry = resolve_series_roots.apply_root_resolution(entry)

        resolved = entry.get("resolved_series_root") or {}
        self.assertEqual(resolved.get("character"), "邪")
        self.assertEqual(resolved.get("root"), "qa")
        self.assertEqual(resolved.get("source"), "head_graph_supported_root")
        self.assertGreaterEqual(resolved.get("support_count", 0), 2)

    def test_02_11_component_series_root_breaks_conflicting_shengfu_tie(self) -> None:
        component_entry = json.loads((ROOT / "data/entries/curation/02-05.json").read_text(encoding="utf-8"))
        component_root_index = resolve_series_roots.build_component_root_index([component_entry])
        entry = json.loads((ROOT / "data/entries/curation/02-11.json").read_text(encoding="utf-8"))
        entry = resolve_series_roots.apply_root_resolution(entry, component_root_index=component_root_index)

        resolved = entry.get("resolved_series_root") or {}
        self.assertEqual(resolved.get("character"), "覤")
        self.assertEqual(resolved.get("root"), "kak")
        self.assertEqual(resolved.get("source"), "head_graph_supported_root")
        self.assertGreaterEqual(resolved.get("support_count", 0), 2)

    def test_component_root_index_covers_resolved_candidates_and_phonetic_components(self) -> None:
        candidate_entry = json.loads((ROOT / "data/entries/curation/03-49.json").read_text(encoding="utf-8"))
        component_entry = json.loads((ROOT / "data/entries/curation/04-07.json").read_text(encoding="utf-8"))
        index = resolve_series_roots.build_component_root_index([candidate_entry, component_entry])

        self.assertEqual(index["廧"]["root"], "saṅ")
        self.assertEqual(index["𣪘"]["root"], "kuu")

    def test_component_root_index_prefers_dominant_root_when_minor_conflict_exists(self) -> None:
        dominant_entry = json.loads((ROOT / "data/entries/curation/22-01.json").read_text(encoding="utf-8"))
        conflicting_entry = json.loads((ROOT / "data/entries/curation/20-10.json").read_text(encoding="utf-8"))
        index = resolve_series_roots.build_component_root_index([dominant_entry, conflicting_entry])

        self.assertEqual(index["𠯑"]["root"], "kot")
        self.assertGreaterEqual(index["𠯑"]["support_count"], 2)

    def test_07_18_reuses_dominant_phonetic_component_root(self) -> None:
        dominant_entry = json.loads((ROOT / "data/entries/curation/22-01.json").read_text(encoding="utf-8"))
        conflicting_entry = json.loads((ROOT / "data/entries/curation/20-10.json").read_text(encoding="utf-8"))
        component_root_index = resolve_series_roots.build_component_root_index(
            [dominant_entry, conflicting_entry]
        )
        entry = json.loads((ROOT / "data/entries/curation/07-18.json").read_text(encoding="utf-8"))
        entry = resolve_series_roots.apply_root_resolution(entry, component_root_index=component_root_index)

        resolved = entry.get("resolved_series_root") or {}
        self.assertEqual(resolved.get("character"), "咶")
        self.assertEqual(resolved.get("root"), "kot")
        self.assertEqual(resolved.get("source"), "head_graph_supported_root")
        self.assertIn("phonetic_component_series_root", resolved.get("supporting_sources", []))

    def test_03_50_reuses_same_character_root_from_resolved_packet(self) -> None:
        hint_entry = json.loads((ROOT / "data/entries/curation/03-49.json").read_text(encoding="utf-8"))
        component_root_index = resolve_series_roots.build_component_root_index([hint_entry])
        entry = json.loads((ROOT / "data/entries/curation/03-50.json").read_text(encoding="utf-8"))
        entry = resolve_series_roots.apply_root_resolution(entry, component_root_index=component_root_index)

        resolved = entry.get("resolved_series_root") or {}
        self.assertEqual(resolved.get("character"), "廧")
        self.assertEqual(resolved.get("root"), "saṅ")
        self.assertEqual(resolved.get("source"), "same_character_series_root")

    def test_03_56_head_supplement_variant_of_shuang_supplies_root(self) -> None:
        supplement = resolve_series_roots.load_head_supplement(
            ROOT / "data/series_root_head_supplement.json"
        )
        entry = json.loads((ROOT / "data/entries/curation/03-56.json").read_text(encoding="utf-8"))
        entry = resolve_series_roots.apply_root_resolution(entry, head_supplement=supplement)

        resolved = entry.get("resolved_series_root") or {}
        self.assertEqual(resolved.get("character"), "𡙁")
        self.assertEqual(resolved.get("root"), "saṅ")
        self.assertEqual(resolved.get("source"), "head_graph_supplement")

    def test_04_39_head_supplement_variant_of_nai_supplies_root(self) -> None:
        supplement = resolve_series_roots.load_head_supplement(
            ROOT / "data/series_root_head_supplement.json"
        )
        entry = json.loads((ROOT / "data/entries/curation/04-39.json").read_text(encoding="utf-8"))
        entry = resolve_series_roots.apply_root_resolution(entry, head_supplement=supplement)

        resolved = entry.get("resolved_series_root") or {}
        self.assertEqual(resolved.get("character"), "迺")
        self.assertEqual(resolved.get("root"), "ny")
        self.assertEqual(resolved.get("source"), "head_graph_supplement")

    def test_07_15_head_supplement_supplies_tje_root(self) -> None:
        supplement = resolve_series_roots.load_head_supplement(
            ROOT / "data/series_root_head_supplement.json"
        )
        entry = json.loads((ROOT / "data/entries/curation/07-15.json").read_text(encoding="utf-8"))
        entry = resolve_series_roots.apply_root_resolution(entry, head_supplement=supplement)

        resolved = entry.get("resolved_series_root") or {}
        self.assertEqual(resolved.get("character"), "卮")
        self.assertEqual(resolved.get("root"), "te")
        self.assertEqual(resolved.get("source"), "head_graph_supplement")

    def test_16_18_head_supplement_supplies_zhao_root(self) -> None:
        supplement = resolve_series_roots.load_head_supplement(
            ROOT / "data/series_root_head_supplement.json"
        )
        entry = json.loads((ROOT / "data/entries/curation/16-18.json").read_text(encoding="utf-8"))
        entry = resolve_series_roots.apply_root_resolution(entry, head_supplement=supplement)

        resolved = entry.get("resolved_series_root") or {}
        self.assertEqual(resolved.get("character"), "肇")
        self.assertEqual(resolved.get("root"), "law")
        self.assertEqual(resolved.get("source"), "head_graph_supplement")

    def test_16_22_head_supplement_supplies_shao_family_root(self) -> None:
        supplement = resolve_series_roots.load_head_supplement(
            ROOT / "data/series_root_head_supplement.json"
        )
        entry = json.loads((ROOT / "data/entries/curation/16-22.json").read_text(encoding="utf-8"))
        entry = resolve_series_roots.apply_root_resolution(entry, head_supplement=supplement)

        resolved = entry.get("resolved_series_root") or {}
        self.assertEqual(resolved.get("character"), "少")
        self.assertEqual(resolved.get("root"), "sew")
        self.assertEqual(resolved.get("source"), "head_graph_supplement")

    def test_16_38_head_supplement_supplies_biao_root(self) -> None:
        supplement = resolve_series_roots.load_head_supplement(
            ROOT / "data/series_root_head_supplement.json"
        )
        entry = json.loads((ROOT / "data/entries/curation/16-38.json").read_text(encoding="utf-8"))
        entry = resolve_series_roots.apply_root_resolution(entry, head_supplement=supplement)

        resolved = entry.get("resolved_series_root") or {}
        self.assertEqual(resolved.get("character"), "驫")
        self.assertEqual(resolved.get("root"), "piw")
        self.assertEqual(resolved.get("source"), "head_graph_supported_root")
        self.assertIn("head_graph_supplement", resolved.get("supporting_sources", []))

    def test_19_03_head_supplement_supplies_gua_variant_root(self) -> None:
        supplement = resolve_series_roots.load_head_supplement(
            ROOT / "data/series_root_head_supplement.json"
        )
        entry = json.loads((ROOT / "data/entries/curation/19-03.json").read_text(encoding="utf-8"))
        entry = resolve_series_roots.apply_root_resolution(entry, head_supplement=supplement)

        resolved = entry.get("resolved_series_root") or {}
        self.assertEqual(resolved.get("character"), "𩰬")
        self.assertEqual(resolved.get("root"), "kuay")
        self.assertEqual(resolved.get("source"), "head_graph_supplement")

    def test_20_06_head_supplement_supplies_yi_root(self) -> None:
        supplement = resolve_series_roots.load_head_supplement(
            ROOT / "data/series_root_head_supplement.json"
        )
        entry = json.loads((ROOT / "data/entries/curation/20-06.json").read_text(encoding="utf-8"))
        entry = resolve_series_roots.apply_root_resolution(entry, head_supplement=supplement)

        resolved = entry.get("resolved_series_root") or {}
        self.assertEqual(resolved.get("character"), "帠")
        self.assertEqual(resolved.get("root"), "ṅy")
        self.assertEqual(resolved.get("source"), "head_graph_supplement")

    def test_21_03_head_supplement_supplies_ga_root(self) -> None:
        supplement = resolve_series_roots.load_head_supplement(
            ROOT / "data/series_root_head_supplement.json"
        )
        entry = json.loads((ROOT / "data/entries/curation/21-03.json").read_text(encoding="utf-8"))
        entry = resolve_series_roots.apply_root_resolution(entry, head_supplement=supplement)

        resolved = entry.get("resolved_series_root") or {}
        self.assertEqual(resolved.get("character"), "舝")
        self.assertEqual(resolved.get("root"), "ɡat")
        self.assertEqual(resolved.get("source"), "head_graph_supplement")

    def test_28_16_head_supplement_supplies_lei_root(self) -> None:
        supplement = resolve_series_roots.load_head_supplement(
            ROOT / "data/series_root_head_supplement.json"
        )
        entry = json.loads((ROOT / "data/entries/curation/28-16.json").read_text(encoding="utf-8"))
        entry = resolve_series_roots.apply_root_resolution(entry, head_supplement=supplement)

        resolved = entry.get("resolved_series_root") or {}
        self.assertEqual(resolved.get("character"), "磊")
        self.assertEqual(resolved.get("root"), "ruy")
        self.assertEqual(resolved.get("source"), "head_graph_supplement")

    def test_04_08_reuses_resolved_phonetic_component_family_root(self) -> None:
        component_entry = json.loads((ROOT / "data/entries/curation/04-07.json").read_text(encoding="utf-8"))
        component_root_index = resolve_series_roots.build_component_root_index([component_entry])
        entry = json.loads((ROOT / "data/entries/curation/04-08.json").read_text(encoding="utf-8"))
        entry = resolve_series_roots.apply_root_resolution(entry, component_root_index=component_root_index)

        resolved = entry.get("resolved_series_root") or {}
        self.assertEqual(resolved.get("character"), "𣪘")
        self.assertEqual(resolved.get("root"), "kuu")
        self.assertEqual(resolved.get("source"), "same_character_series_root")

    def test_25_21_wiktionary_variant_reuses_referenced_root(self) -> None:
        referenced_entry = json.loads((ROOT / "data/entries/curation/25-20.json").read_text(encoding="utf-8"))
        component_root_index = resolve_series_roots.build_component_root_index([referenced_entry])
        entry = json.loads((ROOT / "data/entries/curation/25-21.json").read_text(encoding="utf-8"))
        entry = resolve_series_roots.apply_root_resolution(entry, component_root_index=component_root_index)

        resolved = entry.get("resolved_series_root") or {}
        self.assertEqual(resolved.get("character"), "邍")
        self.assertEqual(resolved.get("root"), "ṅar")
        self.assertEqual(resolved.get("source"), "wiktionary_variant_series_root")

    def test_01_40_explicit_b_header_uses_head_shengfu(self) -> None:
        entry = json.loads((ROOT / "data/entries/curation/01-40.json").read_text(encoding="utf-8"))
        entry = resolve_series_roots.apply_root_resolution(entry)

        resolved = entry.get("resolved_series_root") or {}
        self.assertEqual(resolved.get("character"), "樗")
        self.assertEqual(resolved.get("root"), "kua")
        self.assertEqual(resolved.get("source"), "head_graph_oc_shengfu")

    def test_03_64_mc_coda_breaks_shengfu_only_tie(self) -> None:
        entry = json.loads((ROOT / "data/entries/curation/03-64.json").read_text(encoding="utf-8"))
        entry = resolve_series_roots.apply_root_resolution(entry)

        resolved = entry.get("resolved_series_root") or {}
        self.assertEqual(resolved.get("character"), "莽")
        self.assertEqual(resolved.get("root"), "maṅ")
        self.assertEqual(resolved.get("source"), "head_graph_mc_coda")

    def test_02_12_labialized_oc_coda_is_preserved(self) -> None:
        entry = json.loads((ROOT / "data/entries/curation/02-12.json").read_text(encoding="utf-8"))
        entry = resolve_series_roots.apply_root_resolution(entry)

        resolved = entry.get("resolved_series_root") or {}
        self.assertEqual(resolved.get("character"), "霍")
        self.assertEqual(resolved.get("root"), "quok")

    def test_07_16_explicit_head_bs_beats_conflicting_shengfu(self) -> None:
        entry = json.loads((ROOT / "data/entries/curation/07-16.json").read_text(encoding="utf-8"))
        entry = resolve_series_roots.apply_root_resolution(entry)

        resolved = entry.get("resolved_series_root") or {}
        self.assertEqual(resolved.get("character"), "豸")
        self.assertEqual(resolved.get("root"), "te")
        self.assertEqual(resolved.get("source"), "head_graph_bs_head")

    def test_10_14_direct_head_shengfu_beats_component_root_hint(self) -> None:
        component_entry = json.loads((ROOT / "data/entries/curation/11-13.json").read_text(encoding="utf-8"))
        component_root_index = resolve_series_roots.build_component_root_index([component_entry])
        entry = json.loads((ROOT / "data/entries/curation/10-14.json").read_text(encoding="utf-8"))
        entry = resolve_series_roots.apply_root_resolution(entry, component_root_index=component_root_index)

        resolved = entry.get("resolved_series_root") or {}
        self.assertEqual(resolved.get("character"), "𧱓")
        self.assertEqual(resolved.get("root"), "to")
        self.assertEqual(resolved.get("source"), "head_graph_shengfu_head")

    def test_02_03_falls_back_to_b_suffix_when_a_lacks_oc_evidence(self) -> None:
        entry = json.loads((ROOT / "data/entries/curation/02-03.json").read_text(encoding="utf-8"))
        entry = resolve_series_roots.apply_root_resolution(entry)

        resolved = entry.get("resolved_series_root") or {}
        self.assertEqual(resolved.get("character"), "戟")
        self.assertEqual(resolved.get("root"), "kak")
        self.assertEqual(resolved.get("source"), "head_graph_oc_bs")
        self.assertGreaterEqual(resolved.get("support_count", 0), 2)

    def test_26_28_supplemental_shengfu_rows_cover_variant_and_combined_forms(self) -> None:
        supplement = resolve_series_roots.load_head_supplement(
            ROOT / "data/series_root_head_supplement.json"
        )
        entry = json.loads((ROOT / "data/entries/curation/26-28.json").read_text(encoding="utf-8"))
        entry = resolve_series_roots.merge_supplemental_shengfu_rows(entry, supplement)
        by_character = {candidate["character"]: candidate for candidate in entry["proposed_additions"]}

        self.assertTrue(by_character["姉"]["shengfu_character_rows"])
        self.assertTrue(by_character["柿"]["shengfu_character_rows"])
        self.assertTrue(by_character["柹"]["shengfu_character_rows"])
        self.assertEqual(
            by_character["姉"]["shengfu_character_rows"][0]["phonetic_component"],
            "𠂔",
        )
        self.assertEqual(
            by_character["柿"]["shengfu_character_rows"][0]["oc_syllable"],
            "zrɯʔ",
        )

    def test_26_30_mc_onset_breaks_single_head_root_tie(self) -> None:
        entry = json.loads((ROOT / "data/entries/curation/26-30.json").read_text(encoding="utf-8"))
        entry = resolve_series_roots.apply_root_resolution(entry)

        resolved = entry.get("resolved_series_root") or {}
        self.assertEqual(resolved.get("character"), "自")
        self.assertEqual(resolved.get("root"), "tsit")
        self.assertEqual(resolved.get("source"), "head_graph_mc_onset")


if __name__ == "__main__":
    unittest.main()
