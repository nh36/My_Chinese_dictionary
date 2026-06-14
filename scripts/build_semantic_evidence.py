from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import inventory_tex


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
BINARY_IDS = {"⿰", "⿱", "⿴", "⿵", "⿶", "⿷", "⿸", "⿹", "⿺", "⿻"}
TRINARY_IDS = {"⿲", "⿳"}
IDS_NOTE_RE = re.compile(r"\[[^]]*\]")
COMPONENT_ALIASES = {
    "王": "玉",
    "礻": "示",
    "衤": "衣",
    "忄": "心",
    "扌": "手",
    "氵": "水",
    "钅": "金",
    "釒": "金",
    "艹": "艸",
    "亻": "人",
    "⺮": "竹",
    "飠": "食",
    "饣": "食",
    "訁": "言",
    "疒": "疒",
}


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

    characters = dedupe_preserve(CHINESE_CHAR_RE.findall(character_line))
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
    resolved_abbreviation = inventory_matches[0].get("abbreviation") if inventory_matches else None

    return {
        "source": "ids_top_level",
        "character": character,
        "ids": ids,
        "phonetic_component": phonetic_component,
        "semantic_component": semantic_component,
        "position": position,
        "abbreviation": resolved_abbreviation,
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
        return rf"{{\large{{\textsuperscript{{{abbreviation}:}}{root}}}}},"
    if position == "suffix-dot":
        return rf"{{\large{{{root}\textsuperscript{{·{abbreviation}}}}}}},"
    if position == "suffix-colon":
        return rf"{{\large{{{root}\textsuperscript{{:{abbreviation}}}}}}},"
    return None


def enrich_curated_entry(entry: dict[str, Any], evidence: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    raise RuntimeError("Use enrich_curated_entry_with_ids instead.")


def enrich_curated_entry_with_ids(
    entry: dict[str, Any],
    evidence: dict[str, list[dict[str, Any]]],
    ids_map: dict[str, str],
    graph_lookup: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    for candidate in entry.get("proposed_additions", []):
        matches = evidence.get(candidate["character"], [])
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

        han_compound = (candidate.get("wiktionary_validation") or {}).get("han_compound")
        if han_compound and han_compound.get("semantic_components") and han_compound.get("phonetic_components"):
            explicit_semantic = normalize_component_graph(han_compound["semantic_components"][0])
            explicit_phonetic = han_compound["phonetic_components"][0]
            explicit_candidate = resolve_semantic_from_ids(
                character=candidate["character"],
                phonetic_component=explicit_phonetic,
                ids_map=ids_map,
                graph_lookup=graph_lookup,
            )
            candidate["wiktionary_semantic_validation"] = {
                "semantic_component": explicit_semantic,
                "phonetic_component": explicit_phonetic,
                "resolved_from_ids": explicit_candidate,
            }
            if explicit_candidate and explicit_candidate.get("abbreviation"):
                candidate["semantic_assignment"] = {
                    "token": None,
                    "abbreviation": explicit_candidate["abbreviation"],
                    "position": explicit_candidate["position"],
                    "inventory_matches": explicit_candidate["inventory_matches"],
                    "source": "wiktionary_han_compound",
                    "semantic_component": explicit_candidate["semantic_component"],
                }
                if candidate.get("transliteration_latex") is None and entry.get("tex_entry") is not None:
                    root = extract_series_root_latex(entry["tex_entry"]["raw_block"])
                    if root:
                        candidate["transliteration_latex"] = compose_transliteration_from_root(
                            root,
                            candidate["semantic_assignment"],
                        )
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
