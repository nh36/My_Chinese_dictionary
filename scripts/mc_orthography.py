from __future__ import annotations

from typing import Any


AUTO_CORRECTION_STATUS = "auto-corrected-baxter-o-to-schwa"
ANOMALY_STATUS = "nwh-o-without-bs-o"


def normalize_nwh_mc_against_bs(nwh_form: str | None, bs_form: str | None) -> tuple[str | None, str | None]:
    if not nwh_form:
        return nwh_form, None
    if "o" not in nwh_form:
        return nwh_form, None
    if bs_form and "o" in bs_form:
        return nwh_form.replace("o", "ə"), AUTO_CORRECTION_STATUS
    return nwh_form, ANOMALY_STATUS


def summarize_row(row: dict[str, Any], *, normalized_nwh: str | None, status: str) -> dict[str, Any]:
    return {
        "source_row_number": row.get("source_row_number"),
        "character": row.get("normalized_character") or row.get("character"),
        "normalized_mc_nwh_before": row.get("normalized_mc_nwh"),
        "normalized_mc_nwh_after": normalized_nwh,
        "normalized_mc_bs": row.get("normalized_mc_bs"),
        "status": status,
    }


def normalize_mand2mc_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    auto_corrected_rows: list[dict[str, Any]] = []
    anomaly_rows: list[dict[str, Any]] = []

    for row in records:
        normalized_nwh = row.get("normalized_mc_nwh")
        normalized_bs = row.get("normalized_mc_bs")
        corrected_nwh, status = normalize_nwh_mc_against_bs(normalized_nwh, normalized_bs)
        row["normalized_mc_nwh"] = corrected_nwh

        if status == AUTO_CORRECTION_STATUS:
            auto_corrected_rows.append(summarize_row(row, normalized_nwh=corrected_nwh, status=status))
        elif status == ANOMALY_STATUS:
            anomaly_rows.append(summarize_row(row, normalized_nwh=corrected_nwh, status=status))

    return {
        "auto_corrected_count": len(auto_corrected_rows),
        "anomaly_count": len(anomaly_rows),
        "auto_corrected_rows": auto_corrected_rows,
        "anomaly_rows": anomaly_rows,
    }


def normalize_mand2mc_frame(frame) -> dict[str, Any]:
    auto_corrected_rows: list[dict[str, Any]] = []
    anomaly_rows: list[dict[str, Any]] = []

    for index in frame.index.tolist():
        row = {
            "source_row_number": frame.at[index, "source_row_number"] if "source_row_number" in frame.columns else None,
            "character": frame.at[index, "character"] if "character" in frame.columns else None,
            "normalized_character": frame.at[index, "normalized_character"] if "normalized_character" in frame.columns else None,
            "normalized_mc_nwh": frame.at[index, "normalized_mc_nwh"] if "normalized_mc_nwh" in frame.columns else None,
            "normalized_mc_bs": frame.at[index, "normalized_mc_bs"] if "normalized_mc_bs" in frame.columns else None,
        }
        corrected_nwh, status = normalize_nwh_mc_against_bs(
            row.get("normalized_mc_nwh"),
            row.get("normalized_mc_bs"),
        )
        frame.at[index, "normalized_mc_nwh"] = corrected_nwh
        if status == AUTO_CORRECTION_STATUS:
            auto_corrected_rows.append(summarize_row(row, normalized_nwh=corrected_nwh, status=status))
        elif status == ANOMALY_STATUS:
            anomaly_rows.append(summarize_row(row, normalized_nwh=corrected_nwh, status=status))

    summary = {
        "auto_corrected_count": len(auto_corrected_rows),
        "anomaly_count": len(anomaly_rows),
        "auto_corrected_rows": auto_corrected_rows,
        "anomaly_rows": anomaly_rows,
    }
    frame.attrs["mc_orthography_summary"] = summary
    return summary
