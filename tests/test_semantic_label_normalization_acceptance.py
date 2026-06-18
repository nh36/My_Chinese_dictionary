from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SemanticLabelNormalizationAcceptanceTests(unittest.TestCase):
    def test_no_os_superscript_labels_remain_in_authoritative_or_generated_outputs(self) -> None:
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
        self.assertIn(("田", "ager"), rows)
        self.assertIn(("田", "forn"), rows)
        self.assertEqual(rows[("田", "forn")]["scope"], "only_in")
        self.assertEqual(rows[("田", "forn")]["only_in"], ["盧"])
        self.assertEqual(rows[("田", "forn")]["duplicate_graph_status"], "intentional_scoped_duplicate")

    def test_integrated_semantic_output_tracks_blocked_and_placeholder_labels(self) -> None:
        integrated = json.loads(
            (ROOT / "data/semantic_components/integrated_semantic_components.json").read_text(encoding="utf-8")
        )

        self.assertEqual(integrated["summary"]["ambiguous_used_abbreviation_count"], 0)
        self.assertEqual(integrated["summary"]["duplicate_graph_conflict_count"], 0)
        self.assertEqual(integrated["summary"]["intentional_scoped_duplicate_graph_count"], 1)
        self.assertNotIn("os", integrated["blocked_used_abbreviations"])
        self.assertNotIn("bos", integrated["blocked_used_abbreviations"])
        self.assertIn("den", integrated["blocked_used_abbreviations"])
        self.assertIn("xxx", integrated["placeholder_used_abbreviations"])
        self.assertEqual(integrated["missing_used_abbreviations"], [])

    def test_audit_output_confirms_bos_review_and_den_block(self) -> None:
        audit = json.loads(
            (ROOT / "data/semantic_components/semantic_label_normalization_audit.json").read_text(encoding="utf-8")
        )

        blocked_labels = {occurrence["label"] for occurrence in audit["blocked_occurrences"]}
        self.assertEqual(blocked_labels, {"den"})
        self.assertTrue(audit["infirm_occurrences"])
        self.assertTrue(audit["bos_occurrences"])
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
