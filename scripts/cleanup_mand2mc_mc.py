from __future__ import annotations

import argparse
from pathlib import Path

import mc_orthography
import spreadsheet_import


DEFAULT_INPUT = "data/derived/mand2mc.csv"
DEFAULT_OUTPUT = "data/derived/mand2mc.csv"
DEFAULT_REPORT = "reports/cleanup_mand2mc_mc.md"


def render_report(*, source_path: Path, summary: dict[str, object]) -> str:
    lines = [
        "# Mand2MC MC cleanup",
        "",
        f"- Source file: `{source_path}`",
        f"- Auto-corrected NWH MC rows (`o → ə` when Baxter MC also has `o`): {summary['auto_corrected_count']}",
        f"- Remaining anomalous NWH MC rows with `o`: {summary['anomaly_count']}",
        "",
    ]

    for title, rows in [
        ("## Auto-corrected rows", summary["auto_corrected_rows"]),
        ("## Remaining anomalies", summary["anomaly_rows"]),
    ]:
        lines.extend(
            [
                title,
                "",
                "| Row | Character | NWH before | NWH after | Baxter MC |",
                "| ---: | --- | --- | --- | --- |",
            ]
        )
        if rows:
            for row in rows:
                lines.append(
                    f"| {row['source_row_number']} | {row['character'] or ''} | "
                    f"`{row['normalized_mc_nwh_before'] or ''}` | "
                    f"`{row['normalized_mc_nwh_after'] or ''}` | "
                    f"`{row['normalized_mc_bs'] or ''}` |"
                )
        else:
            lines.append("|  |  |  |  |  |")
        lines.append("")

    return "\n".join(lines) + "\n"


def cleanup_mand2mc_csv(input_path: Path, output_path: Path, report_path: Path) -> dict[str, object]:
    pd = spreadsheet_import.import_pandas()
    frame = pd.read_csv(input_path, dtype=object).where(lambda table: table.notna(), None)
    summary = mc_orthography.normalize_mand2mc_frame(frame)
    spreadsheet_import.write_csv(frame, output_path)
    spreadsheet_import.write_markdown_report(
        render_report(source_path=input_path, summary=summary),
        report_path,
    )
    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Clean existing derived Mand2MC MC transcriptions so NWH o aligns to ə when Baxter MC has o.")
    parser.add_argument("--input", default=DEFAULT_INPUT)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--report-out", default=DEFAULT_REPORT)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    cleanup_mand2mc_csv(
        input_path=Path(args.input),
        output_path=Path(args.output),
        report_path=Path(args.report_out),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
