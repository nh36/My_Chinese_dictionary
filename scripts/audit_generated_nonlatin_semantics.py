from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import build_semantic_evidence


DEFAULT_CURATION_DIR = "data/entries/curation"
DEFAULT_SEMANTIC_INVENTORY = "data/current_semantic_components.json"
DEFAULT_IDS_PATH = "data/raw/cjkvi_ids.txt"
DEFAULT_JSON_OUT = "data/derived/nonlatin_generated_semantics.json"
DEFAULT_REPORT_OUT = "reports/nonlatin_generated_semantics.md"

EXISTING_VARIANT_PROPOSALS = {
    "虎": {
        "target_graph": "虍",
        "reason": "Full-form tiger graph vs the radical-form graph already labeled in the inventory.",
    },
    "歺": {
        "target_graph": "歹",
        "reason": "Death-radical variant that should be reviewed against the existing 歹 inventory row.",
    },
}

RESEARCH_HEAVY_GRAPHS = {
    "𣒚",
    "䖵",
    "𤼽",
    "㯻",
    "嗇",
    "殺",
    "𦰩",
}

NEEDS_HUMAN_REVIEW_GRAPHS = {
    "𭯍",
}


def classify_case(
    row: dict[str, Any],
    graph_lookup: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    component = row.get("semantic_component")
    template_alt = row.get("template_alt_graph")
    direct_inventory_matches = graph_lookup.get(component or "", [])
    if direct_inventory_matches:
        target = direct_inventory_matches[0]
        return {
            "classification": "direct_inventory_match",
            "proposal": f"Use existing inventory label `{target['abbreviation']}` for `{component}`.",
            "target_graph": target["graph_raw"],
            "target_abbreviation": target["abbreviation"],
        }

    if component in EXISTING_VARIANT_PROPOSALS:
        target_graph = EXISTING_VARIANT_PROPOSALS[component]["target_graph"]
        matches = graph_lookup.get(target_graph, [])
        abbreviation = matches[0]["abbreviation"] if matches else None
        return {
            "classification": "existing_inventory_variant",
            "proposal": (
                f"Review `{component}` as a variant of `{target_graph}` and, if accepted, "
                f"reuse `{abbreviation}`."
            ),
            "target_graph": target_graph,
            "target_abbreviation": abbreviation,
            "reason": EXISTING_VARIANT_PROPOSALS[component]["reason"],
        }

    if template_alt and template_alt != component:
        matches = graph_lookup.get(template_alt, [])
        abbreviation = matches[0]["abbreviation"] if matches else None
        return {
            "classification": "template_alt_graph",
            "proposal": (
                f"Prefer template alt graph `{template_alt}` over gloss-like token `{component}`; "
                + (
                    f"it can then reuse existing label `{abbreviation}`."
                    if abbreviation
                    else "it then still needs a new Latin label."
                )
            ),
            "target_graph": template_alt,
            "target_abbreviation": abbreviation,
        }

    if component in RESEARCH_HEAVY_GRAPHS:
        return {
            "classification": "research_compound_graph",
            "proposal": (
                f"Investigate whether `{component}` should stay a distinct semantic graph or be reduced "
                "to one of its subcomponents before assigning a Latin label."
            ),
        }

    if component in NEEDS_HUMAN_REVIEW_GRAPHS:
        return {
            "classification": "needs_human_review",
            "proposal": (
                f"Keep `{component}` out of the canonical semantic inventory until a scholar can confirm "
                "whether it is semantic at all; current evidence suggests a rare phonetic component."
            ),
        }

    return {
        "classification": "new_latin_label_needed",
        "proposal": (
            f"Keep `{component}` visible for now and add a new canonical Latin label for this graph "
            "once the inventory decision is reviewed."
        ),
    }


def load_entries(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(entry_path.read_text(encoding="utf-8"))
        for entry_path in sorted(path.glob("*.json"))
    ]


def build_inventory(
    entries: list[dict[str, Any]],
    semantic_inventory: dict[str, Any],
    ids_map: dict[str, str],
) -> dict[str, Any]:
    graph_lookup = build_semantic_evidence.build_inventory_graph_lookup(semantic_inventory)
    cases: list[dict[str, Any]] = []
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for entry in entries:
        for candidate in entry.get("proposed_additions", []):
            semantic_assignment = candidate.get("semantic_assignment") or {}
            abbreviation = semantic_assignment.get("abbreviation")
            if abbreviation is None or build_semantic_evidence.semantic_abbreviation_is_latin(abbreviation):
                continue

            han_compound = (candidate.get("wiktionary_validation") or {}).get("han_compound") or {}
            named_args = han_compound.get("named_args") or {}
            case = {
                "entry_id": entry["id"],
                "character": candidate["character"],
                "abbreviation": abbreviation,
                "semantic_component": build_semantic_evidence.normalize_component_graph(
                    semantic_assignment.get("semantic_component")
                ),
                "position": semantic_assignment.get("position"),
                "source": semantic_assignment.get("source"),
                "template_raw": han_compound.get("template_raw"),
                "template_alt_graph": named_args.get("alt1"),
                "template_gloss_primary": named_args.get("t1"),
                "template_gloss_secondary": named_args.get("t2"),
                "semantic_component_ids": ids_map.get(
                    build_semantic_evidence.normalize_component_graph(semantic_assignment.get("semantic_component"))
                ),
                "transliteration_latex": candidate.get("transliteration_latex"),
                "render_latex": candidate.get("render_latex"),
            }
            proposal = classify_case(case, graph_lookup)
            case.update(proposal)
            cases.append(case)
            grouped[case["semantic_component"]].append(case)

    grouped_rows = []
    for component, rows in sorted(grouped.items()):
        representative = rows[0]
        grouped_rows.append(
            {
                "semantic_component": component,
                "classification": representative["classification"],
                "proposal": representative["proposal"],
                "target_graph": representative.get("target_graph"),
                "target_abbreviation": representative.get("target_abbreviation"),
                "reason": representative.get("reason"),
                "semantic_component_ids": representative.get("semantic_component_ids"),
                "template_alt_graph": representative.get("template_alt_graph"),
                "template_gloss_primary": representative.get("template_gloss_primary"),
                "template_gloss_secondary": representative.get("template_gloss_secondary"),
                "case_count": len(rows),
                "examples": [
                    {
                        "entry_id": row["entry_id"],
                        "character": row["character"],
                        "position": row["position"],
                        "source": row["source"],
                    }
                    for row in rows
                ],
            }
        )

    summary = {
        "case_count": len(cases),
        "unique_component_count": len(grouped_rows),
        "by_classification": dict(Counter(case["classification"] for case in cases)),
        "by_source": dict(Counter(case["source"] for case in cases)),
    }

    return {
        "summary": summary,
        "cases": cases,
        "components": grouped_rows,
    }


def render_report(inventory: dict[str, Any]) -> str:
    summary = inventory["summary"]
    lines = [
        "# Generated non-Latin semantics audit",
        "",
        "- This audit covers live generated semantics in `data/entries/curation/`.",
        "- Commented-out source material is excluded.",
        f"- Generated non-Latin semantic occurrences: {summary['case_count']}",
        f"- Unique unresolved semantic graphs/tokens: {summary['unique_component_count']}",
        "",
        "## By proposed handling",
        "",
        "| Classification | Count |",
        "| --- | ---: |",
    ]
    for classification, count in sorted(summary["by_classification"].items()):
        lines.append(f"| `{classification}` | {count} |")

    lines.extend(
        [
            "",
            "## By source",
            "",
            "| Source | Count |",
            "| --- | ---: |",
        ]
    )
    for source, count in sorted(summary["by_source"].items()):
        lines.append(f"| `{source}` | {count} |")

    sections = [
        "existing_inventory_variant",
        "template_alt_graph",
        "needs_human_review",
        "new_latin_label_needed",
        "research_compound_graph",
    ]
    component_rows = inventory["components"]
    for classification in sections:
        matching = [row for row in component_rows if row["classification"] == classification]
        if not matching:
            continue
        lines.extend(
            [
                "",
                f"## `{classification}`",
                "",
                "| Component | IDS | Example characters | Target / reuse | Proposal |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for row in matching:
            examples = ", ".join(f"`{item['entry_id']}`:{item['character']}" for item in row["examples"][:6])
            target = ""
            if row.get("target_abbreviation"):
                target = f"`{row['target_graph']}` → `{row['target_abbreviation']}`"
            elif row.get("target_graph"):
                target = f"`{row['target_graph']}`"
            ids = (row.get("semantic_component_ids") or "").replace("|", "\\|")
            proposal = row["proposal"].replace("|", "\\|")
            lines.append(
                f"| `{row['semantic_component']}` | `{ids}` | {examples} | {target} | {proposal} |"
            )

    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit generated semantic markers that still use non-Latin graphs.")
    parser.add_argument("--curation-dir", default=DEFAULT_CURATION_DIR)
    parser.add_argument("--semantic-inventory", default=DEFAULT_SEMANTIC_INVENTORY)
    parser.add_argument("--ids-path", default=DEFAULT_IDS_PATH)
    parser.add_argument("--json-out", default=DEFAULT_JSON_OUT)
    parser.add_argument("--report-out", default=DEFAULT_REPORT_OUT)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    entries = load_entries(Path(args.curation_dir))
    semantic_inventory = json.loads(Path(args.semantic_inventory).read_text(encoding="utf-8"))
    ids_map = build_semantic_evidence.load_ids_map(Path(args.ids_path))
    inventory = build_inventory(entries, semantic_inventory, ids_map)
    json_out = Path(args.json_out)
    report_out = Path(args.report_out)
    json_out.parent.mkdir(parents=True, exist_ok=True)
    report_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_out.write_text(render_report(inventory), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
