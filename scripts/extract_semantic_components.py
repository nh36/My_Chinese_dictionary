from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import inventory_tex


SECTION_START = r"\section{Semantic components}"
SECTION_HEADER_RE = re.compile(r"\\section\{([^}]*)\}")
ITEM_START_RE = re.compile(r"^\s*\\item(?:\s|$)")


def finalize_item(current: dict[str, Any] | None, items: list[dict[str, Any]]) -> None:
    if current is None:
        return
    current["end_line"] = current["start_line"] + len(current["raw_lines"]) - 1
    current["raw_latex"] = "\n".join(current["raw_lines"])
    items.append(current)


def collect_semantic_component_items(source_text: str) -> list[dict[str, Any]]:
    lines = source_text.splitlines()
    in_section = False
    current: dict[str, Any] | None = None
    items: list[dict[str, Any]] = []

    for line_number, line in enumerate(lines, start=1):
        code, comment = inventory_tex.split_latex_comment(line)

        if not in_section:
            if SECTION_START in code:
                in_section = True
            continue

        if SECTION_HEADER_RE.search(code):
            finalize_item(current, items)
            current = None
            break

        if ITEM_START_RE.search(code):
            finalize_item(current, items)
            current = {
                "start_line": line_number,
                "raw_lines": [line],
                "comments": [comment.strip()] if comment else [],
            }
            continue

        if current is not None:
            current["raw_lines"].append(line)
            if comment:
                current["comments"].append(comment.strip())

    finalize_item(current, items)
    return items


def parse_item(item: dict[str, Any]) -> dict[str, Any]:
    code_parts: list[str] = []
    for line in item["raw_lines"]:
        code, _ = inventory_tex.split_latex_comment(line)
        stripped = code.strip()
        if not stripped:
            continue
        code_parts.append(stripped)

    joined = " ".join(code_parts).strip()
    if joined.startswith(r"\item"):
        joined = joined[len(r"\item") :].strip()

    tokens = joined.split()
    label_index = None
    for index, token in enumerate(tokens):
        if token.startswith("\\"):
            continue
        if re.search(r"[A-Za-z]", token):
            label_index = index
            break

    graph_raw = " ".join(tokens[:label_index]).strip() if label_index is not None else joined
    label_token = tokens[label_index] if label_index is not None else None
    label_notes = " ".join(tokens[label_index + 1 :]).strip() if label_index is not None else ""
    abbreviation = None
    if label_token is not None:
        match = re.match(r"([A-Za-z]+)", label_token)
        if match:
            abbreviation = match.group(1)
    if abbreviation is None and label_notes:
        match = re.match(r"([A-Za-z]+)", label_notes)
        if match:
            abbreviation = match.group(1)

    return {
        "start_line": item["start_line"],
        "end_line": item["end_line"],
        "graph_raw": graph_raw or None,
        "label_token": label_token,
        "abbreviation": abbreviation,
        "label_notes": label_notes or None,
        "comments": item["comments"],
        "raw_latex": item["raw_latex"],
    }


def build_inventory(source_text: str, source_path: str) -> dict[str, Any]:
    parsed_items = [parse_item(item) for item in collect_semantic_component_items(source_text)]
    abbreviations = sorted({item["abbreviation"] for item in parsed_items if item["abbreviation"]})
    unresolved = [item for item in parsed_items if not item["abbreviation"]]

    return {
        "source_path": source_path,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "item_count": len(parsed_items),
            "unique_abbreviation_count": len(abbreviations),
            "unresolved_item_count": len(unresolved),
        },
        "items": parsed_items,
    }


def render_report(inventory: dict[str, Any]) -> str:
    lines = [
        "# Semantic components inventory",
        "",
        f"- Source: `{inventory['source_path']}`",
        f"- Items: {inventory['summary']['item_count']}",
        f"- Unique abbreviations: {inventory['summary']['unique_abbreviation_count']}",
        f"- Unresolved items: {inventory['summary']['unresolved_item_count']}",
        "",
        "| Lines | Graph | Abbreviation | Label token | Notes | Comments |",
        "| --- | --- | --- | --- | --- | --- |",
    ]

    for item in inventory["items"]:
        lines.append(
            f"| {item['start_line']}-{item['end_line']} | "
            f"`{(item['graph_raw'] or '').replace('`', '\\`').replace('|', '\\|')}` | "
            f"`{item['abbreviation'] or ''}` | "
            f"`{(item['label_token'] or '').replace('`', '\\`').replace('|', '\\|')}` | "
            f"{(item['label_notes'] or '').replace('|', '\\|')} | "
            f"{' / '.join(item['comments']).replace('|', '\\|')} |"
        )

    return "\n".join(lines) + "\n"


def write_outputs(inventory: dict[str, Any], json_path: Path, report_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_path.write_text(render_report(inventory), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract the semantic component inventory from main.tex.")
    parser.add_argument("--source", default="main.tex")
    parser.add_argument("--json-out", default="data/current_semantic_components.json")
    parser.add_argument("--report-out", default="reports/semantic_components_inventory.md")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    source_path = Path(args.source)
    source_text = source_path.read_text(encoding="utf-8")
    inventory = build_inventory(source_text, str(source_path))
    write_outputs(inventory, Path(args.json_out), Path(args.report_out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
