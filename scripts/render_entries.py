from __future__ import annotations

import argparse
import json
from pathlib import Path

import extract_tex_entries


DEFAULT_SAMPLE_INPUT = "data/entries/sample_entries.json"
DEFAULT_MAIN_TEX = "main.tex"
DEFAULT_OUTPUT = "build/generated_entries_sample.tex"
DEFAULT_MAIN_OUTPUT = "build/generated_main_sample.tex"
DEFAULT_REPORT_OUTPUT = "reports/generated_sample_comparison.md"


WARNING_HEADER = [
    "% GENERATED FILE - DO NOT EDIT BY HAND.",
    "% Source data: data/entries/sample_entries.json",
]


def load_sample_entries(input_path: Path) -> list[dict]:
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    return payload["entries"]


def wrap_entry_with_context(entry: dict) -> str:
    context = entry.get("context_environments", [])
    lines: list[str] = []

    for environment in context:
        lines.append(f"\\begin{{{environment['name']}}}{{{environment['arg']}}}")

    lines.append(entry["raw_latex"].rstrip())

    remaining_context = list(context)
    for line in entry["raw_latex"].splitlines():
        code, _ = extract_tex_entries.inventory_tex.split_latex_comment(line)
        for match in extract_tex_entries.BEGIN_MULTICOLS_RE.finditer(code):
            remaining_context.append({"name": "multicols", "arg": match.group(1)})
        for match in extract_tex_entries.BEGIN_SPACING_RE.finditer(code):
            remaining_context.append({"name": "spacing", "arg": match.group(1)})
        for _ in extract_tex_entries.END_SPACING_RE.finditer(code):
            for index in range(len(remaining_context) - 1, -1, -1):
                if remaining_context[index]["name"] == "spacing":
                    del remaining_context[index]
                    break
        for _ in extract_tex_entries.END_MULTICOLS_RE.finditer(code):
            for index in range(len(remaining_context) - 1, -1, -1):
                if remaining_context[index]["name"] == "multicols":
                    del remaining_context[index]
                    break

    for environment in reversed(remaining_context):
        lines.append(f"\\end{{{environment['name']}}}")

    return "\n".join(lines)


def render_entries_tex(entries: list[dict]) -> str:
    blocks = WARNING_HEADER + [""]
    for entry in entries:
        blocks.append(f"% Entry {entry['id']}")
        blocks.append(wrap_entry_with_context(entry))
        blocks.append("")
    return "\n".join(blocks).rstrip() + "\n"


def extract_preamble(main_tex_path: Path) -> str:
    source_text = main_tex_path.read_text(encoding="utf-8")
    marker = "\\begin{document}"
    if marker not in source_text:
        raise ValueError(f"{main_tex_path} does not contain \\begin{{document}}.")
    return source_text.split(marker, 1)[0].rstrip() + "\n"


def render_main_sample(entries: list[dict], main_tex_path: Path) -> str:
    preamble = extract_preamble(main_tex_path)
    body_lines = [
        "\\begin{document}",
        "% GENERATED FILE - DO NOT EDIT BY HAND.",
        "\\section*{Generated sample entries}",
        "",
    ]
    for entry in entries:
        body_lines.append(f"% Entry {entry['id']}")
        body_lines.append(wrap_entry_with_context(entry))
        body_lines.append("")
    body_lines.append("\\end{document}")
    return preamble + "\n".join(body_lines).rstrip() + "\n"


def write_output(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def render_comparison_report(entries: list[dict], sample_input: Path, output_path: Path, main_output_path: Path) -> str:
    lines = [
        "# Generated sample comparison",
        "",
        f"- Sample source: `{sample_input}`",
        f"- Generated entry file: `{output_path}`",
        f"- Generated standalone file: `{main_output_path}`",
        "- Current generator behavior: the sample renderer re-emits each entry's stored `raw_latex` block and adds only the missing outer `multicols` / `spacing` wrappers required to make selected entries self-contained.",
        "- Deliberate differences: generated-file warning headers, standalone wrapper text, and explicit outer environment wrappers when the raw entry block starts inside an already-open environment.",
        "",
        "## Included entries",
        "",
        "| ID | Section | Subsection | Source lines | Head type |",
        "| --- | --- | --- | ---: | --- |",
    ]

    for entry in entries:
        source = entry.get("source", {})
        lines.append(
            f"| `{entry['id']}` | {entry.get('section', '')} | {entry.get('subsection', '')} | "
            f"{source.get('tex_start_line', '')}-{source.get('tex_end_line', '')} | {entry.get('head', {}).get('type', '')} |"
        )

    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render selected sample entries back to LaTeX.")
    parser.add_argument("--sample-input", default=DEFAULT_SAMPLE_INPUT, help="Path to sample entry JSON.")
    parser.add_argument("--main-tex", default=DEFAULT_MAIN_TEX, help="Path to the main TeX source.")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Path to the generated entry-only TeX file.")
    parser.add_argument(
        "--main-output",
        default=DEFAULT_MAIN_OUTPUT,
        help="Path to the generated standalone TeX file.",
    )
    parser.add_argument(
        "--report-out",
        default=DEFAULT_REPORT_OUTPUT,
        help="Path to the generated comparison Markdown report.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    entries = load_sample_entries(Path(args.sample_input))
    output_path = Path(args.output)
    main_output_path = Path(args.main_output)
    report_output_path = Path(args.report_out)
    write_output(output_path, render_entries_tex(entries))
    write_output(main_output_path, render_main_sample(entries, Path(args.main_tex)))
    write_output(
        report_output_path,
        render_comparison_report(entries, Path(args.sample_input), output_path, main_output_path),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
