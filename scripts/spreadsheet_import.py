from __future__ import annotations

import math
from pathlib import Path
from typing import Any


class SpreadsheetDependencyError(RuntimeError):
    pass


class SpreadsheetInputError(RuntimeError):
    pass


def import_pandas():
    try:
        import pandas as pd  # type: ignore
    except ModuleNotFoundError as exc:
        raise SpreadsheetDependencyError(
            "The pandas package is required for spreadsheet imports."
        ) from exc
    return pd


def require_engine_dependency(engine: str) -> None:
    module_name = "openpyxl" if engine == "openpyxl" else "odf"
    package_name = "openpyxl" if engine == "openpyxl" else "odfpy"

    try:
        __import__(module_name)
    except ModuleNotFoundError as exc:
        raise SpreadsheetDependencyError(
            f"The {package_name} package is required to read {engine}-backed spreadsheets."
        ) from exc


def coerce_missing(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    return value


def header_cell_to_name(value: Any) -> str:
    value = coerce_missing(value)
    if value is None:
        return ""
    return str(value)


def normalize_text(value: Any) -> str | None:
    value = coerce_missing(value)
    if value is None:
        return None
    if isinstance(value, float) and value.is_integer():
        text = str(int(value))
    else:
        text = str(value)
    stripped = text.strip()
    return stripped or None


def load_excel_file(path: Path, engine: str):
    pd = import_pandas()
    require_engine_dependency(engine)

    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    return pd.ExcelFile(path, engine=engine)


def read_sheet_with_exact_header(excel_file, sheet_name: str | int, allow_empty: bool = False):
    pd = import_pandas()
    raw_frame = excel_file.parse(sheet_name=sheet_name, header=None, dtype=object)
    raw_frame = raw_frame.where(pd.notna(raw_frame), None)
    resolved_sheet_name = (
        excel_file.sheet_names[sheet_name] if isinstance(sheet_name, int) else sheet_name
    )

    if raw_frame.empty or raw_frame.notna().sum().sum() == 0:
        if allow_empty:
            empty_frame = pd.DataFrame()
            empty_frame.insert(0, "source_row_number", pd.Series(dtype=object))
            empty_frame.insert(1, "source_sheet_name", pd.Series(dtype=object))
            return empty_frame, [], resolved_sheet_name
        raise SpreadsheetInputError(f"Sheet {sheet_name!r} is empty.")

    header = [header_cell_to_name(value) for value in raw_frame.iloc[0].tolist()]
    frame = raw_frame.iloc[1:].reset_index(drop=True).copy()
    frame.columns = header
    frame.insert(0, "source_row_number", range(2, len(frame) + 2))
    frame.insert(1, "source_sheet_name", resolved_sheet_name)
    return frame, header, resolved_sheet_name


def collect_sheet_summaries(excel_file) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []

    for sheet_name in excel_file.sheet_names:
        frame, header, resolved_name = read_sheet_with_exact_header(
            excel_file, sheet_name, allow_empty=True
        )
        summaries.append(
            {
                "sheet_name": resolved_name,
                "data_row_count": len(frame),
                "column_count": len(header),
                "columns": header,
            }
        )

    return summaries


def get_first_matching_series(frame, candidates: list[str]):
    pd = import_pandas()
    lowered_candidates = {candidate.casefold() for candidate in candidates}

    for column_index, column_name in enumerate(frame.columns):
        if not isinstance(column_name, str):
            continue
        if column_name in candidates or column_name.casefold() in lowered_candidates:
            return frame.iloc[:, column_index]

    return pd.Series([None] * len(frame), index=frame.index, dtype=object)


def add_normalized_column(frame, new_name: str, candidates: list[str]) -> None:
    pd = import_pandas()
    source_series = get_first_matching_series(frame, candidates)
    frame[new_name] = pd.Series(
        [normalize_text(value) for value in source_series.tolist()],
        index=frame.index,
        dtype=object,
    )


def count_missing_values(series) -> int:
    return sum(
        1
        for value in series.tolist()
        if coerce_missing(value) is None or coerce_missing(value) == ""
    )


def write_csv(frame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output_path, index=False, encoding="utf-8")


def write_markdown_report(content: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
