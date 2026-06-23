from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import audit_generated_nonlatin_semantics  # noqa: E402
import json  # noqa: E402


class AuditGeneratedNonLatinSemanticsTests(unittest.TestCase):
    def test_classify_case_prefers_existing_variant(self) -> None:
        graph_lookup = {
            "虍": [{"graph_raw": "虍", "abbreviation": "tigr"}],
        }
        result = audit_generated_nonlatin_semantics.classify_case(
            {
                "semantic_component": "虎",
                "template_alt_graph": None,
            },
            graph_lookup,
        )
        self.assertEqual(result["classification"], "existing_inventory_variant")
        self.assertEqual(result["target_abbreviation"], "tigr")

    def test_classify_case_uses_template_alt_graph(self) -> None:
        result = audit_generated_nonlatin_semantics.classify_case(
            {
                "semantic_component": "帽",
                "template_alt_graph": "冃",
            },
            {},
        )
        self.assertEqual(result["classification"], "template_alt_graph")
        self.assertEqual(result["target_graph"], "冃")

    def test_current_unresolved_generated_semantics_match_approved_hold_set(self) -> None:
        inventory = json.loads(
            (ROOT / "data/derived/nonlatin_generated_semantics.json").read_text(encoding="utf-8")
        )
        components = {row["semantic_component"] for row in inventory["components"]}
        self.assertFalse({"一", "同", "坴", "𦰩"} & components)
        self.assertTrue(components)
        self.assertTrue(
            {
                "八",
                "曰",
                "㯻",
                "䖵",
                "殺",
                "𣒚",
                "嗇",
                "𤼽",
                "庚",
            }.isdisjoint(components)
        )


if __name__ == "__main__":
    unittest.main()
