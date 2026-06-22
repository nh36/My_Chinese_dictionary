from __future__ import annotations

import sys
import unittest


ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import fetch_wiktionary_component_roles  # noqa: E402


class FetchWiktionaryComponentRolesTests(unittest.TestCase):
    def test_parse_han_compound_template(self) -> None:
        text = "{{Han compound|日|青|c1=s|c2=p|t1=sun|ls=psc}}"
        parsed = fetch_wiktionary_component_roles.parse_han_compound_template(text)
        self.assertIsNotNone(parsed)
        assert parsed is not None
        self.assertEqual(parsed["semantic_components"], ["日"])
        self.assertEqual(parsed["phonetic_components"], ["青"])

    def test_parse_non_phonosemantic_template(self) -> None:
        text = "{{Han compound|夂|口|ls=ic|t1=sole of foot}}"
        parsed = fetch_wiktionary_component_roles.parse_han_compound_template(text)
        self.assertIsNotNone(parsed)
        assert parsed is not None
        self.assertEqual(parsed["semantic_components"], [])
        self.assertEqual(parsed["phonetic_components"], [])

    def test_parse_all_han_compounds(self) -> None:
        text = "{{Han compound|夂|口|ls=ic}}{{Han compound|酓|欠|ls=psc|c1=p|c2=s}}"
        parsed = fetch_wiktionary_component_roles.parse_all_han_compound_templates(text)
        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[1]["semantic_components"], ["欠"])

    def test_parse_han_compound_template_prefers_alt_graph(self) -> None:
        text = "{{Han compound|帽|由|alt1=冃|c1=s|c2=p|ls=psc}}"
        parsed = fetch_wiktionary_component_roles.parse_han_compound_template(text)
        self.assertIsNotNone(parsed)
        assert parsed is not None
        self.assertEqual(parsed["positional_components"], ["帽", "由"])
        self.assertEqual(parsed["positional_components_raw"], ["帽", "由"])
        self.assertEqual(parsed["semantic_components"], ["帽"])
        self.assertEqual(parsed["phonetic_components"], ["由"])


if __name__ == "__main__":
    unittest.main()
