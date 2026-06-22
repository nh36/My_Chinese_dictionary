from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SemanticLabelNormalizationAcceptanceTests(unittest.TestCase):
    def test_no_blocked_or_placeholder_semantic_labels_remain_in_authoritative_or_generated_outputs(self) -> None:
        paths = [
            ROOT / "main.tex",
            ROOT / "key references/My_Chinese_dictionary/main.tex",
            ROOT / "build/generated_integrated_dictionary.tex",
        ]
        banned = [
            r"\textsuperscript{·os}",
            r"\textsuperscript{:os}",
            r"\textsuperscript{os·}",
            r"\textsuperscript{os:}",
            r"\textsuperscript{·den}",
            r"\textsuperscript{:den}",
            r"\textsuperscript{den·}",
            r"\textsuperscript{den:}",
            r"\textsuperscript{xxx·}",
            r"\textsuperscript{xxx:}",
            r"\textsuperscript{·xxx}",
            r"\textsuperscript{:xxx}",
        ]
        offenders = []
        for path in paths:
            text = path.read_text(encoding="utf-8")
            for token in banned:
                if token in text:
                    offenders.append((str(path), token))
        self.assertEqual(offenders, [])

    def test_semantic_inventory_preserves_distinct_rows_and_scoped_duplicate(self) -> None:
        inventory = json.loads((ROOT / "data/current_semantic_components.json").read_text(encoding="utf-8"))
        rows = {(item.get("graph_raw"), item.get("abbreviation")): item for item in inventory["items"]}

        self.assertIn(("口", "or"), rows)
        self.assertIn(("骨", "oss"), rows)
        self.assertIn(("牛", "bos"), rows)
        self.assertIn(("犛", "grunn"), rows)
        self.assertIn(("疒", "infirm"), rows)
        self.assertIn(("韋", "alut"), rows)
        self.assertIn(("廾", "biman"), rows)
        self.assertIn(("身", "corp"), rows)
        self.assertIn(("殳", "hast"), rows)
        self.assertIn(("鹵", "sal"), rows)
        self.assertIn(("誩", "iurg"), rows)
        self.assertIn(("晶", "splend"), rows)
        self.assertIn(("辛", "acr"), rows)
        self.assertIn(("臤", "firm"), rows)
        self.assertIn(("鼠", "rod"), rows)
        self.assertIn(("矛", "iacul"), rows)
        self.assertIn(("匚", "caps"), rows)
        self.assertIn(("缶", "cad"), rows)
        self.assertIn(("尢", "claud"), rows)
        self.assertIn(("尾", "caud"), rows)
        self.assertIn(("囟", "fontan"), rows)
        self.assertIn(("工", "fabr"), rows)
        self.assertIn(("己", "ipse"), rows)
        self.assertIn(("隶", "nex"), rows)
        self.assertIn(("申", "tend"), rows)
        self.assertIn(("民", "pleb"), rows)
        self.assertIn(("川", "fluvi"), rows)
        self.assertIn(("血", "sangu"), rows)
        self.assertIn(("須", "barb"), rows)
        self.assertIn(("舌", "lingu"), rows)
        self.assertIn(("鬥", "pugn"), rows)
        self.assertIn(("光", "lux"), rows)
        self.assertIn(("音", "son"), rows)
        self.assertIn(("帛", "pann"), rows)
        self.assertIn(("黽", "amph"), rows)
        self.assertIn(("亠", "pav"), rows)
        self.assertIn(("田", "ager"), rows)
        self.assertIn(("田", "forn"), rows)
        self.assertEqual(rows[("田", "forn")]["scope"], "only_in")
        self.assertEqual(rows[("田", "forn")]["only_in"], ["盧"])
        self.assertEqual(rows[("田", "forn")]["duplicate_graph_status"], "intentional_scoped_duplicate")
        self.assertEqual(rows[("疒", "infirm")]["label_token"], "infirm(itas)")

    def test_integrated_semantic_output_has_no_blocked_or_placeholder_usage(self) -> None:
        integrated = json.loads(
            (ROOT / "data/semantic_components/integrated_semantic_components.json").read_text(encoding="utf-8")
        )

        self.assertEqual(integrated["summary"]["ambiguous_used_abbreviation_count"], 0)
        self.assertEqual(integrated["summary"]["duplicate_graph_conflict_count"], 0)
        self.assertEqual(integrated["summary"]["intentional_scoped_duplicate_graph_count"], 1)
        self.assertEqual(integrated["blocked_used_abbreviations"], {})
        self.assertEqual(integrated["placeholder_used_abbreviations"], {})
        self.assertEqual(integrated["missing_used_abbreviations"], [])

    def test_recently_added_semantic_labels_are_used_in_live_entries(self) -> None:
        integrated = json.loads(
            (ROOT / "data/semantic_components/integrated_semantic_components.json").read_text(encoding="utf-8")
        )
        by_abbreviation = {
            item.get("abbreviation"): item for item in integrated["items"] if item.get("abbreviation")
        }
        expected_inventory = {
            "alut": "韋",
            "biman": "廾",
            "cad": "缶",
            "fontan": "囟",
            "caud": "尾",
            "fabr": "工",
            "ipse": "己",
            "nex": "隶",
            "iurg": "誩",
            "splend": "晶",
        }
        for abbreviation, graph in expected_inventory.items():
            self.assertIn(abbreviation, by_abbreviation)
            self.assertEqual(by_abbreviation[abbreviation]["graph_raw"], graph)
            self.assertTrue(by_abbreviation[abbreviation]["used_in_integrated_dictionary"])

        usage = {abbreviation: [] for abbreviation in expected_inventory}
        for path in (ROOT / "data/entries/curation").glob("*.json"):
            entry = json.loads(path.read_text(encoding="utf-8"))
            for candidate in entry.get("proposed_additions", []):
                abbreviation = (candidate.get("semantic_assignment") or {}).get("abbreviation")
                if abbreviation in usage:
                    usage[abbreviation].append((entry["id"], candidate["character"]))

        for abbreviation, hits in usage.items():
            self.assertTrue(hits, msg=f"{abbreviation} is listed in the inventory but unused in curation data")

    def test_audit_output_confirms_bos_review_and_no_live_blocked_or_placeholder_usage(self) -> None:
        audit = json.loads(
            (ROOT / "data/semantic_components/semantic_label_normalization_audit.json").read_text(encoding="utf-8")
        )

        blocked_labels = {occurrence["label"] for occurrence in audit["blocked_occurrences"]}
        self.assertEqual(blocked_labels, set())
        self.assertTrue(audit["infirm_occurrences"])
        self.assertTrue(audit["bos_occurrences"])
        self.assertEqual(audit["placeholder_occurrences"], [])
        self.assertFalse(
            [
                occurrence
                for occurrence in audit["bos_occurrences"]
                if occurrence.get("semantic_component") not in {None, "牛"}
            ]
        )
        self.assertIn(
            {
                "graph": "犛",
                "abbreviation": "grunn",
                "expanded_latin": "(bos) grunn(iens)",
                "candidate_alias": "bos",
                "status": "blocked_ambiguous_alias",
                "currently_used": True,
            },
            audit["unsafe_alias_candidates"],
        )


if __name__ == "__main__":
    unittest.main()
