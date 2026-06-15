from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import hierarchy_utils
import inventory_tex
import mc_resolution
import resolve_series_roots


DEFAULT_TEX_ENTRIES = "data/current_tex_entries.json"
DEFAULT_SEMANTIC_INVENTORY = "data/current_semantic_components.json"
DEFAULT_SHENGFU = "data/derived/shengfu.csv"
DEFAULT_CURATION_DIR = "data/entries/curation"
DEFAULT_REPORT_OUT = "reports/semantic_evidence_reuse.md"
DEFAULT_IDS_PATH = "data/raw/cjkvi_ids.txt"

CHINESE_CHAR_RE = inventory_tex.CHINESE_CHAR_RE
BEGIN_END_RE = re.compile(r"^\\(begin|end)\{")
ITEM_RE = re.compile(r"^\\item\b")
PARAGRAPH_RE = re.compile(r"^\\paragraph\b")
TEXTSUP_RE = re.compile(r"\\textsuperscript\{([^}]*)\}")
TEXTSUP_CONTENT_RE = re.compile(r"(\\textsuperscript\{)([^}]*)(\})")
BINARY_IDS = {"⿰", "⿱", "⿴", "⿵", "⿶", "⿷", "⿸", "⿹", "⿺", "⿻"}
TRINARY_IDS = {"⿲", "⿳"}
IDS_NOTE_RE = re.compile(r"\[[^]]*\]")
IMAGE_CODEPOINT_RE = re.compile(r"U\+([0-9A-F]{4,6})\.png", re.IGNORECASE)
COMPONENT_ALIASES = {
    "王": "玉",
    "玨": "玉",
    "珡": "玉",
    "礻": "示",
    "衤": "衣",
    "忄": "心",
    "扌": "手",
    "氵": "水",
    "钅": "金",
    "釒": "金",
    "艹": "艸",
    "亻": "人",
    "𠦒": "网",
    "⺮": "竹",
    "飠": "食",
    "饣": "食",
    "訁": "言",
    "疒": "疒",
}
WIKTIONARY_CACHE_DIR = Path("data/raw/wiktionary")
GSR_BASE_RE = re.compile(r"^0*(\d+)([a-z]?(?:')?)?$", re.IGNORECASE)
SUPERSCRIPT_RELATION_COLON = "˸"


def dedupe_preserve(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def is_character_line(stripped: str) -> bool:
    if not stripped:
        return False
    if PARAGRAPH_RE.match(stripped) or BEGIN_END_RE.match(stripped) or ITEM_RE.match(stripped):
        return False
    if stripped.startswith("\\textit") or stripped.startswith("{\\large") or stripped.startswith("{{\\textsuperscript"):
        return False
    if "\\includegraphics" in stripped:
        return True
    return bool(CHINESE_CHAR_RE.search(stripped))


def parse_semantic_token(token: str | None, abbreviation_lookup: dict[str, list[dict[str, Any]]]) -> dict[str, Any] | None:
    if not token:
        return None
    stripped = token.strip()
    if stripped.startswith("·"):
        position = "suffix-dot"
    elif stripped.startswith(":"):
        position = "suffix-colon"
    elif stripped.endswith("·"):
        position = "prefix-dot"
    elif stripped.endswith(":"):
        position = "prefix-colon"
    else:
        position = "bare"
    abbreviation = stripped.strip("·:")
    return {
        "token": stripped,
        "abbreviation": abbreviation,
        "position": position,
        "inventory_matches": abbreviation_lookup.get(abbreviation, []),
    }


def parse_occurrence_block(
    *,
    entry_id: str,
    start_line_number: int,
    character_line: str,
    block_lines: list[str],
    inventory_lookup: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    joined = "\n".join(block_lines).strip()
    transliteration_lines = [
        line.strip()
        for line in block_lines[1:]
        if line.strip()
        and not line.strip().startswith("\\textit")
        and not BEGIN_END_RE.match(line.strip())
        and not ITEM_RE.match(line.strip())
    ]
    transliteration_latex = "\n".join(transliteration_lines).strip() or None
    semantic_token = None
    if transliteration_latex:
        match = TEXTSUP_RE.search(transliteration_latex)
        if match:
            semantic_token = match.group(1)

    mc_forms = []
    for line in block_lines:
        mc_forms.extend(inventory_tex.find_macro_arguments(line, "textit"))
    gsr_markers = []
    for line in block_lines:
        _, comment = inventory_tex.split_latex_comment(line)
        if comment:
            gsr_markers.extend(inventory_tex.GSR_RE.findall(comment))
    pinyins = []
    _, first_comment = inventory_tex.split_latex_comment(character_line)
    if first_comment:
        pinyins.extend(inventory_tex.PINYIN_RE.findall(first_comment))

    characters = CHINESE_CHAR_RE.findall(character_line)
    for image_name in inventory_tex.find_macro_arguments(character_line, "includegraphics", has_optional_arg=True):
        match = IMAGE_CODEPOINT_RE.search(image_name)
        if match:
            try:
                characters.append(chr(int(match.group(1), 16)))
            except Exception:
                pass
    characters = dedupe_preserve(characters)
    occurrences = []
    for character in characters:
        occurrences.append(
            {
                "character": character,
                "entry_id": entry_id,
                "source_line_number": start_line_number,
                "character_line_raw": character_line,
                "raw_block": joined,
                "transliteration_latex": transliteration_latex,
                "semantic_assignment": parse_semantic_token(semantic_token, inventory_lookup),
                "mc_forms": dedupe_preserve(mc_forms),
                "gsr_markers": dedupe_preserve(gsr_markers),
                "pinyins": dedupe_preserve(pinyins),
            }
        )
    return occurrences


def build_inventory_lookup(semantic_inventory: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    lookup: dict[str, list[dict[str, Any]]] = {}
    for item in semantic_inventory["items"]:
        abbreviation = item.get("abbreviation")
        if not abbreviation:
            continue
        lookup.setdefault(abbreviation, []).append(
            {
                "graph_raw": item.get("graph_raw"),
                "label_token": item.get("label_token"),
                "start_line": item.get("start_line"),
            }
        )
    return lookup


def build_inventory_graph_lookup(semantic_inventory: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    lookup: dict[str, list[dict[str, Any]]] = {}
    for item in semantic_inventory["items"]:
        graph_raw = item.get("graph_raw")
        if not graph_raw:
            continue
        lookup.setdefault(graph_raw, []).append(
            {
                "graph_raw": graph_raw,
                "label_token": item.get("label_token"),
                "abbreviation": item.get("abbreviation"),
                "start_line": item.get("start_line"),
            }
        )
    return lookup


def load_csv_records(path: Path) -> list[dict[str, Any]]:
    import pandas as pd

    frame = pd.read_csv(path, dtype=object).where(lambda table: table.notna(), None)
    return frame.to_dict("records")


def normalize_component_graph(component: str) -> str:
    return COMPONENT_ALIASES.get(component, component)


def split_gsr_base(value: str | None) -> tuple[int, str] | None:
    if not value:
        return None
    match = GSR_BASE_RE.match(str(value).strip())
    if not match:
        return None
    return int(match.group(1)), (match.group(2) or "").lower()


def load_ids_map(path: Path) -> dict[str, str]:
    ids_map: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        character = parts[1]
        ids = IDS_NOTE_RE.sub("", parts[2]).strip()
        ids_map[character] = ids
    return ids_map


def parse_ids_expression(ids: str, index: int = 0):
    token = ids[index]
    if token in BINARY_IDS:
        left, next_index = parse_ids_expression(ids, index + 1)
        right, final_index = parse_ids_expression(ids, next_index)
        return {"op": token, "children": [left, right]}, final_index
    if token in TRINARY_IDS:
        first, index1 = parse_ids_expression(ids, index + 1)
        second, index2 = parse_ids_expression(ids, index1)
        third, final_index = parse_ids_expression(ids, index2)
        return {"op": token, "children": [first, second, third]}, final_index
    if token == "&":
        end = ids.index(";", index)
        return ids[index : end + 1], end + 1
    return token, index + 1


def resolve_semantic_from_ids(
    *,
    character: str,
    phonetic_component: str | None,
    ids_map: dict[str, str],
    graph_lookup: dict[str, list[dict[str, Any]]],
) -> dict[str, Any] | None:
    if not phonetic_component:
        return None
    ids = ids_map.get(character)
    if not ids:
        return None
    try:
        tree, _ = parse_ids_expression(ids)
    except Exception:
        return None
    if not isinstance(tree, dict):
        return None
    children = tree["children"]
    if len(children) != 2:
        return None

    phonetic_norm = normalize_component_graph(phonetic_component)
    operator = tree["op"]

    def subtree_contains(node: Any, component: str, visited: set[str] | None = None) -> bool:
        visited = visited or set()
        if isinstance(node, str):
            normalized = normalize_component_graph(node)
            if normalized == component:
                return True
            if node in visited:
                return False
            nested_ids = ids_map.get(node)
            if nested_ids:
                try:
                    nested_tree, _ = parse_ids_expression(nested_ids)
                    if isinstance(nested_tree, dict):
                        visited.add(node)
                        return subtree_contains(nested_tree, component, visited)
                except Exception:
                    return False
            return False
        return any(subtree_contains(child, component, visited.copy()) for child in node.get("children", []))

    def subtree_head(node: Any) -> str | None:
        if isinstance(node, str):
            return normalize_component_graph(node)
        if node.get("children"):
            first_child = node["children"][0]
            if isinstance(first_child, str):
                return normalize_component_graph(first_child)
        return None

    left_matches = subtree_contains(children[0], phonetic_norm)
    right_matches = subtree_contains(children[1], phonetic_norm)

    semantic_component = None
    position = None
    if operator == "⿰":
        if right_matches and not left_matches:
            semantic_component = subtree_head(children[0])
            position = "prefix-dot"
        elif left_matches and not right_matches:
            semantic_component = subtree_head(children[1])
            position = "suffix-dot"
    elif operator == "⿱":
        if right_matches and not left_matches:
            semantic_component = subtree_head(children[0])
            position = "prefix-colon"
        elif left_matches and not right_matches:
            semantic_component = subtree_head(children[1])
            position = "suffix-colon"
    elif operator in {"⿸", "⿷", "⿺", "⿹"}:
        if right_matches and not left_matches:
            semantic_component = subtree_head(children[0])
            position = "prefix-dot"
    elif operator in {"⿵", "⿶"}:
        if right_matches and not left_matches:
            semantic_component = subtree_head(children[0])
            position = "prefix-colon"

    if semantic_component is None or position is None:
        return None

    inventory_matches = graph_lookup.get(semantic_component, [])
    resolved_abbreviation = inventory_matches[0].get("abbreviation") if inventory_matches else semantic_component

    return {
        "source": "ids_top_level" if inventory_matches else "ids_component_literal_fallback",
        "character": character,
        "ids": ids,
        "phonetic_component": phonetic_component,
        "semantic_component": semantic_component,
        "position": position,
        "abbreviation": resolved_abbreviation,
        "inventory_matches": inventory_matches,
    }


def resolve_semantic_from_wiktionary_template(
    *,
    character: str,
    han_compound: dict[str, Any],
    ids_map: dict[str, str],
    graph_lookup: dict[str, list[dict[str, Any]]],
) -> dict[str, Any] | None:
    semantic_components = han_compound.get("semantic_components") or []
    phonetic_components = han_compound.get("phonetic_components") or []
    positional = han_compound.get("positional_components") or []
    if not semantic_components and len(phonetic_components) == 1 and len(positional) == 2:
        other = [component for component in positional if normalize_component_graph(component) != normalize_component_graph(phonetic_components[0])]
        if len(other) == 1:
            semantic_components = [other[0]]
    if not phonetic_components and len(semantic_components) == 1 and len(positional) == 2:
        other = [component for component in positional if normalize_component_graph(component) != normalize_component_graph(semantic_components[0])]
        if len(other) == 1:
            phonetic_components = [other[0]]
    if len(semantic_components) != 1 or len(phonetic_components) != 1:
        return None

    semantic_component = normalize_component_graph(semantic_components[0])
    phonetic_component = normalize_component_graph(phonetic_components[0])
    semantic_index = None
    phonetic_index = None
    for index, component in enumerate(positional):
        normalized = normalize_component_graph(component)
        if semantic_index is None and normalized == semantic_component:
            semantic_index = index
        if phonetic_index is None and normalized == phonetic_component:
            phonetic_index = index

    ids = ids_map.get(character)
    operator = None
    if ids:
        try:
            tree, _ = parse_ids_expression(ids)
            if isinstance(tree, dict):
                operator = tree["op"]
        except Exception:
            operator = None

    position = None
    if semantic_index is not None and phonetic_index is not None and operator:
        if operator == "⿰":
            position = "prefix-dot" if semantic_index < phonetic_index else "suffix-dot"
        elif operator == "⿱":
            position = "prefix-colon" if semantic_index < phonetic_index else "suffix-colon"
        elif operator == "⿲":
            position = "prefix-dot" if semantic_index < phonetic_index else "suffix-dot"
        elif operator == "⿳":
            position = "prefix-colon" if semantic_index < phonetic_index else "suffix-colon"
        elif operator in {"⿸", "⿷", "⿺", "⿹"}:
            position = "prefix-dot" if semantic_index < phonetic_index else "suffix-dot"
        elif operator in {"⿵", "⿶"}:
            position = "prefix-colon" if semantic_index < phonetic_index else "suffix-colon"

    if position is None and semantic_index is not None and phonetic_index is not None:
        named_args = han_compound.get("named_args") or {}
        if named_args.get("c1") == "s" and named_args.get("c2") == "p":
            position = "prefix-dot" if semantic_index < phonetic_index else "suffix-dot"
        elif named_args.get("c1") == "p" and named_args.get("c2") == "s":
            position = "suffix-dot" if semantic_index > phonetic_index else "prefix-dot"

    inventory_matches = graph_lookup.get(semantic_component, [])
    abbreviation = inventory_matches[0].get("abbreviation") if inventory_matches else semantic_component
    if not position:
        return None

    return {
        "source": "wiktionary_han_compound" if inventory_matches else "wiktionary_component_literal_fallback",
        "character": character,
        "semantic_component": semantic_component,
        "phonetic_component": phonetic_component,
        "position": position,
        "abbreviation": abbreviation,
        "inventory_matches": inventory_matches,
        "template_raw": han_compound.get("template_raw"),
    }


def load_wiktionary_wikitext_from_cache(character: str) -> str | None:
    cache_path = WIKTIONARY_CACHE_DIR / f"{ord(character):05X}.json"
    if not cache_path.exists():
        return None
    payload = json.loads(cache_path.read_text(encoding="utf-8"))
    return payload.get("wikitext")


def resolve_historical_wiktionary_note(
    character: str,
    ids_map: dict[str, str],
    graph_lookup: dict[str, list[dict[str, Any]]],
) -> dict[str, Any] | None:
    wikitext = load_wiktionary_wikitext_from_cache(character)
    if not wikitext:
        return None

    if character == "禽" and "{{zh-l|*𠦒}}" in wikitext and "phonetic component {{och-l|今}} was added" in wikitext:
        semantic_component = normalize_component_graph("𠦒")
        inventory_matches = graph_lookup.get(semantic_component, [])
        abbreviation = inventory_matches[0].get("abbreviation") if inventory_matches else semantic_component
        return {
            "source": "wiktionary_historical_stage",
            "character": character,
            "semantic_component": semantic_component,
            "phonetic_component": "今",
            "position": "suffix-colon",
            "abbreviation": abbreviation,
            "inventory_matches": inventory_matches,
        }
    return None


def resolve_semantic_from_packet_family(
    *,
    character: str,
    ids_map: dict[str, str],
    graph_lookup: dict[str, list[dict[str, Any]]],
    packet_family: set[str],
) -> dict[str, Any] | None:
    ids = ids_map.get(character)
    if not ids:
        return None
    try:
        tree, _ = parse_ids_expression(ids)
    except Exception:
        return None
    if not isinstance(tree, dict) or len(tree.get("children", [])) != 2:
        return None

    def subtree_has_packet_component(node: Any) -> bool:
        if isinstance(node, str):
            normalized = normalize_component_graph(node)
            if normalized in packet_family:
                return True
            nested_ids = ids_map.get(node)
            if nested_ids:
                try:
                    nested_tree, _ = parse_ids_expression(nested_ids)
                    if isinstance(nested_tree, dict):
                        return subtree_has_packet_component(nested_tree)
                except Exception:
                    return False
            return False
        return any(subtree_has_packet_component(child) for child in node.get("children", []))

    def subtree_head(node: Any) -> str | None:
        if isinstance(node, str):
            return normalize_component_graph(node)
        if node.get("children"):
            first = node["children"][0]
            if isinstance(first, str):
                return normalize_component_graph(first)
        return None

    left = tree["children"][0]
    right = tree["children"][1]
    left_match = subtree_has_packet_component(left)
    right_match = subtree_has_packet_component(right)
    if left_match == right_match:
        return None

    semantic_component = subtree_head(right if left_match else left)
    inventory_matches = graph_lookup.get(semantic_component, [])
    abbreviation = inventory_matches[0].get("abbreviation") if inventory_matches else semantic_component

    operator = tree["op"]
    if operator == "⿰":
        position = "suffix-dot" if left_match else "prefix-dot"
    elif operator == "⿱":
        position = "suffix-colon" if left_match else "prefix-colon"
    elif operator in {"⿸", "⿷", "⿺", "⿹"}:
        position = "suffix-dot" if left_match else "prefix-dot"
    elif operator in {"⿵", "⿶"}:
        position = "suffix-colon" if left_match else "prefix-colon"
    else:
        return None

    return {
        "source": "packet_family_ids" if inventory_matches else "packet_family_component_literal_fallback",
        "character": character,
        "ids": ids,
        "semantic_component": semantic_component,
        "position": position,
        "abbreviation": abbreviation,
        "inventory_matches": inventory_matches,
    }


def merge_graph_lookups(*lookups: dict[str, list[dict[str, Any]]]) -> dict[str, list[dict[str, Any]]]:
    merged: dict[str, list[dict[str, Any]]] = {}
    for lookup in lookups:
        for graph, values in lookup.items():
            merged.setdefault(graph, [])
            merged[graph].extend(values)
    return merged


def build_learned_graph_lookup(
    evidence: dict[str, list[dict[str, Any]]],
    shengfu_rows: list[dict[str, Any]],
    ids_map: dict[str, str],
) -> dict[str, list[dict[str, Any]]]:
    shengfu_by_character: dict[str, list[dict[str, Any]]] = {}
    for row in shengfu_rows:
        character = row.get("normalized_character")
        if not character:
            continue
        shengfu_by_character.setdefault(character, []).append(row)

    component_counts: dict[str, dict[str, int]] = {}
    for character, occurrences in evidence.items():
        shengfu_char_rows = shengfu_by_character.get(character, [])
        if not shengfu_char_rows:
            continue
        phonetic_component = shengfu_char_rows[0].get("normalized_phonetic_component")
        if not phonetic_component:
            continue
        resolved = resolve_semantic_from_ids(
            character=character,
            phonetic_component=phonetic_component,
            ids_map=ids_map,
            graph_lookup={},
        )
        if not resolved or not resolved.get("semantic_component"):
            continue
        semantic_component = resolved["semantic_component"]
        for occurrence in occurrences:
            semantic_assignment = occurrence.get("semantic_assignment")
            if not semantic_assignment or not semantic_assignment.get("abbreviation"):
                continue
            abbreviation = semantic_assignment["abbreviation"]
            component_counts.setdefault(semantic_component, {})
            component_counts[semantic_component][abbreviation] = (
                component_counts[semantic_component].get(abbreviation, 0) + 1
            )

    learned_lookup: dict[str, list[dict[str, Any]]] = {}
    for graph, counts in component_counts.items():
        sorted_counts = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
        if not sorted_counts:
            continue
        abbreviation, count = sorted_counts[0]
        if len(sorted_counts) > 1 and count <= sorted_counts[1][1]:
            continue
        learned_lookup[graph] = [
            {
                "graph_raw": graph,
                "label_token": abbreviation,
                "abbreviation": abbreviation,
                "learned": True,
                "evidence_count": count,
            }
        ]
    return learned_lookup


def build_tex_character_evidence(
    tex_entries: list[dict[str, Any]],
    semantic_inventory: dict[str, Any],
) -> dict[str, list[dict[str, Any]]]:
    inventory_lookup = build_inventory_lookup(semantic_inventory)
    evidence: dict[str, list[dict[str, Any]]] = {}

    for entry in tex_entries:
        head_root = extract_series_root_latex(entry["raw_block"])
        for head_character in entry.get("head", {}).get("characters", []):
            evidence.setdefault(head_character, []).append(
                {
                    "character": head_character,
                    "entry_id": entry["id"],
                    "source_line_number": entry["start_line"],
                    "character_line_raw": entry["paragraph_line_raw"],
                    "raw_block": entry["raw_block"],
                    "transliteration_latex": head_root,
                    "semantic_assignment": None,
                    "mc_forms": entry.get("mc_forms", []),
                    "gsr_markers": entry.get("gsr_markers", []),
                    "pinyins": entry.get("commented_pinyin", []),
                    "is_head_occurrence": True,
                }
            )

        lines = entry["raw_block"].splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            if not is_character_line(stripped):
                i += 1
                continue

            block_lines = [line]
            j = i + 1
            while j < len(lines):
                next_line = lines[j]
                next_stripped = next_line.strip()
                if is_character_line(next_stripped):
                    break
                if PARAGRAPH_RE.match(next_stripped):
                    break
                block_lines.append(next_line)
                j += 1

            occurrences = parse_occurrence_block(
                entry_id=entry["id"],
                start_line_number=entry["start_line"] + i,
                character_line=line,
                block_lines=block_lines,
                inventory_lookup=inventory_lookup,
            )
            for occurrence in occurrences:
                evidence.setdefault(occurrence["character"], []).append(occurrence)
            i = j

    return evidence


def unique_non_null(values: list[Any]) -> list[Any]:
    result: list[Any] = []
    seen: set[str] = set()
    for value in values:
        if value in (None, "", []):
            continue
        key = json.dumps(value, ensure_ascii=False, sort_keys=True)
        if key not in seen:
            seen.add(key)
            result.append(value)
    return result


def normalize_transliteration_latex(value: str | None) -> str | None:
    if not value:
        return None
    lines = []
    for raw_line in value.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("%"):
            continue
        lines.append(stripped)
    normalized = "\n".join(lines) if lines else None
    return normalize_superscript_relation_punctuation(normalized)


def normalize_superscript_relation_punctuation(value: str | None) -> str | None:
    if not value:
        return value

    def replace(match: re.Match[str]) -> str:
        content = match.group(2).replace(":", SUPERSCRIPT_RELATION_COLON)
        return match.group(1) + content + match.group(3)

    return TEXTSUP_CONTENT_RE.sub(replace, value)


def strip_visible_mc_warning(render_latex: str | None) -> str | None:
    if not render_latex:
        return None
    lines = [
        line.rstrip()
        for line in render_latex.splitlines()
        if line.strip() and "[MC disagreement among imported sources]" not in line
    ]
    return normalize_superscript_relation_punctuation("\n".join(lines) if lines else None)


def disambiguate_occurrences(candidate: dict[str, Any], matches: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if len(matches) <= 1:
        return matches
    candidate_gsr = {
        row["gsr"] for row in candidate.get("mand2mc_rows", []) if row.get("gsr")
    } | {
        row["gsr"] for row in candidate.get("bs_gsr_rows", []) if row.get("gsr")
    }
    if candidate_gsr:
        exact = [match for match in matches if set(match.get("gsr_markers", [])) & candidate_gsr]
        if exact:
            return exact
        no_gsr = [match for match in matches if not match.get("gsr_markers")]
        mismatched = [
            match for match in matches if match.get("gsr_markers") and not (set(match.get("gsr_markers", [])) & candidate_gsr)
        ]
        if no_gsr and mismatched:
            return no_gsr

    candidate_mc = {
        row["mc_nwh"] for row in candidate.get("mand2mc_rows", []) if row.get("mc_nwh")
    } | {
        row["mc_bs"] for row in candidate.get("bs_gsr_rows", []) if row.get("mc_bs")
    }
    if candidate_mc:
        mc_matches = [match for match in matches if set(match.get("mc_forms", [])) & candidate_mc]
        if mc_matches:
            return mc_matches

    candidate_pinyin = {
        row["pinyin"] for row in candidate.get("mand2mc_rows", []) if row.get("pinyin")
    } | {
        row["pinyin"] for row in candidate.get("bs_gsr_rows", []) if row.get("pinyin")
    }
    if candidate_pinyin:
        pinyin_matches = [match for match in matches if set(match.get("pinyins", [])) & candidate_pinyin]
        if pinyin_matches:
            return pinyin_matches

    return matches


def maybe_mark_base_graph(candidate: dict[str, Any], ids_map: dict[str, str]) -> dict[str, Any] | None:
    if any(match.get("is_head_occurrence") for match in candidate.get("tex_occurrence_candidates", [])):
        return {
            "token": None,
            "abbreviation": None,
            "position": "none",
            "inventory_matches": [],
            "source": "existing_tex_head",
            "semantic_component": None,
        }

    for row in candidate.get("shengfu_character_rows", []):
        if normalize_component_graph(row.get("phonetic_component", "")) == normalize_component_graph(candidate["character"]):
            return {
                "token": None,
                "abbreviation": None,
                "position": "none",
                "inventory_matches": [],
                "source": "self_phonetic_base",
                "semantic_component": None,
            }

    ids = ids_map.get(candidate["character"])
    if ids and len(ids) == 1 and ids == candidate["character"]:
        return {
            "token": None,
            "abbreviation": None,
            "position": "none",
            "inventory_matches": [],
            "source": "simple_graph",
            "semantic_component": None,
        }
    return None


def maybe_mark_series_head(entry: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any] | None:
    if entry.get("packet_kind") != "missing_series":
        return None
    header_tokens = {
        int(token)
        for token in entry.get("schuessler", {}).get("k_tokens", [])
        if str(token).isdigit()
    }
    if not header_tokens:
        return None
    for row in candidate.get("mand2mc_rows", []) + candidate.get("bs_gsr_rows", []):
        parsed = split_gsr_base(row.get("gsr"))
        if parsed is None:
            continue
        digits, suffix = parsed
        if digits in header_tokens and suffix in {"", "a"}:
            return {
                "token": None,
                "abbreviation": None,
                "position": "none",
                "inventory_matches": [],
                "source": "schuessler_series_head",
                "semantic_component": None,
            }
    return None


def extract_series_root_latex(raw_block: str) -> str | None:
    for line in raw_block.splitlines()[1:]:
        stripped = line.strip()
        if not stripped.startswith("{\\large") and not stripped.startswith("{\\Large"):
            continue
        try:
            outer_content, _ = inventory_tex.parse_braced(stripped, 0)
        except Exception:
            continue
        if not (outer_content.startswith(r"\large") or outer_content.startswith(r"\Large")):
            continue
        brace_index = outer_content.find("{")
        if brace_index == -1:
            continue
        try:
            root, _ = inventory_tex.parse_braced(outer_content, brace_index)
            return root
        except Exception:
            continue
    return None


def compose_transliteration_from_root(root: str, semantic_assignment: dict[str, Any]) -> str | None:
    abbreviation = semantic_assignment.get("abbreviation")
    position = semantic_assignment.get("position")
    if not abbreviation or not position:
        return None
    if position == "prefix-dot":
        return rf"{{\large{{\textsuperscript{{{abbreviation}·}}{root}}}}},"
    if position == "prefix-colon":
        return rf"{{\large{{\textsuperscript{{{abbreviation}{SUPERSCRIPT_RELATION_COLON}}}{root}}}}},"
    if position == "suffix-dot":
        return rf"{{\large{{{root}\textsuperscript{{·{abbreviation}}}}}}},"
    if position == "suffix-colon":
        return rf"{{\large{{{root}\textsuperscript{{{SUPERSCRIPT_RELATION_COLON}{abbreviation}}}}}}},"
    return None


def derive_missing_series_transliteration(entry: dict[str, Any], candidate: dict[str, Any]) -> str | None:
    resolved_root = (entry.get("resolved_series_root") or {}).get("root")
    if not resolved_root:
        return candidate.get("transliteration_latex")
    semantic_assignment = candidate.get("semantic_assignment") or {}
    if semantic_assignment.get("position") == "none":
        return rf"{{\large{{{resolved_root}}}}},"
    return compose_transliteration_from_root(resolved_root, semantic_assignment)


def derive_transliteration_from_resolved_root(root: str | None, candidate: dict[str, Any]) -> str | None:
    if not root:
        return candidate.get("transliteration_latex")
    semantic_assignment = candidate.get("semantic_assignment") or {}
    if semantic_assignment.get("position") == "none":
        return rf"{{\large{{{root}}}}},"
    return compose_transliteration_from_root(root, semantic_assignment)


def derive_candidate_oc_roots(candidate: dict[str, Any], *, mode: str) -> list[str]:
    roots: list[str] = []
    for row in candidate.get("bs_gsr_rows", []):
        root = resolve_series_roots.derive_oc_root(row.get("oc_bs"), mode=mode)
        if root:
            roots.append(root)
    for row in candidate.get("shengfu_character_rows", []):
        oc_syllable = row.get("oc_syllable")
        if oc_syllable:
            root = resolve_series_roots.derive_oc_root(f"*{oc_syllable}", mode=mode)
            if root:
                roots.append(root)
    return dedupe_preserve(roots)


def resolve_generated_node_root(
    candidate: dict[str, Any],
    candidate_children: dict[str, list[dict[str, Any]]],
    candidate_map: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    descendant_characters = hierarchy_utils.collect_descendant_characters(candidate["character"], candidate_children)
    relevant_candidates = [candidate] + [
        candidate_map[character]
        for character in descendant_characters
        if character in candidate_map
    ]
    roots = dedupe_preserve(
        root
        for item in relevant_candidates
        for root in derive_candidate_oc_roots(item, mode="node")
        if root
    )
    head_roots = derive_candidate_oc_roots(candidate, mode="node")
    resolved_root = None
    source = None
    if len(roots) == 1:
        resolved_root = roots[0]
        source = "node_oc_consensus"
    elif head_roots:
        resolved_root = sorted(head_roots, key=len, reverse=True)[0]
        source = "node_head_oc"
    else:
        fallback = hierarchy_utils.extract_large_content(candidate.get("transliteration_latex"))
        if fallback:
            resolved_root = re.sub(TEXTSUP_RE, "", fallback).replace("{", "").replace("}", "")
            source = "node_transliteration_fallback"
    if not resolved_root:
        return None
    return {
        "root": resolved_root,
        "source": source,
        "descendant_count": len(descendant_characters),
    }


def resolve_parent_root_for_candidate(
    entry: dict[str, Any],
    candidate: dict[str, Any],
    candidate_map: dict[str, dict[str, Any]],
) -> str | None:
    assignment = candidate.get("hierarchy_assignment") or {}
    status = assignment.get("status")
    if status == "assigned-to-inherited-node":
        return hierarchy_utils.extract_large_content(assignment.get("parent_rhs_snippet"))
    if status == "assigned-to-candidate-node":
        parent = candidate_map.get(assignment.get("parent_character"))
        if parent:
            node_root = (parent.get("resolved_node_root") or {}).get("root")
            if node_root:
                return node_root
    if entry.get("packet_kind") == "missing_series":
        return (entry.get("resolved_series_root") or {}).get("root")
    if entry.get("tex_entry") is not None:
        return extract_series_root_latex(entry["tex_entry"]["raw_block"])
    return None


def synthesize_render_latex(candidate: dict[str, Any]) -> str | None:
    transliteration_latex = normalize_transliteration_latex(candidate.get("transliteration_latex"))
    if not transliteration_latex:
        return None

    first_line = candidate["character"]
    pinyins = dedupe_preserve(
        [row["pinyin"] for row in candidate.get("mand2mc_rows", []) if row.get("pinyin")]
        + [row["pinyin"] for row in candidate.get("bs_gsr_rows", []) if row.get("pinyin")]
    )
    if pinyins:
        first_line += "\t%" + " / ".join(pinyins)

    gsr_values = dedupe_preserve(
        [row["gsr"] for row in candidate.get("mand2mc_rows", []) if row.get("gsr")]
        + [row["gsr"] for row in candidate.get("bs_gsr_rows", []) if row.get("gsr")]
    )
    resolution = candidate.get("mc_resolution") or mc_resolution.resolve_candidate_mc(candidate)
    mc_forms = resolution["display_forms"]

    lines = [first_line]
    lines.extend(transliteration_latex.splitlines())
    for index, mc_form in enumerate(mc_forms):
        suffix = ""
        if index == 0 and gsr_values:
            suffix = "\t%" + ", ".join(gsr_values)
        lines.append(f"\\textit{{{mc_form}}};{suffix}")
    return "\n".join(lines)


def enrich_curated_entry(entry: dict[str, Any], evidence: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    raise RuntimeError("Use enrich_curated_entry_with_ids instead.")


def enrich_curated_entry_with_ids(
    entry: dict[str, Any],
    evidence: dict[str, list[dict[str, Any]]],
    ids_map: dict[str, str],
    graph_lookup: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    packet_family = {
        normalize_component_graph(candidate["character"])
        for candidate in entry.get("proposed_additions", [])
    }
    if entry.get("tex_entry") is not None and entry.get("entry_hierarchy") is None:
        entry["entry_hierarchy"] = {
            "top_level_head": hierarchy_utils.extract_head_character(entry["tex_entry"].get("head")),
            "nodes": hierarchy_utils.extract_hierarchy_nodes(entry["tex_entry"]["raw_block"]),
        }
    if entry.get("tex_entry"):
        packet_family.update(
            normalize_component_graph(ch) for ch in entry["tex_entry"].get("chinese_characters", [])
        )
    for candidate in entry.get("proposed_additions", []):
        candidate["mc_resolution"] = mc_resolution.resolve_candidate_mc(candidate)
        matches = disambiguate_occurrences(candidate, evidence.get(candidate["character"], []))
        candidate["tex_occurrence_candidates"] = matches

        semantic_assignments = unique_non_null(
            [match.get("semantic_assignment") for match in matches if match.get("semantic_assignment")]
        )
        transliterations = unique_non_null(
            [match.get("transliteration_latex") for match in matches if match.get("transliteration_latex")]
        )
        render_candidates = unique_non_null(
            [match.get("raw_block") for match in matches if match.get("raw_block")]
        )

        if len(semantic_assignments) == 1:
            candidate["semantic_assignment"] = semantic_assignments[0]
        if len(transliterations) == 1:
            candidate["transliteration_latex"] = transliterations[0]
        if len(render_candidates) == 1:
            candidate["render_latex"] = render_candidates[0]

        phonetic_component = None
        if candidate.get("shengfu_character_rows"):
            phonetic_component = candidate["shengfu_character_rows"][0].get("phonetic_component")
        candidate["semantic_candidates_from_ids"] = []
        ids_candidate = resolve_semantic_from_ids(
            character=candidate["character"],
            phonetic_component=phonetic_component,
            ids_map=ids_map,
            graph_lookup=graph_lookup,
        )
        if ids_candidate is not None:
            candidate["semantic_candidates_from_ids"].append(ids_candidate)
            if candidate.get("semantic_assignment") is None and ids_candidate.get("abbreviation"):
                candidate["semantic_assignment"] = {
                    "token": None,
                    "abbreviation": ids_candidate["abbreviation"],
                    "position": ids_candidate["position"],
                    "inventory_matches": ids_candidate["inventory_matches"],
                    "source": ids_candidate["source"],
                    "semantic_component": ids_candidate["semantic_component"],
                }

        if candidate.get("transliteration_latex") is None and entry.get("tex_entry") is not None and candidate.get("semantic_assignment"):
            root = extract_series_root_latex(entry["tex_entry"]["raw_block"])
            if root:
                candidate["transliteration_latex"] = compose_transliteration_from_root(
                    root,
                    candidate["semantic_assignment"],
                )
        if candidate.get("transliteration_latex") is None and entry.get("packet_kind") == "missing_series" and candidate.get("semantic_assignment"):
            resolved_root = (entry.get("resolved_series_root") or {}).get("root")
            if resolved_root:
                candidate["transliteration_latex"] = compose_transliteration_from_root(
                    resolved_root,
                    candidate["semantic_assignment"],
                )

        if candidate.get("semantic_assignment") is None:
            packet_candidate = resolve_semantic_from_packet_family(
                character=candidate["character"],
                ids_map=ids_map,
                graph_lookup=graph_lookup,
                packet_family=packet_family - {normalize_component_graph(candidate["character"])},
            )
            if packet_candidate and packet_candidate.get("abbreviation"):
                candidate["semantic_assignment"] = {
                    "token": None,
                    "abbreviation": packet_candidate["abbreviation"],
                    "position": packet_candidate["position"],
                    "inventory_matches": packet_candidate["inventory_matches"],
                    "source": packet_candidate["source"],
                    "semantic_component": packet_candidate["semantic_component"],
                }
                if candidate.get("transliteration_latex") is None and entry.get("tex_entry") is not None:
                    root = extract_series_root_latex(entry["tex_entry"]["raw_block"])
                    if root:
                        candidate["transliteration_latex"] = compose_transliteration_from_root(
                            root,
                            candidate["semantic_assignment"],
                        )
                if candidate.get("transliteration_latex") is None and entry.get("packet_kind") == "missing_series":
                    resolved_root = (entry.get("resolved_series_root") or {}).get("root")
                    if resolved_root:
                        candidate["transliteration_latex"] = compose_transliteration_from_root(
                            resolved_root,
                            candidate["semantic_assignment"],
                        )
        if candidate.get("semantic_assignment") is None:
            base_graph = maybe_mark_base_graph(candidate, ids_map)
            if base_graph is not None:
                candidate["semantic_assignment"] = base_graph
        candidate["transliteration_latex"] = normalize_transliteration_latex(candidate.get("transliteration_latex"))
        candidate["render_latex"] = strip_visible_mc_warning(candidate.get("render_latex"))
        if candidate.get("render_latex") is None:
            candidate["render_latex"] = synthesize_render_latex(candidate)

        han_templates = (candidate.get("wiktionary_validation") or {}).get("han_compounds") or []
        explicit_candidate = None
        for han_compound in han_templates:
            if han_compound.get("semantic_components") or han_compound.get("phonetic_components"):
                explicit_candidate = resolve_semantic_from_wiktionary_template(
                    character=candidate["character"],
                    han_compound=han_compound,
                    ids_map=ids_map,
                    graph_lookup=graph_lookup,
                )
                if explicit_candidate:
                    break
        candidate["wiktionary_semantic_validation"] = None
        if explicit_candidate:
            candidate["wiktionary_semantic_validation"] = {
                "semantic_component": explicit_candidate["semantic_component"],
                "phonetic_component": explicit_candidate["phonetic_component"],
                "resolved_assignment": explicit_candidate,
            }
            candidate["semantic_assignment"] = {
                "token": None,
                "abbreviation": explicit_candidate["abbreviation"],
                "position": explicit_candidate["position"],
                "inventory_matches": explicit_candidate["inventory_matches"],
                "source": explicit_candidate["source"],
                "semantic_component": explicit_candidate["semantic_component"],
            }
            if candidate.get("transliteration_latex") is None and entry.get("tex_entry") is not None:
                root = extract_series_root_latex(entry["tex_entry"]["raw_block"])
                if root:
                    candidate["transliteration_latex"] = compose_transliteration_from_root(
                        root,
                        candidate["semantic_assignment"],
                    )
            if candidate.get("transliteration_latex") is None and entry.get("packet_kind") == "missing_series":
                resolved_root = (entry.get("resolved_series_root") or {}).get("root")
                if resolved_root:
                    candidate["transliteration_latex"] = compose_transliteration_from_root(
                        resolved_root,
                        candidate["semantic_assignment"],
                    )
        elif candidate.get("semantic_assignment") is None:
            historical_candidate = resolve_historical_wiktionary_note(
                candidate["character"], ids_map, graph_lookup
            )
            if historical_candidate is not None:
                candidate["semantic_assignment"] = {
                    "token": None,
                    "abbreviation": historical_candidate["abbreviation"],
                    "position": historical_candidate["position"],
                    "inventory_matches": historical_candidate["inventory_matches"],
                    "source": historical_candidate["source"],
                    "semantic_component": historical_candidate["semantic_component"],
                }
                if candidate.get("transliteration_latex") is None and entry.get("tex_entry") is not None:
                    root = extract_series_root_latex(entry["tex_entry"]["raw_block"])
                    if root:
                        candidate["transliteration_latex"] = compose_transliteration_from_root(
                            root,
                            candidate["semantic_assignment"],
                        )
                if candidate.get("transliteration_latex") is None and entry.get("packet_kind") == "missing_series":
                    resolved_root = (entry.get("resolved_series_root") or {}).get("root")
                    if resolved_root:
                        candidate["transliteration_latex"] = compose_transliteration_from_root(
                            resolved_root,
                            candidate["semantic_assignment"],
                        )
        if candidate.get("semantic_assignment") is None:
            series_head = maybe_mark_series_head(entry, candidate)
            if series_head is not None:
                candidate["semantic_assignment"] = series_head
        if entry.get("packet_kind") == "missing_series":
            candidate["transliteration_latex"] = derive_missing_series_transliteration(entry, candidate)
            candidate["render_latex"] = synthesize_render_latex(candidate)
        candidate["hierarchy_assignment"] = None
    hierarchy = entry.get("entry_hierarchy") or {}
    hierarchy_nodes = hierarchy.get("nodes") or []
    top_level_head = hierarchy.get("top_level_head")
    if top_level_head is None and entry.get("packet_kind") == "missing_series" and entry.get("proposed_additions"):
        top_level_head = entry["proposed_additions"][0]["character"]
    candidate_characters = {candidate["character"] for candidate in entry.get("proposed_additions", [])}
    for candidate in entry.get("proposed_additions", []):
        if hierarchy_nodes:
            candidate["hierarchy_assignment"] = hierarchy_utils.assign_candidate_to_inherited_hierarchy(
                candidate,
                hierarchy_nodes,
                top_level_head,
            )
        if candidate.get("hierarchy_assignment") is None:
            candidate["hierarchy_assignment"] = hierarchy_utils.assign_candidate_to_candidate(
                candidate,
                candidate_characters,
                top_level_head,
            )
    candidate_children = hierarchy_utils.collect_candidate_children(entry)
    candidate_map = {candidate["character"]: candidate for candidate in entry.get("proposed_additions", [])}
    for candidate in entry.get("proposed_additions", []):
        if candidate.get("semantic_assignment") is None and candidate_children.get(candidate["character"]):
            candidate["semantic_assignment"] = {
                "token": None,
                "abbreviation": None,
                "position": "none",
                "inventory_matches": [],
                "source": "generated_subseries_head",
                "semantic_component": None,
            }
    for candidate in entry.get("proposed_additions", []):
        if candidate_children.get(candidate["character"]):
            candidate["resolved_node_root"] = resolve_generated_node_root(
                candidate,
                candidate_children,
                candidate_map,
            )
        else:
            candidate["resolved_node_root"] = None
    for candidate in entry.get("proposed_additions", []):
        parent_root = resolve_parent_root_for_candidate(entry, candidate, candidate_map)
        if parent_root:
            candidate["transliteration_latex"] = derive_transliteration_from_resolved_root(parent_root, candidate)
            candidate["render_latex"] = synthesize_render_latex(candidate)
    return entry


def write_curated_entry(entry: dict[str, Any], path: Path) -> None:
    path.write_text(json.dumps(entry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def render_report(entries: list[dict[str, Any]]) -> str:
    total_candidates = sum(len(entry.get("proposed_additions", [])) for entry in entries)
    semantic_ready = sum(
        1 for entry in entries for candidate in entry.get("proposed_additions", []) if candidate.get("semantic_assignment")
    )
    transliteration_ready = sum(
        1 for entry in entries for candidate in entry.get("proposed_additions", []) if candidate.get("transliteration_latex")
    )
    render_ready = sum(
        1 for entry in entries for candidate in entry.get("proposed_additions", []) if candidate.get("render_latex")
    )

    lines = [
        "# Semantic evidence reuse",
        "",
        f"- Curated entries inspected: {len(entries)}",
        f"- Proposed additions inspected: {total_candidates}",
        f"- Additions with reusable semantic assignment from existing TeX: {semantic_ready}",
        f"- Additions with reusable transliteration LaTeX from existing TeX: {transliteration_ready}",
        f"- Additions with reusable render block from existing TeX: {render_ready}",
        f"- Additions with IDS-derived semantic candidates: {sum(1 for entry in entries for c in entry.get('proposed_additions', []) if c.get('semantic_candidates_from_ids'))}",
        f"- Additions with explicit Wiktionary Han-compound support: {sum(1 for entry in entries for c in entry.get('proposed_additions', []) if c.get('wiktionary_semantic_validation'))}",
        f"- Additions assigned to inherited hierarchy nodes: {sum(1 for entry in entries for c in entry.get('proposed_additions', []) if (c.get('hierarchy_assignment') or {}).get('status') == 'assigned-to-inherited-node')}",
        f"- Additions assigned under generated candidate nodes: {sum(1 for entry in entries for c in entry.get('proposed_additions', []) if (c.get('hierarchy_assignment') or {}).get('status') == 'assigned-to-candidate-node')}",
        f"- Additions requiring MC investigation because BS/GSR has a reading absent from Mand2MC: {sum(1 for entry in entries for c in entry.get('proposed_additions', []) if (c.get('mc_resolution') or {}).get('needs_investigation'))}",
        "",
        "| GSC | Proposed additions | Semantic reuse | Transliteration reuse | Render-block reuse |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]

    for entry in entries:
        candidates = entry.get("proposed_additions", [])
        lines.append(
            f"| `{entry['id']}` | {len(candidates)} | "
            f"{sum(1 for c in candidates if c.get('semantic_assignment'))} | "
            f"{sum(1 for c in candidates if c.get('transliteration_latex'))} | "
            f"{sum(1 for c in candidates if c.get('render_latex'))} |"
        )

    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Reuse existing TeX character analyses as semantic evidence for curated packets.")
    parser.add_argument("--tex-entries", default=DEFAULT_TEX_ENTRIES)
    parser.add_argument("--semantic-inventory", default=DEFAULT_SEMANTIC_INVENTORY)
    parser.add_argument("--curation-dir", default=DEFAULT_CURATION_DIR)
    parser.add_argument("--shengfu", default=DEFAULT_SHENGFU)
    parser.add_argument("--ids-path", default=DEFAULT_IDS_PATH)
    parser.add_argument("--report-out", default=DEFAULT_REPORT_OUT)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    tex_entries = json.loads(Path(args.tex_entries).read_text(encoding="utf-8"))["entries"]
    semantic_inventory = json.loads(Path(args.semantic_inventory).read_text(encoding="utf-8"))
    curation_dir = Path(args.curation_dir)
    report_path = Path(args.report_out)

    inventory_lookup = build_inventory_lookup(semantic_inventory)
    graph_lookup = build_inventory_graph_lookup(semantic_inventory)
    ids_map = load_ids_map(Path(args.ids_path))
    evidence = build_tex_character_evidence(tex_entries, semantic_inventory)
    shengfu_rows = load_csv_records(Path(args.shengfu))
    learned_graph_lookup = build_learned_graph_lookup(evidence, shengfu_rows, ids_map)
    merged_graph_lookup = merge_graph_lookups(graph_lookup, learned_graph_lookup)
    enriched_entries: list[dict[str, Any]] = []
    for path in sorted(curation_dir.glob("*.json")):
        entry = json.loads(path.read_text(encoding="utf-8"))
        entry = enrich_curated_entry_with_ids(entry, evidence, ids_map, merged_graph_lookup)
        write_curated_entry(entry, path)
        enriched_entries.append(entry)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_report(enriched_entries), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
