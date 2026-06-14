from __future__ import annotations

import sys
import unittest


ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_semantic_evidence  # noqa: E402


class BuildSemanticEvidenceTests(unittest.TestCase):
    def test_parse_semantic_token(self) -> None:
        lookup = {"arb": [{"graph_raw": "木"}]}
        token = build_semantic_evidence.parse_semantic_token("arb·", lookup)
        self.assertEqual(token["abbreviation"], "arb")
        self.assertEqual(token["position"], "prefix-dot")
        self.assertEqual(token["inventory_matches"][0]["graph_raw"], "木")

    def test_enrich_curated_entry_reuses_single_existing_occurrence(self) -> None:
        entry = {
            "id": "18-18",
            "proposed_additions": [{"character": "加"}],
        }
        evidence = {
            "加": [
                {
                    "character": "加",
                    "transliteration_latex": r"{\large{kay}}",
                    "semantic_assignment": {"abbreviation": "arb", "position": "prefix-dot"},
                    "raw_block": "加\n{\\large{kay}}\n\\textit{kae};",
                }
            ]
        }
        enriched = build_semantic_evidence.enrich_curated_entry_with_ids(
            entry, evidence, {}, {"arb": [{"graph_raw": "木", "label_token": "arb(or)", "abbreviation": "arb"}]}
        )
        candidate = enriched["proposed_additions"][0]
        self.assertEqual(candidate["transliteration_latex"], r"{\large{kay}}")
        self.assertEqual(candidate["semantic_assignment"]["abbreviation"], "arb")
        self.assertIn("render_latex", candidate)

    def test_resolve_semantic_from_ids(self) -> None:
        ids_map = {"枷": "⿰木加", "嘉": "⿱壴加", "菇": "⿱艹姑", "姑": "⿰女古"}
        inventory_lookup = {
            "木": [{"graph_raw": "木", "label_token": "arb(or)", "abbreviation": "arb"}],
            "壴": [{"graph_raw": "壴", "label_token": "tympan(um)", "abbreviation": "tympan"}],
            "艸": [{"graph_raw": "艸", "label_token": "herb(a)", "abbreviation": "herb"}],
        }
        left = build_semantic_evidence.resolve_semantic_from_ids(
            character="枷",
            phonetic_component="加",
            ids_map=ids_map,
            graph_lookup=inventory_lookup,
        )
        above = build_semantic_evidence.resolve_semantic_from_ids(
            character="嘉",
            phonetic_component="加",
            ids_map=ids_map,
            graph_lookup=inventory_lookup,
        )
        recursive = build_semantic_evidence.resolve_semantic_from_ids(
            character="菇",
            phonetic_component="古",
            ids_map=ids_map,
            graph_lookup=inventory_lookup,
        )
        self.assertEqual(left["position"], "prefix-dot")
        self.assertEqual(left["abbreviation"], "arb")
        self.assertEqual(above["position"], "prefix-colon")
        self.assertEqual(above["abbreviation"], "tympan")
        self.assertEqual(recursive["abbreviation"], "herb")

    def test_compose_transliteration_from_root(self) -> None:
        self.assertEqual(
            build_semantic_evidence.compose_transliteration_from_root("ka", {"abbreviation": "arb", "position": "prefix-dot"}),
            r"{\large{\textsuperscript{arb·}ka}},",
        )
        self.assertEqual(
            build_semantic_evidence.compose_transliteration_from_root("ka", {"abbreviation": "conch", "position": "suffix-colon"}),
            r"{\large{ka\textsuperscript{:conch}}},",
        )

    def test_build_learned_graph_lookup(self) -> None:
        evidence = {
            "痢": [
                {
                    "semantic_assignment": {"abbreviation": "infirm"},
                }
            ]
        }
        shengfu_rows = [
            {"normalized_character": "痢", "normalized_phonetic_component": "利"},
        ]
        ids_map = {"痢": "⿸疒利"}
        learned = build_semantic_evidence.build_learned_graph_lookup(evidence, shengfu_rows, ids_map)
        self.assertEqual(learned["疒"][0]["abbreviation"], "infirm")


if __name__ == "__main__":
    unittest.main()
