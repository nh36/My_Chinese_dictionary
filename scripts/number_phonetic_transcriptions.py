from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import build_semantic_evidence
import hierarchy_utils
import render_curated_series


DEFAULT_CURATION_DIR = "data/entries/curation"
DEFAULT_INTEGRATED_SERIES_DIR = "data/entries/integrated_series"
DEFAULT_REPORT_OUT = "reports/transcription_numbering.md"
DEFAULT_AB_REPORT_OUT = "reports/ab_subseries_classification.md"

SUBSCRIPT_DIGITS = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
SUBSCRIPT_TO_DIGIT = {sub: digit for digit, sub in zip("0123456789", "₀₁₂₃₄₅₆₇₈₉")}
SUBSCRIPT_RE = re.compile(r"([₀₁₂₃₄₅₆₇₈₉]+)$")


def to_subscript(number: int) -> str:
    return str(number).translate(SUBSCRIPT_DIGITS)


def split_root_ordinal(root: str | None) -> tuple[str | None, int]:
    if root is None:
        return None, 1
    match = SUBSCRIPT_RE.search(root)
    if not match:
        return root, 1
    digits = "".join(SUBSCRIPT_TO_DIGIT[char] for char in match.group(1))
    return root[: match.start()], int(digits)


def format_root_ordinal(base_root: str, ordinal: int) -> str:
    if ordinal <= 1:
        return base_root
    return f"{base_root}{to_subscript(ordinal)}"


def iter_parent_root_candidates(
    candidates: list[dict[str, Any]],
    candidate_children: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    ordered: list[dict[str, Any]] = []
    for candidate in candidates:
        children = candidate_children.get(candidate["character"], [])
        if not children:
            continue
        ordered.append(candidate)
        ordered.extend(iter_parent_root_candidates(children, candidate_children))
    return ordered


def split_missing_entry_candidates(entry: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    candidate_children = hierarchy_utils.collect_candidate_children(entry)
    head_character = entry["proposed_additions"][0]["character"] if entry.get("proposed_additions") else None
    direct_candidates: list[dict[str, Any]] = []
    head_child_candidates: list[dict[str, Any]] = []
    for index, candidate in enumerate(entry.get("proposed_additions", [])):
        if index == 0:
            continue
        assignment = candidate.get("hierarchy_assignment") or {}
        status = assignment.get("status")
        parent_character = assignment.get("parent_character")
        if status == "assigned-to-inherited-node":
            continue
        if status == "assigned-to-top-level":
            if candidate_children.get(candidate["character"]):
                head_child_candidates.append(candidate)
            else:
                direct_candidates.append(candidate)
            continue
        if status == "assigned-to-candidate-node":
            if head_character and parent_character == head_character:
                if candidate_children.get(candidate["character"]):
                    head_child_candidates.append(candidate)
                else:
                    direct_candidates.append(candidate)
            continue
        direct_candidates.append(candidate)
    return direct_candidates, head_child_candidates


def mutable_series_root_occurrence(entry: dict[str, Any]) -> dict[str, Any] | None:
    root_data = entry.get("resolved_series_root")
    if not root_data:
        return None
    current_root = root_data.get("display_root") or root_data.get("root")
    if not current_root:
        return None
    return {
        "mutable": True,
        "kind": "series-root",
        "entry_id": entry["id"],
        "character": (root_data.get("character") or (entry.get("proposed_additions") or [{}])[0].get("character")),
        "root_data": root_data,
        "current_root": current_root,
    }


def mutable_subseries_root_occurrences(entry: dict[str, Any]) -> list[dict[str, Any]]:
    candidate_children = hierarchy_utils.collect_candidate_children(entry)
    occurrences: list[dict[str, Any]] = []
    if entry["packet_kind"] == "missing_series":
        direct_candidates, head_child_candidates = split_missing_entry_candidates(entry)
        ordered_candidates = (
            iter_parent_root_candidates(direct_candidates, candidate_children)
            + iter_parent_root_candidates(head_child_candidates, candidate_children)
        )
    else:
        hierarchy_nodes = (entry.get("entry_hierarchy") or {}).get("nodes") or []
        grouped_by_parent: dict[str, list[dict[str, Any]]] = {}
        top_level_candidates = [
            candidate
            for candidate in entry.get("proposed_additions", [])
            if (candidate.get("hierarchy_assignment") or {}).get("status")
            not in {"assigned-to-inherited-node", "assigned-to-candidate-node"}
        ]
        for candidate in entry.get("proposed_additions", []):
            assignment = candidate.get("hierarchy_assignment") or {}
            if assignment.get("status") == "assigned-to-inherited-node" and assignment.get("parent_character"):
                grouped_by_parent.setdefault(assignment["parent_character"], []).append(candidate)
        ordered_candidates = iter_parent_root_candidates(top_level_candidates, candidate_children)
        for node in hierarchy_nodes:
            ordered_candidates.extend(
                iter_parent_root_candidates(grouped_by_parent.get(node.get("key_character")) or [], candidate_children)
            )

    for candidate in ordered_candidates:
        root_data = candidate.get("resolved_node_root")
        if not root_data:
            continue
        current_root = root_data.get("display_root") or root_data.get("root")
        if not current_root:
            continue
        occurrences.append(
            {
                "mutable": True,
                "kind": "subseries-root",
                "entry_id": entry["id"],
                "character": candidate["character"],
                "root_data": root_data,
                "current_root": current_root,
            }
        )
    return occurrences


def baseline_root_occurrences(entry: dict[str, Any]) -> list[dict[str, Any]]:
    tex_entry = entry.get("tex_entry")
    if not tex_entry:
        return []
    occurrences: list[dict[str, Any]] = []
    top_root = build_semantic_evidence.extract_series_root_latex(tex_entry["raw_block"])
    if top_root:
        occurrences.append(
            {
                "mutable": False,
                "kind": "baseline-series-root",
                "entry_id": entry["id"],
                "character": hierarchy_utils.extract_head_character(tex_entry.get("head")),
                "root_data": None,
                "current_root": top_root,
            }
        )
    for node in hierarchy_utils.extract_hierarchy_nodes(tex_entry["raw_block"]):
        rhs_root = hierarchy_utils.extract_large_content(node.get("rhs_snippet"))
        if not rhs_root:
            continue
        occurrences.append(
            {
                "mutable": False,
                "kind": "baseline-subseries-root",
                "entry_id": entry["id"],
                "character": node.get("key_character"),
                "root_data": None,
                "current_root": rhs_root,
            }
        )
    return occurrences


def iter_document_root_occurrences(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ordered_entries = render_curated_series.sort_entries(entries)
    missing_entries = [entry for entry in ordered_entries if entry["packet_kind"] == "missing_series"]
    existing_entries = [entry for entry in ordered_entries if entry["packet_kind"] != "missing_series"]

    occurrences: list[dict[str, Any]] = []
    for entry in missing_entries:
        root_occurrence = mutable_series_root_occurrence(entry)
        if root_occurrence is not None:
            occurrences.append(root_occurrence)
        occurrences.extend(mutable_subseries_root_occurrences(entry))

    for entry in existing_entries:
        occurrences.extend(baseline_root_occurrences(entry))
        occurrences.extend(mutable_subseries_root_occurrences(entry))

    return occurrences


def load_integrated_records(series_dir: Path) -> list[dict[str, Any]]:
    if not series_dir.exists():
        return []
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(series_dir.glob("*.json"), key=lambda path: render_curated_series.entry_sort_key({"id": path.stem}))
    ]


def iter_integrated_document_root_occurrences(
    entries: list[dict[str, Any]],
    integrated_records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    entry_by_id = {entry["id"]: entry for entry in entries if entry.get("id")}
    ordered_records = sorted(integrated_records, key=render_curated_series.entry_sort_key)
    occurrences: list[dict[str, Any]] = []

    for record in ordered_records:
        entry_id = record.get("id")
        current_entry = entry_by_id.get(entry_id) if entry_id else None
        render_mode = record.get("render_mode")
        preferred_hand_entry = record.get("preferred_hand_entry")

        if preferred_hand_entry is not None:
            pseudo_hand_entry = {"id": entry_id, "tex_entry": preferred_hand_entry}
        else:
            pseudo_hand_entry = None

        if render_mode == "generated_missing_series":
            if current_entry is None:
                continue
            root_occurrence = mutable_series_root_occurrence(current_entry)
            if root_occurrence is not None:
                occurrences.append(root_occurrence)
            occurrences.extend(mutable_subseries_root_occurrences(current_entry))
            continue

        if render_mode == "hand_with_generated_additions":
            if pseudo_hand_entry is not None:
                occurrences.extend(baseline_root_occurrences(pseudo_hand_entry))
            if current_entry is not None:
                occurrences.extend(mutable_subseries_root_occurrences(current_entry))
            continue

        if render_mode == "hand_only":
            if pseudo_hand_entry is not None:
                occurrences.extend(baseline_root_occurrences(pseudo_hand_entry))
            continue

        if current_entry is not None:
            occurrences.extend(iter_document_root_occurrences([current_entry]))

    return occurrences


def apply_numbering(
    entries: list[dict[str, Any]],
    integrated_records: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    counters: dict[str, int] = {}
    mutable_count = 0
    renumbered_count = 0
    duplicates: dict[str, int] = {}
    report_rows: list[dict[str, Any]] = []
    order_source = "curation_order"

    if integrated_records:
        occurrences = iter_integrated_document_root_occurrences(entries, integrated_records)
        order_source = "integrated_render_order"
    else:
        occurrences = iter_document_root_occurrences(entries)

    for occurrence in occurrences:
        base_root, existing_ordinal = split_root_ordinal(occurrence["current_root"])
        if not base_root:
            continue
        next_count = counters.get(base_root, 0) + 1
        if occurrence["mutable"]:
            assigned_ordinal = next_count
            counters[base_root] = assigned_ordinal
            display_root = format_root_ordinal(base_root, assigned_ordinal)
            root_data = occurrence["root_data"]
            root_data["base_root"] = base_root
            root_data["ordinal"] = assigned_ordinal
            root_data["display_root"] = display_root
            root_data["numbering_source"] = "document_order_occurrence"
            mutable_count += 1
            if display_root != occurrence["current_root"]:
                renumbered_count += 1
        else:
            assigned_ordinal = max(next_count, existing_ordinal)
            counters[base_root] = assigned_ordinal
            display_root = occurrence["current_root"]
        duplicates[base_root] = counters[base_root]
        report_rows.append(
            {
                "entry_id": occurrence["entry_id"],
                "kind": occurrence["kind"],
                "character": occurrence["character"],
                "base_root": base_root,
                "ordinal": assigned_ordinal,
                "display_root": display_root,
                "mutable": occurrence["mutable"],
            }
        )

    for entry in entries:
        candidate_map = {candidate["character"]: candidate for candidate in entry.get("proposed_additions", [])}
        for candidate in entry.get("proposed_additions", []):
            parent_display_root = build_semantic_evidence.resolve_parent_display_root_for_candidate(
                entry, candidate, candidate_map
            )
            if parent_display_root:
                candidate["transliteration_latex"] = build_semantic_evidence.derive_transliteration_from_resolved_root(
                    parent_display_root, candidate
                )
                candidate["render_latex"] = build_semantic_evidence.synthesize_render_latex(candidate)

    duplicate_roots = {root: count for root, count in duplicates.items() if count > 1}
    return {
        "order_source": order_source,
        "mutable_root_count": mutable_count,
        "renumbered_root_count": renumbered_count,
        "duplicate_root_count": len(duplicate_roots),
        "duplicate_roots": duplicate_roots,
        "rows": report_rows,
    }


def render_report(summary: dict[str, Any]) -> str:
    lines = [
        "# Transcription numbering",
        "",
        f"- Ordering source: {summary['order_source']}",
        f"- Mutable series/subseries roots inspected: {summary['mutable_root_count']}",
        f"- Roots whose display label changed after document-wide renumbering: {summary['renumbered_root_count']}",
        f"- Duplicate phonetic bases encountered in document order: {summary['duplicate_root_count']}",
        "",
        "| GSC | Kind | Character | Base root | Ordinal | Display root | Mutable |",
        "| --- | --- | --- | --- | ---: | --- | --- |",
    ]
    for row in summary["rows"]:
        lines.append(
            f"| `{row['entry_id']}` | `{row['kind']}` | {row['character'] or ''} | "
            f"`{row['base_root']}` | {row['ordinal']} | `{row['display_root']}` | "
            f"{'yes' if row['mutable'] else 'no'} |"
        )
    return "\n".join(lines) + "\n"


def load_entries(curation_dir: Path) -> list[dict[str, Any]]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(curation_dir.glob("*.json"))
    ]


def write_entries(entries: list[dict[str, Any]], curation_dir: Path) -> None:
    for entry in entries:
        path = curation_dir / f"{entry['id']}.json"
        path.write_text(json.dumps(entry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Assign document-wide ordinal subscripts to duplicate phonetic transcriptions.")
    parser.add_argument("--curation-dir", default=DEFAULT_CURATION_DIR)
    parser.add_argument("--integrated-series-dir", default=DEFAULT_INTEGRATED_SERIES_DIR)
    parser.add_argument("--report-out", default=DEFAULT_REPORT_OUT)
    parser.add_argument("--ab-report-out", default=DEFAULT_AB_REPORT_OUT)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    curation_dir = Path(args.curation_dir)
    entries = load_entries(curation_dir)
    integrated_records = load_integrated_records(Path(args.integrated_series_dir))
    summary = apply_numbering(entries, integrated_records=integrated_records or None)
    write_entries(entries, curation_dir)
    report_path = Path(args.report_out)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_report(summary), encoding="utf-8")
    ab_report_path = Path(args.ab_report_out)
    ab_report_path.parent.mkdir(parents=True, exist_ok=True)
    ab_report_path.write_text(build_semantic_evidence.render_ab_subseries_report(entries), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
