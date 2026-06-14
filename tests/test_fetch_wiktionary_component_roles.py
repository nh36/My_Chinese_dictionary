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


if __name__ == "__main__":
    unittest.main()
