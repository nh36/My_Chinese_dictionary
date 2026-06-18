from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import extract_semantic_components
import render_curated_series


DEFAULT_CURRENT_SOURCE = "main.tex"
DEFAULT_PILOT_SOURCE = "key references/My_Chinese_dictionary/main.tex"
DEFAULT_CURRENT_ENTRIES = "data/current_tex_entries.json"
DEFAULT_CURATION_DIR = "data/entries/curation"
DEFAULT_JSON_OUT = "data/semantic_components/integrated_semantic_components.json"
DEFAULT_REPORT_OUT = "reports/integrated_semantic_components.md"
TEXTSUP_RE = re.compile(r"\\textsuperscript\{([^}]*)\}")
ALPHA_RE = re.compile(r"[A-Za-z]+")
IGNORED_MACRO_TOKENS = {"includegraphics", "raisebox", "height", "ex"}
LABEL_STEM_RE = re.compile(r"([A-Za-z]+)(?=\()")
IGNORED_LABEL_WORDS = {"in", "only"}


def load_inventory(source_path: Path) -> dict[str, Any]:
    source_text = source_path.read_text(encoding="utf-8")
    return extract_semantic_components.build_inventory(source_text, str(source_path))


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
    if not text:
        return set()
    tokens: set[str] = set()
    for content in TEXTSUP_RE.findall(text):
        if "\\" in content:
            continue
        for token in ALPHA_RE.findall(content):
            if token in IGNORED_MACRO_TOKENS:
                continue
            tokens.add(token)
    return tokens


def iter_label_forms(text: str | None) -> set[str]:
    if not text:
        return set()
    forms = {stem.lower() for stem in LABEL_STEM_RE.findall(text) if stem.lower() not in IGNORED_LABEL_WORDS}
    normalized = re.sub(r"[^A-Za-z]+", " ", text.replace("(", "").replace(")", " "))
    forms.update(word.lower() for word in normalized.split() if word.lower() not in IGNORED_LABEL_WORDS)
    return forms


def item_forms(item: dict[str, Any]) -> set[str]:
    forms = set()
    abbreviation = item.get("abbreviation")
    if abbreviation:
        forms.add(abbreviation.lower())
    forms.update(iter_label_forms(item.get("expanded_latin")))
    return forms


def match_used_abbreviations(
    used_abbreviations: set[str], forms_by_key: dict[tuple[str, str], set[str]]
) -> tuple[dict[str, tuple[str, str]], dict[str, list[tuple[str, str]]], set[str]]:
    exact_index: dict[str, set[tuple[str, str]]] = defaultdict(set)
    for key, forms in forms_by_key.items():
        for form in forms:
            exact_index[form].add(key)

    unique_matches: dict[str, tuple[str, str]] = {}
    ambiguous_matches: dict[str, list[tuple[str, str]]] = {}
    unmatched: set[str] = set()

    for abbreviation in sorted(used_abbreviations):
        exact_matches = exact_index.get(abbreviation, set())
        if len(exact_matches) == 1:
            unique_matches[abbreviation] = next(iter(exact_matches))
            continue
        if len(exact_matches) > 1:
            ambiguous_matches[abbreviation] = sorted(exact_matches)
            continue

        prefix_matches = {
            key
            for key, forms in forms_by_key.items()
            if any(form.startswith(abbreviation) and form != abbreviation for form in forms)
        }
        if len(prefix_matches) == 1:
            unique_matches[abbreviation] = next(iter(prefix_matches))
            continue
        if len(prefix_matches) > 1:
            ambiguous_matches[abbreviation] = sorted(prefix_matches)
            continue

        unmatched.add(abbreviation)

    return unique_matches, ambiguous_matches, unmatched


def describe_semantic_item(item: dict[str, Any]) -> str:
    graph = item.get("graph_raw") or "—"
    abbreviation = item.get("abbreviation")
    if abbreviation:
        return f"{graph}/{abbreviation}"
    return graph


def build_usage_placeholder(
    abbreviation: str,
    note: str,
    *,
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
        "comments": [],
        "sources": sources,
        "used_abbreviations_current_tex": [abbreviation] if used_in_current_tex else [],
        "used_abbreviations_curated_series": [abbreviation] if used_in_curated_series else [],
        "used_abbreviation_aliases": [],
        "used_in_current_tex": used_in_current_tex,
        "used_in_curated_series": used_in_curated_series,
        "used_in_integrated_dictionary": used_in_current_tex or used_in_curated_series,
        "listed_only_in_inventory": False,
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


def collect_used_abbreviations(current_entries: list[dict[str, Any]], curated_entries: list[dict[str, Any]]) -> tuple[set[str], set[str]]:
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


def merge_inventories(
    current_inventory: dict[str, Any],
    pilot_inventory: dict[str, Any],
    current_entries: list[dict[str, Any]],
    curated_entries: list[dict[str, Any]],
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
                    "comments": list(item.get("comments") or []),
                    "sources": [],
                    "conflicts": [],
                }
                ordered_keys.append(key)
            else:
                record = merged[key]
                for field, label in (("label_token", "expanded_latin"), ("label_notes", "notes"), ("comments", "comments")):
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
                    "comments": item.get("comments") or [],
                    "raw_latex": item.get("raw_latex"),
                }
            )

    items: list[dict[str, Any]] = []
    for key in ordered_keys:
        record = merged[key]
        abbreviation = record.get("abbreviation")
        items.append(
            {
                "graph_raw": record.get("graph_raw"),
                "abbreviation": abbreviation,
                "expanded_latin": record.get("expanded_latin"),
                "notes": record.get("notes"),
                "comments": record.get("comments"),
                "sources": record.get("sources"),
                "used_abbreviations_current_tex": [],
                "used_abbreviations_curated_series": [],
                "used_abbreviation_aliases": [],
                "used_in_current_tex": False,
                "used_in_curated_series": False,
                "used_in_integrated_dictionary": False,
                "listed_only_in_inventory": True,
                "conflicts": record.get("conflicts"),
            }
        )

    item_by_key = {semantic_key(item): item for item in items}
    forms_by_key = {key: item_forms(item_by_key[key]) for key in item_by_key}

    matched_current, ambiguous_current, unmatched_current = match_used_abbreviations(used_in_tex, forms_by_key)
    matched_curated, ambiguous_curated, unmatched_curated = match_used_abbreviations(used_in_curated, forms_by_key)

    for abbreviation, key in matched_current.items():
        item = item_by_key[key]
        item["used_in_current_tex"] = True
        if abbreviation != (item.get("abbreviation") or "").lower():
            item["used_abbreviations_current_tex"].append(abbreviation)
    for abbreviation, key in matched_curated.items():
        item = item_by_key[key]
        item["used_in_curated_series"] = True
        if abbreviation != (item.get("abbreviation") or "").lower():
            item["used_abbreviations_curated_series"].append(abbreviation)

    for item in items:
        aliases = sorted(set(item["used_abbreviations_current_tex"]) | set(item["used_abbreviations_curated_series"]))
        item["used_abbreviation_aliases"] = aliases
        item["used_in_integrated_dictionary"] = item["used_in_current_tex"] or item["used_in_curated_series"]
        item["listed_only_in_inventory"] = not item["used_in_integrated_dictionary"]

    ambiguous_used_abbreviations: dict[str, list[str]] = {}
    for abbreviation in sorted(set(ambiguous_current) | set(ambiguous_curated)):
        matching_keys = ambiguous_current.get(abbreviation) or ambiguous_curated.get(abbreviation) or []
        ambiguous_used_abbreviations[abbreviation] = [describe_semantic_item(item_by_key[key]) for key in matching_keys]
        items.append(
            build_usage_placeholder(
                abbreviation,
                "Used in dictionary entries, but ambiguously matches more than one semantic-component row: "
                + ", ".join(ambiguous_used_abbreviations[abbreviation]),
                used_in_current_tex=abbreviation in ambiguous_current,
                used_in_curated_series=abbreviation in ambiguous_curated,
            )
        )

    missing_used_abbreviations = sorted(unmatched_current | unmatched_curated)
    for abbreviation in missing_used_abbreviations:
        items.append(
            build_usage_placeholder(
                abbreviation,
                "Used in dictionary entries, but no semantic-component row currently defines it.",
                used_in_current_tex=abbreviation in unmatched_current,
                used_in_curated_series=abbreviation in unmatched_curated,
            )
        )

    canonical_items = [
        item
        for item in items
        if any(source["source"] in {"current_main_tex", "earlier_pilot"} for source in item.get("sources", []))
    ]

    abbreviation_to_graphs: dict[str, set[str]] = defaultdict(set)
    graph_to_abbreviations: dict[str, set[str]] = defaultdict(set)
    for item in canonical_items:
        if item.get("abbreviation"):
            abbreviation_to_graphs[item["abbreviation"]].add(item.get("graph_raw") or "")
        if item.get("graph_raw"):
            graph_to_abbreviations[item["graph_raw"]].add(item.get("abbreviation") or "")

    duplicate_abbreviations = {
        abbr: sorted(graphs)
        for abbr, graphs in abbreviation_to_graphs.items()
        if len(graphs) > 1
    }
    duplicate_graphs = {
        graph: sorted(abbrs)
        for graph, abbrs in graph_to_abbreviations.items()
        if len({abbr for abbr in abbrs if abbr}) > 1
    }

    entry_aliases = sorted(
        {
            abbreviation
            for item in items
            for abbreviation in item.get("used_abbreviation_aliases", [])
        }
    )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sources": {
            "current_main_tex": current_inventory["source_path"],
            "earlier_pilot": pilot_inventory["source_path"],
        },
        "summary": {
            "integrated_item_count": len(items),
            "current_item_count": current_inventory["summary"]["item_count"],
            "pilot_item_count": pilot_inventory["summary"]["item_count"],
            "items_in_both_sources": sum(
                1 for item in items if {source["source"] for source in item["sources"]} == {"current_main_tex", "earlier_pilot"}
            ),
            "current_only_item_count": sum(
                1 for item in items if {source["source"] for source in item["sources"]} == {"current_main_tex"}
            ),
            "pilot_only_item_count": sum(
                1 for item in items if {source["source"] for source in item["sources"]} == {"earlier_pilot"}
            ),
            "entry_alias_count": len(entry_aliases),
            "duplicate_abbreviation_count": len(duplicate_abbreviations),
            "duplicate_graph_conflict_count": len(duplicate_graphs),
            "ambiguous_used_abbreviation_count": len(ambiguous_used_abbreviations),
            "missing_used_abbreviation_count": len(missing_used_abbreviations),
        },
        "duplicate_abbreviations": duplicate_abbreviations,
        "duplicate_graphs": duplicate_graphs,
        "entry_aliases": entry_aliases,
        "ambiguous_used_abbreviations": ambiguous_used_abbreviations,
        "missing_used_abbreviations": missing_used_abbreviations,
        "items": items,
    }


def render_report(data: dict[str, Any]) -> str:
    lines = [
        "# Integrated semantic components",
        "",
        f"- Current semantic source: `{data['sources']['current_main_tex']}`",
        f"- Earlier pilot semantic source: `{data['sources']['earlier_pilot']}`",
        f"- Integrated items: {data['summary']['integrated_item_count']}",
        f"- Items present in both sources: {data['summary']['items_in_both_sources']}",
        f"- Current-only items: {data['summary']['current_only_item_count']}",
        f"- Pilot-only items: {data['summary']['pilot_only_item_count']}",
        f"- Entry-form aliases matched to canonical semantic rows: {data['summary']['entry_alias_count']}",
        f"- Duplicate abbreviations with multiple graphs: {data['summary']['duplicate_abbreviation_count']}",
        f"- Duplicate graphs with conflicting abbreviations: {data['summary']['duplicate_graph_conflict_count']}",
        f"- Ambiguous abbreviations used in entries: {data['summary']['ambiguous_used_abbreviation_count']}",
        f"- Abbreviations used in entries but missing from the semantic list: {data['summary']['missing_used_abbreviation_count']}",
        "",
    ]

    if data["entry_aliases"]:
        lines.extend(
            [
                "## Entry-form aliases matched to canonical semantic rows",
                "",
                ", ".join(f"`{abbr}`" for abbr in data["entry_aliases"]),
                "",
            ]
        )

    if data["ambiguous_used_abbreviations"]:
        lines.extend(
            [
                "## Abbreviations used in entries with ambiguous semantic matches",
                "",
                "| Abbreviation | Matching semantic rows |",
                "| --- | --- |",
            ]
        )
        for abbreviation, matches in sorted(data["ambiguous_used_abbreviations"].items()):
            lines.append(f"| `{abbreviation}` | {'; '.join(f'`{match}`' for match in matches)} |")
        lines.append("")

    if data["missing_used_abbreviations"]:
        lines.extend(
            [
                "## Abbreviations used in entries but missing from the semantic list",
                "",
                ", ".join(f"`{abbr}`" for abbr in data["missing_used_abbreviations"]),
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
            lines.append(f"| `{graph}` | {'; '.join(f'`{abbr}`' for abbr in abbreviations)} |")
        lines.append("")

    lines.extend(
        [
            "## Integrated inventory",
            "",
            "| Graph | Abbr. | Expanded Latin | Notes | Entry-form aliases | Used in dictionary | Provenance |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for item in data["items"]:
        provenance = ", ".join(source["source"] for source in item["sources"])
        used = "yes" if item["used_in_integrated_dictionary"] else "no"
        notes = " / ".join(
            part for part in [item.get("notes")] + list(item.get("comments") or []) if part
        )
        aliases = ", ".join(f"`{abbr}`" for abbr in item.get("used_abbreviation_aliases", []))
        lines.append(
            f"| `{(item.get('graph_raw') or '').replace('`', '\\`')}` | "
            f"`{item.get('abbreviation') or ''}` | "
            f"`{item.get('expanded_latin') or ''}` | "
            f"{notes.replace('|', '\\|')} | {aliases} | {used} | {provenance} |"
        )
    lines.append("")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build an integrated semantic-component inventory from current main.tex and the earlier pilot.")
    parser.add_argument("--current-source", default=DEFAULT_CURRENT_SOURCE)
    parser.add_argument("--pilot-source", default=DEFAULT_PILOT_SOURCE)
    parser.add_argument("--current-entries", default=DEFAULT_CURRENT_ENTRIES)
    parser.add_argument("--curation-dir", default=DEFAULT_CURATION_DIR)
    parser.add_argument("--json-out", default=DEFAULT_JSON_OUT)
    parser.add_argument("--report-out", default=DEFAULT_REPORT_OUT)
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
    integrated = merge_inventories(current_inventory, pilot_inventory, current_entries, curated_entries)

    json_out = Path(args.json_out)
    report_out = Path(args.report_out)
    json_out.parent.mkdir(parents=True, exist_ok=True)
    report_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(integrated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_out.write_text(render_report(integrated), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
