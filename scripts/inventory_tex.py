from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SECTION_RE = re.compile(r"\\section\{([^}]*)\}")
SUBSECTION_RE = re.compile(r"\\subsection\{([^}]*)\}")
GSR_RE = re.compile(r"\b\d{4}[a-z](?:')?\b")
PINYIN_RE = re.compile(r"\b[a-zA-ZvVüÜ]+[1-5]\b")
CHINESE_CHAR_RE = re.compile(
    "["
    "\u3400-\u4DBF"
    "\u4E00-\u9FFF"
    "\uF900-\uFAFF"
    "\U00020000-\U0002A6DF"
    "\U0002A700-\U0002B73F"
    "\U0002B740-\U0002B81F"
    "\U0002B820-\U0002CEAF"
    "\U0002CEB0-\U0002EBEF"
    "]"
)


def parse_braced(text: str, start_index: int) -> tuple[str, int]:
    if start_index >= len(text) or text[start_index] != "{":
        raise ValueError(f"Expected '{{' at index {start_index}")

    depth = 0
    for index in range(start_index, len(text)):
        char = text[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start_index + 1 : index], index + 1

    raise ValueError("Unbalanced braces in LaTeX source")


def parse_bracketed(text: str, start_index: int) -> tuple[str, int]:
    if start_index >= len(text) or text[start_index] != "[":
        raise ValueError(f"Expected '[' at index {start_index}")

    depth = 0
    for index in range(start_index, len(text)):
        char = text[index]
        if char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
            if depth == 0:
                return text[start_index + 1 : index], index + 1

    raise ValueError("Unbalanced brackets in LaTeX source")


def split_latex_comment(line: str) -> tuple[str, str | None]:
    escaped = False
    for index, char in enumerate(line):
        if char == "\\" and not escaped:
            escaped = True
            continue
        if char == "%" and not escaped:
            return line[:index], line[index + 1 :]
        escaped = False
    return line, None


def find_macro_arguments(text: str, macro_name: str, has_optional_arg: bool = False) -> list[str]:
    needle = f"\\{macro_name}"
    arguments: list[str] = []
    search_from = 0

    while True:
        index = text.find(needle, search_from)
        if index == -1:
            return arguments

        cursor = index + len(needle)
        while cursor < len(text) and text[cursor].isspace():
            cursor += 1

        if has_optional_arg and cursor < len(text) and text[cursor] == "[":
            _, cursor = parse_bracketed(text, cursor)
            while cursor < len(text) and text[cursor].isspace():
                cursor += 1

        if cursor < len(text) and text[cursor] == "{":
            argument, cursor = parse_braced(text, cursor)
            arguments.append(argument)
        else:
            cursor += 1

        search_from = cursor


def extract_paragraph_metadata(line: str) -> dict[str, Any] | None:
    marker = "\\paragraph"
    start = line.find(marker)
    if start == -1:
        return None

    cursor = start + len(marker)
    while cursor < len(line) and line[cursor].isspace():
        cursor += 1

    if cursor >= len(line) or line[cursor] != "{":
        return None

    paragraph_arg, cursor = parse_braced(line, cursor)
    if not paragraph_arg.startswith("\\textoversetlarge"):
        return {
            "heading_raw": paragraph_arg,
            "heading_extra_raw": line[cursor:].strip(),
            "gsc_number": None,
            "head_raw": paragraph_arg,
        }

    inner_cursor = len("\\textoversetlarge")
    while inner_cursor < len(paragraph_arg) and paragraph_arg[inner_cursor].isspace():
        inner_cursor += 1

    if inner_cursor >= len(paragraph_arg) or paragraph_arg[inner_cursor] != "{":
        return None

    gsc_number, inner_cursor = parse_braced(paragraph_arg, inner_cursor)
    while inner_cursor < len(paragraph_arg) and paragraph_arg[inner_cursor].isspace():
        inner_cursor += 1

    if inner_cursor >= len(paragraph_arg) or paragraph_arg[inner_cursor] != "{":
        return None

    head_raw, inner_cursor = parse_braced(paragraph_arg, inner_cursor)
    return {
        "heading_raw": paragraph_arg,
        "heading_extra_raw": line[cursor:].strip(),
        "gsc_number": gsc_number,
        "head_raw": head_raw,
    }


def add_unique(target: list[str], values: list[str]) -> None:
    seen = set(target)
    for value in values:
        if value not in seen:
            target.append(value)
            seen.add(value)


def summarize_counter(counter: Counter[str], limit: int = 20) -> list[dict[str, Any]]:
    return [{"value": value, "count": count} for value, count in counter.most_common(limit)]


def collect_inventory(source_text: str, source_path: str = "main.tex") -> dict[str, Any]:
    lines = source_text.splitlines()
    sections: list[dict[str, Any]] = []
    subsections: list[dict[str, Any]] = []
    entries: list[dict[str, Any]] = []
    image_refs: list[dict[str, Any]] = []
    mc_forms_all: list[str] = []
    gsr_markers_all: list[str] = []
    commented_pinyin_all: list[str] = []

    current_section: str | None = None
    current_subsection: str | None = None
    current_entry: dict[str, Any] | None = None

    total_itemize_blocks = 0
    document_itemize_depth = 0
    document_max_itemize_depth = 0

    def finalize_entry(end_line: int) -> None:
        nonlocal current_entry
        if current_entry is None:
            return

        current_entry["end_line"] = end_line
        current_entry["line_count"] = end_line - current_entry["start_line"] + 1
        current_entry.pop("_current_itemize_depth", None)
        entries.append(current_entry)
        current_entry = None

    for line_number, line in enumerate(lines, start=1):
        code, comment = split_latex_comment(line)
        section_match = SECTION_RE.search(code)
        subsection_match = SUBSECTION_RE.search(code)
        paragraph_metadata = extract_paragraph_metadata(code)

        if (section_match or subsection_match) and current_entry is not None:
            finalize_entry(line_number - 1)

        if paragraph_metadata:
            finalize_entry(line_number - 1)
            current_entry = {
                "section": current_section,
                "subsection": current_subsection,
                "gsc_number": paragraph_metadata["gsc_number"],
                "head_raw": paragraph_metadata["head_raw"],
                "heading_raw": paragraph_metadata["heading_raw"],
                "heading_extra_raw": paragraph_metadata["heading_extra_raw"],
                "has_image_head": "includegraphics" in paragraph_metadata["head_raw"]
                or "includegraphics" in paragraph_metadata["heading_extra_raw"],
                "start_line": line_number,
                "end_line": line_number,
                "line_count": 1,
                "image_refs": [],
                "mc_forms": [],
                "gsr_markers": [],
                "commented_pinyin": [],
                "chinese_characters": [],
                "itemize_block_count": 0,
                "max_itemize_depth": 0,
                "_current_itemize_depth": 0,
            }

        if section_match:
            current_section = section_match.group(1)
            sections.append({"title": current_section, "line_number": line_number})

        if subsection_match:
            current_subsection = subsection_match.group(1)
            subsections.append(
                {
                    "title": current_subsection,
                    "section": current_section,
                    "line_number": line_number,
                }
            )

        line_images = find_macro_arguments(code, "includegraphics", has_optional_arg=True)
        line_mc_forms = find_macro_arguments(code, "textit")
        line_gsr_markers = GSR_RE.findall(comment or "")
        line_commented_pinyin = PINYIN_RE.findall(comment or "")
        line_chinese_characters = CHINESE_CHAR_RE.findall(line)

        for image_file in line_images:
            image_refs.append({"file": image_file, "line_number": line_number})

        mc_forms_all.extend(line_mc_forms)
        gsr_markers_all.extend(line_gsr_markers)
        commented_pinyin_all.extend(line_commented_pinyin)

        begin_itemize_count = code.count("\\begin{itemize}")
        end_itemize_count = code.count("\\end{itemize}")

        for _ in range(begin_itemize_count):
            total_itemize_blocks += 1
            document_itemize_depth += 1
            document_max_itemize_depth = max(document_max_itemize_depth, document_itemize_depth)

        for _ in range(end_itemize_count):
            document_itemize_depth = max(0, document_itemize_depth - 1)

        if current_entry is not None:
            add_unique(current_entry["image_refs"], line_images)
            add_unique(current_entry["mc_forms"], line_mc_forms)
            add_unique(current_entry["gsr_markers"], line_gsr_markers)
            add_unique(current_entry["commented_pinyin"], line_commented_pinyin)
            add_unique(current_entry["chinese_characters"], line_chinese_characters)

            for _ in range(begin_itemize_count):
                current_entry["itemize_block_count"] += 1
                current_entry["_current_itemize_depth"] += 1
                current_entry["max_itemize_depth"] = max(
                    current_entry["max_itemize_depth"],
                    current_entry["_current_itemize_depth"],
                )

            for _ in range(end_itemize_count):
                current_entry["_current_itemize_depth"] = max(
                    0, current_entry["_current_itemize_depth"] - 1
                )

    finalize_entry(len(lines))

    subsection_entry_counts = Counter(
        entry["subsection"] for entry in entries if entry.get("subsection")
    )
    image_counter = Counter(image["file"] for image in image_refs)

    summary = {
        "line_count": len(lines),
        "section_count": len(sections),
        "subsection_count": len(subsections),
        "entry_count": len(entries),
        "image_reference_count": len(image_refs),
        "unique_image_count": len(image_counter),
        "mc_form_count": len(mc_forms_all),
        "unique_mc_form_count": len(set(mc_forms_all)),
        "gsr_marker_count": len(gsr_markers_all),
        "unique_gsr_marker_count": len(set(gsr_markers_all)),
        "commented_pinyin_count": len(commented_pinyin_all),
        "unique_commented_pinyin_count": len(set(commented_pinyin_all)),
        "chinese_character_count": len(CHINESE_CHAR_RE.findall(source_text)),
        "unique_chinese_character_count": len(set(CHINESE_CHAR_RE.findall(source_text))),
        "itemize_block_count": total_itemize_blocks,
        "max_itemize_depth": document_max_itemize_depth,
        "entries_with_itemize": sum(1 for entry in entries if entry["itemize_block_count"] > 0),
        "entries_with_nested_itemize": sum(1 for entry in entries if entry["max_itemize_depth"] > 1),
        "entries_with_image_refs": sum(1 for entry in entries if entry["image_refs"]),
        "entries_with_image_heads": sum(1 for entry in entries if entry["has_image_head"]),
    }

    return {
        "source_path": source_path,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": summary,
        "sections": sections,
        "subsections": [
            {
                **subsection,
                "entry_count": subsection_entry_counts.get(subsection["title"], 0),
            }
            for subsection in subsections
        ],
        "entries": entries,
        "images": {
            "references": image_refs,
            "by_file": summarize_counter(image_counter, limit=len(image_counter)),
        },
        "top_mc_forms": summarize_counter(Counter(mc_forms_all)),
        "top_gsr_markers": summarize_counter(Counter(gsr_markers_all)),
        "top_commented_pinyin": summarize_counter(Counter(commented_pinyin_all)),
    }


def render_markdown_report(inventory: dict[str, Any]) -> str:
    summary = inventory["summary"]
    sections = inventory["sections"]
    subsections = inventory["subsections"]
    entries = inventory["entries"]
    image_files = inventory["images"]["by_file"]

    lines = [
        "# Current TeX inventory",
        "",
        f"- Source: `{inventory['source_path']}`",
        f"- Generated: `{inventory['generated_at']}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
    ]

    for key in [
        "line_count",
        "section_count",
        "subsection_count",
        "entry_count",
        "image_reference_count",
        "unique_image_count",
        "mc_form_count",
        "unique_mc_form_count",
        "gsr_marker_count",
        "unique_gsr_marker_count",
        "commented_pinyin_count",
        "unique_commented_pinyin_count",
        "chinese_character_count",
        "unique_chinese_character_count",
        "itemize_block_count",
        "max_itemize_depth",
        "entries_with_itemize",
        "entries_with_nested_itemize",
        "entries_with_image_refs",
        "entries_with_image_heads",
    ]:
        label = key.replace("_", " ")
        lines.append(f"| {label} | {summary[key]} |")

    lines.extend(
        [
            "",
            "## Major sections",
            "",
            "| Line | Section |",
            "| ---: | --- |",
        ]
    )
    lines.extend(f"| {section['line_number']} | {section['title']} |" for section in sections)

    lines.extend(
        [
            "",
            "## Dictionary subsections",
            "",
            "| Line | Section | Subsection | Entries |",
            "| ---: | --- | --- | ---: |",
        ]
    )
    lines.extend(
        f"| {subsection['line_number']} | {subsection['section']} | {subsection['title']} | {subsection['entry_count']} |"
        for subsection in subsections
    )

    lines.extend(
        [
            "",
            "## Entry headings",
            "",
            "| Start line | End line | Subsection | GSC | Head raw | Image head | Images | MC forms | GSR markers | Max itemize depth |",
            "| ---: | ---: | --- | --- | --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for entry in entries:
        head_raw = entry["head_raw"].replace("|", "\\|")
        gsc_number = entry["gsc_number"] or ""
        subsection = entry["subsection"] or ""
        image_head = "yes" if entry["has_image_head"] else ""
        lines.append(
            f"| {entry['start_line']} | {entry['end_line']} | {subsection} | {gsc_number} | `{head_raw}` | {image_head} | "
            f"{len(entry['image_refs'])} | {len(entry['mc_forms'])} | {len(entry['gsr_markers'])} | {entry['max_itemize_depth']} |"
        )

    lines.extend(
        [
            "",
            "## Image references",
            "",
            "| File | References |",
            "| --- | ---: |",
        ]
    )
    lines.extend(f"| `{image['value']}` | {image['count']} |" for image in image_files)

    return "\n".join(lines) + "\n"


def write_outputs(
    inventory: dict[str, Any],
    json_path: Path,
    report_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(
        json.dumps(inventory, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    report_path.write_text(render_markdown_report(inventory), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inventory the current TeX source.")
    parser.add_argument("--source", default="main.tex", help="Path to the TeX source file.")
    parser.add_argument(
        "--json-out",
        default="data/current_tex_inventory.json",
        help="Path to write the JSON inventory.",
    )
    parser.add_argument(
        "--report-out",
        default="reports/current_inventory.md",
        help="Path to write the Markdown inventory report.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    source_path = Path(args.source)
    source_text = source_path.read_text(encoding="utf-8")
    inventory = collect_inventory(source_text, source_path=str(source_path))
    write_outputs(inventory, Path(args.json_out), Path(args.report_out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
