from __future__ import annotations

import sys
import unittest


ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import evaluate_pilot_render  # noqa: E402


class EvaluatePilotRenderTests(unittest.TestCase):
    def test_evaluator_flags_not_ready_when_semantics_missing(self) -> None:
        entries = [
            {
                "tex_entry": None,
                "proposed_additions": [
                    {
                        "character": "各",
                    }
                ],
            }
        ]
        metrics = evaluate_pilot_render.evaluate_entries(entries, "[provisional draft]")
        self.assertEqual(metrics["overall_status"], "not ready")
        self.assertEqual(metrics["semantic_ready"], 0)
        self.assertEqual(metrics["provisional_marker_count"], 1)

    def test_evaluator_ready_case(self) -> None:
        entries = [
            {
                "tex_entry": {"id": "18-18"},
                "proposed_additions": [
                    {
                        "character": "加",
                        "semantic_assignment": {"abbreviation": "arb", "position": "prefix-dot"},
                        "transliteration_latex": r"{\textsuperscript{arb·}}kay",
                        "render_latex": r"加 {\large{\textsuperscript{arb·}kay}}, \textit{kae};",
                    }
                ],
            }
        ]
        metrics = evaluate_pilot_render.evaluate_entries(entries, "rendered")
        self.assertEqual(metrics["overall_status"], "ready")
        self.assertEqual(metrics["semantic_ready"], 1)


if __name__ == "__main__":
    unittest.main()
