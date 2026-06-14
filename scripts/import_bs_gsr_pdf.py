from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

import spreadsheet_import


DEFAULT_INPUT = "key references/Reconstructions in GSR order.pdf"
DEFAULT_OUTPUT = "data/derived/bs_gsr.csv"
DEFAULT_REPORT = "reports/import_bs_gsr_pdf.md"

ROW_RE = re.compile(
    r"^(?P<character>\S+)\s+"
    r"(?P<pinyin>\S+)\s+"
    r"(?P<mc>\S+)\s+"
    r"(?P<mc_analyzed>\([^)]*\))\s+"
    r"(?P<lemma>.+?)\s+"
    r"(?:(?P<gsr_raw>--|-?[0-9]{1,4}[a-z]{0,3}(?:[’'])?)\s+)?"
    r"U\+(?P<unicode>[0-9A-F]+)\s*$",
    re.IGNORECASE,
)


def extract_pdf_text(pdf_path: Path) -> str:
    if shutil.which("pdftotext") is None:
        raise RuntimeError("pdftotext is required to extract the BS/GSR PDF.")

    completed = subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), "-"],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return completed.stdout


def normalize_gsr(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip().replace("’", "'")
    if not cleaned or cleaned == "--":
        return None
    return cleaned


def parse_bs_gsr_line(line: str) -> dict[str, Any] | None:
    match = ROW_RE.match(line.rstrip())
    if not match:
        return None

    lemma = match.group("lemma").strip()
    parts = re.split(r"\s{2,}", lemma, maxsplit=1)
    if len(parts) == 2:
        oc = parts[0].strip() or None
        gloss = parts[1].strip() or None
    elif len(parts) == 1:
        only = parts[0].strip()
        if only.startswith("*") or only.startswith("{"):
            oc = only or None
            gloss = None
        else:
            oc = None
            gloss = only or None
    else:
        return None
    gsr_raw = match.group("gsr_raw")

    return {
        "character": match.group("character"),
        "pinyin": match.group("pinyin"),
        "mc_bs": match.group("mc"),
        "mc_analyzed": match.group("mc_analyzed"),
        "oc_bs": oc,
        "gloss": gloss,
        "gsr_raw": gsr_raw,
        "normalized_gsr": normalize_gsr(gsr_raw),
        "unicode_utf16": f"U+{match.group('unicode')}",
    }


def import_bs_gsr_pdf(pdf_path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    text = extract_pdf_text(pdf_path)
    pages = text.split("\f")
    rows: list[dict[str, Any]] = []
    unparsed_candidates: list[dict[str, Any]] = []

    for page_number, page_text in enumerate(pages, start=1):
        for line_number, line in enumerate(page_text.splitlines(), start=1):
            if "U+" not in line:
                continue
            parsed = parse_bs_gsr_line(line)
            if parsed is None:
                unparsed_candidates.append(
                    {
                        "page_number": page_number,
                        "line_number": line_number,
                        "line": line.rstrip(),
                    }
                )
                continue
            parsed["source_page_number"] = page_number
            parsed["source_line_number"] = line_number
            rows.append(parsed)

    return rows, unparsed_candidates


def build_dataframe(rows: list[dict[str, Any]]):
    pd = spreadsheet_import.import_pandas()
    frame = pd.DataFrame(rows)
    if not frame.empty:
        frame = frame[
            [
                "source_page_number",
                "source_line_number",
                "character",
                "pinyin",
                "mc_bs",
                "mc_analyzed",
                "oc_bs",
                "gloss",
                "gsr_raw",
                "normalized_gsr",
                "unicode_utf16",
            ]
        ]
    return frame


def render_report(
    *,
    pdf_path: Path,
    frame,
    unparsed_candidates: list[dict[str, Any]],
) -> str:
    unique_gsr = sorted({value for value in frame["normalized_gsr"].dropna().tolist()}) if not frame.empty else []
    spot_check_keys = [
        ("可", "0001a"),
        ("歌", "0001q"),
        ("我", "0002a"),
        ("多", "0003a"),
        ("左", "0005a"),
    ]
    rows = frame.to_dict("records")
    lines = [
        "# Baxter-Sagart GSR PDF import report",
        "",
        f"- Source file: `{pdf_path}`",
        f"- Parsed rows: {len(frame)}",
        f"- Rows with normalized GSR values: {int(frame['normalized_gsr'].notna().sum()) if not frame.empty else 0}",
        f"- Unique normalized GSR values: {len(unique_gsr)}",
        f"- Unparsed candidate lines containing `U+`: {len(unparsed_candidates)}",
        "",
        "## Spot checks",
        "",
        "| Character | GSR | Found | MC | Page | Unicode |",
        "| --- | --- | --- | --- | ---: | --- |",
    ]

    for character, gsr in spot_check_keys:
        match = next(
            (
                row
                for row in rows
                if row["character"] == character and row["normalized_gsr"] == gsr
            ),
            None,
        )
        if match is None:
            lines.append(f"| {character} | {gsr} | no |  |  |  |")
        else:
            lines.append(
                f"| {character} | {gsr} | yes | {match['mc_bs']} | {match['source_page_number']} | {match['unicode_utf16']} |"
            )

    lines.extend(
        [
            "",
            "## Unparsed candidate sample",
            "",
        ]
    )

    if unparsed_candidates:
        for item in unparsed_candidates[:20]:
            lines.append(
                f"- page {item['page_number']}, line {item['line_number']}: `{item['line'].replace('`', '\\`')}`"
            )
    else:
        lines.append("- None")

    return "\n".join(lines) + "\n"


def write_outputs(frame, report_text: str, csv_path: Path, report_path: Path) -> None:
    spreadsheet_import.write_csv(frame, csv_path)
    spreadsheet_import.write_markdown_report(report_text, report_path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Import the Baxter-Sagart GSR-order PDF.")
    parser.add_argument("--input", default=DEFAULT_INPUT, help="Path to the BS/GSR PDF.")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Path to the derived CSV.")
    parser.add_argument("--report-out", default=DEFAULT_REPORT, help="Path to the Markdown report.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    rows, unparsed_candidates = import_bs_gsr_pdf(Path(args.input))
    frame = build_dataframe(rows)
    report_text = render_report(
        pdf_path=Path(args.input),
        frame=frame,
        unparsed_candidates=unparsed_candidates,
    )
    write_outputs(frame, report_text, Path(args.output), Path(args.report_out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
