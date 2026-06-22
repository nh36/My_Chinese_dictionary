from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import extract_tex_entries
import note_utils
import render_curated_series


DEFAULT_CURRENT_ENTRIES = "data/current_tex_entries.json"
DEFAULT_PILOT_SOURCE = "key references/My_Chinese_dictionary/main.tex"
DEFAULT_CURATION_DIR = "data/entries/curation"
DEFAULT_OUTPUT_DIR = "data/entries/integrated_series"
DEFAULT_CONFLICT_REPORT = "reports/integrated_series_conflicts.md"
DEFAULT_SUMMARY_REPORT = "reports/integration_summary.md"


def load_current_entries(path: Path) -> dict[str, dict[str, Any]]:
    return {
        entry["id"]: entry
        for entry in json.loads(path.read_text(encoding="utf-8"))["entries"]
        if entry.get("id")
    }


def load_pilot_entries(path: Path) -> dict[str, dict[str, Any]]:
    source_text = path.read_text(encoding="utf-8")
    return {
        entry["id"]: entry
        for entry in extract_tex_entries.extract_entries(source_text, source_path=str(path))["entries"]
        if entry.get("id")
    }


def load_active_curated_entries(curation_dir: Path) -> dict[str, dict[str, Any]]:
    entries: dict[str, dict[str, Any]] = {}
    for entry_id in render_curated_series.DEFAULT_IDS:
        path = curation_dir / f"{entry_id}.json"
        if path.exists():
            entries[entry_id] = json.loads(path.read_text(encoding="utf-8"))
    return entries


def normalize_raw_block(raw_block: str | None) -> str:
    if not raw_block:
        return ""
    return "\n".join(line.rstrip() for line in raw_block.splitlines()).strip()


def derive_schuessler(entry_id: str, curated_entry: dict[str, Any] | None) -> dict[str, Any]:
    if curated_entry and curated_entry.get("schuessler"):
        return curated_entry["schuessler"]
    left, _, right = entry_id.partition("-")
    return {"gsc_id": entry_id, "rhyme_section": int(left), "series_number": int(right)}


def build_record(
    entry_id: str,
    current_entry: dict[str, Any] | None,
    pilot_entry: dict[str, Any] | None,
    curated_entry: dict[str, Any] | None,
    pilot_source_path: Path,
) -> dict[str, Any]:
    hand_entry = current_entry or pilot_entry
    provenance: list[dict[str, Any]] = []
    status_flags: list[str] = []
    conflicts: list[dict[str, Any]] = []

    if current_entry is not None:
        provenance.append(
            {
                "source": "current_main_tex",
                "source_path": "main.tex",
                "start_line": current_entry.get("start_line"),
                "end_line": current_entry.get("end_line"),
                "subsection": current_entry.get("subsection"),
            }
        )
        status_flags.append("hand_authored_current_tex")
    if pilot_entry is not None:
        provenance.append(
            {
                "source": "earlier_pilot",
                "source_path": str(pilot_source_path),
                "start_line": pilot_entry.get("start_line"),
                "end_line": pilot_entry.get("end_line"),
                "subsection": pilot_entry.get("subsection"),
            }
        )
        status_flags.append("imported_from_previous_pilot")
    if current_entry is not None and pilot_entry is not None:
        status_flags.append("present_in_both_hand_sources")
        if normalize_raw_block(current_entry.get("raw_block")) != normalize_raw_block(pilot_entry.get("raw_block")):
            conflicts.append(
                {
                    "kind": "hand_source_raw_mismatch",
                    "current_source": "main.tex",
                    "pilot_source": str(pilot_source_path),
                }
            )

    if curated_entry is not None:
        provenance.append(
            {
                "source": "current_curation",
                "source_path": f"data/entries/curation/{entry_id}.json",
                "packet_kind": curated_entry.get("packet_kind"),
                "status": curated_entry.get("status"),
            }
        )
        status_flags.append("needs_review")
        if curated_entry.get("packet_kind") == "existing_addendum" and hand_entry is not None:
            status_flags.append("generated_with_hand_baseline")
        else:
            status_flags.append("generated_candidate")

    if hand_entry is not None and curated_entry is None:
        status_flags.append("hand_checked")

    pilot_matches_current = (
        current_entry is not None
        and pilot_entry is not None
        and normalize_raw_block(current_entry.get("raw_block")) == normalize_raw_block(pilot_entry.get("raw_block"))
    )
    normalized_notes = note_utils.collect_record_notes(
        entry_id=entry_id,
        hand_entry=hand_entry,
        curated_entry=curated_entry,
    )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "id": entry_id,
        "schuessler": derive_schuessler(entry_id, curated_entry),
        "preferred_hand_entry": hand_entry,
        "pilot_entry": None if pilot_matches_current else pilot_entry,
        "curated_entry": curated_entry,
        "provenance": provenance,
        "status_flags": status_flags,
        "conflicts": conflicts,
        "normalized_notes": normalized_notes,
        "note_summary": note_utils.summarize_notes(normalized_notes),
        "render_mode": (
            "hand_with_generated_additions"
            if curated_entry and curated_entry.get("packet_kind") == "existing_addendum" and hand_entry is not None
            else "generated_missing_series"
            if curated_entry is not None
            else "hand_only"
            if hand_entry is not None
            else "unresolved"
        ),
    }


def write_integrated_records(records: list[dict[str, Any]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for record in records:
        (output_dir / f"{record['id']}.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )


def render_conflict_report(records: list[dict[str, Any]]) -> str:
    raw_conflicts = [record for record in records if record["conflicts"]]
    pilot_only = [record for record in records if record["pilot_entry"] and not record["preferred_hand_entry"]]
    generated_only = [record for record in records if record["render_mode"] == "generated_missing_series"]

    lines = [
        "# Integrated series conflicts",
        "",
        f"- Integrated series records: {len(records)}",
        f"- Hand-source raw mismatches: {len(raw_conflicts)}",
        f"- Pilot-only entries: {len(pilot_only)}",
        f"- Generated-only missing-series packets: {len(generated_only)}",
        "",
    ]

    if raw_conflicts:
        lines.extend(
            [
                "## Hand-source mismatches",
                "",
                "| GSC | Conflicts |",
                "| --- | --- |",
            ]
        )
        for record in raw_conflicts:
            lines.append(f"| `{record['id']}` | {', '.join(conflict['kind'] for conflict in record['conflicts'])} |")
        lines.append("")

    lines.extend(
        [
            "## Generated-only packets",
            "",
            "| GSC | Packet kind | Status flags |",
            "| --- | --- | --- |",
        ]
    )
    for record in generated_only:
        packet_kind = (record.get("curated_entry") or {}).get("packet_kind", "")
        lines.append(f"| `{record['id']}` | `{packet_kind}` | {', '.join(record['status_flags'])} |")
    lines.append("")
    return "\n".join(lines)


def render_summary_report(records: list[dict[str, Any]]) -> str:
    current_count = sum(1 for record in records if any(source["source"] == "current_main_tex" for source in record["provenance"]))
    pilot_count = sum(1 for record in records if any(source["source"] == "earlier_pilot" for source in record["provenance"]))
    curated_count = sum(1 for record in records if any(source["source"] == "current_curation" for source in record["provenance"]))
    generated_missing = sum(1 for record in records if record["render_mode"] == "generated_missing_series")
    hand_with_addenda = sum(1 for record in records if record["render_mode"] == "hand_with_generated_additions")
    hand_only = sum(1 for record in records if record["render_mode"] == "hand_only")
    conflict_count = sum(1 for record in records if record["conflicts"])

    lines = [
        "# Integration summary",
        "",
        f"- Integrated series count: {len(records)}",
        f"- Current hand-authored series count: {current_count}",
        f"- Earlier pilot hand-authored series count: {pilot_count}",
        f"- Active curated packet count: {curated_count}",
        f"- Hand-only rendered entries: {hand_only}",
        f"- Hand baseline + generated addenda entries: {hand_with_addenda}",
        f"- Generated missing-series entries: {generated_missing}",
        f"- Records with hand-source conflicts: {conflict_count}",
        "",
        "| GSC | Render mode | Status flags |",
        "| --- | --- | --- |",
    ]
    for record in records:
        lines.append(f"| `{record['id']}` | `{record['render_mode']}` | {', '.join(record['status_flags'])} |")
    lines.append("")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build an integrated series model from current main.tex, the earlier pilot, and current curated packets.")
    parser.add_argument("--current-entries", default=DEFAULT_CURRENT_ENTRIES)
    parser.add_argument("--pilot-source", default=DEFAULT_PILOT_SOURCE)
    parser.add_argument("--curation-dir", default=DEFAULT_CURATION_DIR)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--conflict-report", default=DEFAULT_CONFLICT_REPORT)
    parser.add_argument("--summary-report", default=DEFAULT_SUMMARY_REPORT)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    current_entries = load_current_entries(Path(args.current_entries))
    pilot_source_path = Path(args.pilot_source)
    pilot_entries = load_pilot_entries(pilot_source_path)
    curated_entries = load_active_curated_entries(Path(args.curation_dir))

    all_ids = sorted(set(current_entries) | set(pilot_entries) | set(curated_entries), key=lambda entry_id: render_curated_series.entry_sort_key({"id": entry_id}))
    records = [
        build_record(
            entry_id,
            current_entries.get(entry_id),
            pilot_entries.get(entry_id),
            curated_entries.get(entry_id),
            pilot_source_path,
        )
        for entry_id in all_ids
    ]

    write_integrated_records(records, Path(args.output_dir))

    conflict_path = Path(args.conflict_report)
    summary_path = Path(args.summary_report)
    conflict_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    conflict_path.write_text(render_conflict_report(records), encoding="utf-8")
    summary_path.write_text(render_summary_report(records), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
