from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import build_coverage_model
import hierarchy_utils
import mc_resolution


DEFAULT_TEX_ENTRIES = "data/current_tex_entries.json"
DEFAULT_MAND2MC = "data/derived/mand2mc.csv"
DEFAULT_SHENGFU = "data/derived/shengfu.csv"
DEFAULT_BS_GSR = "data/derived/bs_gsr.csv"
DEFAULT_SCHUESSLER_PDF = "key references/Schuessler, Axel 2009/Schuessler 2009.pdf"
DEFAULT_OUTPUT_DIR = "data/series_packets"
DEFAULT_REPORT_DIR = "reports/series_packets"
DEFAULT_PILOT_IDS = [
    "04-04",
    "02-01",
    "02-32",
    "03-32",
    "38-03",
    "04-30",
    "03-49",
    "03-57",
    "03-65",
    "04-02",
    "12-01",
    "04-26",
    "04-29",
    "12-08",
    "12-25",
    "11-12",
    "16-15",
    "16-20",
    "16-01",
    "26-38",
    "27-08",
    "32-16",
    "33-30",
    "24-21",
    "25-15",
    "28-11",
    "24-01",
    "09-25",
    "09-17",
    "16-06",
    "16-33",
    "03-38",
    "13-32",
    "07-25",
    "07-29",
    "07-08",
    "04-61",
    "34-23",
    "35-01",
    "35-21",
    "18-18",
    "21-01",
    "01-01",
    "01-43",
]


def sanitize_mand_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_row_number": row.get("source_row_number"),
        "character": row.get("normalized_character"),
        "pinyin": row.get("normalized_pinyin"),
        "mc_nwh": row.get("normalized_mc_nwh"),
        "mc_bs": row.get("normalized_mc_bs"),
        "gsr": row.get("normalized_gsr"),
    }


def sanitize_bs_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_page_number": row.get("source_page_number"),
        "character": row.get("character"),
        "pinyin": row.get("pinyin"),
        "mc_bs": row.get("mc_bs"),
        "mc_analyzed": row.get("mc_analyzed"),
        "oc_bs": row.get("oc_bs"),
        "gloss": row.get("gloss"),
        "gsr": row.get("normalized_gsr"),
        "unicode_utf16": row.get("unicode_utf16"),
    }


def sanitize_shengfu_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_row_number": row.get("source_row_number"),
        "character": row.get("normalized_character"),
        "phonetic_component": row.get("normalized_phonetic_component"),
        "component_level": row.get("normalized_component_level"),
        "secondary_component": row.get("normalized_secondary_component"),
        "fanqie": row.get("normalized_fanqie"),
        "source": row.get("normalized_source"),
        "oc_initial": row.get("normalized_oc_initial"),
        "oc_rhyme": row.get("normalized_oc_rhyme"),
        "oc_syllable": row.get("normalized_oc_syllable"),
    }


def load_gsc_coverage_rows(path: Path) -> dict[str, dict[str, Any]]:
    rows = build_coverage_model.load_csv_records(path)
    return {row["gsc_id"]: row for row in rows}


def load_entries_by_id(path: Path) -> dict[str, dict[str, Any]]:
    entries = build_coverage_model.load_entries(path)
    return {entry["id"]: entry for entry in entries}


def build_candidate_rows(
    *,
    candidate_characters: list[str],
    tex_entry: dict[str, Any] | None,
    matched_mand_rows: list[dict[str, Any]],
    matched_bs_rows: list[dict[str, Any]],
    shengfu_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    tex_characters = set(tex_entry.get("chinese_characters", [])) if tex_entry else set()
    candidate_rows: list[dict[str, Any]] = []

    for character in candidate_characters:
        mand_rows_for_char = [
            sanitize_mand_row(row)
            for row in matched_mand_rows
            if row.get("normalized_character") == character
        ]
        bs_rows_for_char = [
            sanitize_bs_row(row)
            for row in matched_bs_rows
            if row.get("character") == character
        ]
        shengfu_char_rows = [
            sanitize_shengfu_row(row)
            for row in shengfu_rows
            if row.get("normalized_character") == character
        ]
        shengfu_component_rows = [
            sanitize_shengfu_row(row)
            for row in shengfu_rows
            if row.get("normalized_phonetic_component") == character
        ]

        candidate = {
            "character": character,
            "in_tex": character in tex_characters,
            "mand2mc_rows": mand_rows_for_char,
            "bs_gsr_rows": bs_rows_for_char,
            "shengfu_character_rows": shengfu_char_rows,
            "shengfu_component_rows": shengfu_component_rows,
        }
        candidate["mc_resolution"] = mc_resolution.resolve_candidate_mc(candidate)
        candidate["mand_bs_mc_disagreement"] = candidate["mc_resolution"]["needs_investigation"]
        candidate_rows.append(candidate)

    return candidate_rows


def build_series_packet(
    *,
    gsc_id: str,
    entries_by_id: dict[str, dict[str, Any]],
    gsc_coverage_rows: dict[str, dict[str, Any]],
    mand_rows: list[dict[str, Any]],
    shengfu_rows: list[dict[str, Any]],
    bs_rows: list[dict[str, Any]],
    schuessler_headers: list[dict[str, Any]],
) -> dict[str, Any]:
    tex_entry = entries_by_id.get(gsc_id)
    coverage_row = gsc_coverage_rows[gsc_id]
    header = next(header for header in schuessler_headers if header["gsc_id"] == gsc_id)
    mand_index = build_coverage_model.index_rows_by_gsr(mand_rows, "normalized_gsr")
    bs_index = build_coverage_model.index_rows_by_gsr(bs_rows, "normalized_gsr")
    if tex_entry is None:
        source_tokens = header["k_tokens"]
        source_token_strategy = "schuessler_k_tokens"
    else:
        source_tokens = build_coverage_model.dedupe_preserve(
            [
                str(parts[0])
                for token in tex_entry.get("gsr_markers", [])
                if (parts := build_coverage_model.split_gsr_token(token)) is not None
            ]
        )
        source_token_strategy = "tex_gsr_prefixes"

    matched_mand_rows = build_coverage_model.rows_for_gsr_tokens(
        source_tokens, mand_index, "normalized_gsr"
    )
    matched_bs_rows = build_coverage_model.rows_for_gsr_tokens(
        source_tokens, bs_index, "normalized_gsr"
    )
    candidate_characters = build_coverage_model.dedupe_preserve(
        [row["normalized_character"] for row in matched_mand_rows if row.get("normalized_character")]
        + [row["character"] for row in matched_bs_rows if row.get("character")]
    )
    candidate_rows = build_candidate_rows(
        candidate_characters=candidate_characters,
        tex_entry=tex_entry,
        matched_mand_rows=matched_mand_rows,
        matched_bs_rows=matched_bs_rows,
        shengfu_rows=shengfu_rows,
    )

    packet_kind = "existing_addendum" if tex_entry else "missing_series"

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "gsc_id": gsc_id,
        "packet_kind": packet_kind,
        "candidate_source_strategy": source_token_strategy,
        "candidate_source_tokens": source_tokens,
        "schuessler": header,
        "coverage": coverage_row,
        "tex_entry": {
            "id": tex_entry["id"],
            "section": tex_entry["section"],
            "subsection": tex_entry["subsection"],
            "head": tex_entry["head"],
            "context_environments": tex_entry.get("context_environments", []),
            "start_line": tex_entry["start_line"],
            "end_line": tex_entry["end_line"],
            "chinese_characters": tex_entry["chinese_characters"],
            "commented_pinyin": tex_entry["commented_pinyin"],
            "mc_forms": tex_entry["mc_forms"],
            "gsr_markers": tex_entry["gsr_markers"],
            "raw_block": tex_entry["raw_block"],
        }
        if tex_entry
        else None,
        "entry_hierarchy": {
            "top_level_head": hierarchy_utils.extract_head_character(tex_entry["head"]),
            "nodes": hierarchy_utils.extract_hierarchy_nodes(tex_entry["raw_block"]),
        }
        if tex_entry
        else None,
        "candidate_characters": candidate_rows,
        "source_rows": {
            "mand2mc": [sanitize_mand_row(row) for row in matched_mand_rows],
            "bs_gsr": [sanitize_bs_row(row) for row in matched_bs_rows],
        },
        "notes": [
            "Machine-assembled curation packet; preserve all evidence and review before merging into main.tex.",
            "Do not treat candidate character lists or source matches as settled editorial decisions.",
        ],
    }


def render_packet_report(packet: dict[str, Any]) -> str:
    coverage = packet["coverage"]
    lines = [
        f"# Series packet {packet['gsc_id']}",
        "",
        f"- Packet kind: `{packet['packet_kind']}`",
        f"- Schuessler K tokens: `{coverage['schuessler_k_tokens']}`",
        f"- Candidate-source strategy: `{packet['candidate_source_strategy']}` with tokens `{'; '.join(packet['candidate_source_tokens'])}`",
        f"- Schuessler page: {coverage['schuessler_source_page']}",
        f"- TeX present: {coverage['in_tex']}",
        f"- Mand2MC character count: {coverage['mand2mc_character_count']}",
        f"- BS/GSR character count: {coverage['bs_gsr_character_count']}",
        f"- Combined source character count: {coverage['combined_source_character_count']}",
        "",
    ]

    if packet["tex_entry"] is not None:
        tex_entry = packet["tex_entry"]
        lines.extend(
            [
                "## Existing TeX entry",
                "",
                f"- Entry ID: `{tex_entry['id']}`",
                f"- Section/subsection: `{tex_entry['section']}` / `{tex_entry['subsection']}`",
                f"- Source lines: {tex_entry['start_line']}-{tex_entry['end_line']}",
                "",
                "```tex",
                tex_entry["raw_block"].rstrip(),
                "```",
                "",
            ]
        )

    lines.extend(
        [
            "## Candidate characters",
            "",
            "| Character | In TeX | Mand2MC rows | BS/GSR rows | Shengfu rows | As phonetic component | MC disagreement |",
            "| --- | --- | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for item in packet["candidate_characters"]:
        lines.append(
            f"| {item['character']} | {'yes' if item['in_tex'] else 'no'} | "
            f"{len(item['mand2mc_rows'])} | {len(item['bs_gsr_rows'])} | "
            f"{len(item['shengfu_character_rows'])} | {len(item['shengfu_component_rows'])} | "
            f"{'yes' if item['mand_bs_mc_disagreement'] else ''} |"
        )

    lines.extend(
        [
            "",
            "## Candidate characters not already in TeX",
            "",
        ]
    )
    not_in_tex = [item["character"] for item in packet["candidate_characters"] if not item["in_tex"]]
    lines.append(", ".join(not_in_tex) if not_in_tex else "None")

    return "\n".join(lines) + "\n"


def write_packet(packet: dict[str, Any], output_dir: Path, report_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"{packet['gsc_id']}.json").write_text(
        json.dumps(packet, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (report_dir / f"{packet['gsc_id']}.md").write_text(
        render_packet_report(packet),
        encoding="utf-8",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Export hand-checkable series packets.")
    parser.add_argument("--tex-entries", default=DEFAULT_TEX_ENTRIES)
    parser.add_argument("--mand2mc", default=DEFAULT_MAND2MC)
    parser.add_argument("--shengfu", default=DEFAULT_SHENGFU)
    parser.add_argument("--bs-gsr", default=DEFAULT_BS_GSR)
    parser.add_argument("--schuessler-pdf", default=DEFAULT_SCHUESSLER_PDF)
    parser.add_argument("--gsc-coverage", default="data/derived/gsc_series_coverage.csv")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--report-dir", default=DEFAULT_REPORT_DIR)
    parser.add_argument("--ids", nargs="+", default=DEFAULT_PILOT_IDS)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    entries_by_id = load_entries_by_id(Path(args.tex_entries))
    gsc_coverage_rows = load_gsc_coverage_rows(Path(args.gsc_coverage))
    mand_rows = build_coverage_model.load_csv_records(Path(args.mand2mc))
    shengfu_rows = build_coverage_model.load_csv_records(Path(args.shengfu))
    bs_rows = build_coverage_model.load_csv_records(Path(args.bs_gsr))
    schuessler_headers = build_coverage_model.parse_schuessler_headers(Path(args.schuessler_pdf))

    for gsc_id in args.ids:
        packet = build_series_packet(
            gsc_id=gsc_id,
            entries_by_id=entries_by_id,
            gsc_coverage_rows=gsc_coverage_rows,
            mand_rows=mand_rows,
            shengfu_rows=shengfu_rows,
            bs_rows=bs_rows,
            schuessler_headers=schuessler_headers,
        )
        write_packet(packet, Path(args.output_dir), Path(args.report_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
