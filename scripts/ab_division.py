from __future__ import annotations

import re
from typing import Any


PALATAL_ONLY_ONSETS = {"c", "j", "ś", "ź"}
VOWEL_RE = re.compile(r"[aeiouyəɨɛɔ]")
TEXTOVERSET_RE = re.compile(r"\\textoverset\{[ab]\}\{([ao])\}")


def dedupe_preserve(values: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def normalize_mc_form(form: str) -> str:
    normalized = form.strip().rstrip(".,;")
    normalized = re.sub(r"[0-9]+$", "", normalized)
    normalized = re.sub(r"[HX]$", "", normalized)
    return normalized


def split_onset_and_rhyme(form: str) -> tuple[str, str]:
    match = VOWEL_RE.search(form)
    if not match:
        return form, ""
    return form[: match.start()], form[match.start() :]


def classify_mc_form(form: str) -> dict[str, str]:
    normalized = normalize_mc_form(form)
    onset, rhyme = split_onset_and_rhyme(normalized)
    if not rhyme:
        return {
            "form": form,
            "normalized": normalized,
            "class": "unknown",
            "reason": "no_vowel_detected",
        }
    if onset in PALATAL_ONLY_ONSETS:
        return {
            "form": form,
            "normalized": normalized,
            "class": "b",
            "reason": "palatal_initial",
        }
    if not onset and rhyme.startswith("i"):
        return {
            "form": form,
            "normalized": normalized,
            "class": "unknown",
            "reason": "zero_onset_bare_i",
        }
    if rhyme.startswith(("i", "y")):
        return {
            "form": form,
            "normalized": normalized,
            "class": "b",
            "reason": "explicit_i_medial",
        }
    return {
        "form": form,
        "normalized": normalized,
        "class": "a",
        "reason": "no_i_medial",
    }


def summarize_group_class(form_analyses: list[dict[str, str]]) -> tuple[str, str]:
    counts: dict[str, int] = {}
    for analysis in form_analyses:
        counts[analysis["class"]] = counts.get(analysis["class"], 0) + 1
    if counts.get("a") and not counts.get("b"):
        if counts.get("unknown"):
            return "a", "known forms point to type a; ambiguous forms remain"
        return "a", "all extracted forms lack an i-medial after the onset"
    if counts.get("b") and not counts.get("a"):
        if counts.get("unknown"):
            return "b", "known forms point to type b; ambiguous forms remain"
        return "b", "all extracted forms show an i-medial or a dedicated palatal onset"
    if counts.get("a") and counts.get("b"):
        return "mixed", "the extracted forms point to both type a and type b"
    return "unknown", "the extracted forms are too ambiguous for this rule"


def collect_candidate_display_forms(candidate: dict[str, Any]) -> list[str]:
    resolution = candidate.get("mc_resolution") or {}
    if resolution.get("display_forms"):
        return dedupe_preserve([form for form in resolution["display_forms"] if form])
    forms = [
        row.get("mc_nwh")
        for row in candidate.get("mand2mc_rows", [])
        if row.get("mc_nwh")
    ] + [
        row.get("mc_bs")
        for row in candidate.get("bs_gsr_rows", [])
        if row.get("mc_bs")
    ]
    return dedupe_preserve(forms)


def collect_group_display_forms(candidates: list[dict[str, Any]]) -> list[str]:
    forms: list[str] = []
    for candidate in candidates:
        forms.extend(collect_candidate_display_forms(candidate))
    return dedupe_preserve(forms)


def root_needs_division_marker(root: str | None) -> bool:
    if not root:
        return False
    if TEXTOVERSET_RE.search(root):
        return False
    return any(vowel in root for vowel in ("a", "o"))


def decorate_root_with_division(root: str, division_class: str) -> str:
    if division_class not in {"a", "b"} or not root_needs_division_marker(root):
        return root
    candidates = [(root.find(vowel), vowel) for vowel in ("a", "o") if root.find(vowel) != -1]
    if not candidates:
        return root
    index, vowel = sorted(candidates)[0]
    return root[:index] + rf"\textoverset{{{division_class}}}{{{vowel}}}" + root[index + 1 :]


def resolve_root_display(root: str | None, mc_forms: list[str]) -> dict[str, Any]:
    form_analyses = [classify_mc_form(form) for form in dedupe_preserve(mc_forms)]
    division_class, note = summarize_group_class(form_analyses)
    mark_required = bool(root) and division_class in {"a", "b"} and root_needs_division_marker(root)
    display_root = decorate_root_with_division(root, division_class) if root and mark_required else root
    return {
        "display_root": display_root,
        "division_class": division_class,
        "division_note": note,
        "mark_required": mark_required,
        "mc_forms": dedupe_preserve(mc_forms),
        "form_analyses": form_analyses,
    }
