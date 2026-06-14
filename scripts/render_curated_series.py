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


def dedupe_preserve(values: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def render_context_wrapped_block(context_environments: list[dict[str, str]], body_lines: list[str]) -> str:
    lines: list[str] = []
    for environment in context_environments:
        lines.append(f"\\begin{{{environment['name']}}}{{{environment['arg']}}}")
    lines.extend(body_lines)
    for environment in reversed(context_environments):
        lines.append(f"\\end{{{environment['name']}}}")
    return "\n".join(lines)


def build_existing_heading_line(entry: dict[str, Any]) -> str:
    tex_entry = entry["tex_entry"]
    return (
        f"\\paragraph{{\\textoversetlarge{{{entry['id']}}}{{{tex_entry['head']['raw']}}}}}"
        f"{tex_entry['head'].get('heading_extra_raw', '')}"
    )


def collect_candidate_pinyins(candidate: dict[str, Any]) -> list[str]:
    return dedupe_preserve(
        [row["pinyin"] for row in candidate["mand2mc_rows"] if row.get("pinyin")]
        + [row["pinyin"] for row in candidate["bs_gsr_rows"] if row.get("pinyin")]
    )


def collect_candidate_mc_forms(candidate: dict[str, Any]) -> list[str]:
    mand_forms = [row["mc_nwh"] for row in candidate["mand2mc_rows"] if row.get("mc_nwh")]
    if mand_forms:
        return dedupe_preserve(mand_forms)
    return dedupe_preserve([row["mc_bs"] for row in candidate["bs_gsr_rows"] if row.get("mc_bs")])


def collect_candidate_gsr_values(candidate: dict[str, Any]) -> list[str]:
    return dedupe_preserve(
        [row["gsr"] for row in candidate["mand2mc_rows"] if row.get("gsr")]
        + [row["gsr"] for row in candidate["bs_gsr_rows"] if row.get("gsr")]
    )


def render_candidate_lines(candidate: dict[str, Any]) -> list[str]:
    render_latex = candidate.get("render_latex")
    if render_latex:
        return [line.rstrip() for line in render_latex.splitlines() if line.strip()]

    character = candidate["character"]
    pinyins = collect_candidate_pinyins(candidate)
    mc_forms = collect_candidate_mc_forms(candidate)
    gsr_values = collect_candidate_gsr_values(candidate)
    transliteration_latex = candidate.get("transliteration_latex")

    first_line = character
    if pinyins:
        first_line += f"\t%{' / '.join(pinyins)}"
    lines = [first_line]

    if transliteration_latex:
        lines.extend(line.rstrip() for line in transliteration_latex.splitlines() if line.strip())

    if mc_forms:
        for index, mc_form in enumerate(mc_forms):
            comment = ""
            if index == 0 and gsr_values:
                comment = "\t%" + ", ".join(gsr_values)
            lines.append(f"\\textit{{{mc_form}}};{comment}")
    elif gsr_values:
        lines.append("% no MC extracted\t%" + ", ".join(gsr_values))

    if candidate["mand_bs_mc_disagreement"]:
        lines.append("{\\footnotesize[MC disagreement among imported sources]}")

    return lines


def render_missing_series_entry(entry: dict[str, Any]) -> str:
    head_character = entry["proposed_additions"][0]["character"] if entry["proposed_additions"] else entry["id"]
    body_lines = [
        f"\\paragraph{{\\textoversetlarge{{{entry['id']}}}{{\\huge{{{head_character}}}}}}}",
        "{\\small\\itshape[provisional draft for a missing series; transliteration and semantic analysis still to review]}",
    ]
    for candidate in entry["proposed_additions"]:
        body_lines.extend(render_candidate_lines(candidate))
    return render_context_wrapped_block(
        [{"name": "multicols", "arg": "2"}, {"name": "spacing", "arg": "0.7"}],
        body_lines,
    )


def render_existing_addendum_entry(entry: dict[str, Any]) -> str:
    tex_entry = entry["tex_entry"]
    body_lines = [
        build_existing_heading_line(entry),
        "{\\small\\itshape[proposed additions from imported sources]}",
    ]
    for candidate in entry["proposed_additions"]:
        body_lines.extend(render_candidate_lines(candidate))
    return render_context_wrapped_block(tex_entry.get("context_environments", []), body_lines)


def render_curated_entry(entry: dict[str, Any]) -> str:
    if entry["packet_kind"] == "missing_series":
        return render_missing_series_entry(entry)

    wrapped_tex_entry = render_entries.wrap_entry_with_context(
        {
            "raw_latex": entry["tex_entry"]["raw_block"],
            "context_environments": entry["tex_entry"].get("context_environments", []),
        }
    ).rstrip()
    addition_block = render_existing_addendum_entry(entry).rstrip()
    return wrapped_tex_entry + "\n\n" + addition_block


def render_document(entries: list[dict[str, Any]], main_tex_path: Path) -> str:
    body = [
        "\\begin{document}",
        "% GENERATED FILE - DO NOT EDIT BY HAND.",
        "\\section*{Curated pilot series in comparable format}",
        "",
    ]
    missing_entries = [entry for entry in entries if entry["packet_kind"] == "missing_series"]
    existing_entries = [entry for entry in entries if entry["packet_kind"] != "missing_series"]

    if missing_entries:
        body.extend(
            [
                "\\subsection*{Pilot missing series drafts}",
                "",
            ]
        )
        for entry in missing_entries:
            body.append(render_curated_entry(entry))
            body.append("")

    if existing_entries:
        body.extend(
            [
                "\\subsection*{Pilot addenda to existing series}",
                "",
            ]
        )
        for entry in existing_entries:
            body.append(render_curated_entry(entry))
            body.append("")
    body.append("\\end{document}")
    return extract_preamble(main_tex_path) + "\n".join(body) + "\n"


def render_report(entries: list[dict[str, Any]], tex_path: Path) -> str:
    lines = [
        "# Generated curated series sample",
        "",
        f"- Generated TeX file: `{tex_path}`",
        "- This file is a review document, not final dictionary output.",
        "- Missing-series packets are rendered as provisional dictionary-style draft entries.",
        "- Existing-series packets show the original TeX baseline followed by a comparable-format additions block.",
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
