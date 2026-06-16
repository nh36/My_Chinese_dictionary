from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import mc_orthography
import spreadsheet_import


DEFAULT_INPUT = "key references/Mand2MC2009-06-08 copy.ods"
DEFAULT_OUTPUT = "data/derived/mand2mc.csv"
DEFAULT_REPORT = "reports/import_mand2mc.md"
DEFAULT_SHEET = "Feuil1"


def transform_mand2mc(frame):
    transformed = frame.copy()
    spreadsheet_import.add_normalized_column(
        transformed,
        "normalized_character",
        ["", "character", "Character", "字", "漢字"],
    )
    spreadsheet_import.add_normalized_column(
        transformed,
        "normalized_pinyin",
        ["pinyin", "Pinyin", "拼音"],
    )
    spreadsheet_import.add_normalized_column(
        transformed,
        "normalized_mc_nwh",
        ["MC (NWH)", "MC(NWH)", "MC NWH"],
    )
    spreadsheet_import.add_normalized_column(
        transformed,
        "normalized_mc_bs",
        ["MC (B&S)", "MC(B&S)", "MC B&S", "MC (BS)"],
    )
    spreadsheet_import.add_normalized_column(
        transformed,
        "normalized_gsr",
        ["GSR", "GSR#"],
    )
    spreadsheet_import.add_normalized_column(
        transformed,
        "normalized_hanyu_dazidian",
        ["漢語大字典"],
    )
    spreadsheet_import.add_normalized_column(
        transformed,
        "normalized_guangyun",
        ["廣韻"],
    )
    mc_orthography.normalize_mand2mc_frame(transformed)
    return transformed


def render_report(
    *,
    source_path: Path,
    source_sheet_name: str,
    transformed_frame,
    raw_columns: list[str],
    sheet_summaries: list[dict[str, Any]],
) -> str:
    mc_summary = transformed_frame.attrs.get(
        "mc_orthography_summary",
        {
            "auto_corrected_count": 0,
            "anomaly_count": 0,
            "auto_corrected_rows": [],
            "anomaly_rows": [],
        },
    )
    normalized_columns = [
        "normalized_character",
        "normalized_pinyin",
        "normalized_mc_nwh",
        "normalized_mc_bs",
        "normalized_gsr",
        "normalized_hanyu_dazidian",
        "normalized_guangyun",
    ]

    lines = [
        "# Mand2MC import report",
        "",
        f"- Source file: `{source_path}`",
        f"- Imported sheet: `{source_sheet_name}`",
        f"- Data rows: {len(transformed_frame)}",
        f"- Raw column count: {len(raw_columns)}",
        f"- Auto-corrected NWH MC rows (`o → ə` when Baxter MC also has `o`): {mc_summary['auto_corrected_count']}",
        f"- Remaining anomalous NWH MC rows with `o`: {mc_summary['anomaly_count']}",
        "",
        "## Key normalized-column coverage",
        "",
        "| Column | Missing values |",
        "| --- | ---: |",
    ]

    for column in normalized_columns:
        missing = spreadsheet_import.count_missing_values(transformed_frame[column])
        lines.append(f"| `{column}` | {missing} |")

    lines.extend(
        [
            "",
            "## Raw columns",
            "",
        ]
    )
    for column in raw_columns:
        display = column if column else "(blank column name)"
        lines.append(f"- `{display}`")

    lines.extend(
        [
            "",
            "## Workbook sheets",
            "",
            "| Sheet | Data rows | Columns |",
            "| --- | ---: | ---: |",
        ]
    )
    for summary in sheet_summaries:
        lines.append(
            f"| `{summary['sheet_name']}` | {summary['data_row_count']} | {summary['column_count']} |"
        )

    lines.extend(
        [
            "",
            "## MC orthography corrections",
            "",
            "| Row | Character | NWH before | NWH after | Baxter MC |",
            "| ---: | --- | --- | --- | --- |",
        ]
    )
    if mc_summary["auto_corrected_rows"]:
        for row in mc_summary["auto_corrected_rows"][:40]:
            lines.append(
                f"| {row['source_row_number']} | {row['character'] or ''} | "
                f"`{row['normalized_mc_nwh_before'] or ''}` | "
                f"`{row['normalized_mc_nwh_after'] or ''}` | "
                f"`{row['normalized_mc_bs'] or ''}` |"
            )
    else:
        lines.append("|  |  |  |  |  |")

    if mc_summary["anomaly_rows"]:
        lines.extend(
            [
                "",
                "## Remaining anomalous NWH MC rows",
                "",
                "| Row | Character | NWH | Baxter MC |",
                "| ---: | --- | --- | --- |",
            ]
        )
        for row in mc_summary["anomaly_rows"][:40]:
            lines.append(
                f"| {row['source_row_number']} | {row['character'] or ''} | "
                f"`{row['normalized_mc_nwh_before'] or ''}` | "
                f"`{row['normalized_mc_bs'] or ''}` |"
            )

    return "\n".join(lines) + "\n"


def import_mand2mc(input_path: Path, output_path: Path, report_path: Path, sheet_name: str) -> None:
    excel_file = spreadsheet_import.load_excel_file(input_path, engine="odf")
    raw_frame, raw_columns, resolved_sheet_name = spreadsheet_import.read_sheet_with_exact_header(
        excel_file, sheet_name
    )
    transformed_frame = transform_mand2mc(raw_frame)
    sheet_summaries = spreadsheet_import.collect_sheet_summaries(excel_file)

    spreadsheet_import.write_csv(transformed_frame, output_path)
    spreadsheet_import.write_markdown_report(
        render_report(
            source_path=input_path,
            source_sheet_name=resolved_sheet_name,
            transformed_frame=transformed_frame,
            raw_columns=raw_columns,
            sheet_summaries=sheet_summaries,
        ),
        report_path,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Import the Mand2MC spreadsheet.")
    parser.add_argument("--input", default=DEFAULT_INPUT, help="Path to the .ods source file.")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Path to the output CSV file.")
    parser.add_argument("--report-out", default=DEFAULT_REPORT, help="Path to the Markdown report.")
    parser.add_argument("--sheet", default=DEFAULT_SHEET, help="Worksheet name to import.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    import_mand2mc(
        input_path=Path(args.input),
        output_path=Path(args.output),
        report_path=Path(args.report_out),
        sheet_name=args.sheet,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
