from __future__ import annotations

from typing import Any


def dedupe(values: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def resolve_candidate_mc(candidate: dict[str, Any]) -> dict[str, Any]:
    mand2mc_nwh_forms = dedupe(
        [row.get("mc_nwh") for row in candidate.get("mand2mc_rows", []) if row.get("mc_nwh")]
    )
    mand2mc_bs_forms = dedupe(
        [row.get("mc_bs") for row in candidate.get("mand2mc_rows", []) if row.get("mc_bs")]
    )
    bs_gsr_forms = dedupe(
        [row.get("mc_bs") for row in candidate.get("bs_gsr_rows", []) if row.get("mc_bs")]
    )

    mand2mc_bs_set = set(mand2mc_bs_forms)
    bs_not_in_mand2mc = [form for form in bs_gsr_forms if form not in mand2mc_bs_set]
    mand2mc_not_in_bs_gsr = (
        [form for form in mand2mc_bs_forms if form not in set(bs_gsr_forms)]
        if bs_gsr_forms
        else []
    )

    if bs_not_in_mand2mc:
        status = "investigate-bs-not-in-mand2mc"
    elif mand2mc_nwh_forms or mand2mc_bs_forms:
        status = "mand2mc-authoritative"
    elif bs_gsr_forms:
        status = "bs-gsr-fallback"
    else:
        status = "no-mc-available"

    return {
        "status": status,
        "authoritative_source": "mand2mc" if (mand2mc_nwh_forms or mand2mc_bs_forms) else "bs_gsr",
        "display_forms": mand2mc_nwh_forms or bs_gsr_forms,
        "mand2mc_nwh_forms": mand2mc_nwh_forms,
        "mand2mc_bs_forms": mand2mc_bs_forms,
        "bs_gsr_forms": bs_gsr_forms,
        "bs_not_in_mand2mc": bs_not_in_mand2mc,
        "mand2mc_not_in_bs_gsr": mand2mc_not_in_bs_gsr,
        "needs_investigation": bool(bs_not_in_mand2mc),
    }
