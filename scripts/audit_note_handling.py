from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import note_utils
import render_curated_series


DEFAULT_INTEGRATED_SERIES_DIR = "data/entries/integrated_series"
DEFAULT_JSON_OUT = "data/derived/note_inventory.json"
DEFAULT_REPORT_OUT = "reports/note_inventory.md"


def load_integrated_records(series_dir: Path) -> list[dict[str, Any]]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(series_dir.glob("*.json"), key=lambda path: render_curated_series.entry_sort_key({"id": path.stem}))
    ]


def build_inventory(records: list[dict[str, Any]]) -> dict[str, Any]:
    notes: list[dict[str, Any]] = []
    for record in records:
        normalized_notes = record.get("normalized_notes")
        if normalized_notes is None:
            normalized_notes = note_utils.collect_record_notes(
                entry_id=record["id"],
                hand_entry=record.get("preferred_hand_entry"),
                curated_entry=record.get("curated_entry"),
            )
        notes.extend(normalized_notes)

    by_entry: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for note in notes:
        by_entry[note["entry_id"]].append(note)

    summary = {
        "entry_count_with_notes": len(by_entry),
        "total_notes": len(notes),
        "by_source_layer": dict(Counter(note["source_layer"] for note in notes)),
        "by_category": dict(Counter(note["category"] for note in notes)),
        "by_visibility": dict(Counter(note["visibility"] for note in notes)),
        "by_recommended_rendering": dict(Counter(note["recommended_rendering"] for note in notes)),
    }
    return {
        "summary": summary,
        "notes": notes,
    }


def render_report(inventory: dict[str, Any]) -> str:
    summary = inventory["summary"]
    notes = inventory["notes"]
    lines = [
        "# Note inventory",
        "",
        "- Commented-out source material is excluded from this inventory.",
        f"- Entries with at least one note: {summary['entry_count_with_notes']}",
        f"- Total notes inventoried: {summary['total_notes']}",
        "",
        "## By source layer",
        "",
        "| Source layer | Count |",
        "| --- | ---: |",
    ]
    for source_layer, count in sorted(summary["by_source_layer"].items()):
        lines.append(f"| `{source_layer}` | {count} |")

    lines.extend(
        [
            "",
            "## By category",
            "",
            "| Category | Count |",
            "| --- | ---: |",
        ]
    )
    for category, count in sorted(summary["by_category"].items()):
        lines.append(f"| `{category}` | {count} |")

    lines.extend(
        [
            "",
            "## By recommended rendering",
            "",
            "| Rendering policy | Count |",
            "| --- | ---: |",
        ]
    )
    for rendering, count in sorted(summary["by_recommended_rendering"].items()):
        lines.append(f"| `{rendering}` | {count} |")

    examples_by_category: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for note in notes:
        examples_by_category[note["category"]].append(note)

    for category in sorted(examples_by_category):
        lines.extend(
            [
                "",
                f"## Examples: `{category}`",
                "",
                "| GSC | Source layer | Anchor | Rendering | Text |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for note in examples_by_category[category][:10]:
            anchor = note["anchor_kind"]
            if note.get("anchor_value"):
                anchor += f": {note['anchor_value']}"
            text = note["text"].replace("|", "\\|")
            lines.append(
                f"| `{note['entry_id']}` | `{note['source_layer']}` | {anchor} | "
                f"`{note['recommended_rendering']}` | {text} |"
            )

    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit visible and structured note handling across integrated series records.")
    parser.add_argument("--integrated-series-dir", default=DEFAULT_INTEGRATED_SERIES_DIR)
    parser.add_argument("--json-out", default=DEFAULT_JSON_OUT)
    parser.add_argument("--report-out", default=DEFAULT_REPORT_OUT)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    records = load_integrated_records(Path(args.integrated_series_dir))
    inventory = build_inventory(records)
    json_out = Path(args.json_out)
    report_out = Path(args.report_out)
    json_out.parent.mkdir(parents=True, exist_ok=True)
    report_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_out.write_text(render_report(inventory), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
