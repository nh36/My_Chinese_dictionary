from __future__ import annotations

import sys
import unittest


ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_integrated_semantic_components  # noqa: E402


class BuildIntegratedSemanticComponentsTests(unittest.TestCase):
    def test_extract_latin_tokens_ignores_image_macros(self) -> None:
        text = r"{\large{\textsuperscript{hom·}qay}}, {\large{tak\textsuperscript{˸\raisebox{0.1ex}{\includegraphics[height=1.6ex]{U+2349A.png}}}}},"
        tokens = build_integrated_semantic_components.iter_semantic_tokens(text)
        self.assertIn("hom", tokens)
        self.assertNotIn("includegraphics", tokens)

    def test_semantic_key_uses_graph_and_abbreviation(self) -> None:
        item = {"graph_raw": "木", "abbreviation": "arb"}
        self.assertEqual(build_integrated_semantic_components.semantic_key(item), ("木", "arb"))

    def test_match_used_abbreviations_handles_unique_prefix_and_missing(self) -> None:
        forms_by_key = {
            ("手", "man"): {"man", "manus"},
            ("土", "terr"): {"terr", "terra"},
        }
        matched, ambiguous, unmatched = build_integrated_semantic_components.match_used_abbreviations(
            {"manu", "ter", "xxx"}, forms_by_key
        )

        self.assertEqual(matched["manu"], ("手", "man"))
        self.assertEqual(matched["ter"], ("土", "terr"))
        self.assertEqual(ambiguous, {})
        self.assertEqual(unmatched, {"xxx"})


if __name__ == "__main__":
    unittest.main()
