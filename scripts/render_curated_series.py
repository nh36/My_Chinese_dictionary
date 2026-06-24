from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import hierarchy_utils
import mc_resolution


DEFAULT_INPUT_DIR = "data/entries/curation"
DEFAULT_IDS = [
    "04-04",
    "02-01",
    "02-32",
    "02-25",
    "03-32",
    "38-03",
    "04-30",
    "03-49",
    "03-57",
    "03-65",
    "04-02",
    "04-12",
    "12-01",
    "05-16",
    "07-14",
    "08-14",
    "08-19",
    "12-10",
    "12-19",
    "04-26",
    "04-29",
    "12-08",
    "12-25",
    "11-12",
    "13-22",
    "13-47",
    "13-45",
    "38-16",
    "14-14",
    "14-18",
    "16-15",
    "16-20",
    "16-01",
    "16-13",
    "16-14",
    "26-38",
    "27-08",
    "32-16",
    "33-30",
    "24-21",
    "24-23",
    "24-58",
    "25-15",
    "25-17",
    "25-19",
    "26-06",
    "26-27",
    "26-14",
    "26-15",
    "26-29",
    "28-05",
    "28-11",
    "28-15",
    "29-41",
    "24-01",
    "09-01",
    "09-25",
    "09-17",
    "16-06",
    "16-10",
    "16-39",
    "16-33",
    "03-38",
    "13-32",
    "07-25",
    "07-29",
    "07-08",
    "07-12",
    "04-61",
    "10-39",
    "16-24",
    "24-41",
    "24-54",
    "31-20",
    "33-02",
    "33-05",
    "37-01",
    "02-40",
    "09-19",
    "10-35",
    "13-76",
    "16-03",
    "25-02",
    "29-01",
    "29-09",
    "30-14",
    "31-02",
    "32-05",
    "32-08",
    "36-12",
    "03-43",
    "09-29",
    "13-36",
    "33-15",
    "33-36",
    "34-17",
    "34-23",
    "32-40",
    "35-21",
    "16-21",
    "26-05",
    "31-16",
    "36-06",
    "36-14",
    "38-11",
    "02-31",
    "03-39",
    "09-11",
    "10-37",
    "13-72",
    "17-05",
    "17-07",
    "25-12",
    "28-01",
    "29-11",
    "30-01",
    "33-13",
    "34-13",
    "36-11",
    "38-05",
    "02-17",
    "03-26",
    "03-48",
    "05-33",
    "06-13",
    "07-03",
    "07-11",
    "08-12",
    "11-21",
    "16-31",
    "19-02",
    "19-09",
    "23-07",
    "23-27",
    "24-47",
    "25-24",
    "25-25",
    "25-31",
    "29-15",
    "29-17",
    "32-38",
    "32-26",
    "35-03",
    "36-07",
    "38-14",
    "02-38",
    "03-24",
    "03-42",
    "04-05",
    "04-17",
    "01-57",
    "19-04",
    "19-22",
    "03-23",
    "01-18",
    "01-42",
    "01-62",
    "19-01",
    "19-06",
    "19-21",
    "13-03",
    "13-30",
    "16-30",
    "18-09",
    "21-31",
    "35-10",
    "36-05",
    "34-18",
    "09-09",
    "22-13",
    "37-16",
    "01-38",
    "01-19",
    "19-18",
    "04-45",
    "05-06",
    "12-03",
    "25-11",
    "33-29",
    "18-18",
    "21-01",
    "01-01",
    "01-51",
    "01-43",
    "22-01",
    "22-03",
    "23-17",
    "38-25",
    "38-28",
    "03-10",
    "03-01",
    "03-35",
    "04-15",
    "04-21",
    "04-35",
    "06-05",
    "06-19",
    "06-20",
    "13-73",
    "13-57",
    "14-02",
    "14-22",
    "07-20",
    "16-02",
    "24-56",
    "27-04",
    "30-02",
    "36-18",
    "17-08",
    "22-05",
    "21-26",
    "37-15",
    "03-12",
    "36-26",
    "11-15",
    "37-08",
    "12-15",
    "24-49",
    "34-24",
    "34-26",
    "22-02",
    "02-08",
    "30-11",
    "37-02",
    "33-25",
    "33-20",
    "03-16",
    "05-12",
    "24-35",
    "27-02",
    "32-33",
    "23-10",
    "03-20",
    "04-40",
    "13-08",
    "38-18",
    "26-24",
    "26-39",
    "36-01",
    "02-23",
    "05-10",
    "21-25",
    "37-19",
    "04-41",
    "06-09",
    "23-03",
    "11-13",
    "24-11",
    "14-23",
    "09-04",
    "01-09",
    "07-21",
    "06-10",
    "29-42",
    "02-22",
    "20-02",
    "25-28",
    "29-33",
    "05-13",
    "36-22",
    "23-05",
    "32-09",
    "21-12",
    "20-18",
    "23-20",
    "24-12",
    "29-13",
    "38-07",
    "30-21",
    "02-02",
    "13-16",
    "26-09",
    "34-12",
    "16-41",
    "04-23",
    "34-15",
    "35-12",
    "13-27",
    "15-09",
    "25-38",
    "33-01",
    "26-28",
    "11-06",
    "04-13",
    "34-16",
    "31-17",
    "32-22",
    "34-21",
    "06-17",
    "09-03",
    "09-10",
    "11-23",
    "15-06",
    "32-10",
    "24-08",
    "27-06",
    "34-11",
    "34-30",
    "03-31",
    "04-49",
    "32-01",
    "12-09",
    "26-17",
    "11-14",
    "32-07",
    "04-38",
    "34-14",
    "13-48",
    "24-30",
    "25-20",
    "29-08",
    "31-09",
    "20-01",
    "20-03",
    "20-13",
    "20-16",
    "21-19",
    "21-23",
    "22-10",
    "24-02",
    "24-39",
    "25-01",
    "25-14",
    "34-01",
    "38-04",
    "02-27",
]
DEFAULT_MAIN_TEX = "main.tex"
DEFAULT_OUTPUT = "build/generated_curated_series_sample.tex"
DEFAULT_PDF_OUTPUT = "build/generated_curated_series_sample.pdf"
DEFAULT_REPORT = "reports/generated_curated_series_sample.md"
COLUMN_GUARDRAIL_MACROS = [
    r"\newsavebox{\pilotentrybox}",
    r"\newlength{\pilotentrygap}",
    r"\setlength{\pilotentrygap}{0.75\baselineskip}",
    r"\makeatletter",
    r"\long\def\pilotentry#1{%",
    r"  \sbox{\pilotentrybox}{\begin{minipage}{\columnwidth}#1\end{minipage}}%",
    r"  \ifdim\pagetotal>\topskip",
    r"    \vspace{\pilotentrygap}",
    r"  \fi",
    r"  \usebox{\pilotentrybox}\par",
    r"}",
    r"\makeatother",
]
COLUMN_CONTEXT_PREFIXES = (
    r"\begin{multicols}",
    r"\begin{multicols*}",
    r"\begin{spacing}",
    r"\end{spacing}",
    r"\end{multicols}",
    r"\end{multicols*}",
)


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


def entry_sort_key(entry: dict[str, Any]) -> tuple[int, int, str]:
    schuessler = entry.get("schuessler") or {}
    rhyme_section = schuessler.get("rhyme_section")
    series_number = schuessler.get("series_number")
    if rhyme_section is not None and series_number is not None:
        return (int(rhyme_section), int(series_number), entry["id"])
    left, _, right = entry["id"].partition("-")
    try:
        return (int(left), int(right), entry["id"])
    except ValueError:
        return (9999, 9999, entry["id"])


def sort_entries(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(entries, key=entry_sort_key)


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
    resolution = candidate.get("mc_resolution") or mc_resolution.resolve_candidate_mc(candidate)
    return resolution["display_forms"]


def collect_candidate_gsr_values(candidate: dict[str, Any]) -> list[str]:
    return dedupe_preserve(
        [row["gsr"] for row in candidate["mand2mc_rows"] if row.get("gsr")]
        + [row["gsr"] for row in candidate["bs_gsr_rows"] if row.get("gsr")]
    )


def render_candidate_lines(candidate: dict[str, Any]) -> list[str]:
    render_latex = candidate.get("render_latex")
    if render_latex:
        return [
            line.rstrip()
            for line in render_latex.splitlines()
            if line.strip() and "[MC disagreement among imported sources]" not in line
        ]

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

    return lines


def resolve_candidate_display_character(candidate: dict[str, Any]) -> str:
    character = candidate["character"]
    render_latex = candidate.get("render_latex")
    if render_latex:
        first_line = render_latex.splitlines()[0].strip()
        if first_line.startswith(character):
            if "\t%" in first_line:
                return first_line.split("\t%", 1)[0]
            return first_line
    return character


def render_candidate_body_lines(candidate: dict[str, Any]) -> list[str]:
    lines = render_candidate_lines(candidate)
    return lines[1:] if len(lines) > 1 else []


def build_candidate_heading_line(candidate: dict[str, Any]) -> str:
    line = rf"{{\Large{{{resolve_candidate_display_character(candidate)}}}}}"
    pinyins = collect_candidate_pinyins(candidate)
    if pinyins:
        line += f"\t%{' / '.join(pinyins)}"
    return line


def render_candidate_node(
    candidate: dict[str, Any],
    candidate_children: dict[str, list[dict[str, Any]]],
) -> list[str]:
    lines = [r"\item " + build_candidate_heading_line(candidate)]
    body_lines = render_candidate_body_lines(candidate)
    transliteration_lines: list[str] = []
    mc_lines: list[str] = []
    for line in body_lines:
        if line.startswith(r"\textit{") or line.startswith("% no MC"):
            mc_lines.append(line)
        else:
            transliteration_lines.append(line)
    lines.extend(transliteration_lines)
    root_data = candidate.get("resolved_node_root") or {}
    resolved_node_root = root_data.get("display_root") or root_data.get("root")
    if resolved_node_root:
        lines.append(rf"= {{\large{{{resolved_node_root}}}}},")
    lines.extend(mc_lines)
    children = candidate_children.get(candidate["character"], [])
    if children:
        lines.extend(render_candidate_group_lines(children, candidate_children))
    return lines


def render_candidate_group_lines(
    candidates: list[dict[str, Any]],
    candidate_children: dict[str, list[dict[str, Any]]],
) -> list[str]:
    lines: list[str] = []
    parent_candidates: list[dict[str, Any]] = []
    for candidate in candidates:
        if candidate_children.get(candidate["character"]):
            parent_candidates.append(candidate)
            continue
        lines.extend(render_candidate_lines(candidate))

    if parent_candidates:
        lines.append(r"\begin{itemize}[noitemsep]")
        for candidate in parent_candidates:
            lines.extend(render_candidate_node(candidate, candidate_children))
        lines.append(r"\end{itemize}")
    return lines


def render_head_mc_lines(candidate: dict[str, Any]) -> list[str]:
    mc_forms = collect_candidate_mc_forms(candidate)
    gsr_values = collect_candidate_gsr_values(candidate)
    lines: list[str] = []
    for index, mc_form in enumerate(mc_forms):
        comment = ""
        if index == 0 and gsr_values:
            comment = "\t%" + ", ".join(gsr_values)
        lines.append(f"\\textit{{{mc_form}}};{comment}")
    return lines


def strip_column_context_lines(raw_block: str) -> str:
    filtered_lines = [
        line.rstrip()
        for line in raw_block.splitlines()
        if line.strip() and not any(line.strip().startswith(prefix) for prefix in COLUMN_CONTEXT_PREFIXES)
    ]
    return "\n".join(filtered_lines)


def wrap_entry_guardrail(rendered_entry: str) -> str:
    body = rendered_entry.rstrip()
    return "\n".join(
        [
            r"\pilotentry{%",
            body,
            r"}",
        ]
    )


def resolve_missing_series_head(entry: dict[str, Any]) -> tuple[str, dict[str, Any] | None]:
    resolved = entry.get("resolved_series_root") or {}
    proposed_additions = entry.get("proposed_additions", [])
    head_character = resolved.get("character")
    if resolved.get("source") == "head_graph_supplement" and head_character:
        return head_character, None
    if proposed_additions:
        return proposed_additions[0]["character"], proposed_additions[0]
    candidate_map = {candidate["character"]: candidate for candidate in proposed_additions}
    if head_character:
        return head_character, candidate_map.get(head_character)
    return entry["id"], None


def render_missing_series_heading_character(
    head_character: str,
    head_candidate: dict[str, Any] | None,
) -> str:
    if head_candidate and head_candidate.get("render_latex"):
        first_line = head_candidate["render_latex"].splitlines()[0].strip()
        if first_line.startswith(head_character):
            if "\t%" in first_line:
                return first_line.split("\t%", 1)[0]
            return first_line
    return head_character


def render_missing_series_entry(entry: dict[str, Any]) -> str:
    head_character, head_candidate = resolve_missing_series_head(entry)
    heading_character = render_missing_series_heading_character(head_character, head_candidate)
    resolved_root_data = entry.get("resolved_series_root") or {}
    resolved_root = resolved_root_data.get("display_root") or resolved_root_data.get("root")
    body_lines = [
        f"\\paragraph{{\\textoversetlarge{{{entry['id']}}}{{\\huge{{{heading_character}}}}}}}",
    ]
    if resolved_root:
        body_lines.append(rf"{{\large{{{resolved_root}}}}},")
    if head_candidate is not None:
        body_lines.extend(render_head_mc_lines(head_candidate))

    candidate_children = hierarchy_utils.collect_candidate_children(entry)
    direct_candidates: list[dict[str, Any]] = []
    head_child_candidates: list[dict[str, Any]] = []
    head_candidate_character = head_candidate["character"] if head_candidate is not None else None
    for candidate in entry["proposed_additions"]:
        if head_candidate_character and candidate["character"] == head_candidate_character:
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

    body_lines.extend(render_candidate_group_lines(direct_candidates, candidate_children))
    if head_child_candidates:
        body_lines.append(r"\begin{itemize}[noitemsep]")
        for candidate in head_child_candidates:
            body_lines.extend(render_candidate_node(candidate, candidate_children))
        body_lines.append(r"\end{itemize}")
    return "\n".join(body_lines)


def render_existing_addendum_entry(entry: dict[str, Any]) -> str:
    tex_entry = entry["tex_entry"]
    body_lines = [
        f"% Proposed additions from imported sources for {entry['id']}",
    ]
    hierarchy = entry.get("entry_hierarchy") or {}
    hierarchy_nodes = hierarchy.get("nodes") or []
    candidate_children = hierarchy_utils.collect_candidate_children(entry)
    grouped_by_parent: dict[str, list[dict[str, Any]]] = {}
    top_level_candidates = [
        candidate
        for candidate in entry["proposed_additions"]
        if (candidate.get("hierarchy_assignment") or {}).get("status")
        not in {"assigned-to-inherited-node", "assigned-to-candidate-node"}
    ]

    for candidate in entry["proposed_additions"]:
        assignment = candidate.get("hierarchy_assignment") or {}
        if assignment.get("status") == "assigned-to-inherited-node" and assignment.get("parent_character"):
            grouped_by_parent.setdefault(assignment["parent_character"], []).append(candidate)

    body_lines.extend(render_candidate_group_lines(top_level_candidates, candidate_children))
    if grouped_by_parent:
        body_lines.append(r"\begin{itemize}[noitemsep]")
        for node in hierarchy_nodes:
            parent = node.get("key_character")
            grouped_candidates = grouped_by_parent.get(parent) or []
            if not grouped_candidates:
                continue
            if node.get("rhs_snippet"):
                body_lines.append(rf"\item {node['display_line']} = {node['rhs_snippet']}")
            else:
                body_lines.append(rf"\item {node['display_line']}")
            body_lines.extend(render_candidate_group_lines(grouped_candidates, candidate_children))
        body_lines.append(r"\end{itemize}")
    return "\n".join(body_lines)


def render_curated_entry(entry: dict[str, Any]) -> str:
    if entry["packet_kind"] == "missing_series":
        return render_missing_series_entry(entry)

    wrapped_tex_entry = strip_column_context_lines(entry["tex_entry"]["raw_block"]).rstrip()
    addition_block = render_existing_addendum_entry(entry).rstrip()
    return wrapped_tex_entry + "\n\n" + addition_block


def render_entry_blocks(entries: list[dict[str, Any]]) -> list[str]:
    lines: list[str] = []
    for entry in entries:
        lines.append(wrap_entry_guardrail(render_curated_entry(entry)))
        lines.append("")
    return lines


def render_document(entries: list[dict[str, Any]], main_tex_path: Path) -> str:
    entries = sort_entries(entries)
    body = [
        "\\begin{document}",
        "% GENERATED FILE - DO NOT EDIT BY HAND.",
        "\\section*{Curated pilot series in comparable format}",
        "",
    ]
    body.extend(COLUMN_GUARDRAIL_MACROS)
    body.append("")
    missing_entries = [entry for entry in entries if entry["packet_kind"] == "missing_series"]
    existing_entries = [entry for entry in entries if entry["packet_kind"] != "missing_series"]

    if missing_entries or existing_entries:
        if missing_entries:
            body.extend(
                [
                    "\\subsection*{Pilot missing series drafts}",
                    "",
                ]
            )
        elif existing_entries:
            body.extend(
                [
                    "\\subsection*{Pilot addenda to existing series}",
                    "",
                ]
            )

        body.extend(
            [
                r"\begin{multicols*}{2}",
                r"\raggedcolumns",
                r"\begin{spacing}{0.7}",
            ]
        )
        if missing_entries:
            body.extend(render_entry_blocks(missing_entries))
        if existing_entries:
            if missing_entries:
                body.extend(
                    [
                        r"\medskip",
                        r"{\large\bfseries Pilot addenda to existing series\par}",
                        r"\smallskip",
                    ]
                )
            body.extend(render_entry_blocks(existing_entries))
        body.extend(
            [
                r"\end{spacing}",
                r"\end{multicols*}",
            ]
        )
        body.append("")
    body.append("\\end{document}")
    return extract_preamble(main_tex_path) + "\n".join(body) + "\n"


def render_report(entries: list[dict[str, Any]], tex_path: Path) -> str:
    entries = sort_entries(entries)
    lines = [
        "# Generated curated series sample",
        "",
        f"- Generated TeX file: `{tex_path}`",
        "- This file is a review document, not final dictionary output.",
        "- Missing-series packets are rendered as provisional dictionary-style draft entries with a resolved packet root line when available.",
        "- Existing-series packets show the original TeX baseline followed by a comparable-format additions block.",
        "",
        "| GSC | Packet kind | Existing TeX baseline | Proposed additions | Hierarchy-linked additions |",
        "| --- | --- | --- | ---: | ---: |",
    ]
    for entry in entries:
        hierarchy_linked = sum(
            1
            for candidate in entry.get("proposed_additions", [])
            if (candidate.get("hierarchy_assignment") or {}).get("status")
            in {"assigned-to-inherited-node", "assigned-to-candidate-node"}
        )
        lines.append(
            f"| `{entry['id']}` | `{entry['packet_kind']}` | "
            f"{'yes' if entry.get('tex_entry') else 'no'} | {len(entry['proposed_additions'])} | {hierarchy_linked} |"
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
