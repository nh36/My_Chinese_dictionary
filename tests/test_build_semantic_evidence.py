from __future__ import annotations

import sys
import unittest


ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_semantic_evidence  # noqa: E402


class BuildSemanticEvidenceTests(unittest.TestCase):
    def test_normalize_component_graph_maps_dao_side_form(self) -> None:
        self.assertEqual(build_semantic_evidence.normalize_component_graph("刂"), "刀")

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
        ids_map = {
            "枷": "⿰木加",
            "嘉": "⿱壴加",
            "菇": "⿱艹姑",
            "姑": "⿰女古",
            "團": "⿴囗專",
            "簧": "⿱竹黄",
            "𨠑": "⿰酉㐌",
            "褏": "⿳亠⿰③由𧘇",
        }
        inventory_lookup = {
            "木": [{"graph_raw": "木", "label_token": "arb(or)", "abbreviation": "arb"}],
            "壴": [{"graph_raw": "壴", "label_token": "tympan(um)", "abbreviation": "tympan"}],
            "艸": [{"graph_raw": "艸", "label_token": "herb(a)", "abbreviation": "herb"}],
            "囗": [{"graph_raw": "囗", "label_token": "cla(usum)", "abbreviation": "cla"}],
            "竹": [{"graph_raw": "竹", "label_token": "bamb(us)", "abbreviation": "bamb"}],
            "酉": [{"graph_raw": "酉", "label_token": "vin(um)", "abbreviation": "vin"}],
            "衣": [{"graph_raw": "衣", "label_token": "vest(imentum)", "abbreviation": "vest"}],
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
        enclosure = build_semantic_evidence.resolve_semantic_from_ids(
            character="團",
            phonetic_component="專",
            ids_map=ids_map,
            graph_lookup=inventory_lookup,
        )
        normalized_component = build_semantic_evidence.resolve_semantic_from_ids(
            character="簧",
            phonetic_component="黃",
            ids_map=ids_map,
            graph_lookup=inventory_lookup,
        )
        component_alias = build_semantic_evidence.resolve_semantic_from_ids(
            character="𨠑",
            phonetic_component="它",
            ids_map=ids_map,
            graph_lookup=inventory_lookup,
        )
        trinary = build_semantic_evidence.resolve_semantic_from_ids(
            character="褏",
            phonetic_component="由",
            ids_map=ids_map,
            graph_lookup=inventory_lookup,
        )
        self.assertEqual(left["position"], "prefix-dot")
        self.assertEqual(left["abbreviation"], "arb")
        self.assertEqual(above["position"], "prefix-colon")
        self.assertEqual(above["abbreviation"], "tympan")
        self.assertEqual(recursive["abbreviation"], "herb")
        self.assertEqual(enclosure["position"], "prefix-colon")
        self.assertEqual(enclosure["abbreviation"], "cla")
        self.assertEqual(normalized_component["position"], "prefix-colon")
        self.assertEqual(normalized_component["abbreviation"], "bamb")
        self.assertEqual(component_alias["position"], "prefix-dot")
        self.assertEqual(component_alias["abbreviation"], "vin")
        self.assertEqual(trinary["position"], "suffix-colon")
        self.assertEqual(trinary["abbreviation"], "vest")

    def test_compose_transliteration_from_root(self) -> None:
        self.assertEqual(
            build_semantic_evidence.compose_transliteration_from_root("ka", {"abbreviation": "arb", "position": "prefix-dot"}),
            r"{\large{\textsuperscript{arb·}ka}},",
        )
        self.assertEqual(
            build_semantic_evidence.compose_transliteration_from_root("ka", {"abbreviation": "conch", "position": "suffix-colon"}),
            r"{\large{ka\textsuperscript{˸conch}}},",
        )
        rendered = build_semantic_evidence.compose_transliteration_from_root(
            "tak",
            {"abbreviation": "𣒚", "semantic_component": "𣒚", "position": "suffix-colon"},
        )
        self.assertIn(r"\includegraphics[height=1.6ex]{U+2349A.png}", rendered)

    def test_resolve_semantic_from_wiktionary_template(self) -> None:
        ids_map = {"台": "⿱厶口", "錦": "⿰金帛", "琴": "⿱玨今"}
        graph_lookup = {
            "口": [{"graph_raw": "口", "label_token": "or(is)", "abbreviation": "or"}],
            "玉": [{"graph_raw": "玉", "label_token": "gem(ma)", "abbreviation": "gem"}],
        }
        template = {
            "semantic_components": ["口"],
            "phonetic_components": ["㠯"],
            "positional_components": ["㠯", "口"],
            "template_raw": "{{Han compound|㠯|口|c1=p|c2=s|ls=psc}}",
        }
        resolved = build_semantic_evidence.resolve_semantic_from_wiktionary_template(
            character="台",
            han_compound=template,
            ids_map=ids_map,
            graph_lookup=graph_lookup,
        )
        self.assertEqual(resolved["abbreviation"], "or")
        self.assertEqual(resolved["position"], "suffix-colon")

    def test_resolve_semantic_from_packet_family(self) -> None:
        ids_map = {"眙": "⿰目台", "褏": "⿳亠⿰③由𧘇"}
        graph_lookup = {
            "目": [{"graph_raw": "目", "label_token": "ocul(us)", "abbreviation": "ocul"}],
            "衣": [{"graph_raw": "衣", "label_token": "vest(imentum)", "abbreviation": "vest"}],
        }
        resolved = build_semantic_evidence.resolve_semantic_from_packet_family(
            character="眙",
            ids_map=ids_map,
            graph_lookup=graph_lookup,
            packet_family={"台", "以"},
        )
        trinary = build_semantic_evidence.resolve_semantic_from_packet_family(
            character="褏",
            ids_map=ids_map,
            graph_lookup=graph_lookup,
            packet_family={"由", "柚", "油"},
        )
        self.assertEqual(resolved["abbreviation"], "ocul")
        self.assertEqual(resolved["position"], "prefix-dot")
        self.assertEqual(trinary["abbreviation"], "vest")
        self.assertEqual(trinary["position"], "suffix-colon")

    def test_resolve_semantic_from_parent_ids(self) -> None:
        ids_map = {
            "盍": "⿱去皿",
            "刧": "⿰去刀",
        }
        graph_lookup = {
            "刀": [{"graph_raw": "刀", "label_token": "cult(er)", "abbreviation": "cult"}],
        }
        resolved = build_semantic_evidence.resolve_semantic_from_parent_ids(
            character="刧",
            parent_character="盍",
            ids_map=ids_map,
            graph_lookup=graph_lookup,
        )
        self.assertEqual(resolved["abbreviation"], "cult")
        self.assertEqual(resolved["position"], "suffix-dot")

    def test_resolve_semantic_from_parent_ids_does_not_overreach_nested_relations(self) -> None:
        ids_map = {
            "㜝": "⿰女酓",
            "酓": "⿱今酉",
            "金": "⿱人⿻王丷",
            "低": "⿰亻氐",
            "眂": "⿰目氏",
            "䩦": "⿱攸革",
            "修": "⿰⿰亻丨⿱夂彡",
        }
        graph_lookup = {
            "女": [{"graph_raw": "女", "label_token": "fem(ina)", "abbreviation": "fem"}],
            "目": [{"graph_raw": "目", "label_token": "ocul(us)", "abbreviation": "ocul"}],
            "革": [{"graph_raw": "革", "label_token": "cori(um)", "abbreviation": "cori"}],
        }
        self.assertIsNone(
            build_semantic_evidence.resolve_semantic_from_parent_ids(
                character="金",
                parent_character="㜝",
                ids_map=ids_map,
                graph_lookup=graph_lookup,
            )
        )
        self.assertIsNone(
            build_semantic_evidence.resolve_semantic_from_parent_ids(
                character="眂",
                parent_character="低",
                ids_map=ids_map,
                graph_lookup=graph_lookup,
            )
        )
        self.assertIsNone(
            build_semantic_evidence.resolve_semantic_from_parent_ids(
                character="修",
                parent_character="䩦",
                ids_map=ids_map,
                graph_lookup=graph_lookup,
            )
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

    def test_refresh_curated_tex_entry_from_current_tex_replaces_stale_baseline(self) -> None:
        tex_entries = [
            {
                "id": "01-43",
                "head": {"characters": ["予"], "raw": r"\huge{予}"},
                "raw_block": "\\paragraph{X}\n野\n{\\large{\\textsuperscript{vic·}la}},",
            }
        ]
        entry = {
            "id": "01-43",
            "tex_entry": {
                "id": "01-43",
                "head": {"characters": ["予"], "raw": r"\huge{予}"},
                "raw_block": "\\paragraph{X}\n野\n{\\large{\\textsuperscript{xxx·}la}},",
            },
        }

        refreshed = build_semantic_evidence.refresh_curated_tex_entry_from_current_tex(
            entry,
            build_semantic_evidence.build_tex_entry_index(tex_entries),
        )

        self.assertIn(r"\textsuperscript{vic·}la", refreshed["tex_entry"]["raw_block"])
        self.assertNotIn(r"\textsuperscript{xxx·}la", refreshed["tex_entry"]["raw_block"])
        self.assertEqual(refreshed["entry_hierarchy"]["top_level_head"], "予")

    def test_canonicalize_semantic_assignment_from_inventory_rewrites_literal_component_label(self) -> None:
        candidate = {
            "character": "鼫",
            "semantic_assignment": {
                "abbreviation": "鼠",
                "semantic_component": "鼠",
                "position": "prefix-dot",
                "inventory_matches": [],
            },
            "transliteration_latex": r"{\large{\textsuperscript{鼠·}tak}},",
            "render_latex": r"鼫\n{\large{\textsuperscript{鼠·}tak}},",
        }
        graph_lookup = {
            "鼠": [{"graph_raw": "鼠", "label_token": "mus", "abbreviation": "mus"}],
        }

        changed = build_semantic_evidence.canonicalize_semantic_assignment_from_inventory(candidate, graph_lookup)

        self.assertTrue(changed)
        self.assertEqual(candidate["semantic_assignment"]["abbreviation"], "mus")
        self.assertEqual(candidate["transliteration_latex"], None)
        self.assertEqual(candidate["render_latex"], None)

    def test_resolve_generated_node_root_adds_ab_display_root(self) -> None:
        candidate = {
            "character": "布",
            "mc_resolution": {"display_forms": ["puH"]},
            "bs_gsr_rows": [],
            "transliteration_latex": r"{\large{pa\textsuperscript{˸lint}}},",
        }
        child = {
            "character": "怖",
            "mc_resolution": {"display_forms": ["phuH"]},
            "bs_gsr_rows": [],
            "transliteration_latex": r"{\large{\textsuperscript{cor·}pa}},",
        }
        resolved = build_semantic_evidence.resolve_generated_node_root(
            candidate,
            {"布": [child]},
            {"布": candidate, "怖": child},
            parent_root="pa",
            primary_packet_token=None,
            packet_tokens=set(),
        )
        self.assertEqual(resolved["division_class"], "a")
        self.assertEqual(resolved["display_root"], r"p\textoverset{a}{a}")

    def test_repair_candidate_parent_cycles_demotes_mutual_cycle_to_top_level(self) -> None:
        entry = {
            "proposed_additions": [
                {
                    "character": "亡",
                    "hierarchy_assignment": {
                        "status": "assigned-to-top-level",
                        "parent_character": "亡",
                    },
                },
                {
                    "character": "詤",
                    "hierarchy_assignment": {
                        "status": "assigned-to-candidate-node",
                        "parent_character": "㡃",
                    },
                },
                {
                    "character": "㡃",
                    "hierarchy_assignment": {
                        "status": "assigned-to-candidate-node",
                        "parent_character": "詤",
                    },
                },
            ]
        }

        build_semantic_evidence.repair_candidate_parent_cycles(entry, "亡")

        by_character = {candidate["character"]: candidate for candidate in entry["proposed_additions"]}
        self.assertEqual(
            by_character["詤"]["hierarchy_assignment"]["status"],
            "assigned-to-top-level",
        )
        self.assertEqual(
            by_character["詤"]["hierarchy_assignment"]["parent_character"],
            "亡",
        )
        self.assertEqual(
            by_character["㡃"]["hierarchy_assignment"]["status"],
            "assigned-to-top-level",
        )
        self.assertEqual(
            by_character["㡃"]["hierarchy_assignment"]["parent_character"],
            "亡",
        )

    def test_missing_series_same_gsr_fallback_marks_unresolved_variant(self) -> None:
        entry = {
            "id": "04-45",
            "packet_kind": "missing_series",
            "schuessler": {"k_tokens": ["943"]},
            "proposed_additions": [
                {
                    "character": "才",
                    "mand2mc_rows": [{"gsr": "0943a"}],
                    "bs_gsr_rows": [{"gsr": "0943a", "oc_bs": "*dzˤə"}],
                    "shengfu_character_rows": [{"phonetic_component": "才", "oc_syllable": "zɯ̠"}],
                },
                {
                    "character": "在",
                    "mand2mc_rows": [{"gsr": "0943i"}],
                    "bs_gsr_rows": [],
                    "shengfu_character_rows": [{"phonetic_component": "才", "oc_syllable": "zɯ̠ʔ"}],
                    "wiktionary_validation": {"available": False, "han_compound": None, "han_compounds": []},
                },
            ],
            "resolved_series_root": {"root": "tsy", "display_root": "tsy"},
        }
        enriched = build_semantic_evidence.enrich_curated_entry_with_ids(entry, {}, {}, {})
        variant = next(candidate for candidate in enriched["proposed_additions"] if candidate["character"] == "在")
        self.assertEqual(variant["semantic_assignment"]["position"], "none")
        self.assertEqual(variant["semantic_assignment"]["source"], "same_series_variant")
        self.assertEqual(variant["transliteration_latex"], r"{\large{tsy}},")

    def test_resolve_parent_display_root_falls_back_to_series_root_when_parent_node_root_missing(self) -> None:
        entry = {
            "packet_kind": "missing_series",
            "resolved_series_root": {"root": "koṅ", "display_root": "koṅ"},
        }
        parent = {"character": "廾", "resolved_node_root": None}
        child = {
            "character": "共",
            "hierarchy_assignment": {
                "status": "assigned-to-candidate-node",
                "parent_character": "廾",
            },
        }
        root = build_semantic_evidence.resolve_parent_display_root_for_candidate(
            entry,
            child,
            {"廾": parent, "共": child},
        )
        self.assertEqual(root, "koṅ")

    def test_resolve_parent_display_root_uses_series_root_for_packet_head_parent(self) -> None:
        entry = {
            "packet_kind": "missing_series",
            "resolved_series_root": {"root": "quaṅ", "display_root": "quaṅ"},
            "proposed_additions": [{"character": "皇"}],
        }
        parent = {"character": "皇", "resolved_node_root": {"root": "gaṅ", "display_root": "gaṅ"}}
        child = {
            "character": "徨",
            "hierarchy_assignment": {
                "status": "assigned-to-candidate-node",
                "parent_character": "皇",
            },
        }
        root = build_semantic_evidence.resolve_parent_display_root_for_candidate(
            entry,
            child,
            {"皇": parent, "徨": child},
        )
        self.assertEqual(root, "quaṅ")


if __name__ == "__main__":
    unittest.main()
