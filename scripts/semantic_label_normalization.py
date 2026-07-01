from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


DEFAULT_CONFIG_PATH = Path("data/semantic_components/semantic_aliases.json")
DEFAULT_SUPPLEMENT_PATH = Path("data/semantic_components/semantic_label_supplement.json")
TEXTSUP_RE = re.compile(r"\\textsuperscript\{([^}]*)\}")
LATIN_WORD_RE = re.compile(r"[A-Za-z]+")
ASCII_LABEL_RE = re.compile(r"^[A-Za-z]+$")
ONLY_IN_RE = re.compile(r"^\((?:only in|in)\s+(.+?)\)$")
IGNORED_MACRO_TOKENS = {"includegraphics", "raisebox", "height", "ex"}


def load_normalization_config(path: Path | None = None) -> dict[str, Any]:
    config_path = path or DEFAULT_CONFIG_PATH
    data = json.loads(config_path.read_text(encoding="utf-8"))

    aliases = {alias.lower(): canonical.lower() for alias, canonical in data.get("aliases", {}).items()}

    blocked_aliases: dict[str, dict[str, Any]] = {}
    for alias, value in data.get("blocked_aliases", {}).items():
        if isinstance(value, dict):
            targets = [str(target).lower() for target in value.get("targets", [])]
            reason = value.get("reason")
        else:
            targets = [str(target).lower() for target in value]
            reason = None
        blocked_aliases[alias.lower()] = {
            "targets": targets,
            "reason": reason,
        }

    intentional_scoped_duplicates = []
    for item in data.get("intentional_scoped_duplicate_graphs", []):
        intentional_scoped_duplicates.append(
            {
                "graph": item["graph"],
                "abbreviation": item["abbreviation"].lower(),
                "only_in": list(item.get("only_in", [])),
                "paired_with": item.get("paired_with"),
                "note": item.get("note"),
            }
        )

    return {
        "path": str(config_path),
        "aliases": aliases,
        "blocked_aliases": blocked_aliases,
        "placeholder_labels": {label.lower() for label in data.get("placeholder_labels", ["xxx"])},
        "audit_watch_tokens": {label.lower() for label in data.get("audit_watch_tokens", [])},
        "intentional_scoped_duplicate_graphs": intentional_scoped_duplicates,
    }


def load_semantic_label_supplement(path: Path | None = None) -> dict[str, Any]:
    supplement_path = path or DEFAULT_SUPPLEMENT_PATH
    if not supplement_path.exists():
        return {"path": str(supplement_path), "items": []}

    data = json.loads(supplement_path.read_text(encoding="utf-8"))
    items = data.get("items") or []
    return {
        "path": str(supplement_path),
        "generated_at": data.get("generated_at"),
        "items": items,
    }


def normalize_superscript_label(content: str | None, *, preserve_non_ascii: bool = False) -> str | None:
    if not content or "\\" in content:
        return None
    stripped = content.strip().strip("·:˸").strip()
    if not stripped:
        return None
    if ASCII_LABEL_RE.fullmatch(stripped):
        lowered = stripped.lower()
        if lowered in IGNORED_MACRO_TOKENS:
            return None
        return lowered
    if preserve_non_ascii and (LATIN_WORD_RE.search(stripped) or any("\u4e00" <= character <= "\u9fff" for character in stripped)):
        return stripped
    return None


def iter_semantic_labels_from_text(text: str | None, *, preserve_non_ascii: bool = False) -> list[str]:
    if not text:
        return []
    labels: list[str] = []
    for content in TEXTSUP_RE.findall(text):
        label = normalize_superscript_label(content, preserve_non_ascii=preserve_non_ascii)
        if label is not None:
            labels.append(label)
    return labels


def extract_only_in_values(label_notes: str | None) -> list[str]:
    if not label_notes:
        return []
    match = ONLY_IN_RE.match(label_notes.strip())
    if match is None:
        return []
    return [value.strip() for value in re.split(r"[，,;/]", match.group(1)) if value.strip()]


def find_intentional_scoped_duplicate(
    *,
    graph: str | None,
    abbreviation: str | None,
    only_in: list[str],
    config: dict[str, Any],
) -> dict[str, Any] | None:
    if not graph or not abbreviation:
        return None
    normalized_only_in = sorted(only_in)
    for item in config.get("intentional_scoped_duplicate_graphs", []):
        if item["graph"] != graph:
            continue
        if item["abbreviation"] != abbreviation.lower():
            continue
        if sorted(item.get("only_in", [])) != normalized_only_in:
            continue
        return item
    return None


def normalize_inventory_metadata(
    *,
    graph: str | None,
    abbreviation: str | None,
    label_notes: str | None,
    config: dict[str, Any],
) -> dict[str, Any]:
    only_in = extract_only_in_values(label_notes)
    scope = "only_in" if only_in else "general"
    intentional_duplicate = find_intentional_scoped_duplicate(
        graph=graph,
        abbreviation=abbreviation,
        only_in=only_in,
        config=config,
    )
    return {
        "scope": scope,
        "only_in": only_in,
        "duplicate_graph_status": (
            "intentional_scoped_duplicate" if intentional_duplicate is not None else None
        ),
        "note": intentional_duplicate.get("note") if intentional_duplicate is not None else None,
    }


def build_canonical_index(items: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    index: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        abbreviation = (item.get("abbreviation") or "").lower()
        if not abbreviation:
            continue
        index.setdefault(abbreviation, []).append(item)
    return index


def classify_semantic_label(
    label: str | None,
    canonical_index: dict[str, list[dict[str, Any]]],
    config: dict[str, Any],
) -> dict[str, Any]:
    if label is None:
        return {"classification": "nonsemantic_markup_or_phonological_marker"}

    if not ASCII_LABEL_RE.fullmatch(label):
        return {"classification": "needs_review"}

    if label in canonical_index:
        return {
            "classification": "canonical",
            "canonical_abbreviation": label,
            "matched_items": canonical_index[label],
        }

    alias_target = config["aliases"].get(label)
    if alias_target is not None and alias_target in canonical_index:
        return {
            "classification": "explicit_alias",
            "canonical_abbreviation": alias_target,
            "matched_items": canonical_index[alias_target],
        }

    if label in config["placeholder_labels"]:
        return {"classification": "placeholder"}

    blocked = config["blocked_aliases"].get(label)
    if blocked is not None:
        return {
            "classification": "blocked_ambiguous_alias",
            "targets": blocked["targets"],
            "reason": blocked.get("reason"),
        }

    return {"classification": "missing_from_inventory"}


def expansion_words(text: str | None) -> set[str]:
    if not text:
        return set()
    normalized = re.sub(r"[^A-Za-z]+", " ", text.replace("(", "").replace(")", ""))
    return {word.lower() for word in normalized.split() if word}


def matches_old_heuristic(token: str, expanded_latin: str | None) -> bool:
    for word in expansion_words(expanded_latin):
        if word == token:
            return True
        if word.startswith(token):
            return True
    return False


def describe_semantic_item(item: dict[str, Any]) -> str:
    graph = item.get("graph_raw") or "—"
    abbreviation = item.get("abbreviation") or ""
    if abbreviation:
        return f"{graph}/{abbreviation}"
    return graph
