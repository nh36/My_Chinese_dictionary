from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import ab_division
import extract_tex_entries
import inventory_tex


DEFAULT_SOURCE_PATH = "main.tex"
DEFAULT_ENTRIES_PATH = "data/current_tex_entries.json"
DEFAULT_IDS = ["18-01", "01-67"]
DEFAULT_JSON_OUT = "data/derived/pilot_ab_subseries.json"
DEFAULT_REPORT_OUT = "reports/pilot_ab_subseries.md"
DEFAULT_TEX_OUT = "build/pilot_ab_subseries_review.tex"

TEXTOVERSET_RE = re.compile(r"\\textoverset\{([ab])\}")
LARGE_RE = re.compile(r"\{\\Large\{([^}]*)\}\}")
CHAR_RE = re.compile(r"[\u3400-\u9fff\U00020000-\U0002ceaf]")
def dedupe_preserve(values: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def load_entries(entries_path: Path, source_path: Path) -> dict[str, dict[str, Any]]:
    if entries_path.exists():
        entries_data = json.loads(entries_path.read_text(encoding="utf-8"))
    else:
        source_text = source_path.read_text(encoding="utf-8")
        entries_data = extract_tex_entries.extract_entries(source_text, source_path=str(source_path))
    return {entry["id"]: entry for entry in entries_data["entries"]}


def parse_item_blocks(entry: dict[str, Any]) -> list[dict[str, Any]]:
    lines = entry["raw_block"].splitlines()
    blocks: list[dict[str, Any]] = []
    open_blocks: dict[int, dict[str, Any]] = {}
    depth = 0

    def close_block(target_depth: int, end_index: int) -> None:
        block = open_blocks.pop(target_depth, None)
        if block is None:
            return
        block["end_line"] = entry["start_line"] + end_index

    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith(r"\end{itemize}"):
            close_block(depth, max(index - 1, 0))
            depth = max(depth - 1, 0)
            continue
        if stripped.startswith(r"\begin{itemize}"):
            depth += 1
            continue
        if stripped.startswith(r"\item"):
            close_block(depth, max(index - 1, 0))
            block = {
                "depth": depth,
                "start_line": entry["start_line"] + index,
                "end_line": entry["start_line"] + index,
                "lines": [line],
            }
            blocks.append(block)
            open_blocks[depth] = block
            continue

        active_depths = [candidate_depth for candidate_depth in open_blocks if candidate_depth <= depth]
        if not active_depths:
            continue
        open_blocks[max(active_depths)]["lines"].append(line)

    last_index = len(lines) - 1
    for target_depth in sorted(open_blocks, reverse=True):
        close_block(target_depth, last_index)
    return blocks


def extract_head_character(block_text: str) -> str | None:
    match = LARGE_RE.search(block_text)
    if match:
        characters = CHAR_RE.findall(match.group(1))
        if characters:
            return characters[0]
    leading_text = block_text.split(r"\textit", 1)[0]
    characters = CHAR_RE.findall(leading_text)
    return characters[0] if characters else None


def normalize_rhs_latex(block_text: str) -> str | None:
    match = re.search(r"=\s*(\{\\large\{)", block_text)
    if not match:
        return None
    start = match.start(1)
    rhs_text, _ = inventory_tex.parse_braced(block_text, start)
    cursor = len(r"\large")
    while cursor < len(rhs_text) and rhs_text[cursor].isspace():
        cursor += 1
    if cursor < len(rhs_text) and rhs_text[cursor] == "{":
        inner_text, _ = inventory_tex.parse_braced(rhs_text, cursor)
        return inner_text
    return rhs_text


def extract_head_mc_forms(block_lines: list[str], head_character: str | None) -> list[str]:
    forms: list[str] = []
    seen_head = False
    for line in block_lines:
        code, _ = inventory_tex.split_latex_comment(line)
        if not seen_head:
            if head_character and head_character in code:
                seen_head = True
            elif LARGE_RE.search(code):
                seen_head = True
            else:
                continue
        elif CHAR_RE.search(code):
            characters = set(CHAR_RE.findall(code))
            if not head_character or head_character not in characters:
                break
        forms.extend(inventory_tex.find_macro_arguments(code, "textit"))
    return dedupe_preserve(forms)


def normalize_mc_form(form: str) -> str:
    return ab_division.normalize_mc_form(form)


def split_onset_and_rhyme(form: str) -> tuple[str, str]:
    return ab_division.split_onset_and_rhyme(form)


def classify_mc_form(form: str) -> dict[str, str]:
    return ab_division.classify_mc_form(form)


def summarize_group_class(form_analyses: list[dict[str, str]]) -> tuple[str, str]:
    return ab_division.summarize_group_class(form_analyses)


def analyze_entry(entry: dict[str, Any]) -> dict[str, Any]:
    subgroup_analyses: list[dict[str, Any]] = []
    for block in parse_item_blocks(entry):
        block_text = "\n".join(block["lines"])
        rhs_latex = normalize_rhs_latex(block_text)
        if not rhs_latex:
            continue
        label_match = TEXTOVERSET_RE.search(rhs_latex)
        if not label_match:
            continue

        head_character = extract_head_character(block_text)
        mc_forms = extract_head_mc_forms(block["lines"], head_character)
        form_analyses = [classify_mc_form(form) for form in mc_forms]
        predicted_class, prediction_note = summarize_group_class(form_analyses)
        subgroup_analyses.append(
            {
                "head_character": head_character,
                "depth": block["depth"],
                "start_line": block["start_line"],
                "end_line": block["end_line"],
                "handwritten_class": label_match.group(1),
                "predicted_class": predicted_class,
                "matches_handwritten": predicted_class == label_match.group(1),
                "prediction_note": prediction_note,
                "mc_forms": mc_forms,
                "all_block_mc_forms": dedupe_preserve(inventory_tex.find_macro_arguments(block_text, "textit")),
                "form_analyses": form_analyses,
                "rhs_latex": rhs_latex,
            }
        )

    head_characters = CHAR_RE.findall(entry["head"]["raw"])
    return {
        "id": entry["id"],
        "head_character": head_characters[0] if head_characters else entry["head"]["raw"],
        "subsection": entry["subsection"],
        "start_line": entry["start_line"],
        "end_line": entry["end_line"],
        "subgroups": subgroup_analyses,
    }


def build_analysis(entries_by_id: dict[str, dict[str, Any]], entry_ids: list[str]) -> dict[str, Any]:
    analyses = [analyze_entry(entries_by_id[entry_id]) for entry_id in entry_ids]
    subgroup_count = sum(len(entry["subgroups"]) for entry in analyses)
    matched_count = sum(
        1
        for entry in analyses
        for subgroup in entry["subgroups"]
        if subgroup["matches_handwritten"]
    )
    return {
        "pilot_entry_ids": entry_ids,
        "summary": {
            "entry_count": len(analyses),
            "subgroup_count": subgroup_count,
            "matched_count": matched_count,
        },
        "entries": analyses,
    }


def escape_markdown(value: str) -> str:
    return value.replace("`", "\\`").replace("|", "\\|").replace("\n", " ")


def render_markdown(analysis: dict[str, Any]) -> str:
    lines = [
        "# Pilot a/b subseries detection",
        "",
        "- Pilot goal: infer handwritten subseries `a/b` marking from the MC forms attached to each subgroup.",
        "- Current conservative rule: use the subgroup head's own MC forms as the primary signal; treat a subgroup as **b** when those forms show an `i`-medial after the onset (for example `gie`, `phiu`, `ṅiəH`), and as **a** when they do not (for example `ka`, `puH`).",
        "- Bare `i` with zero onset is left unresolved in this pilot; it does not occur in the selected examples.",
        "",
        f"- Pilot entries reviewed: {', '.join(f'`{entry_id}`' for entry_id in analysis['pilot_entry_ids'])}",
        f"- Handwritten a/b subgroups found in those entries: {analysis['summary']['subgroup_count']}",
        f"- Prediction matches the handwritten label in the pilot sample: {analysis['summary']['matched_count']}/{analysis['summary']['subgroup_count']}",
        "",
    ]

    for entry in analysis["entries"]:
        lines.extend(
            [
                f"## `{entry['id']}` ({entry['head_character']})",
                "",
                f"- Source lines: {entry['start_line']}-{entry['end_line']}",
                "",
                "| Head | Handwritten | Predicted | MC forms | RHS LaTeX | Note |",
                "| --- | --- | --- | --- | --- | --- |",
            ]
        )
        for subgroup in entry["subgroups"]:
            lines.append(
                f"| {subgroup['head_character'] or '?'} | `{subgroup['handwritten_class']}` | "
                f"`{subgroup['predicted_class']}` | "
                f"`{escape_markdown(', '.join(subgroup['mc_forms']))}` | "
                f"`{escape_markdown(subgroup['rhs_latex'])}` | {subgroup['prediction_note']} |"
            )
        lines.append("")

    return "\n".join(lines) + "\n"


def escape_latex(value: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    return value


def render_tex(analysis: dict[str, Any]) -> str:
    lines = [
        r"\documentclass[11pt]{article}",
        r"\usepackage[a4paper,margin=1in]{geometry}",
        r"\usepackage{array}",
        r"\usepackage{booktabs}",
        r"\usepackage{enumitem}",
        r"\usepackage{fontspec}",
        r"\usepackage{tabularx}",
        r"\setmainfont{Charis SIL}",
        r"\newfontfamily\hanfont{BabelStone Han}",
        r"\newcommand{\han}[1]{{\hanfont #1}}",
        r"\setlength{\parindent}{0pt}",
        r"\setlength{\parskip}{0.6em}",
        r"\begin{document}",
        r"\section*{Pilot a/b subseries detection}",
        r"This pilot infers handwritten subgroup `a/b' labels from the Middle Chinese forms attached to each subgroup in the hand-written \texttt{main.tex}. It uses the subgroup head's own MC forms as the primary signal.",
        r"\begin{enumerate}[nosep]",
        r"\item Treat a subgroup as type `b' when its extracted MC forms show an `i'-medial after the onset, for example \texttt{gie}, \texttt{phiu}, or \texttt{ṅiəH}.",
        r"\item Treat a subgroup as type `a' when the extracted forms lack that `i'-medial, for example \texttt{ka} or \texttt{puH}.",
        r"\item Leave bare zero-onset \texttt{i-} forms unresolved; this ambiguity does not arise in the selected pilot entries.",
        r"\end{enumerate}",
        (
            "Pilot entries reviewed: "
            + ", ".join(rf"\texttt{{{escape_latex(entry_id)}}}" for entry_id in analysis["pilot_entry_ids"])
            + "."
        ),
        (
            f"Matched handwritten label in {analysis['summary']['matched_count']}"
            f"/{analysis['summary']['subgroup_count']} inspected subgroups."
        ),
        "",
    ]

    for entry in analysis["entries"]:
        lines.extend(
            [
                rf"\subsection*{{{escape_latex(entry['id'])} (\han{{{entry['head_character']}}})}}",
                rf"Source lines {entry['start_line']}--{entry['end_line']}.",
                r"{\small",
                r"\begin{tabularx}{\textwidth}{@{}>{\raggedright\arraybackslash}p{1.4cm}cc>{\raggedright\arraybackslash}X>{\raggedright\arraybackslash}X@{}}",
                r"\toprule",
                r"Head & Hand & Pred & MC forms & Handwritten RHS LaTeX \\",
                r"\midrule",
            ]
        )
        for subgroup in entry["subgroups"]:
            lines.append(
                rf"\han{{{subgroup['head_character'] or '?'}}} & "
                rf"\texttt{{{escape_latex(subgroup['handwritten_class'])}}} & "
                rf"\texttt{{{escape_latex(subgroup['predicted_class'])}}} & "
                rf"{escape_latex(', '.join(subgroup['mc_forms']))} & "
                rf"{escape_latex(subgroup['rhs_latex'])} \\"
            )
        lines.extend(
            [
                r"\bottomrule",
                r"\end{tabularx}",
                r"}",
                r"\begin{itemize}[nosep]",
            ]
        )
        for subgroup in entry["subgroups"]:
            lines.append(
                rf"\item \han{{{subgroup['head_character'] or '?'}}}: "
                rf"{escape_latex(subgroup['prediction_note'])}."
            )
        lines.extend(
            [
                r"\end{itemize}",
                "",
            ]
        )

    lines.append(r"\end{document}")
    return "\n".join(lines) + "\n"


def write_output(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Pilot inference of handwritten a/b subseries labels from Middle Chinese forms.")
    parser.add_argument("--source-path", default=DEFAULT_SOURCE_PATH)
    parser.add_argument("--entries-path", default=DEFAULT_ENTRIES_PATH)
    parser.add_argument("--ids", nargs="+", default=DEFAULT_IDS)
    parser.add_argument("--json-out", default=DEFAULT_JSON_OUT)
    parser.add_argument("--report-out", default=DEFAULT_REPORT_OUT)
    parser.add_argument("--tex-out", default=DEFAULT_TEX_OUT)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    entries_by_id = load_entries(Path(args.entries_path), Path(args.source_path))
    analysis = build_analysis(entries_by_id, args.ids)
    write_output(Path(args.json_out), json.dumps(analysis, ensure_ascii=False, indent=2) + "\n")
    write_output(Path(args.report_out), render_markdown(analysis))
    write_output(Path(args.tex_out), render_tex(analysis))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
