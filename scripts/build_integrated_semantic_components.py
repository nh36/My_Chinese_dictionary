from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import extract_semantic_components
import render_curated_series
import semantic_label_normalization


DEFAULT_CURRENT_SOURCE = "main.tex"
DEFAULT_PILOT_SOURCE = "key references/My_Chinese_dictionary/main.tex"
DEFAULT_CURRENT_ENTRIES = "data/current_tex_entries.json"
DEFAULT_CURATION_DIR = "data/entries/curation"
DEFAULT_JSON_OUT = "data/semantic_components/integrated_semantic_components.json"
DEFAULT_REPORT_OUT = "reports/integrated_semantic_components.md"
DEFAULT_ALIAS_CONFIG = "data/semantic_components/semantic_aliases.json"


def load_inventory(source_path: Path) -> dict[str, Any]:
    source_text = source_path.read_text(encoding="utf-8")
    return extract_semantic_components.build_inventory(source_text, str(source_path))


def supplement_item_to_inventory_item(item: dict[str, Any], supplement_path: str) -> dict[str, Any]:
    abbreviation = item.get("abbreviation")
    graph_raw = item.get("graph_raw")
    return {
        "graph_raw": graph_raw,
        "abbreviation": abbreviation,
        "expanded_latin": item.get("label_token") or abbreviation,
        "notes": item.get("notes"),
        "scope": item.get("scope", "general"),
        "only_in": list(item.get("only_in") or []),
        "duplicate_graph_status": item.get("duplicate_graph_status"),
        "note": item.get("note"),
        "comments": list(item.get("comments") or []),
        "sources": [
            {
                "source": "semantic_label_supplement",
                "source_path": supplement_path,
                "start_line": None,
                "end_line": None,
                "label_token": item.get("label_token"),
                "label_notes": item.get("label_notes"),
                "scope": item.get("scope", "general"),
                "only_in": list(item.get("only_in") or []),
                "duplicate_graph_status": item.get("duplicate_graph_status"),
                "note": item.get("note"),
                "comments": list(item.get("comments") or []),
                "raw_latex": None,
            }
        ],
        "used_abbreviations_current_tex": [],
        "used_abbreviations_curated_series": [],
        "used_abbreviation_aliases": [],
        "used_in_current_tex": False,
        "used_in_curated_series": False,
        "used_in_integrated_dictionary": False,
        "listed_only_in_inventory": True,
        "classification": "canonical",
        "conflicts": [],
    }


def semantic_key(item: dict[str, Any]) -> tuple[str, str]:
    return ((item.get("graph_raw") or "").strip(), item.get("abbreviation") or "")


def normalize_for_compare(value: Any) -> Any:
    if isinstance(value, str):
        return " ".join(value.split())
    if isinstance(value, list):
        return [normalize_for_compare(item) for item in value]
    return value


def is_empty_value(value: Any) -> bool:
    return value is None or value == "" or value == []


def iter_semantic_tokens(text: str | None) -> set[str]:
    return set(semantic_label_normalization.iter_semantic_labels_from_text(text))


def build_usage_placeholder(
    abbreviation: str,
    note: str,
    *,
    classification: str,
    used_in_current_tex: bool,
    used_in_curated_series: bool,
) -> dict[str, Any]:
    sources = []
    if used_in_current_tex:
        sources.append({"source": "current-usage"})
    if used_in_curated_series:
        sources.append({"source": "curated-usage"})
    return {
        "graph_raw": None,
        "abbreviation": abbreviation,
        "expanded_latin": None,
        "notes": note,
        "scope": "general",
        "only_in": [],
        "duplicate_graph_status": None,
        "note": None,
        "comments": [],
        "sources": sources,
        "used_abbreviations_current_tex": [abbreviation] if used_in_current_tex else [],
        "used_abbreviations_curated_series": [abbreviation] if used_in_curated_series else [],
        "used_abbreviation_aliases": [],
        "used_in_current_tex": used_in_current_tex,
        "used_in_curated_series": used_in_curated_series,
        "used_in_integrated_dictionary": used_in_current_tex or used_in_curated_series,
        "listed_only_in_inventory": False,
        "classification": classification,
        "conflicts": [
            {
                "field": "abbreviation",
                "source": "entry_usage",
                "existing": None,
                "incoming": abbreviation,
                "note": note,
            }
        ],
    }


def collect_used_abbreviations(
    current_entries: list[dict[str, Any]],
    curated_entries: list[dict[str, Any]],
) -> tuple[set[str], set[str]]:
    used_in_tex: set[str] = set()
    for entry in current_entries:
        used_in_tex.update(iter_semantic_tokens(entry.get("raw_block")))

    used_in_curated: set[str] = set()
    for entry in curated_entries:
        for candidate in entry.get("proposed_additions", []):
            used_in_curated.update(iter_semantic_tokens(candidate.get("transliteration_latex")))
            used_in_curated.update(iter_semantic_tokens(candidate.get("render_latex")))

    return used_in_tex, used_in_curated


def source_label(source_name: str) -> str:
    return "current_main_tex" if source_name == "current" else "earlier_pilot"


def describe_item_reference(item: dict[str, Any]) -> str:
    return semantic_label_normalization.describe_semantic_item(item)


def merge_inventories(
    current_inventory: dict[str, Any],
    pilot_inventory: dict[str, Any],
    current_entries: list[dict[str, Any]],
    curated_entries: list[dict[str, Any]],
    normalization_config: dict[str, Any],
) -> dict[str, Any]:
    used_in_tex, used_in_curated = collect_used_abbreviations(current_entries, curated_entries)
    merged: dict[tuple[str, str], dict[str, Any]] = {}
    ordered_keys: list[tuple[str, str]] = []

    for source_name, inventory in (("current", current_inventory), ("pilot", pilot_inventory)):
        for item in inventory["items"]:
            key = semantic_key(item)
            if key not in merged:
                merged[key] = {
                    "graph_raw": item.get("graph_raw"),
                    "abbreviation": item.get("abbreviation"),
                    "expanded_latin": item.get("label_token"),
                    "notes": item.get("label_notes"),
                    "scope": item.get("scope", "general"),
                    "only_in": list(item.get("only_in") or []),
                    "duplicate_graph_status": item.get("duplicate_graph_status"),
                    "note": item.get("note"),
                    "comments": list(item.get("comments") or []),
                    "sources": [],
                    "conflicts": [],
                }
                ordered_keys.append(key)
            else:
                record = merged[key]
                for field, label in (
                    ("label_token", "expanded_latin"),
                    ("label_notes", "notes"),
                    ("scope", "scope"),
                    ("only_in", "only_in"),
                    ("duplicate_graph_status", "duplicate_graph_status"),
                    ("note", "note"),
                    ("comments", "comments"),
                ):
                    existing = normalize_for_compare(record.get(label))
                    incoming = normalize_for_compare(item.get(field))
                    if not is_empty_value(existing) and not is_empty_value(incoming) and existing != incoming:
                        record["conflicts"].append(
                            {
                                "field": field,
                                "source": source_label(source_name),
                                "existing": record.get(label),
                                "incoming": item.get(field),
                            }
                        )
                if item.get("comments"):
                    for comment in item["comments"]:
                        if comment not in record["comments"]:
                            record["comments"].append(comment)

            merged[key]["sources"].append(
                {
                    "source": source_label(source_name),
                    "source_path": inventory["source_path"],
                    "start_line": item.get("start_line"),
                    "end_line": item.get("end_line"),
                    "label_token": item.get("label_token"),
                    "label_notes": item.get("label_notes"),
                    "scope": item.get("scope", "general"),
                    "only_in": item.get("only_in") or [],
                    "duplicate_graph_status": item.get("duplicate_graph_status"),
                    "note": item.get("note"),
                    "comments": item.get("comments") or [],
                    "raw_latex": item.get("raw_latex"),
                }
            )

    supplement = semantic_label_normalization.load_semantic_label_supplement()
    for item in supplement["items"]:
        key = semantic_key(item)
        if key in merged:
            continue
        merged[key] = supplement_item_to_inventory_item(item, supplement["path"])
        ordered_keys.append(key)

    items: list[dict[str, Any]] = []
    for key in ordered_keys:
        record = merged[key]
        items.append(
            {
                "graph_raw": record.get("graph_raw"),
                "abbreviation": record.get("abbreviation"),
                "expanded_latin": record.get("expanded_latin"),
                "notes": record.get("notes"),
                "scope": record.get("scope", "general"),
                "only_in": record.get("only_in") or [],
                "duplicate_graph_status": record.get("duplicate_graph_status"),
                "note": record.get("note"),
                "comments": record.get("comments"),
                "sources": record.get("sources"),
                "used_abbreviations_current_tex": [],
                "used_abbreviations_curated_series": [],
                "used_abbreviation_aliases": [],
                "used_in_current_tex": False,
                "used_in_curated_series": False,
                "used_in_integrated_dictionary": False,
                "listed_only_in_inventory": True,
                "classification": "canonical",
                "conflicts": record.get("conflicts"),
            }
        )

    canonical_index = semantic_label_normalization.build_canonical_index(items)
    item_by_key = {semantic_key(item): item for item in items}

    entry_aliases: set[str] = set()
    blocked_used_abbreviations: dict[str, dict[str, Any]] = {}
    needs_review_used_abbreviations: dict[str, dict[str, Any]] = {}
    placeholder_used_abbreviations: dict[str, dict[str, Any]] = {}
    missing_used_abbreviations: set[str] = set()

    for label in sorted(used_in_tex | used_in_curated):
        classification = semantic_label_normalization.classify_semantic_label(
            label,
            canonical_index,
            normalization_config,
        )
        used_in_current = label in used_in_tex
        used_in_curated_series = label in used_in_curated
        kind = classification["classification"]

        if kind in {"canonical", "explicit_alias"}:
            for matched_item in classification.get("matched_items", []):
                item = item_by_key[semantic_key(matched_item)]
                item["used_in_current_tex"] = item["used_in_current_tex"] or used_in_current
                item["used_in_curated_series"] = item["used_in_curated_series"] or used_in_curated_series
                if kind == "explicit_alias":
                    if used_in_current and label not in item["used_abbreviations_current_tex"]:
                        item["used_abbreviations_current_tex"].append(label)
                    if used_in_curated_series and label not in item["used_abbreviations_curated_series"]:
                        item["used_abbreviations_curated_series"].append(label)
                    entry_aliases.add(label)
            continue

        if kind == "blocked_ambiguous_alias":
            blocked_used_abbreviations[label] = {
                "targets": classification["targets"],
                "reason": classification.get("reason"),
                "used_in_current_tex": used_in_current,
                "used_in_curated_series": used_in_curated_series,
            }
            note = "Blocked ambiguous alias used in dictionary entries."
            if classification.get("reason"):
                note += f" {classification['reason']}"
            note += " Candidate canonical targets: " + ", ".join(classification["targets"]) + "."
            items.append(
                build_usage_placeholder(
                    label,
                    note,
                    classification="blocked_ambiguous_alias",
                    used_in_current_tex=used_in_current,
                    used_in_curated_series=used_in_curated_series,
                )
            )
            continue

        if kind == "needs_review":
            needs_review_used_abbreviations[label] = {
                "used_in_current_tex": used_in_current,
                "used_in_curated_series": used_in_curated_series,
            }
            items.append(
                build_usage_placeholder(
                    label,
                    "Label form used in dictionary entries, but it is neither a canonical ASCII abbreviation nor an approved alias.",
                    classification="needs_review",
                    used_in_current_tex=used_in_current,
                    used_in_curated_series=used_in_curated_series,
                )
            )
            continue

        if kind == "placeholder":
            placeholder_used_abbreviations[label] = {
                "used_in_current_tex": used_in_current,
                "used_in_curated_series": used_in_curated_series,
            }
            items.append(
                build_usage_placeholder(
                    label,
                    "Unresolved placeholder semantic label used in dictionary entries.",
                    classification="placeholder",
                    used_in_current_tex=used_in_current,
                    used_in_curated_series=used_in_curated_series,
                )
            )
            continue

        missing_used_abbreviations.add(label)
        items.append(
            build_usage_placeholder(
                label,
                "Used in dictionary entries, but no semantic-component row currently defines it.",
                classification="missing_from_inventory",
                used_in_current_tex=used_in_current,
                used_in_curated_series=used_in_curated_series,
            )
        )

    for item in items:
        item["used_abbreviations_current_tex"] = sorted(set(item["used_abbreviations_current_tex"]))
        item["used_abbreviations_curated_series"] = sorted(set(item["used_abbreviations_curated_series"]))
        item["used_abbreviation_aliases"] = sorted(
            set(item["used_abbreviations_current_tex"]) | set(item["used_abbreviations_curated_series"])
        )
        item["used_in_integrated_dictionary"] = item["used_in_current_tex"] or item["used_in_curated_series"]
        item["listed_only_in_inventory"] = not item["used_in_integrated_dictionary"]

    canonical_items = [
        item
        for item in items
        if any(source["source"] in {"current_main_tex", "earlier_pilot"} for source in item.get("sources", []))
    ]

    abbreviation_to_graphs: dict[str, set[str]] = defaultdict(set)
    graph_to_items: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in canonical_items:
        if item.get("abbreviation"):
            abbreviation_to_graphs[item["abbreviation"]].add(item.get("graph_raw") or "")
        if item.get("graph_raw"):
            graph_to_items[item["graph_raw"]].append(item)

    duplicate_abbreviations = {
        abbreviation: sorted(graphs)
        for abbreviation, graphs in abbreviation_to_graphs.items()
        if len(graphs) > 1
    }

    intentional_scoped_duplicate_graphs: dict[str, list[dict[str, Any]]] = {}
    duplicate_graph_conflicts: dict[str, list[str]] = {}
    for graph, graph_items in graph_to_items.items():
        distinct_abbreviations = {item.get("abbreviation") for item in graph_items if item.get("abbreviation")}
        if len(distinct_abbreviations) <= 1:
            continue

        scoped_rows = []
        for item in graph_items:
            scoped_duplicate = semantic_label_normalization.find_intentional_scoped_duplicate(
                graph=item.get("graph_raw"),
                abbreviation=item.get("abbreviation"),
                only_in=item.get("only_in") or [],
                config=normalization_config,
            )
            if scoped_duplicate is not None:
                scoped_rows.append(
                    {
                        "abbreviation": item.get("abbreviation"),
                        "scope": item.get("scope", "general"),
                        "only_in": item.get("only_in") or [],
                        "note": scoped_duplicate.get("note"),
                        "paired_with": scoped_duplicate.get("paired_with"),
                    }
                )

        if scoped_rows and all(row.get("paired_with") in distinct_abbreviations for row in scoped_rows):
            intentional_scoped_duplicate_graphs[graph] = scoped_rows
            continue

        duplicate_graph_conflicts[graph] = sorted(distinct_abbreviations)

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "normalization_config_path": normalization_config["path"],
        "sources": {
            "current_main_tex": current_inventory["source_path"],
            "earlier_pilot": pilot_inventory["source_path"],
        },
        "summary": {
            "integrated_item_count": len(items),
            "current_item_count": current_inventory["summary"]["item_count"],
            "pilot_item_count": pilot_inventory["summary"]["item_count"],
            "items_in_both_sources": sum(
                1 for item in canonical_items if {source["source"] for source in item["sources"]} == {"current_main_tex", "earlier_pilot"}
            ),
            "current_only_item_count": sum(
                1 for item in canonical_items if {source["source"] for source in item["sources"]} == {"current_main_tex"}
            ),
            "pilot_only_item_count": sum(
                1 for item in canonical_items if {source["source"] for source in item["sources"]} == {"earlier_pilot"}
            ),
            "entry_alias_count": len(entry_aliases),
            "blocked_alias_count": len(normalization_config["blocked_aliases"]),
            "blocked_used_abbreviation_count": len(blocked_used_abbreviations),
            "needs_review_used_abbreviation_count": len(needs_review_used_abbreviations),
            "placeholder_used_abbreviation_count": len(placeholder_used_abbreviations),
            "duplicate_abbreviation_count": len(duplicate_abbreviations),
            "duplicate_graph_conflict_count": len(duplicate_graph_conflicts),
            "intentional_scoped_duplicate_graph_count": len(intentional_scoped_duplicate_graphs),
            "ambiguous_used_abbreviation_count": 0,
            "missing_used_abbreviation_count": len(missing_used_abbreviations),
        },
        "aliases": normalization_config["aliases"],
        "blocked_aliases": normalization_config["blocked_aliases"],
        "duplicate_abbreviations": duplicate_abbreviations,
        "duplicate_graphs": duplicate_graph_conflicts,
        "intentional_scoped_duplicate_graphs": intentional_scoped_duplicate_graphs,
        "entry_aliases": sorted(entry_aliases),
        "ambiguous_used_abbreviations": {},
        "blocked_used_abbreviations": blocked_used_abbreviations,
        "needs_review_used_abbreviations": needs_review_used_abbreviations,
        "placeholder_used_abbreviations": placeholder_used_abbreviations,
        "missing_used_abbreviations": sorted(missing_used_abbreviations),
        "items": items,
    }


def render_report(data: dict[str, Any]) -> str:
    lines = [
        "# Integrated semantic components",
        "",
        f"- Current semantic source: `{data['sources']['current_main_tex']}`",
        f"- Earlier pilot semantic source: `{data['sources']['earlier_pilot']}`",
        f"- Normalization config: `{data['normalization_config_path']}`",
        f"- Integrated items: {data['summary']['integrated_item_count']}",
        f"- Items present in both sources: {data['summary']['items_in_both_sources']}",
        f"- Current-only items: {data['summary']['current_only_item_count']}",
        f"- Pilot-only items: {data['summary']['pilot_only_item_count']}",
        f"- Entry-form aliases matched to canonical semantic rows: {data['summary']['entry_alias_count']}",
        f"- Blocked ambiguous aliases configured: {data['summary']['blocked_alias_count']}",
        f"- Blocked ambiguous aliases used in entries: {data['summary']['blocked_used_abbreviation_count']}",
        f"- Needs-review labels used in entries: {data['summary']['needs_review_used_abbreviation_count']}",
        f"- Placeholder labels used in entries: {data['summary']['placeholder_used_abbreviation_count']}",
        f"- Duplicate abbreviations with multiple graphs: {data['summary']['duplicate_abbreviation_count']}",
        f"- Duplicate graphs with true conflicts: {data['summary']['duplicate_graph_conflict_count']}",
        f"- Intentional scoped duplicate graphs: {data['summary']['intentional_scoped_duplicate_graph_count']}",
        f"- Ambiguous abbreviations used in entries: {data['summary']['ambiguous_used_abbreviation_count']}",
        f"- Abbreviations used in entries but missing from the semantic list: {data['summary']['missing_used_abbreviation_count']}",
        "",
    ]

    if data["entry_aliases"]:
        lines.extend(
            [
                "## Entry-form aliases matched to canonical semantic rows",
                "",
                ", ".join(f"`{abbreviation}`" for abbreviation in data["entry_aliases"]),
                "",
            ]
        )

    lines.extend(
        [
            "## Blocked ambiguous aliases",
            "",
            "| Alias | Candidate canonical labels | Reason |",
            "| --- | --- | --- |",
        ]
    )
    for alias, payload in sorted(data["blocked_aliases"].items()):
        lines.append(
            f"| `{alias}` | {', '.join(f'`{target}`' for target in payload['targets'])} | {payload.get('reason') or ''} |"
        )
    lines.append("")

    if data["blocked_used_abbreviations"]:
        lines.extend(
            [
                "## Blocked ambiguous aliases used in entries",
                "",
                "| Alias | Candidate canonical labels | Used in current TeX | Used in curated series | Reason |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for alias, payload in sorted(data["blocked_used_abbreviations"].items()):
            lines.append(
                f"| `{alias}` | {', '.join(f'`{target}`' for target in payload['targets'])} | "
                f"{'yes' if payload['used_in_current_tex'] else 'no'} | "
                f"{'yes' if payload['used_in_curated_series'] else 'no'} | "
                f"{payload.get('reason') or ''} |"
            )
        lines.append("")

    if data["needs_review_used_abbreviations"]:
        lines.extend(
            [
                "## Needs-review labels used in entries",
                "",
                "| Label | Used in current TeX | Used in curated series |",
                "| --- | --- | --- |",
            ]
        )
        for alias, payload in sorted(data["needs_review_used_abbreviations"].items()):
            lines.append(
                f"| `{alias}` | {'yes' if payload['used_in_current_tex'] else 'no'} | {'yes' if payload['used_in_curated_series'] else 'no'} |"
            )
        lines.append("")

    if data["placeholder_used_abbreviations"]:
        lines.extend(
            [
                "## Placeholder labels used in entries",
                "",
                "| Label | Used in current TeX | Used in curated series |",
                "| --- | --- | --- |",
            ]
        )
        for alias, payload in sorted(data["placeholder_used_abbreviations"].items()):
            lines.append(
                f"| `{alias}` | {'yes' if payload['used_in_current_tex'] else 'no'} | {'yes' if payload['used_in_curated_series'] else 'no'} |"
            )
        lines.append("")

    if data["missing_used_abbreviations"]:
        lines.extend(
            [
                "## Abbreviations used in entries but missing from the semantic list",
                "",
                ", ".join(f"`{abbreviation}`" for abbreviation in data["missing_used_abbreviations"]),
                "",
            ]
        )

    if data["duplicate_abbreviations"]:
        lines.extend(
            [
                "## Duplicate abbreviations across different graphs",
                "",
                "| Abbreviation | Graphs |",
                "| --- | --- |",
            ]
        )
        for abbreviation, graphs in sorted(data["duplicate_abbreviations"].items()):
            lines.append(f"| `{abbreviation}` | {'; '.join(f'`{graph}`' for graph in graphs)} |")
        lines.append("")

    if data["intentional_scoped_duplicate_graphs"]:
        lines.extend(
            [
                "## Intentional scoped duplicate graphs",
                "",
                "| Graph | Abbreviation | Scope | Only in | Note |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for graph, rows in sorted(data["intentional_scoped_duplicate_graphs"].items()):
            for row in rows:
                lines.append(
                    f"| `{graph}` | `{row['abbreviation']}` | {row['scope']} | "
                    f"{', '.join(row['only_in'])} | {row.get('note') or ''} |"
                )
        lines.append("")

    if data["duplicate_graphs"]:
        lines.extend(
            [
                "## Graphs with conflicting abbreviations",
                "",
                "| Graph | Abbreviations |",
                "| --- | --- |",
            ]
        )
        for graph, abbreviations in sorted(data["duplicate_graphs"].items()):
            lines.append(f"| `{graph}` | {'; '.join(f'`{abbreviation}`' for abbreviation in abbreviations)} |")
        lines.append("")

    lines.extend(
        [
            "## Integrated inventory",
            "",
            "| Graph | Abbr. | Expanded Latin | Notes | Scope | Only in | Duplicate graph | Note | Entry-form aliases | Used in dictionary | Provenance |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for item in data["items"]:
        provenance = ", ".join(source["source"] for source in item["sources"])
        used = "yes" if item["used_in_integrated_dictionary"] else "no"
        notes = " / ".join(part for part in [item.get("notes")] + list(item.get("comments") or []) if part)
        aliases = ", ".join(f"`{abbreviation}`" for abbreviation in item.get("used_abbreviation_aliases", []))
        lines.append(
            f"| `{(item.get('graph_raw') or '').replace('`', '\\`')}` | "
            f"`{item.get('abbreviation') or ''}` | "
            f"`{item.get('expanded_latin') or ''}` | "
            f"{notes.replace('|', '\\|')} | "
            f"{item.get('scope', 'general')} | "
            f"{', '.join(item.get('only_in') or []).replace('|', '\\|')} | "
            f"{(item.get('duplicate_graph_status') or '').replace('|', '\\|')} | "
            f"{(item.get('note') or '').replace('|', '\\|')} | "
            f"{aliases} | {used} | {provenance} |"
        )
    lines.append("")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build an integrated semantic-component inventory from current main.tex and the earlier pilot."
    )
    parser.add_argument("--current-source", default=DEFAULT_CURRENT_SOURCE)
    parser.add_argument("--pilot-source", default=DEFAULT_PILOT_SOURCE)
    parser.add_argument("--current-entries", default=DEFAULT_CURRENT_ENTRIES)
    parser.add_argument("--curation-dir", default=DEFAULT_CURATION_DIR)
    parser.add_argument("--json-out", default=DEFAULT_JSON_OUT)
    parser.add_argument("--report-out", default=DEFAULT_REPORT_OUT)
    parser.add_argument("--alias-config", default=DEFAULT_ALIAS_CONFIG)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    current_inventory = load_inventory(Path(args.current_source))
    pilot_inventory = load_inventory(Path(args.pilot_source))
    current_entries = json.loads(Path(args.current_entries).read_text(encoding="utf-8"))["entries"]
    curated_entries = [
        json.loads((Path(args.curation_dir) / f"{entry_id}.json").read_text(encoding="utf-8"))
        for entry_id in render_curated_series.DEFAULT_IDS
        if (Path(args.curation_dir) / f"{entry_id}.json").exists()
    ]
    normalization_config = semantic_label_normalization.load_normalization_config(Path(args.alias_config))
    integrated = merge_inventories(
        current_inventory,
        pilot_inventory,
        current_entries,
        curated_entries,
        normalization_config,
    )

    json_out = Path(args.json_out)
    report_out = Path(args.report_out)
    json_out.parent.mkdir(parents=True, exist_ok=True)
    report_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(integrated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_out.write_text(render_report(integrated), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
