from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import spreadsheet_import


DEFAULT_INPUT = "key references/声符级别-2022.06.07.xlsx"
DEFAULT_OUTPUT = "data/derived/shengfu.csv"
DEFAULT_REPORT = "reports/import_shengfu.md"
DEFAULT_SHEET = "Sheet1"


def transform_shengfu(frame):
    transformed = frame.copy()
    spreadsheet_import.add_normalized_column(
        transformed,
        "normalized_character",
        ["字", "character", "Character"],
    )
    spreadsheet_import.add_normalized_column(
        transformed,
        "normalized_phonetic_component",
        ["声符", "聲符"],
    )
    spreadsheet_import.add_normalized_column(
        transformed,
        "normalized_component_level",
        ["声符级别", "聲符級別"],
    )
    spreadsheet_import.add_normalized_column(
        transformed,
        "normalized_secondary_component",
        ["次級聲符", "次级声符", "次級声符"],
    )
    spreadsheet_import.add_normalized_column(
        transformed,
        "normalized_fanqie",
        ["反切"],
    )
    spreadsheet_import.add_normalized_column(
        transformed,
        "normalized_source",
        ["来源", "來源"],
    )
    spreadsheet_import.add_normalized_column(
        transformed,
        "normalized_oc_initial",
        ["上古声", "上古聲"],
    )
    spreadsheet_import.add_normalized_column(
        transformed,
        "normalized_oc_rhyme",
        ["上古韵", "上古韻"],
    )
    spreadsheet_import.add_normalized_column(
        transformed,
        "normalized_oc_syllable",
        ["上古音节", "上古音節"],
    )
    return transformed


def render_report(
    *,
    source_path: Path,
    source_sheet_name: str,
    transformed_frame,
    raw_columns: list[str],
    sheet_summaries: list[dict[str, Any]],
) -> str:
    normalized_columns = [
        "normalized_character",
        "normalized_phonetic_component",
        "normalized_component_level",
        "normalized_secondary_component",
        "normalized_fanqie",
        "normalized_source",
        "normalized_oc_initial",
        "normalized_oc_rhyme",
        "normalized_oc_syllable",
    ]

    lines = [
        "# Shengfu import report",
        "",
        f"- Source file: `{source_path}`",
        f"- Imported sheet: `{source_sheet_name}`",
        f"- Data rows: {len(transformed_frame)}",
        f"- Raw column count: {len(raw_columns)}",
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

    return "\n".join(lines) + "\n"


def import_shengfu(input_path: Path, output_path: Path, report_path: Path, sheet_name: str) -> None:
    excel_file = spreadsheet_import.load_excel_file(input_path, engine="openpyxl")
    raw_frame, raw_columns, resolved_sheet_name = spreadsheet_import.read_sheet_with_exact_header(
        excel_file, sheet_name
    )
    transformed_frame = transform_shengfu(raw_frame)
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
    parser = argparse.ArgumentParser(description="Import the Shengfu spreadsheet.")
    parser.add_argument("--input", default=DEFAULT_INPUT, help="Path to the .xlsx source file.")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Path to the output CSV file.")
    parser.add_argument("--report-out", default=DEFAULT_REPORT, help="Path to the Markdown report.")
    parser.add_argument("--sheet", default=DEFAULT_SHEET, help="Worksheet name to import.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    import_shengfu(
        input_path=Path(args.input),
        output_path=Path(args.output),
        report_path=Path(args.report_out),
        sheet_name=args.sheet,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
