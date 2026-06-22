from __future__ import annotations

import re
from collections import Counter
from typing import Any

import inventory_tex


FOOTNOTE_TOKEN = r"\footnote{"
VISIBLE_NOTE_IGNORE_PREFIXES = (
    r"\paragraph",
    r"\begin{",
    r"\end{",
    r"\item",
    r"\textit{",
    r"{\large",
    r"{\Large",
    r"% no MC",
)
NOTE_BLOCK_START_RE = re.compile(
    r"(?:\\textbf\{|"
    r"\bI need to\b|"
    r"\bI will have to\b|"
    r"\bI do not see\b|"
    r"\bI find this\b|"
    r"\bI prefer\b|"
    r"\bAcc\. to Wiktionary\b|"
    r"\bBaxter\b|"
    r"\bRelevant article\b|"
    r"\bSeems to me\b|"
    r"\bnot a XS character\b|"
    r"\bCHECK\b)",
)
LARGE_ITEM_RE = re.compile(r"\\item\s+\{\\Large\{([^}]+)\}\}")
HEADLINE_CHAR_RE = re.compile(r"\{\\huge\{([^}]+)\}\}")


def normalize_note_text(text: str | None) -> str:
    if not text:
        return ""
    return " ".join(text.replace("\n", " ").split())


def classify_note_text(text: str, source_layer: str) -> str:
    lowered = text.casefold()
    if source_layer == "curation_entry_note":
        return "workflow_internal"
    if source_layer == "curation_semantic_review":
        return "semantic_unresolved"
    if source_layer == "curation_division_note":
        return "structural_internal"
    if source_layer == "curation_mc_investigation":
        return "mc_conflict"
    if source_layer == "curation_research_note":
        return "semantic_analysis"
    if "swjz" in lowered or "wiktionary" in lowered or "baxter" in lowered or "sagart" in lowered or "zhengzhang" in lowered or "boltz" in lowered or "ibid." in lowered:
        return "source_reference"
    if "i need to" in lowered or "i will have to" in lowered or "i have left off" in lowered or "not yet hand-checked" in lowered or "staging area" in lowered or "check " in lowered:
        return "workflow_internal"
    if "not a xs character" in lowered or "not clear to me" in lowered or "i do not see" in lowered or "i find this a hard one" in lowered or lowered.startswith("i prefer "):
        return "editorial_uncertainty"
    return "analysis_note"


def recommended_rendering(note: dict[str, Any]) -> str:
    visibility = note.get("visibility")
    source_layer = note.get("source_layer")
    category = note.get("category")
    if visibility == "internal":
        return "internal_only"
    if source_layer == "hand_footnote":
        return "footnote"
    if category in {"source_reference", "analysis_note", "editorial_uncertainty", "semantic_analysis", "mc_conflict"}:
        return "series_end_note"
    return "internal_only"


def infer_anchor(entry_id: str, context_line: str | None) -> tuple[str, str | None]:
    if not context_line:
        return "entry", None
    large_item = LARGE_ITEM_RE.search(context_line)
    if large_item is not None:
        return "character", large_item.group(1)
    headline = HEADLINE_CHAR_RE.search(context_line)
    if headline is not None:
        return "series", headline.group(1)
    stripped = context_line.strip()
    if stripped and inventory_tex.CHINESE_CHAR_RE.match(stripped[0]):
        return "character", stripped[0]
    return "entry", None


def find_line_number(text: str, start_index: int, base_line: int) -> int:
    return base_line + text.count("\n", 0, start_index)


def extract_footnotes_from_hand_entry(entry_id: str, raw_block: str, start_line: int) -> list[dict[str, Any]]:
    lines = raw_block.splitlines()
    notes: list[dict[str, Any]] = []
    index = 0
    while True:
        footnote_index = raw_block.find(FOOTNOTE_TOKEN, index)
        if footnote_index == -1:
            return notes
        brace_index = footnote_index + len(r"\footnote")
        content, end_index = inventory_tex.parse_braced(raw_block, brace_index)
        line_number = find_line_number(raw_block, footnote_index, start_line)
        context_line_index = max(0, min(line_number - start_line, len(lines) - 1))
        context_line = lines[context_line_index] if lines else None
        anchor_kind, anchor_value = infer_anchor(entry_id, context_line)
        text = normalize_note_text(content)
        note = {
            "entry_id": entry_id,
            "source_layer": "hand_footnote",
            "visibility": "rendered",
            "anchor_kind": anchor_kind,
            "anchor_value": anchor_value,
            "line_number": line_number,
            "text": text,
        }
        note["category"] = classify_note_text(text, note["source_layer"])
        note["recommended_rendering"] = recommended_rendering(note)
        notes.append(note)
        index = end_index


def is_visible_prose_note_start(stripped: str) -> bool:
    if not stripped or stripped.startswith("%"):
        return False
    if stripped.startswith(VISIBLE_NOTE_IGNORE_PREFIXES):
        return False
    if stripped.startswith(r"{\includegraphics"):
        return False
    first = stripped[0]
    if inventory_tex.CHINESE_CHAR_RE.match(first):
        return False
    return bool(NOTE_BLOCK_START_RE.search(stripped))


def is_visible_prose_note_continuation(stripped: str) -> bool:
    if not stripped or stripped.startswith("%"):
        return False
    if stripped.startswith(VISIBLE_NOTE_IGNORE_PREFIXES):
        return False
    if stripped.startswith(r"{\includegraphics"):
        return False
    first = stripped[0]
    if inventory_tex.CHINESE_CHAR_RE.match(first):
        return False
    if re.search(r"\d{4}[a-z](?:')?$", stripped):
        return False
    if re.search(r"[A-Za-z]{3,}", stripped):
        return True
    if re.fullmatch(r"[^\s]+(?:\s+[^\s]+){0,2}", stripped):
        return False
    return True


def extract_visible_prose_notes_from_hand_entry(entry_id: str, raw_block: str, start_line: int) -> list[dict[str, Any]]:
    notes: list[dict[str, Any]] = []
    active_lines: list[str] = []
    active_start_line: int | None = None

    def flush() -> None:
        nonlocal active_lines, active_start_line
        if not active_lines or active_start_line is None:
            active_lines = []
            active_start_line = None
            return
        text = normalize_note_text(" ".join(active_lines))
        note = {
            "entry_id": entry_id,
            "source_layer": "hand_prose_note",
            "visibility": "rendered",
            "anchor_kind": "series",
            "anchor_value": None,
            "line_number": active_start_line,
            "text": text,
        }
        note["category"] = classify_note_text(text, note["source_layer"])
        note["recommended_rendering"] = recommended_rendering(note)
        notes.append(note)
        active_lines = []
        active_start_line = None

    for offset, line in enumerate(raw_block.splitlines()[1:], start=1):
        stripped = line.strip()
        if is_visible_prose_note_start(stripped):
            if active_start_line is None:
                active_start_line = start_line + offset
            active_lines.append(stripped)
            continue
        if active_start_line is not None and is_visible_prose_note_continuation(stripped):
            active_lines.append(stripped)
            continue
        flush()

    flush()
    return notes


def collect_hand_entry_notes(hand_entry: dict[str, Any] | None, entry_id: str) -> list[dict[str, Any]]:
    if not hand_entry:
        return []
    raw_block = hand_entry.get("raw_block") or ""
    start_line = hand_entry.get("start_line") or 1
    return extract_footnotes_from_hand_entry(entry_id, raw_block, start_line) + extract_visible_prose_notes_from_hand_entry(entry_id, raw_block, start_line)


def make_internal_note(
    *,
    entry_id: str,
    source_layer: str,
    text: str,
    anchor_kind: str = "entry",
    anchor_value: str | None = None,
) -> dict[str, Any]:
    normalized = normalize_note_text(text)
    note = {
        "entry_id": entry_id,
        "source_layer": source_layer,
        "visibility": "internal",
        "anchor_kind": anchor_kind,
        "anchor_value": anchor_value,
        "line_number": None,
        "text": normalized,
    }
    note["category"] = classify_note_text(normalized, source_layer)
    note["recommended_rendering"] = recommended_rendering(note)
    return note


def collect_curation_notes(curated_entry: dict[str, Any] | None, entry_id: str) -> list[dict[str, Any]]:
    if not curated_entry:
        return []
    notes: list[dict[str, Any]] = []
    for text in curated_entry.get("notes") or []:
        notes.append(make_internal_note(entry_id=entry_id, source_layer="curation_entry_note", text=text))

    resolved_series_root = curated_entry.get("resolved_series_root") or {}
    if resolved_series_root.get("division_note"):
        notes.append(
            make_internal_note(
                entry_id=entry_id,
                source_layer="curation_division_note",
                text=resolved_series_root["division_note"],
                anchor_kind="series",
                anchor_value=resolved_series_root.get("character"),
            )
        )

    for candidate in curated_entry.get("proposed_additions", []):
        character = candidate.get("character")
        review = candidate.get("semantic_assignment_review") or {}
        if review:
            text = (
                f"Suppressed non-Latin semantic marker `{review.get('original_abbreviation')}` "
                f"for component `{review.get('semantic_component')}` "
                f"from `{review.get('original_source')}`."
            )
            notes.append(
                make_internal_note(
                    entry_id=entry_id,
                    source_layer="curation_semantic_review",
                    text=text,
                    anchor_kind="character",
                    anchor_value=character,
                )
            )

        semantic_assignment = candidate.get("semantic_assignment") or {}
        if semantic_assignment.get("research_note"):
            note = {
                "entry_id": entry_id,
                "source_layer": "curation_research_note",
                "visibility": "internal",
                "anchor_kind": "character",
                "anchor_value": character,
                "line_number": None,
                "text": normalize_note_text(semantic_assignment["research_note"]),
            }
            note["category"] = classify_note_text(note["text"], note["source_layer"])
            note["recommended_rendering"] = "series_end_note"
            notes.append(note)

        mc_resolution = candidate.get("mc_resolution") or {}
        if mc_resolution.get("needs_investigation"):
            missing_readings = ", ".join(mc_resolution.get("bs_not_in_mand2mc") or [])
            text = "BS/GSR has readings absent from Mand2MC."
            if missing_readings:
                text += f" Missing in Mand2MC: {missing_readings}."
            notes.append(
                make_internal_note(
                    entry_id=entry_id,
                    source_layer="curation_mc_investigation",
                    text=text,
                    anchor_kind="character",
                    anchor_value=character,
                )
            )

        resolved_node_root = candidate.get("resolved_node_root") or {}
        if resolved_node_root.get("division_note"):
            notes.append(
                make_internal_note(
                    entry_id=entry_id,
                    source_layer="curation_division_note",
                    text=resolved_node_root["division_note"],
                    anchor_kind="character",
                    anchor_value=character,
                )
            )
    return notes


def collect_record_notes(
    *,
    entry_id: str,
    hand_entry: dict[str, Any] | None,
    curated_entry: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    return collect_hand_entry_notes(hand_entry, entry_id) + collect_curation_notes(curated_entry, entry_id)


def summarize_notes(notes: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "total": len(notes),
        "by_source_layer": dict(Counter(note["source_layer"] for note in notes)),
        "by_category": dict(Counter(note["category"] for note in notes)),
        "by_visibility": dict(Counter(note["visibility"] for note in notes)),
        "by_recommended_rendering": dict(Counter(note["recommended_rendering"] for note in notes)),
    }
