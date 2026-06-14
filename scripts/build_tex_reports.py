from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import extract_tex_entries
import inventory_tex


def escape_markdown_code(value: str) -> str:
    return value.replace("`", "\\`").replace("|", "\\|").replace("\n", " ")


def entry_sort_key(entry: dict[str, Any]) -> tuple[int, int, int]:
    entry_id = entry.get("id") or ""
    if "-" in entry_id:
        left, right = entry_id.split("-", 1)
        if left.isdigit() and right.isdigit():
            return (int(left), int(right), entry.get("start_line", 0))
    return (9999, 9999, entry.get("start_line", 0))


def gsr_sort_key(marker: str) -> tuple[int, str, int, str]:
    digits = marker[:4]
    suffix = marker[4:]
    base = suffix.rstrip("'")
    prime_count = len(suffix) - len(base)
    return (int(digits), base, prime_count, suffix)


def load_entries_data(entries_path: Path, source_path: Path) -> dict[str, Any]:
    if entries_path.exists():
        return json.loads(entries_path.read_text(encoding="utf-8"))

    source_text = source_path.read_text(encoding="utf-8")
    return extract_tex_entries.extract_entries(source_text, source_path=str(source_path))


def render_tex_entries_by_gsr(entries_data: dict[str, Any]) -> str:
    gsr_to_entries: dict[str, list[dict[str, Any]]] = defaultdict(list)
    entries_with_gsr = 0

    for entry in entries_data["entries"]:
        if entry["gsr_markers"]:
            entries_with_gsr += 1
        for marker in entry["gsr_markers"]:
            gsr_to_entries[marker].append(entry)

    lines = [
        "# TeX entries by GSR",
        "",
        f"- Entries with at least one GSR marker: {entries_with_gsr}",
        f"- Unique GSR markers: {len(gsr_to_entries)}",
        "",
        "| GSR | Entries |",
        "| --- | --- |",
    ]

    for marker in sorted(gsr_to_entries, key=gsr_sort_key):
        rendered_entries = []
        for entry in sorted(gsr_to_entries[marker], key=entry_sort_key):
            head_raw = escape_markdown_code(entry["head"]["raw"])
            rendered_entries.append(
                f"`{entry['id']}` (`{head_raw}`; lines {entry['start_line']}-{entry['end_line']})"
            )
        lines.append(f"| `{marker}` | {'<br>'.join(rendered_entries)} |")

    return "\n".join(lines) + "\n"


def render_tex_entries_without_gsr(entries_data: dict[str, Any]) -> str:
    missing = [entry for entry in entries_data["entries"] if not entry["gsr_markers"]]
    missing.sort(key=entry_sort_key)

    lines = [
        "# TeX entries without GSR",
        "",
        f"- Entries without any extracted GSR marker: {len(missing)}",
        "",
        "| GSC | Subsection | Lines | Head raw | MC forms | Commented pinyin |",
        "| --- | --- | ---: | --- | ---: | ---: |",
    ]

    for entry in missing:
        head_raw = escape_markdown_code(entry["head"]["raw"])
        lines.append(
            f"| `{entry['id']}` | `{entry['subsection']}` | {entry['start_line']}-{entry['end_line']} | "
            f"`{head_raw}` | {len(entry['mc_forms'])} | {len(entry['commented_pinyin'])} |"
        )

    return "\n".join(lines) + "\n"


def render_rare_glyphs_report(entries_data: dict[str, Any], asset_dir: Path) -> str:
    asset_files = sorted(path.name for path in asset_dir.glob("*.png"))
    asset_file_set = set(asset_files)
    image_counter: Counter[str] = Counter()
    head_counter: Counter[str] = Counter()
    entries_by_image: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for entry in entries_data["entries"]:
        head_images = set(entry["head"]["image_refs"])
        for image in entry["image_refs"]:
            image_counter[image] += 1
            if image in head_images:
                head_counter[image] += 1
            entries_by_image[image].append(entry)

    referenced_files = sorted(image_counter)
    missing_assets = sorted(set(referenced_files) - asset_file_set)
    unreferenced_assets = sorted(asset_file_set - set(referenced_files))

    lines = [
        "# Rare glyphs and images",
        "",
        f"- Asset directory: `{asset_dir}`",
        f"- PNG files present: {len(asset_files)}",
        f"- Unique image files referenced in `main.tex`: {len(referenced_files)}",
        f"- Missing referenced assets: {len(missing_assets)}",
        f"- Unreferenced checked-in PNG assets: {len(unreferenced_assets)}",
        "",
        "## Referenced image files",
        "",
        "| File | References | Used in heads | Entries |",
        "| --- | ---: | ---: | --- |",
    ]

    for image in referenced_files:
        rendered_entries = []
        seen_entry_ids: set[str] = set()
        for entry in sorted(entries_by_image[image], key=entry_sort_key):
            if entry["id"] in seen_entry_ids:
                continue
            seen_entry_ids.add(entry["id"])
            rendered_entries.append(f"`{entry['id']}`")
        lines.append(
            f"| `{image}` | {image_counter[image]} | {head_counter[image]} | {' '.join(rendered_entries)} |"
        )

    lines.extend(
        [
            "",
            "## Missing referenced assets",
            "",
        ]
    )
    if missing_assets:
        for image in missing_assets:
            lines.append(f"- `{image}`")
    else:
        lines.append("- None")

    lines.extend(
        [
            "",
            "## Unreferenced checked-in PNG assets",
            "",
        ]
    )
    if unreferenced_assets:
        for image in unreferenced_assets:
            lines.append(f"- `{image}`")
    else:
        lines.append("- None")

    return "\n".join(lines) + "\n"


def classify_label(token: str) -> str:
    stripped = token.strip()
    if stripped.startswith("·"):
        return "suffix-dot"
    if stripped.startswith(":"):
        return "suffix-colon"
    if stripped.endswith("·"):
        return "prefix-dot"
    if stripped.endswith(":"):
        return "prefix-colon"
    return "bare"


def render_semantic_labels_report(entries_data: dict[str, Any]) -> str:
    token_counter: Counter[str] = Counter()
    entries_by_token: dict[str, set[str]] = defaultdict(set)
    examples_by_token: dict[str, str] = {}

    for entry in entries_data["entries"]:
        tokens = inventory_tex.find_macro_arguments(entry["raw_body"], "textsuperscript")
        for token in tokens:
            normalized = token.strip()
            token_counter[normalized] += 1
            entries_by_token[normalized].add(entry["id"])
            examples_by_token.setdefault(normalized, entry["id"])

    shape_counter = Counter(classify_label(token) for token in token_counter)

    lines = [
        "# Semantic labels used in TeX",
        "",
        f"- Total `\\textsuperscript{{...}}` occurrences in extracted entries: {sum(token_counter.values())}",
        f"- Unique superscript tokens: {len(token_counter)}",
        "",
        "## Token shapes",
        "",
        "| Shape | Unique tokens |",
        "| --- | ---: |",
    ]

    for shape in ["prefix-dot", "prefix-colon", "suffix-dot", "suffix-colon", "bare"]:
        lines.append(f"| {shape} | {shape_counter.get(shape, 0)} |")

    lines.extend(
        [
            "",
            "## Tokens",
            "",
            "| Token | Shape | Occurrences | Entries | Example entry |",
            "| --- | --- | ---: | ---: | --- |",
        ]
    )

    for token, count in token_counter.most_common():
        shape = classify_label(token)
        entry_count = len(entries_by_token[token])
        example = examples_by_token[token]
        lines.append(
            f"| `{escape_markdown_code(token)}` | {shape} | {count} | {entry_count} | `{example}` |"
        )

    return "\n".join(lines) + "\n"


def write_report(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_reports(
    entries_data: dict[str, Any],
    reports_dir: Path,
    asset_dir: Path,
) -> None:
    write_report(reports_dir / "tex_entries_by_gsr.md", render_tex_entries_by_gsr(entries_data))
    write_report(
        reports_dir / "tex_entries_without_gsr.md",
        render_tex_entries_without_gsr(entries_data),
    )
    write_report(
        reports_dir / "rare_glyphs_and_images.md",
        render_rare_glyphs_report(entries_data, asset_dir),
    )
    write_report(
        reports_dir / "semantic_labels_used_in_tex.md",
        render_semantic_labels_report(entries_data),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build TeX-derived Markdown reports.")
    parser.add_argument("--source", default="main.tex", help="Path to the TeX source file.")
    parser.add_argument(
        "--entries-json",
        default="data/current_tex_entries.json",
        help="Path to the extracted entry JSON file.",
    )
    parser.add_argument(
        "--reports-dir",
        default="reports",
        help="Directory where Markdown reports will be written.",
    )
    parser.add_argument(
        "--asset-dir",
        default="hard-character-images",
        help="Directory containing checked-in PNG glyph assets.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    entries_data = load_entries_data(Path(args.entries_json), Path(args.source))
    build_reports(entries_data, Path(args.reports_dir), Path(args.asset_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
