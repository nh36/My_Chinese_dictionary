from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import audit_generated_nonlatin_semantics  # noqa: E402


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


if __name__ == "__main__":
    unittest.main()
