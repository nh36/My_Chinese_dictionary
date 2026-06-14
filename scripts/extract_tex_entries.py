from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import inventory_tex


BEGIN_MULTICOLS_RE = inventory_tex.re.compile(r"\\begin\{multicols\}\{([^}]*)\}")
BEGIN_SPACING_RE = inventory_tex.re.compile(r"\\begin\{spacing\}\{([^}]*)\}")
END_MULTICOLS_RE = inventory_tex.re.compile(r"\\end\{multicols\}")
END_SPACING_RE = inventory_tex.re.compile(r"\\end\{spacing\}")


def collect_entry_contexts(lines: list[str]) -> dict[int, list[dict[str, str]]]:
    contexts: dict[int, list[dict[str, str]]] = {}
    environment_stack: list[dict[str, str]] = []

    for line_number, line in enumerate(lines, start=1):
        code, _ = inventory_tex.split_latex_comment(line)
        if inventory_tex.extract_paragraph_metadata(code):
            contexts[line_number] = [dict(item) for item in environment_stack]

        for match in BEGIN_MULTICOLS_RE.finditer(code):
            environment_stack.append({"name": "multicols", "arg": match.group(1)})
        for match in BEGIN_SPACING_RE.finditer(code):
            environment_stack.append({"name": "spacing", "arg": match.group(1)})

        for _ in END_SPACING_RE.finditer(code):
            for index in range(len(environment_stack) - 1, -1, -1):
                if environment_stack[index]["name"] == "spacing":
                    del environment_stack[index]
                    break
        for _ in END_MULTICOLS_RE.finditer(code):
            for index in range(len(environment_stack) - 1, -1, -1):
                if environment_stack[index]["name"] == "multicols":
                    del environment_stack[index]
                    break

    return contexts


def build_itemize_events(entry_lines: list[str], start_line: int) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    depth = 0

    for offset, line in enumerate(entry_lines):
        code, _ = inventory_tex.split_latex_comment(line)
        line_number = start_line + offset

        begin_count = code.count("\\begin{itemize}")
        end_count = code.count("\\end{itemize}")

        for _ in range(begin_count):
            depth += 1
            events.append({"line_number": line_number, "kind": "begin", "depth": depth})

        for _ in range(end_count):
            events.append({"line_number": line_number, "kind": "end", "depth": depth})
            depth = max(0, depth - 1)

    return events


def extract_head_data(entry: dict[str, Any]) -> dict[str, Any]:
    head_raw = entry["head_raw"]
    heading_extra_raw = entry["heading_extra_raw"]
    head_images = inventory_tex.find_macro_arguments(head_raw, "includegraphics", has_optional_arg=True)
    extra_images = inventory_tex.find_macro_arguments(
        heading_extra_raw, "includegraphics", has_optional_arg=True
    )
    head_characters = inventory_tex.CHINESE_CHAR_RE.findall(head_raw + heading_extra_raw)

    if head_images:
        head_type = "image"
    elif extra_images:
        head_type = "character_with_image"
    else:
        head_type = "character"

    return {
        "type": head_type,
        "raw": head_raw,
        "heading_extra_raw": heading_extra_raw,
        "characters": list(dict.fromkeys(head_characters)),
        "image_refs": list(dict.fromkeys(head_images + extra_images)),
    }


def build_body_raw(entry_lines: list[str]) -> str:
    if not entry_lines:
        return ""

    first_line = entry_lines[0]
    code, _ = inventory_tex.split_latex_comment(first_line)
    paragraph_metadata = inventory_tex.extract_paragraph_metadata(code)
    if paragraph_metadata is None:
        return "\n".join(entry_lines)

    first_body_parts: list[str] = []
    if paragraph_metadata["heading_extra_raw"]:
        first_body_parts.append(paragraph_metadata["heading_extra_raw"])

    remaining_lines = entry_lines[1:]
    if remaining_lines:
        first_body_parts.extend(remaining_lines)

    return "\n".join(first_body_parts)


def extract_entries(source_text: str, source_path: str = "main.tex") -> dict[str, Any]:
    inventory = inventory_tex.collect_inventory(source_text, source_path=source_path)
    lines = source_text.splitlines()
    entry_contexts = collect_entry_contexts(lines)
    extracted_entries: list[dict[str, Any]] = []

    for entry in inventory["entries"]:
        start_index = entry["start_line"] - 1
        end_index = entry["end_line"]
        entry_lines = lines[start_index:end_index]
        raw_block = "\n".join(entry_lines)
        body_raw = build_body_raw(entry_lines)

        extracted_entries.append(
            {
                "id": entry["gsc_number"],
                "section": entry["section"],
                "subsection": entry["subsection"],
                "start_line": entry["start_line"],
                "end_line": entry["end_line"],
                "line_count": entry["line_count"],
                "head": extract_head_data(entry),
                "context_environments": entry_contexts.get(entry["start_line"], []),
                "raw_block": raw_block,
                "raw_body": body_raw,
                "paragraph_line_raw": entry_lines[0] if entry_lines else "",
                "chinese_characters": entry["chinese_characters"],
                "commented_pinyin": entry["commented_pinyin"],
                "mc_forms": entry["mc_forms"],
                "gsr_markers": entry["gsr_markers"],
                "image_refs": entry["image_refs"],
                "itemize": {
                    "block_count": entry["itemize_block_count"],
                    "max_depth": entry["max_itemize_depth"],
                    "events": build_itemize_events(entry_lines, entry["start_line"]),
                },
            }
        )

    return {
        "source_path": source_path,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "entry_count": len(extracted_entries),
        "entries": extracted_entries,
    }


def write_entries(entries_data: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(entries_data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract entry-level data from the TeX source.")
    parser.add_argument("--source", default="main.tex", help="Path to the TeX source file.")
    parser.add_argument(
        "--output",
        default="data/current_tex_entries.json",
        help="Path to write the extracted entries JSON.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    source_path = Path(args.source)
    source_text = source_path.read_text(encoding="utf-8")
    entries_data = extract_entries(source_text, source_path=str(source_path))
    write_entries(entries_data, Path(args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
