from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import hierarchy_utils


DEFAULT_INPUT_DIR = "data/entries/curation"
DEFAULT_TEX_PATH = "build/generated_curated_series_sample.tex"
DEFAULT_REPORT_OUT = "reports/pilot_render_readiness.md"
TEXTSUP_RE = re.compile(r"\\textsuperscript\{[^}]*\}")


def load_curated_entries(input_dir: Path) -> list[dict[str, Any]]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(input_dir.glob("*.json"))
    ]


def evaluate_entries(entries: list[dict[str, Any]], rendered_tex: str) -> dict[str, Any]:
    proposed_additions = [
        candidate
        for entry in entries
        for candidate in entry.get("proposed_additions", [])
    ]
    total_proposed = len(proposed_additions)

    semantic_ready = sum(1 for candidate in proposed_additions if candidate.get("semantic_assignment"))
    placement_ready = sum(
        1
        for candidate in proposed_additions
        if (candidate.get("semantic_assignment") or {}).get("position")
    )
    transliteration_ready = sum(1 for candidate in proposed_additions if candidate.get("transliteration_latex"))
    render_ready = sum(1 for candidate in proposed_additions if candidate.get("render_latex"))
    packets_with_existing_baseline = sum(1 for entry in entries if entry.get("tex_entry"))
    provisional_marker_count = rendered_tex.count("[provisional draft")
    proposed_marker_count = rendered_tex.count("[proposed additions")
    baseline_relation_colon_count = 0
    for line in rendered_tex.splitlines():
        if "{\\large" not in line and "{\\Large" not in line:
            continue
        stripped = TEXTSUP_RE.sub("", line)
        if ":" in stripped:
            baseline_relation_colon_count += stripped.count(":")
    generated_subseries_heads = []
    rendered_subseries_heads = 0
    for entry in entries:
        candidate_children = hierarchy_utils.collect_candidate_children(entry)
        for candidate in entry.get("proposed_additions", []):
            resolved_node_root = (candidate.get("resolved_node_root") or {}).get("root")
            if not candidate_children.get(candidate["character"]) or not resolved_node_root:
                continue
            generated_subseries_heads.append(candidate["character"])
            item_token = rf"\item {{\Large{{{candidate['character']}}}"
            equals_token = rf"= {{\large{{{resolved_node_root}}}}},"
            position = rendered_tex.find(item_token)
            if position != -1 and equals_token in rendered_tex[position : position + 500]:
                rendered_subseries_heads += 1

    return {
        "packet_count": len(entries),
        "total_proposed_additions": total_proposed,
        "semantic_ready": semantic_ready,
        "placement_ready": placement_ready,
        "transliteration_ready": transliteration_ready,
        "render_ready": render_ready,
        "packets_with_existing_baseline": packets_with_existing_baseline,
        "provisional_marker_count": provisional_marker_count,
        "proposed_marker_count": proposed_marker_count,
        "baseline_relation_colon_count": baseline_relation_colon_count,
        "generated_subseries_head_count": len(generated_subseries_heads),
        "rendered_subseries_head_count": rendered_subseries_heads,
        "overall_status": (
            "ready"
            if total_proposed
            and semantic_ready == total_proposed
            and placement_ready == total_proposed
            and transliteration_ready == total_proposed
            and render_ready == total_proposed
            and provisional_marker_count == 0
            and baseline_relation_colon_count == 0
            and rendered_subseries_heads == len(generated_subseries_heads)
            else "not ready"
        ),
    }


def render_report(metrics: dict[str, Any]) -> str:
    lines = [
        "# Pilot render readiness",
        "",
        f"- Overall status: **{metrics['overall_status']}**",
        f"- Curated packet count: {metrics['packet_count']}",
        f"- Proposed additions under review: {metrics['total_proposed_additions']}",
        "",
        "| Check | Ready | Total |",
        "| --- | ---: | ---: |",
        f"| Semantic assignment present | {metrics['semantic_ready']} | {metrics['total_proposed_additions']} |",
        f"| Semantic placement present | {metrics['placement_ready']} | {metrics['total_proposed_additions']} |",
        f"| Transliteration LaTeX present | {metrics['transliteration_ready']} | {metrics['total_proposed_additions']} |",
        f"| Candidate render LaTeX present | {metrics['render_ready']} | {metrics['total_proposed_additions']} |",
        f"| Relation `:` kept out of baseline text | {metrics['total_proposed_additions'] if metrics['baseline_relation_colon_count'] == 0 else 0} | {metrics['total_proposed_additions']} |",
        f"| Generated subseries heads rendered with `=` root lines | {metrics['rendered_subseries_head_count']} | {metrics['generated_subseries_head_count']} |",
        "",
        "## Render markers",
        "",
        f"- Existing-baseline packets: {metrics['packets_with_existing_baseline']}",
        f"- `[provisional draft ...]` markers in rendered review TeX: {metrics['provisional_marker_count']}",
        f"- `[proposed additions ...]` markers in rendered review TeX: {metrics['proposed_marker_count']}",
        f"- Baseline relation-colon count in rendered large-text lines: {metrics['baseline_relation_colon_count']}",
        "",
        "## Interpretation",
        "",
    ]

    if metrics["overall_status"] == "ready":
        lines.append("- The current pilot meets the structural readiness checks encoded by this evaluator.")
    else:
        lines.extend(
            [
                "- The current pilot is still structurally incomplete for side-by-side scholarly review.",
                "- In particular, the proposed additions still need explicit semantic assignments, side/position decisions, abstract transliteration forms, and rendered LaTeX blocks comparable to `main.tex`.",
            ]
        )

    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate whether a rendered pilot is structurally comparable to main.tex.")
    parser.add_argument("--input-dir", default=DEFAULT_INPUT_DIR)
    parser.add_argument("--tex-path", default=DEFAULT_TEX_PATH)
    parser.add_argument("--report-out", default=DEFAULT_REPORT_OUT)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    entries = load_curated_entries(Path(args.input_dir))
    rendered_tex = Path(args.tex_path).read_text(encoding="utf-8")
    report = render_report(evaluate_entries(entries, rendered_tex))
    Path(args.report_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.report_out).write_text(report, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
