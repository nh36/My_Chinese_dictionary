from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import semantic_label_normalization  # noqa: E402


class SemanticLabelNormalizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = semantic_label_normalization.load_normalization_config(
            ROOT / "data/semantic_components/semantic_aliases.json"
        )
        cls.canonical_index = {
            "ager": [{"graph_raw": "田", "abbreviation": "ager"}],
            "or": [{"graph_raw": "口", "abbreviation": "or"}],
            "oss": [{"graph_raw": "骨", "abbreviation": "oss"}],
            "bos": [{"graph_raw": "牛", "abbreviation": "bos"}],
            "grunn": [{"graph_raw": "犛", "abbreviation": "grunn"}],
        }

    def test_classify_semantic_label_prefers_canonical_before_blocked_alias(self) -> None:
        classified = semantic_label_normalization.classify_semantic_label(
            "bos",
            self.canonical_index,
            self.config,
        )
        self.assertEqual(classified["classification"], "canonical")
        self.assertEqual(classified["canonical_abbreviation"], "bos")

    def test_classify_semantic_label_handles_alias_blocked_and_placeholder(self) -> None:
        self.assertEqual(
            semantic_label_normalization.classify_semantic_label("ag", self.canonical_index, self.config)[
                "classification"
            ],
            "explicit_alias",
        )
        blocked = semantic_label_normalization.classify_semantic_label("os", self.canonical_index, self.config)
        self.assertEqual(blocked["classification"], "blocked_ambiguous_alias")
        self.assertEqual(blocked["targets"], ["or", "oss"])
        self.assertEqual(
            semantic_label_normalization.classify_semantic_label("xxx", self.canonical_index, self.config)[
                "classification"
            ],
            "placeholder",
        )

    def test_old_heuristic_matching_exposes_problematic_forms(self) -> None:
        self.assertTrue(semantic_label_normalization.matches_old_heuristic("bos", "(bos) grunn(iens)"))
        self.assertTrue(semantic_label_normalization.matches_old_heuristic("manu", "man(us)"))
        self.assertTrue(semantic_label_normalization.matches_old_heuristic("draco", "(draco), dracon(is)"))


if __name__ == "__main__":
    unittest.main()
