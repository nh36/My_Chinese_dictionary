from __future__ import annotations

import sys
import unittest


ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_integrated_semantic_components  # noqa: E402
import semantic_label_normalization  # noqa: E402


class BuildIntegratedSemanticComponentsTests(unittest.TestCase):
    def test_extract_latin_tokens_ignores_image_macros(self) -> None:
        text = r"{\large{\textsuperscript{hom·}qay}}, {\large{tak\textsuperscript{˸\raisebox{0.1ex}{\includegraphics[height=1.6ex]{U+2349A.png}}}}},"
        tokens = build_integrated_semantic_components.iter_semantic_tokens(text)
        self.assertIn("hom", tokens)
        self.assertNotIn("includegraphics", tokens)

    def test_semantic_key_uses_graph_and_abbreviation(self) -> None:
        item = {"graph_raw": "木", "abbreviation": "arb"}
        self.assertEqual(build_integrated_semantic_components.semantic_key(item), ("木", "arb"))

    def test_merge_inventories_uses_explicit_aliases_but_blocks_ambiguous_aliases(self) -> None:
        base_items = [
            {
                "graph_raw": "田",
                "abbreviation": "ager",
                "label_token": "ager",
                "label_notes": None,
                "scope": "general",
                "only_in": [],
                "duplicate_graph_status": None,
                "note": None,
                "comments": [],
                "start_line": 1,
                "end_line": 1,
                "raw_latex": r"\item 田 ager",
            },
            {
                "graph_raw": "田",
                "abbreviation": "forn",
                "label_token": "forn(us)",
                "label_notes": "(only in 盧)",
                "scope": "only_in",
                "only_in": ["盧"],
                "duplicate_graph_status": "intentional_scoped_duplicate",
                "note": "Same visible graph as 田/ager, but different semantic label and restricted use.",
                "comments": [],
                "start_line": 2,
                "end_line": 2,
                "raw_latex": r"\item 田 forn(us) (only in 盧)",
            },
            {
                "graph_raw": "口",
                "abbreviation": "or",
                "label_token": "(os,) or(is)",
                "label_notes": None,
                "scope": "general",
                "only_in": [],
                "duplicate_graph_status": None,
                "note": None,
                "comments": [],
                "start_line": 3,
                "end_line": 3,
                "raw_latex": r"\item 口 (os,) or(is)",
            },
            {
                "graph_raw": "骨",
                "abbreviation": "oss",
                "label_token": "(os,) oss(is)",
                "label_notes": None,
                "scope": "general",
                "only_in": [],
                "duplicate_graph_status": None,
                "note": None,
                "comments": [],
                "start_line": 4,
                "end_line": 4,
                "raw_latex": r"\item 骨 (os,) oss(is)",
            },
            {
                "graph_raw": "牛",
                "abbreviation": "bos",
                "label_token": "bos",
                "label_notes": None,
                "scope": "general",
                "only_in": [],
                "duplicate_graph_status": None,
                "note": None,
                "comments": [],
                "start_line": 5,
                "end_line": 5,
                "raw_latex": r"\item 牛 bos",
            },
            {
                "graph_raw": "犛",
                "abbreviation": "grunn",
                "label_token": "(bos) grunn(iens)",
                "label_notes": "(only in 斄)",
                "scope": "only_in",
                "only_in": ["斄"],
                "duplicate_graph_status": None,
                "note": None,
                "comments": [],
                "start_line": 6,
                "end_line": 6,
                "raw_latex": r"\item 犛 (bos) grunn(iens) (only in 斄)",
            },
        ]
        current_inventory = {
            "source_path": "main.tex",
            "summary": {"item_count": len(base_items)},
            "items": base_items,
        }
        pilot_inventory = {
            "source_path": "pilot.tex",
            "summary": {"item_count": len(base_items)},
            "items": base_items,
        }
        current_entries = [
            {
                "raw_block": r"{\large{\textsuperscript{ag·}qay}} {\large{qoy{\textsuperscript{·os}}}}",
            }
        ]
        curated_entries = [
            {
                "proposed_additions": [
                    {
                        "transliteration_latex": r"{\large{\textsuperscript{bos·}la}},",
                        "render_latex": r"牥 {\large{\textsuperscript{bos·}la}},",
                    }
                ]
            }
        ]
        normalization_config = semantic_label_normalization.load_normalization_config(
            ROOT / "data/semantic_components/semantic_aliases.json"
        )

        merged = build_integrated_semantic_components.merge_inventories(
            current_inventory,
            pilot_inventory,
            current_entries,
            curated_entries,
            normalization_config,
        )

        self.assertEqual(merged["entry_aliases"], ["ag"])
        self.assertIn("os", merged["blocked_used_abbreviations"])
        self.assertNotIn("bos", merged["blocked_used_abbreviations"])
        self.assertEqual(merged["summary"]["duplicate_graph_conflict_count"], 0)
        self.assertEqual(merged["summary"]["intentional_scoped_duplicate_graph_count"], 1)


if __name__ == "__main__":
    unittest.main()
