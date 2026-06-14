from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import spreadsheet_import


DEFAULT_TEX_ENTRIES = "data/current_tex_entries.json"
DEFAULT_MAND2MC = "data/derived/mand2mc.csv"
DEFAULT_SHENGFU = "data/derived/shengfu.csv"
DEFAULT_REPORTS_DIR = "reports"


def load_entries(entries_path: Path) -> list[dict[str, Any]]:
    if not entries_path.exists():
        raise FileNotFoundError(f"TeX entry JSON not found: {entries_path}")
    payload = json.loads(entries_path.read_text(encoding="utf-8"))
    return payload["entries"]


def load_csv(path: Path):
    pd = spreadsheet_import.import_pandas()
    if not path.exists():
        raise FileNotFoundError(f"Derived CSV not found: {path}")
    frame = pd.read_csv(path, dtype=object).where(lambda table: table.notna(), None)
    return frame


def escape_markdown(value: Any) -> str:
    if value is None:
        return ""
    return str(value).replace("`", "\\`").replace("|", "\\|").replace("\n", " ")


def build_tex_character_index(entries: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    index: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in entries:
        seen: set[str] = set()
        for character in entry.get("chinese_characters", []):
            if character in seen:
                continue
            seen.add(character)
            index[character].append(entry)
    return index


def build_tex_head_character_set(entries: list[dict[str, Any]]) -> set[str]:
    result: set[str] = set()
    for entry in entries:
        for character in entry.get("head", {}).get("characters", []):
            result.add(character)
    return result


def find_rows_not_in_tex(mand2mc_frame, character_index: dict[str, list[dict[str, Any]]]):
    missing_rows: list[dict[str, Any]] = []
    for row in mand2mc_frame.to_dict("records"):
        character = row.get("normalized_character")
        if not character:
            continue
        if character not in character_index:
            missing_rows.append(row)
    return missing_rows


def find_candidate_mc_conflicts(mand2mc_frame, character_index: dict[str, list[dict[str, Any]]]):
    conflicts: list[dict[str, Any]] = []

    for row in mand2mc_frame.to_dict("records"):
        character = row.get("normalized_character")
        mc_nwh = row.get("normalized_mc_nwh")
        if not character or not mc_nwh:
            continue

        matched_entries = character_index.get(character, [])
        if not matched_entries:
            continue

        matched_by_gsr = []
        gsr = row.get("normalized_gsr")
        if gsr:
            matched_by_gsr = [
                entry for entry in matched_entries if gsr in entry.get("gsr_markers", [])
            ]

        candidate_entries = matched_by_gsr or matched_entries
        if any(mc_nwh in entry.get("mc_forms", []) for entry in candidate_entries):
            continue

        conflicts.append(
            {
                "row": row,
                "matched_entries": candidate_entries,
                "matched_by_gsr": bool(matched_by_gsr),
            }
        )

    return conflicts


def find_shengfu_groups_missing_from_tex(shengfu_frame, tex_head_characters: set[str]):
    grouped_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in shengfu_frame.to_dict("records"):
        component = row.get("normalized_phonetic_component")
        if not component:
            continue
        grouped_rows[component].append(row)

    missing_groups = []
    for component, rows in grouped_rows.items():
        if component not in tex_head_characters:
            missing_groups.append(
                {
                    "component": component,
                    "row_count": len(rows),
                    "sample_characters": sorted(
                        {
                            row.get("normalized_character")
                            for row in rows
                            if row.get("normalized_character")
                        }
                    )[:10],
                }
            )

    missing_groups.sort(key=lambda item: (-item["row_count"], item["component"]))
    return missing_groups


def render_mand2mc_rows_not_in_tex(missing_rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Mand2MC rows not in TeX",
        "",
        f"- Rows whose normalized character is absent from extracted TeX characters: {len(missing_rows)}",
        "",
        "| Source row | Character | Pinyin | MC (NWH) | GSR |",
        "| ---: | --- | --- | --- | --- |",
    ]

    for row in missing_rows:
        lines.append(
            f"| {escape_markdown(row.get('source_row_number'))} | {escape_markdown(row.get('normalized_character'))} | "
            f"{escape_markdown(row.get('normalized_pinyin'))} | {escape_markdown(row.get('normalized_mc_nwh'))} | "
            f"{escape_markdown(row.get('normalized_gsr'))} |"
        )

    return "\n".join(lines) + "\n"


def render_tex_forms_conflicting_with_mand2mc(conflicts: list[dict[str, Any]]) -> str:
    lines = [
        "# TeX forms conflicting with Mand2MC",
        "",
        "- This is an entry-level candidate-conflict report.",
        "- A row is listed when a Mand2MC character matches at least one extracted TeX entry, but the row's normalized `MC (NWH)` form is absent from the matched entry's extracted `\\textit{...}` forms.",
        "",
        f"- Candidate conflicts: {len(conflicts)}",
        "",
        "| Character | Mand2MC row | Mand2MC MC (NWH) | GSR | Match scope | Matching TeX entries |",
        "| --- | ---: | --- | --- | --- | --- |",
    ]

    for conflict in conflicts:
        row = conflict["row"]
        match_scope = "character+GSR" if conflict["matched_by_gsr"] else "character"
        rendered_entries = []
        for entry in conflict["matched_entries"]:
            rendered_entries.append(
                f"`{entry['id']}` MC={escape_markdown(', '.join(entry.get('mc_forms', [])))} GSR={escape_markdown(', '.join(entry.get('gsr_markers', [])))}"
            )
        lines.append(
            f"| {escape_markdown(row.get('normalized_character'))} | {escape_markdown(row.get('source_row_number'))} | "
            f"{escape_markdown(row.get('normalized_mc_nwh'))} | {escape_markdown(row.get('normalized_gsr'))} | "
            f"{match_scope} | {'<br>'.join(rendered_entries)} |"
        )

    return "\n".join(lines) + "\n"


def render_shengfu_groups_missing_from_tex(missing_groups: list[dict[str, Any]]) -> str:
    lines = [
        "# Shengfu groups missing from TeX",
        "",
        "- This report compares normalized Shengfu phonetic-component values against extracted TeX head characters.",
        f"- Missing phonetic-component groups: {len(missing_groups)}",
        "",
        "| Component | Rows | Sample characters |",
        "| --- | ---: | --- |",
    ]

    for group in missing_groups:
        lines.append(
            f"| {escape_markdown(group['component'])} | {group['row_count']} | "
            f"{escape_markdown(', '.join(group['sample_characters']))} |"
        )

    return "\n".join(lines) + "\n"


def write_reports(entries, mand2mc_frame, shengfu_frame, reports_dir: Path) -> None:
    character_index = build_tex_character_index(entries)
    tex_head_characters = build_tex_head_character_set(entries)

    spreadsheet_import.write_markdown_report(
        render_mand2mc_rows_not_in_tex(find_rows_not_in_tex(mand2mc_frame, character_index)),
        reports_dir / "mand2mc_rows_not_in_tex.md",
    )
    spreadsheet_import.write_markdown_report(
        render_tex_forms_conflicting_with_mand2mc(
            find_candidate_mc_conflicts(mand2mc_frame, character_index)
        ),
        reports_dir / "tex_forms_conflicting_with_mand2mc.md",
    )
    spreadsheet_import.write_markdown_report(
        render_shengfu_groups_missing_from_tex(
            find_shengfu_groups_missing_from_tex(shengfu_frame, tex_head_characters)
        ),
        reports_dir / "shengfu_groups_missing_from_tex.md",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compare derived source tables against TeX entries.")
    parser.add_argument("--tex-entries", default=DEFAULT_TEX_ENTRIES, help="Path to current_tex_entries.json.")
    parser.add_argument("--mand2mc", default=DEFAULT_MAND2MC, help="Path to derived Mand2MC CSV.")
    parser.add_argument("--shengfu", default=DEFAULT_SHENGFU, help="Path to derived Shengfu CSV.")
    parser.add_argument("--reports-dir", default=DEFAULT_REPORTS_DIR, help="Directory for Markdown reports.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    entries = load_entries(Path(args.tex_entries))
    mand2mc_frame = load_csv(Path(args.mand2mc))
    shengfu_frame = load_csv(Path(args.shengfu))
    write_reports(entries, mand2mc_frame, shengfu_frame, Path(args.reports_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
