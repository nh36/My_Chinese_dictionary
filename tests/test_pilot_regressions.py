from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import evaluate_pilot_render  # noqa: E402


class PilotRegressionTests(unittest.TestCase):
    def test_current_pilot_readiness_is_ready(self) -> None:
        entries = evaluate_pilot_render.load_curated_entries(ROOT / "data/entries/curation")
        rendered = (ROOT / "build/generated_curated_series_sample.tex").read_text(encoding="utf-8")
        metrics = evaluate_pilot_render.evaluate_entries(entries, rendered)
        self.assertEqual(metrics["overall_status"], "ready")

    def test_current_curated_entries_have_full_semantic_and_transliteration_coverage(self) -> None:
        entries = evaluate_pilot_render.load_curated_entries(ROOT / "data/entries/curation")
        proposed = [c for e in entries for c in e.get("proposed_additions", [])]
        self.assertTrue(proposed)
        self.assertTrue(all(c.get("semantic_assignment") for c in proposed))
        self.assertTrue(all(c.get("transliteration_latex") for c in proposed))
        self.assertTrue(all(c.get("render_latex") for c in proposed))


if __name__ == "__main__":
    unittest.main()
