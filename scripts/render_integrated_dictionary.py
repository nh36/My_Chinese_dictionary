from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import render_curated_series


DEFAULT_SEMANTIC_JSON = "data/semantic_components/integrated_semantic_components.json"
DEFAULT_SERIES_DIR = "data/entries/integrated_series"
DEFAULT_MAIN_TEX = "main.tex"
DEFAULT_OUTPUT = "build/generated_integrated_dictionary.tex"
DEFAULT_PDF_OUTPUT = "build/generated_integrated_dictionary.pdf"
DEFAULT_REPORT_OUT = "reports/integration_summary.md"


def load_integrated_items(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_integrated_records(series_dir: Path) -> list[dict[str, Any]]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(series_dir.glob("*.json"), key=lambda path: render_curated_series.entry_sort_key({"id": path.stem}))
    ]


def sanitize_hand_entry(raw_block: str) -> str:
    filtered = render_curated_series.strip_column_context_lines(raw_block)
    lines = [line for line in filtered.splitlines() if line.strip() and line.strip() not in {r"\end{document}", r"\begin{document}"}]
    return "\n".join(lines).rstrip()


def render_semantic_section(semantic_data: dict[str, Any]) -> list[str]:
    lines = [
        r"\section*{Integrated semantic components}",
        "",
        r"\begin{multicols*}{2}",
        r"\raggedcolumns",
        r"\begin{spacing}{0.8}",
        r"\begin{itemize}[noitemsep]",
    ]
    for item in semantic_data["items"]:
        graph = item.get("graph_raw") or "—"
        abbreviation = item.get("abbreviation") or ""
        expanded = item.get("expanded_latin") or ""
        note_parts = [item.get("notes")] + list(item.get("comments") or [])
        aliases = item.get("used_abbreviation_aliases") or []
        if aliases:
            note_parts.append("entry aliases: " + ", ".join(aliases))
        notes = " / ".join(part for part in note_parts if part)
        provenance_labels = []
        for source_name in sorted({source["source"] for source in item.get("sources", [])}):
            if source_name == "current_main_tex":
                provenance_labels.append("current")
            elif source_name == "earlier_pilot":
                provenance_labels.append("pilot")
            else:
                provenance_labels.append(source_name)
        provenance = "+".join(provenance_labels)
        body = graph
        if abbreviation:
            body += rf" \textbf{{{abbreviation}}}"
        if expanded and expanded != abbreviation:
            body += f" {expanded}"
        if notes:
            body += f" --- {notes}"
        body += rf" {{\footnotesize[{provenance}]}}"
        lines.append(r"\item " + body)
    lines.extend(
        [
            r"\end{itemize}",
            r"\end{spacing}",
            r"\end{multicols*}",
            "",
        ]
    )
    return lines


def render_integrated_entry(record: dict[str, Any]) -> str:
    curated_entry = record.get("curated_entry")
    hand_entry = record.get("preferred_hand_entry")
    render_mode = record.get("render_mode")

    if render_mode == "hand_with_generated_additions" and curated_entry is not None:
        return render_curated_series.render_curated_entry(curated_entry)
    if render_mode == "generated_missing_series" and curated_entry is not None:
        return render_curated_series.render_curated_entry(curated_entry)
    if hand_entry is not None:
        return sanitize_hand_entry(hand_entry["raw_block"])
    pilot_entry = record.get("pilot_entry")
    if pilot_entry is not None:
        return sanitize_hand_entry(pilot_entry["raw_block"])
    return rf"\paragraph{{\textoversetlarge{{{record['id']}}}{{\huge{{{record['id']}}}}}}}"


def render_review_appendix(records: list[dict[str, Any]]) -> list[str]:
    generated_only = [record for record in records if record.get("render_mode") == "generated_missing_series"]
    hand_with_addenda = [record for record in records if record.get("render_mode") == "hand_with_generated_additions"]
    conflicts = [record for record in records if record.get("conflicts")]

    lines = [
        r"\section*{Integration review appendix}",
        "",
        rf"\textbf{{Generated missing-series packets}}: {len(generated_only)}\\",
        rf"\textbf{{Hand-authored entries with generated addenda}}: {len(hand_with_addenda)}\\",
        rf"\textbf{{Hand-source conflicts}}: {len(conflicts)}\\",
        "",
    ]
    if conflicts:
        lines.append(r"\begin{itemize}[noitemsep]")
        for record in conflicts:
            lines.append(rf"\item {record['id']}: {', '.join(conflict['kind'] for conflict in record['conflicts'])}")
        lines.append(r"\end{itemize}")
    lines.append("")
    return lines


def render_document(semantic_data: dict[str, Any], records: list[dict[str, Any]], main_tex_path: Path) -> str:
    body = [
        r"\begin{document}",
        r"% GENERATED FILE - DO NOT EDIT BY HAND.",
        r"\section*{Integrated xiéshēng dictionary review}",
        "",
    ]
    body.extend(render_curated_series.COLUMN_GUARDRAIL_MACROS)
    body.append("")
    body.extend(render_semantic_section(semantic_data))
    body.extend(
        [
            r"\section*{Integrated xiéshēng dictionary}",
            "",
            r"\begin{multicols*}{2}",
            r"\raggedcolumns",
            r"\begin{spacing}{0.7}",
        ]
    )
    for record in records:
        body.append(render_curated_series.wrap_entry_guardrail(render_integrated_entry(record)))
        body.append("")
    body.extend(
        [
            r"\end{spacing}",
            r"\end{multicols*}",
            "",
        ]
    )
    body.extend(render_review_appendix(records))
    body.append(r"\end{document}")
    return render_curated_series.extract_preamble(main_tex_path) + "\n".join(body) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render the integrated semantic-component list and xiéshēng dictionary review document.")
    parser.add_argument("--semantic-json", default=DEFAULT_SEMANTIC_JSON)
    parser.add_argument("--series-dir", default=DEFAULT_SERIES_DIR)
    parser.add_argument("--main-tex", default=DEFAULT_MAIN_TEX)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    semantic_data = load_integrated_items(Path(args.semantic_json))
    records = load_integrated_records(Path(args.series_dir))
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_document(semantic_data, records, Path(args.main_tex)), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
