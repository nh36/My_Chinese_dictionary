from __future__ import annotations

import re
from typing import Any


CHAR_RE = re.compile(r"[\u3400-\u9fff\U00020000-\U0002ceaf]")
RHS_RE = re.compile(r"=\s*(\{\\large\{.*)", re.DOTALL)


def dedupe(values: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def extract_hierarchy_nodes(raw_block: str) -> list[dict[str, Any]]:
    lines = raw_block.splitlines()
    nodes: list[dict[str, Any]] = []
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or stripped.startswith("%"):
            continue
        normalized = stripped.replace(r"\item", "", 1).strip()
        if r"{\Large{" not in normalized or normalized.startswith(r"\paragraph{"):
            continue
        if not CHAR_RE.search(normalized):
            continue
        window = "\n".join(lines[index : index + 4])
        rhs_match = RHS_RE.search(window)
        if not rhs_match:
            continue
        rhs = rhs_match.group(1).strip().splitlines()[0]
        key_characters = dedupe(CHAR_RE.findall(normalized))
        nodes.append(
            {
                "display_line": normalized,
                "rhs_snippet": rhs[:120],
                "key_character": key_characters[0] if key_characters else None,
                "key_characters": key_characters,
            }
        )
    return nodes


def extract_head_character(head: dict[str, Any] | None) -> str | None:
    if not head:
        return None
    raw = head.get("raw")
    if not raw:
        return None
    matches = CHAR_RE.findall(raw)
    return matches[0] if matches else None


def iter_phonetic_hints(candidate: dict[str, Any]) -> list[dict[str, str]]:
    hints: list[dict[str, str]] = []

    semantic_validation = candidate.get("wiktionary_semantic_validation") or {}
    phonetic_component = semantic_validation.get("phonetic_component")
    if phonetic_component:
        hints.append({"value": phonetic_component, "source": "wiktionary_semantic_validation"})

    wiktionary_validation = candidate.get("wiktionary_validation") or {}
    for han_compound in wiktionary_validation.get("han_compounds") or []:
        for component in han_compound.get("phonetic_components") or []:
            hints.append({"value": component, "source": "wiktionary_han_compound"})

    for row in candidate.get("shengfu_character_rows", []):
        if row.get("phonetic_component"):
            hints.append({"value": row["phonetic_component"], "source": "shengfu_phonetic_component"})
        if row.get("secondary_component"):
            hints.append({"value": row["secondary_component"], "source": "shengfu_secondary_component"})

    deduped: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for hint in hints:
        key = (hint["value"], hint["source"])
        if hint["value"] and key not in seen:
            seen.add(key)
            deduped.append(hint)
    return deduped


def assign_candidate_hierarchy(
    candidate: dict[str, Any],
    hierarchy_nodes: list[dict[str, Any]],
    top_level_head: str | None,
) -> dict[str, Any] | None:
    hints = iter_phonetic_hints(candidate)
    for hint in hints:
        for node in hierarchy_nodes:
            if hint["value"] and hint["value"] in node.get("key_characters", []):
                return {
                    "status": "assigned-to-node",
                    "parent_character": node.get("key_character"),
                    "parent_display_line": node.get("display_line"),
                    "parent_rhs_snippet": node.get("rhs_snippet"),
                    "source": hint["source"],
                    "phonetic_hint": hint["value"],
                }
        if top_level_head and hint["value"] == top_level_head:
            return {
                "status": "assigned-to-top-level",
                "parent_character": top_level_head,
                "parent_display_line": None,
                "parent_rhs_snippet": None,
                "source": hint["source"],
                "phonetic_hint": hint["value"],
            }
    return None
