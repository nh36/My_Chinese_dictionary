from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import render_entries


DEFAULT_INPUT_DIR = "data/entries/curation"
DEFAULT_IDS = ["02-01", "38-03", "04-30", "18-18", "01-01", "01-43"]
DEFAULT_MAIN_TEX = "main.tex"
DEFAULT_OUTPUT = "build/generated_curated_series_sample.tex"
DEFAULT_PDF_OUTPUT = "build/generated_curated_series_sample.pdf"
DEFAULT_REPORT = "reports/generated_curated_series_sample.md"


def load_curated_entry(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def extract_preamble(main_tex_path: Path) -> str:
    source = main_tex_path.read_text(encoding="utf-8")
    marker = "\\begin{document}"
    if marker not in source:
        raise ValueError(f"{main_tex_path} does not contain \\begin{{document}}.")
    return source.split(marker, 1)[0].rstrip() + "\n"


def render_curated_entry(entry: dict[str, Any]) -> str:
    packet_kind_tex = entry["packet_kind"].replace("_", r"\_")
    lines = [
        f"\\section*{{{entry['id']} candidate packet}}",
        "\\textbf{Status:} machine-curated pilot.\\\\",
        f"\\textbf{{Packet kind:}} {packet_kind_tex}\\\\",
        f"\\textbf{{Schuessler K tokens:}} {entry['coverage']['schuessler_k_tokens']}\\\\",
        f"\\textbf{{Combined source character count:}} {entry['coverage']['combined_source_character_count']}",
        "",
    ]

    if entry.get("tex_entry") is not None:
        wrapped_tex_entry = render_entries.wrap_entry_with_context(
            {
                "raw_latex": entry["tex_entry"]["raw_block"],
                "context_environments": entry["tex_entry"].get("context_environments", []),
            }
        )
        lines.extend(
            [
                "\\subsection*{Existing TeX baseline}",
                wrapped_tex_entry.rstrip(),
                "",
            ]
        )

    lines.extend(
        [
            "\\subsection*{Candidate additions / review targets}",
            "\\begin{itemize}",
        ]
    )
    for candidate in entry["proposed_additions"]:
        lines.append(
            f"\\item {candidate['character']} (Mand2MC rows: {candidate['mand2mc_count']}, "
            f"BS/GSR rows: {candidate['bs_gsr_count']}, Shengfu rows: {candidate['shengfu_character_count']})"
        )
    lines.append("\\end{itemize}")
    lines.append("")
    return "\n".join(lines)


def render_document(entries: list[dict[str, Any]], main_tex_path: Path) -> str:
    body = [
        "\\begin{document}",
        "% GENERATED FILE - DO NOT EDIT BY HAND.",
        "\\section*{Curated pilot series packets}",
        "",
    ]
    for entry in entries:
        body.append(render_curated_entry(entry))
    body.append("\\end{document}")
    return extract_preamble(main_tex_path) + "\n".join(body) + "\n"


def render_report(entries: list[dict[str, Any]], tex_path: Path) -> str:
    lines = [
        "# Generated curated series sample",
        "",
        f"- Generated TeX file: `{tex_path}`",
        "- This file is a review document, not final dictionary output.",
        "",
        "| GSC | Packet kind | Existing TeX baseline | Proposed additions |",
        "| --- | --- | --- | ---: |",
    ]
    for entry in entries:
        lines.append(
            f"| `{entry['id']}` | `{entry['packet_kind']}` | "
            f"{'yes' if entry.get('tex_entry') else 'no'} | {len(entry['proposed_additions'])} |"
        )
    return "\n".join(lines) + "\n"


def write_output(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render curated series packets to a review TeX file.")
    parser.add_argument("--input-dir", default=DEFAULT_INPUT_DIR)
    parser.add_argument("--main-tex", default=DEFAULT_MAIN_TEX)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--report-out", default=DEFAULT_REPORT)
    parser.add_argument("--ids", nargs="+", default=DEFAULT_IDS)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    entries = [
        load_curated_entry(Path(args.input_dir) / f"{gsc_id}.json")
        for gsc_id in args.ids
    ]
    write_output(Path(args.output), render_document(entries, Path(args.main_tex)))
    write_output(Path(args.report_out), render_report(entries, Path(args.output)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
