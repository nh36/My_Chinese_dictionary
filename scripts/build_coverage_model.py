from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import spreadsheet_import


DEFAULT_TEX_ENTRIES = "data/current_tex_entries.json"
DEFAULT_MAND2MC = "data/derived/mand2mc.csv"
DEFAULT_SHENGFU = "data/derived/shengfu.csv"
DEFAULT_BS_GSR = "data/derived/bs_gsr.csv"
DEFAULT_SCHUESSLER_PDF = "key references/Schuessler, Axel 2009/Schuessler 2009.pdf"
DEFAULT_CHARACTER_COVERAGE = "data/derived/character_coverage.csv"
DEFAULT_GSC_COVERAGE = "data/derived/gsc_series_coverage.csv"
DEFAULT_REPORTS_DIR = "reports"

SCHUESSLER_HEADER_RE = re.compile(
    r"^\s*(?P<gsc_id>\d{1,2}-\d{1,2})-?\s*=\s*K\.\s*(?P<rest>.+)$"
)
K_TOKEN_BLOB_RE = re.compile(r"^\s*(?P<blob>(?:\d+[a-z]?(?:-[a-z])?(?:')?(?:\s*,\s*|\s+)?)*)")
K_TOKEN_RANGE_RE = re.compile(r"^(?P<digits>\d+)(?P<start>[a-z])-(?P<end>[a-z])$", re.IGNORECASE)
GSR_TOKEN_RE = re.compile(r"^(?P<digits>\d+)(?P<suffix>[a-z]?(?:')?)?$", re.IGNORECASE)


def expand_k_token_blob(blob: str) -> tuple[list[str], bool]:
    tokens: list[str] = []
    has_explicit_range = False
    for raw_token in re.split(r"[\s,]+", blob.strip()):
        if not raw_token:
            continue
        range_match = K_TOKEN_RANGE_RE.match(raw_token)
        if range_match:
            digits = range_match.group("digits")
            start = range_match.group("start").lower()
            end = range_match.group("end").lower()
            has_explicit_range = True
            for codepoint in range(ord(start), ord(end) + 1):
                tokens.append(f"{digits}{chr(codepoint)}")
            continue
        token_match = re.match(r"\d+[a-z]?(?:')?", raw_token, flags=re.IGNORECASE)
        if token_match:
            tokens.append(token_match.group(0).lower())
    return tokens, has_explicit_range


def extract_schuessler_text(pdf_path: Path) -> str:
    if shutil.which("pdftotext") is None:
        raise RuntimeError("pdftotext is required to extract the Schuessler PDF.")
    completed = subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), "-"],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return completed.stdout


def parse_schuessler_headers(pdf_path: Path) -> list[dict[str, Any]]:
    text = extract_schuessler_text(pdf_path)
    headers: list[dict[str, Any]] = []

    for page_number, page_text in enumerate(text.split("\f"), start=1):
        for line_number, line in enumerate(page_text.splitlines(), start=1):
            match = SCHUESSLER_HEADER_RE.match(line.rstrip())
            if not match:
                continue

            rest = match.group("rest")
            blob_match = K_TOKEN_BLOB_RE.match(rest)
            blob = blob_match.group("blob").strip() if blob_match else ""
            k_tokens, has_explicit_range = expand_k_token_blob(blob)
            if not k_tokens:
                continue
            remainder = rest[blob_match.end() :].strip() if blob_match else ""

            raw_gsc_id = match.group("gsc_id")
            rhyme_section, series_number = [int(part) for part in raw_gsc_id.split("-", 1)]
            gsc_id = f"{rhyme_section:02d}-{series_number:02d}"
            headers.append(
                {
                    "gsc_id": gsc_id,
                    "rhyme_section": rhyme_section,
                    "series_number": series_number,
                    "k_tokens": k_tokens,
                    "has_explicit_k_range": has_explicit_range,
                    "source_remainder_raw": remainder,
                    "is_cross_reference_only": remainder.lower().startswith("for "),
                    "source_page_number": page_number,
                    "source_line_number": line_number,
                    "source_line_raw": line.rstrip(),
                }
            )

    deduped: dict[str, dict[str, Any]] = {}
    for header in headers:
        deduped.setdefault(header["gsc_id"], header)
    return [deduped[key] for key in sorted(deduped, key=lambda item: tuple(int(part) for part in item.split("-")))]


def load_entries(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload["entries"]


def load_csv_records(path: Path) -> list[dict[str, Any]]:
    pd = spreadsheet_import.import_pandas()
    frame = pd.read_csv(path, dtype=object).where(lambda table: table.notna(), None)
    return frame.to_dict("records")


def split_gsr_token(token: str | None) -> tuple[int, str] | None:
    if token is None:
        return None
    cleaned = str(token).strip()
    if not cleaned or cleaned == "--":
        return None
    match = GSR_TOKEN_RE.match(cleaned)
    if not match:
        return None
    return int(match.group("digits")), (match.group("suffix") or "").lower()


def gsr_matches(source_token: str | None, target_token: str) -> bool:
    source_parts = split_gsr_token(source_token)
    target_parts = split_gsr_token(target_token)
    if source_parts is None or target_parts is None:
        return False

    source_digits, source_suffix = source_parts
    target_digits, target_suffix = target_parts
    if source_digits != target_digits:
        return False
    if not target_suffix:
        return True
    return source_suffix.startswith(target_suffix)


def explicit_range_exclusions(header: dict[str, Any], schuessler_headers: list[dict[str, Any]]) -> list[str]:
    if header.get("has_explicit_k_range"):
        return []
    bare_bases = {
        parts[0]
        for token in header.get("k_tokens", [])
        if (parts := split_gsr_token(token)) is not None and parts[1] == ""
    }
    exclusions: list[str] = []
    for other in schuessler_headers:
        if other["gsc_id"] == header["gsc_id"] or not other.get("has_explicit_k_range"):
            continue
        for token in other.get("k_tokens", []):
            parts = split_gsr_token(token)
            if parts is not None and parts[0] in bare_bases:
                exclusions.append(token)
    return dedupe_preserve(exclusions)


def rows_for_header_tokens(
    header: dict[str, Any],
    schuessler_headers: list[dict[str, Any]],
    index: dict[int, list[dict[str, Any]]],
    field_name: str,
) -> list[dict[str, Any]]:
    rows = rows_for_gsr_tokens(header["k_tokens"], index, field_name)
    exclusions = explicit_range_exclusions(header, schuessler_headers)
    if not exclusions:
        return rows
    return [
        row
        for row in rows
        if not any(gsr_matches(token, row.get(field_name)) for token in exclusions)
    ]


def dedupe_preserve(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def index_rows_by_gsr(rows: list[dict[str, Any]], field_name: str) -> dict[int, list[dict[str, Any]]]:
    index: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row_index, row in enumerate(rows):
        row["_row_id"] = row_index
        parts = split_gsr_token(row.get(field_name))
        if parts is None:
            continue
        digits, _ = parts
        index[digits].append(row)
    return index


def rows_for_gsr_tokens(tokens: list[str], index: dict[int, list[dict[str, Any]]], field_name: str) -> list[dict[str, Any]]:
    collected: list[dict[str, Any]] = []
    seen_row_ids: set[int] = set()
    for token in tokens:
        parts = split_gsr_token(token)
        if parts is None:
            continue
        digits, _ = parts
        for row in index.get(digits, []):
            if row["_row_id"] in seen_row_ids:
                continue
            if gsr_matches(row.get(field_name), token):
                seen_row_ids.add(row["_row_id"])
                collected.append(row)
    return collected


def build_character_coverage(
    entries: list[dict[str, Any]],
    mand_rows: list[dict[str, Any]],
    shengfu_rows: list[dict[str, Any]],
    bs_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    coverage: dict[str, dict[str, Any]] = {}

    def ensure(character: str) -> dict[str, Any]:
        if character not in coverage:
            coverage[character] = {
                "character": character,
                "tex_entry_ids": [],
                "tex_gsc_ids": [],
                "tex_gsr_markers": [],
                "tex_mc_forms": [],
                "mand2mc_row_numbers": [],
                "mand2mc_gsr_values": [],
                "mand2mc_pinyin_values": [],
                "mand2mc_mc_nwh_values": [],
                "shengfu_row_numbers": [],
                "shengfu_phonetic_components": [],
                "shengfu_component_levels": [],
                "bs_row_pages": [],
                "bs_gsr_values": [],
                "bs_pinyin_values": [],
                "bs_mc_values": [],
                "bs_oc_values": [],
            }
        return coverage[character]

    for entry in entries:
        for character in entry.get("chinese_characters", []):
            row = ensure(character)
            row["tex_entry_ids"].append(entry["id"])
            row["tex_gsc_ids"].append(entry["id"])
            row["tex_gsr_markers"].extend(entry.get("gsr_markers", []))
            row["tex_mc_forms"].extend(entry.get("mc_forms", []))

    for row_data in mand_rows:
        character = row_data.get("normalized_character")
        if not character:
            continue
        row = ensure(character)
        row["mand2mc_row_numbers"].append(str(row_data.get("source_row_number")))
        if row_data.get("normalized_gsr"):
            row["mand2mc_gsr_values"].append(str(row_data.get("normalized_gsr")))
        if row_data.get("normalized_pinyin"):
            row["mand2mc_pinyin_values"].append(str(row_data.get("normalized_pinyin")))
        if row_data.get("normalized_mc_nwh"):
            row["mand2mc_mc_nwh_values"].append(str(row_data.get("normalized_mc_nwh")))

    for row_data in shengfu_rows:
        character = row_data.get("normalized_character")
        if not character:
            continue
        row = ensure(character)
        row["shengfu_row_numbers"].append(str(row_data.get("source_row_number")))
        if row_data.get("normalized_phonetic_component"):
            row["shengfu_phonetic_components"].append(str(row_data.get("normalized_phonetic_component")))
        if row_data.get("normalized_component_level"):
            row["shengfu_component_levels"].append(str(row_data.get("normalized_component_level")))

    for row_data in bs_rows:
        character = row_data.get("character")
        if not character:
            continue
        row = ensure(character)
        row["bs_row_pages"].append(str(row_data.get("source_page_number")))
        if row_data.get("normalized_gsr"):
            row["bs_gsr_values"].append(str(row_data.get("normalized_gsr")))
        if row_data.get("pinyin"):
            row["bs_pinyin_values"].append(str(row_data.get("pinyin")))
        if row_data.get("mc_bs"):
            row["bs_mc_values"].append(str(row_data.get("mc_bs")))
        if row_data.get("oc_bs"):
            row["bs_oc_values"].append(str(row_data.get("oc_bs")))

    rows: list[dict[str, Any]] = []
    for character, row in coverage.items():
        rows.append(
            {
                "character": character,
                "in_tex": "yes" if row["tex_entry_ids"] else "no",
                "tex_entry_count": len(set(row["tex_entry_ids"])),
                "tex_entry_ids": "; ".join(dedupe_preserve(row["tex_entry_ids"])),
                "tex_gsr_markers": "; ".join(dedupe_preserve(row["tex_gsr_markers"])),
                "tex_mc_forms": "; ".join(dedupe_preserve(row["tex_mc_forms"])),
                "in_mand2mc": "yes" if row["mand2mc_row_numbers"] else "no",
                "mand2mc_row_count": len(row["mand2mc_row_numbers"]),
                "mand2mc_gsr_values": "; ".join(dedupe_preserve(row["mand2mc_gsr_values"])),
                "mand2mc_pinyin_values": "; ".join(dedupe_preserve(row["mand2mc_pinyin_values"])),
                "mand2mc_mc_nwh_values": "; ".join(dedupe_preserve(row["mand2mc_mc_nwh_values"])),
                "in_shengfu": "yes" if row["shengfu_row_numbers"] else "no",
                "shengfu_row_count": len(row["shengfu_row_numbers"]),
                "shengfu_phonetic_components": "; ".join(dedupe_preserve(row["shengfu_phonetic_components"])),
                "shengfu_component_levels": "; ".join(dedupe_preserve(row["shengfu_component_levels"])),
                "in_bs_gsr": "yes" if row["bs_row_pages"] else "no",
                "bs_row_count": len(row["bs_row_pages"]),
                "bs_gsr_values": "; ".join(dedupe_preserve(row["bs_gsr_values"])),
                "bs_pinyin_values": "; ".join(dedupe_preserve(row["bs_pinyin_values"])),
                "bs_mc_values": "; ".join(dedupe_preserve(row["bs_mc_values"])),
                "bs_oc_values": "; ".join(dedupe_preserve(row["bs_oc_values"])),
            }
        )

    rows.sort(key=lambda item: item["character"])
    return rows


def build_gsc_series_coverage(
    entries: list[dict[str, Any]],
    schuessler_headers: list[dict[str, Any]],
    mand_rows: list[dict[str, Any]],
    bs_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    entry_by_id = {entry["id"]: entry for entry in entries}
    mand_index = index_rows_by_gsr(mand_rows, "normalized_gsr")
    bs_index = index_rows_by_gsr(bs_rows, "normalized_gsr")
    rows: list[dict[str, Any]] = []

    for header in schuessler_headers:
        entry = entry_by_id.get(header["gsc_id"])
        matched_mand = rows_for_header_tokens(header, schuessler_headers, mand_index, "normalized_gsr")
        matched_bs = rows_for_header_tokens(header, schuessler_headers, bs_index, "normalized_gsr")
        mand_characters = dedupe_preserve(
            [row["normalized_character"] for row in matched_mand if row.get("normalized_character")]
        )
        bs_characters = dedupe_preserve(
            [row["character"] for row in matched_bs if row.get("character")]
        )
        combined_characters = dedupe_preserve(mand_characters + bs_characters)

        rows.append(
            {
                "gsc_id": header["gsc_id"],
                "rhyme_section": header["rhyme_section"],
                "series_number": header["series_number"],
                "schuessler_k_tokens": "; ".join(header["k_tokens"]),
                "schuessler_source_page": header["source_page_number"],
                "schuessler_cross_reference_only": "yes" if header.get("is_cross_reference_only") else "no",
                "in_tex": "yes" if entry else "no",
                "tex_character_count": len(entry["chinese_characters"]) if entry else 0,
                "tex_characters_sample": "; ".join(entry["chinese_characters"][:10]) if entry else "",
                "mand2mc_row_count": len(matched_mand),
                "mand2mc_character_count": len(mand_characters),
                "mand2mc_characters_sample": "; ".join(mand_characters[:10]),
                "bs_gsr_row_count": len(matched_bs),
                "bs_gsr_character_count": len(bs_characters),
                "bs_gsr_characters_sample": "; ".join(bs_characters[:10]),
                "combined_source_character_count": len(combined_characters),
                "combined_source_characters_sample": "; ".join(combined_characters[:10]),
            }
        )

    rows.sort(key=lambda item: (item["rhyme_section"], item["series_number"]))
    return rows


def build_existing_series_expansion_candidates(
    entries: list[dict[str, Any]],
    mand_rows: list[dict[str, Any]],
    bs_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    mand_index = index_rows_by_gsr(mand_rows, "normalized_gsr")
    bs_index = index_rows_by_gsr(bs_rows, "normalized_gsr")
    candidates: list[dict[str, Any]] = []

    for entry in entries:
        tex_characters = set(entry.get("chinese_characters", []))
        entry_gsr_tokens = dedupe_preserve(entry.get("gsr_markers", []))
        gsr_prefix_tokens = dedupe_preserve(
            [
                str(parts[0])
                for token in entry_gsr_tokens
                if (parts := split_gsr_token(token)) is not None
            ]
        )
        matched_mand = rows_for_gsr_tokens(gsr_prefix_tokens, mand_index, "normalized_gsr")
        matched_bs = rows_for_gsr_tokens(gsr_prefix_tokens, bs_index, "normalized_gsr")
        missing_characters = dedupe_preserve(
            [
                row["normalized_character"]
                for row in matched_mand
                if row.get("normalized_character") and row["normalized_character"] not in tex_characters
            ]
            + [
                row["character"]
                for row in matched_bs
                if row.get("character") and row["character"] not in tex_characters
            ]
        )
        if not missing_characters:
            continue

        candidates.append(
            {
                "gsc_id": entry["id"],
                "subsection": entry["subsection"],
                "candidate_character_count": len(missing_characters),
                "candidate_characters_sample": "; ".join(missing_characters[:20]),
                "tex_character_count": len(tex_characters),
                "gsr_tokens": "; ".join(gsr_prefix_tokens),
            }
        )

    candidates.sort(key=lambda item: (-item["candidate_character_count"], item["gsc_id"]))
    return candidates


def build_missing_shengfu_components(
    shengfu_rows: list[dict[str, Any]],
    entries: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    tex_head_characters = {
        character
        for entry in entries
        for character in entry.get("head", {}).get("characters", [])
    }
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in shengfu_rows:
        component = row.get("normalized_phonetic_component")
        if not component:
            continue
        grouped[component].append(row)

    results = []
    for component, rows in grouped.items():
        if component in tex_head_characters:
            continue
        sample_characters = dedupe_preserve(
            [row["normalized_character"] for row in rows if row.get("normalized_character")]
        )[:10]
        results.append(
            {
                "component": component,
                "row_count": len(rows),
                "sample_characters": "; ".join(sample_characters),
            }
        )
    results.sort(key=lambda item: (-item["row_count"], item["component"]))
    return results


def write_csv_rows(rows: list[dict[str, Any]], output_path: Path) -> None:
    pd = spreadsheet_import.import_pandas()
    frame = pd.DataFrame(rows)
    spreadsheet_import.write_csv(frame, output_path)


def render_gsc_series_coverage_report(gsc_rows: list[dict[str, Any]]) -> str:
    section_counter: dict[int, dict[str, int]] = defaultdict(lambda: {"total": 0, "represented": 0})
    for row in gsc_rows:
        section = int(row["rhyme_section"])
        section_counter[section]["total"] += 1
        if row["in_tex"] == "yes":
            section_counter[section]["represented"] += 1

    lines = [
        "# GSC series coverage",
        "",
        f"- Total GSC series headers extracted from Schuessler PDF: {len(gsc_rows)}",
        f"- Series represented in `main.tex`: {sum(1 for row in gsc_rows if row['in_tex'] == 'yes')}",
        f"- Missing series: {sum(1 for row in gsc_rows if row['in_tex'] == 'no')}",
        "",
        "## Coverage by rhyme section",
        "",
        "| Rhyme section | Total series | Represented in TeX | Missing |",
        "| ---: | ---: | ---: | ---: |",
    ]

    for section in sorted(section_counter):
        total = section_counter[section]["total"]
        represented = section_counter[section]["represented"]
        lines.append(f"| {section:02d} | {total} | {represented} | {total - represented} |")

    return "\n".join(lines) + "\n"


def render_missing_gsc_report(gsc_rows: list[dict[str, Any]]) -> str:
    missing_rows = [row for row in gsc_rows if row["in_tex"] == "no"]
    section_counter: Counter[int] = Counter(int(row["rhyme_section"]) for row in missing_rows)
    sections_missing_entirely = [
        section
        for section in sorted({int(row["rhyme_section"]) for row in gsc_rows})
        if all(row["in_tex"] == "no" for row in gsc_rows if int(row["rhyme_section"]) == section)
    ]

    lines = [
        "# Missing GSC rhymes and series",
        "",
        f"- Missing GSC series: {len(missing_rows)}",
        f"- Rhyme sections missing entirely from `main.tex`: {', '.join(f'{section:02d}' for section in sections_missing_entirely) if sections_missing_entirely else 'None'}",
        "",
        "## Missing series with strongest imported-source evidence",
        "",
        "| GSC | K tokens | Mand2MC chars | BS/GSR chars | Combined source chars | Sample characters |",
        "| --- | --- | ---: | ---: | ---: | --- |",
    ]

    for row in sorted(
        missing_rows,
        key=lambda item: (-int(item["combined_source_character_count"]), item["gsc_id"]),
    )[:200]:
        lines.append(
            f"| `{row['gsc_id']}` | `{row['schuessler_k_tokens']}` | {row['mand2mc_character_count']} | "
            f"{row['bs_gsr_character_count']} | {row['combined_source_character_count']} | "
            f"{row['combined_source_characters_sample']} |"
        )

    lines.extend(
        [
            "",
            "## Missing-series counts by rhyme section",
            "",
            "| Rhyme section | Missing series |",
            "| ---: | ---: |",
        ]
    )
    for section in sorted(section_counter):
        lines.append(f"| {section:02d} | {section_counter[section]} |")

    return "\n".join(lines) + "\n"


def render_expansion_work_queue_report(
    gsc_rows: list[dict[str, Any]],
    existing_series_candidates: list[dict[str, Any]],
    missing_shengfu_components: list[dict[str, Any]],
) -> str:
    missing_series = [row for row in gsc_rows if row["in_tex"] == "no" and int(row["combined_source_character_count"]) > 0]
    lines = [
        "# Expansion work queue",
        "",
        "- This queue is aimed at expanding the project beyond the current hand-written LaTeX.",
        "- It distinguishes between whole missing GSC series, new characters for already represented series, and missing phonetic components from the Shengfu table.",
        "",
        "## A. Missing GSC series with source evidence",
        "",
        "| Priority | GSC | K tokens | Combined source chars | Sample characters |",
        "| ---: | --- | --- | ---: | --- |",
    ]

    for priority, row in enumerate(
        sorted(missing_series, key=lambda item: (-int(item["combined_source_character_count"]), item["gsc_id"]))[:150],
        start=1,
    ):
        lines.append(
            f"| {priority} | `{row['gsc_id']}` | `{row['schuessler_k_tokens']}` | "
            f"{row['combined_source_character_count']} | {row['combined_source_characters_sample']} |"
        )

    lines.extend(
        [
            "",
            "## B. Existing TeX series with additional source-backed characters",
            "",
            "| Priority | GSC | Subsection | Candidate chars | Sample characters |",
            "| ---: | --- | --- | ---: | --- |",
        ]
    )

    for priority, row in enumerate(existing_series_candidates[:150], start=1):
        lines.append(
            f"| {priority} | `{row['gsc_id']}` | `{row['subsection']}` | {row['candidate_character_count']} | "
            f"{row['candidate_characters_sample']} |"
        )

    lines.extend(
        [
            "",
            "## C. Shengfu phonetic components not yet represented as TeX heads",
            "",
            "| Priority | Component | Rows | Sample characters |",
            "| ---: | --- | ---: | --- |",
        ]
    )
    for priority, row in enumerate(missing_shengfu_components[:100], start=1):
        lines.append(
            f"| {priority} | {row['component']} | {row['row_count']} | {row['sample_characters']} |"
        )

    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build a combined expansion coverage model.")
    parser.add_argument("--tex-entries", default=DEFAULT_TEX_ENTRIES)
    parser.add_argument("--mand2mc", default=DEFAULT_MAND2MC)
    parser.add_argument("--shengfu", default=DEFAULT_SHENGFU)
    parser.add_argument("--bs-gsr", default=DEFAULT_BS_GSR)
    parser.add_argument("--schuessler-pdf", default=DEFAULT_SCHUESSLER_PDF)
    parser.add_argument("--character-coverage-out", default=DEFAULT_CHARACTER_COVERAGE)
    parser.add_argument("--gsc-coverage-out", default=DEFAULT_GSC_COVERAGE)
    parser.add_argument("--reports-dir", default=DEFAULT_REPORTS_DIR)
    return parser


def main() -> int:
    args = build_parser().parse_args()

    entries = load_entries(Path(args.tex_entries))
    mand_rows = load_csv_records(Path(args.mand2mc))
    shengfu_rows = load_csv_records(Path(args.shengfu))
    bs_rows = load_csv_records(Path(args.bs_gsr))
    schuessler_headers = parse_schuessler_headers(Path(args.schuessler_pdf))

    character_rows = build_character_coverage(entries, mand_rows, shengfu_rows, bs_rows)
    gsc_rows = build_gsc_series_coverage(entries, schuessler_headers, mand_rows, bs_rows)
    existing_series_candidates = build_existing_series_expansion_candidates(entries, mand_rows, bs_rows)
    missing_shengfu_components = build_missing_shengfu_components(shengfu_rows, entries)

    write_csv_rows(character_rows, Path(args.character_coverage_out))
    write_csv_rows(gsc_rows, Path(args.gsc_coverage_out))
    reports_dir = Path(args.reports_dir)
    spreadsheet_import.write_markdown_report(
        render_gsc_series_coverage_report(gsc_rows),
        reports_dir / "gsc_series_coverage.md",
    )
    spreadsheet_import.write_markdown_report(
        render_missing_gsc_report(gsc_rows),
        reports_dir / "missing_gsc_rhymes_and_series.md",
    )
    spreadsheet_import.write_markdown_report(
        render_expansion_work_queue_report(
            gsc_rows,
            existing_series_candidates,
            missing_shengfu_components,
        ),
        reports_dir / "expansion_work_queue.md",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
