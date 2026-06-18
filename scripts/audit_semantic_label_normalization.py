from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import build_semantic_evidence
import extract_tex_entries
import semantic_label_normalization


DEFAULT_CURRENT_TEX = "main.tex"
DEFAULT_PILOT_TEX = "key references/My_Chinese_dictionary/main.tex"
DEFAULT_CURRENT_ENTRIES = "data/current_tex_entries.json"
DEFAULT_CURRENT_SEMANTICS = "data/current_semantic_components.json"
DEFAULT_CURATION_DIR = "data/entries/curation"
DEFAULT_INTEGRATED_SERIES_DIR = "data/entries/integrated_series"
DEFAULT_IDS = "data/raw/cjkvi_ids.txt"
DEFAULT_JSON_OUT = "data/semantic_components/semantic_label_normalization_audit.json"
DEFAULT_REPORT_OUT = "reports/semantic_label_normalization_audit.md"
DEFAULT_ALIAS_CONFIG = "data/semantic_components/semantic_aliases.json"
DEFAULT_VALIDATION_TEX = [
    "build/generated_curated_series_sample.tex",
    "build/generated_integrated_dictionary.tex",
]


def load_entries_from_tex(path: Path) -> list[dict[str, Any]]:
    source_text = path.read_text(encoding="utf-8")
    return extract_tex_entries.extract_entries(source_text, source_path=str(path))["entries"]


def load_entries_from_json(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))["entries"]


def flatten_tex_occurrences(
    *,
    entries: list[dict[str, Any]],
    source_layer: str,
    source_path: str,
    semantic_inventory: dict[str, Any],
    ids_map: dict[str, str],
    canonical_index: dict[str, list[dict[str, Any]]],
    normalization_config: dict[str, Any],
) -> list[dict[str, Any]]:
    evidence = build_semantic_evidence.build_tex_character_evidence(entries, semantic_inventory)
    occurrences: list[dict[str, Any]] = []
    for character_occurrences in evidence.values():
        for occurrence in character_occurrences:
            semantic_assignment = occurrence.get("semantic_assignment") or {}
            token_raw = semantic_assignment.get("token")
            label = (semantic_assignment.get("abbreviation") or "").lower()
            if not token_raw or not label:
                continue
            classification = semantic_label_normalization.classify_semantic_label(
                label,
                canonical_index,
                normalization_config,
            )
            occurrences.append(
                {
                    "source_layer": source_layer,
                    "source_path": source_path,
                    "series_id": occurrence.get("entry_id"),
                    "character": occurrence.get("character"),
                    "token_raw": token_raw,
                    "label": label,
                    "classification": classification["classification"],
                    "canonical_abbreviation": classification.get("canonical_abbreviation"),
                    "targets": classification.get("targets", []),
                    "reason": classification.get("reason"),
                    "source_line_number": occurrence.get("source_line_number"),
                    "json_path": None,
                    "source_fields": ["raw_block"],
                    "snippet": occurrence.get("transliteration_latex") or occurrence.get("raw_block") or "",
                    "semantic_component": (semantic_assignment.get("inventory_matches") or [{}])[0].get("graph_raw"),
                    "ids": ids_map.get(occurrence.get("character") or ""),
                    "wiktionary_validation": None,
                    "shengfu_summary": None,
                }
            )
    return occurrences


def flatten_candidate_occurrences(
    *,
    container: dict[str, Any],
    source_layer: str,
    source_path: str,
    json_prefix: str,
    canonical_index: dict[str, list[dict[str, Any]]],
    normalization_config: dict[str, Any],
    ids_map: dict[str, str],
) -> list[dict[str, Any]]:
    occurrences: list[dict[str, Any]] = []
    for index, candidate in enumerate(container.get("proposed_additions", [])):
        labels_to_fields: dict[str, set[str]] = defaultdict(set)
        labels_to_raw: dict[str, str] = {}
        for field in ("transliteration_latex", "render_latex"):
            for label in semantic_label_normalization.iter_semantic_labels_from_text(
                candidate.get(field),
                preserve_non_ascii=True,
            ):
                labels_to_fields[label].add(field)
                labels_to_raw.setdefault(label, candidate.get(field) or "")

        for label, fields in labels_to_fields.items():
            assignment = candidate.get("semantic_assignment") or {}
            classification = semantic_label_normalization.classify_semantic_label(
                label,
                canonical_index,
                normalization_config,
            )
            shengfu_summary = None
            if candidate.get("shengfu_character_rows") or candidate.get("shengfu_component_rows"):
                shengfu_summary = {
                    "character_rows": len(candidate.get("shengfu_character_rows") or []),
                    "component_rows": len(candidate.get("shengfu_component_rows") or []),
                }
            occurrences.append(
                {
                    "source_layer": source_layer,
                    "source_path": source_path,
                    "series_id": container.get("id") or container.get("schuessler", {}).get("gsc_id"),
                    "character": candidate.get("character"),
                    "token_raw": (assignment.get("token") or label),
                    "label": label,
                    "classification": classification["classification"],
                    "canonical_abbreviation": classification.get("canonical_abbreviation"),
                    "targets": classification.get("targets", []),
                    "reason": classification.get("reason"),
                    "source_line_number": None,
                    "json_path": f"{json_prefix}.proposed_additions[{index}]",
                    "source_fields": sorted(fields),
                    "snippet": candidate.get("render_latex") or candidate.get("transliteration_latex") or "",
                    "semantic_component": assignment.get("semantic_component"),
                    "ids": ids_map.get(candidate.get("character") or ""),
                    "wiktionary_validation": candidate.get("wiktionary_validation") or candidate.get("wiktionary_semantic_validation"),
                    "shengfu_summary": shengfu_summary,
                }
            )
    return occurrences


def flatten_integrated_series_occurrences(
    *,
    series_dir: Path,
    semantic_inventory: dict[str, Any],
    ids_map: dict[str, str],
    canonical_index: dict[str, list[dict[str, Any]]],
    normalization_config: dict[str, Any],
) -> list[dict[str, Any]]:
    occurrences: list[dict[str, Any]] = []
    for path in sorted(series_dir.glob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))

        preferred_hand_entry = record.get("preferred_hand_entry")
        if preferred_hand_entry:
            occurrences.extend(
                flatten_tex_occurrences(
                    entries=[preferred_hand_entry],
                    source_layer="integrated_series_hand_entry",
                    source_path=str(path),
                    semantic_inventory=semantic_inventory,
                    ids_map=ids_map,
                    canonical_index=canonical_index,
                    normalization_config=normalization_config,
                )
            )

        curated_entry = record.get("curated_entry")
        if curated_entry:
            occurrences.extend(
                flatten_candidate_occurrences(
                    container=curated_entry,
                    source_layer="integrated_series_curated_entry",
                    source_path=str(path),
                    json_prefix="curated_entry",
                    canonical_index=canonical_index,
                    normalization_config=normalization_config,
                    ids_map=ids_map,
                )
            )
    return occurrences


def flatten_validation_tex_occurrences(
    *,
    path: Path,
    canonical_index: dict[str, list[dict[str, Any]]],
    normalization_config: dict[str, Any],
) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    occurrences: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        for content in semantic_label_normalization.TEXTSUP_RE.findall(line):
            label = semantic_label_normalization.normalize_superscript_label(content, preserve_non_ascii=True)
            if label is None:
                continue
            classification = semantic_label_normalization.classify_semantic_label(
                label,
                canonical_index,
                normalization_config,
            )
            occurrences.append(
                {
                    "source_layer": "validation_tex",
                    "source_path": str(path),
                    "series_id": None,
                    "character": None,
                    "token_raw": content,
                    "label": label,
                    "classification": classification["classification"],
                    "canonical_abbreviation": classification.get("canonical_abbreviation"),
                    "targets": classification.get("targets", []),
                    "reason": classification.get("reason"),
                    "source_line_number": line_number,
                    "json_path": None,
                    "source_fields": ["line"],
                    "snippet": line.strip(),
                    "semantic_component": None,
                    "ids": None,
                    "wiktionary_validation": None,
                    "shengfu_summary": None,
                }
            )
    return occurrences


def summarize_occurrences(occurrences: list[dict[str, Any]]) -> dict[str, Any]:
    by_classification = Counter(occurrence["classification"] for occurrence in occurrences)
    by_source = Counter(occurrence["source_layer"] for occurrence in occurrences)
    by_source_and_classification: dict[str, dict[str, int]] = defaultdict(dict)
    for source in sorted(by_source):
        source_occurrences = [occurrence for occurrence in occurrences if occurrence["source_layer"] == source]
        counts = Counter(occurrence["classification"] for occurrence in source_occurrences)
        by_source_and_classification[source] = dict(sorted(counts.items()))
    return {
        "by_classification": dict(sorted(by_classification.items())),
        "by_source": dict(sorted(by_source.items())),
        "by_source_and_classification": by_source_and_classification,
    }


def build_unsafe_alias_audit(
    semantic_inventory: dict[str, Any],
    occurrences: list[dict[str, Any]],
    normalization_config: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[str]]:
    relevant_tokens = set(normalization_config["aliases"]) | set(normalization_config["blocked_aliases"]) | set(
        normalization_config["audit_watch_tokens"]
    )
    used_labels = {occurrence["label"] for occurrence in occurrences}
    rows: list[dict[str, Any]] = []
    matched_tokens: set[str] = set()
    for item in semantic_inventory["items"]:
        abbreviation = (item.get("abbreviation") or "").lower()
        for token in sorted(relevant_tokens):
            if token == abbreviation:
                continue
            if not semantic_label_normalization.matches_old_heuristic(token, item.get("label_token")):
                continue
            matched_tokens.add(token)
            if token in normalization_config["aliases"]:
                status = "explicit_alias"
            elif token in normalization_config["blocked_aliases"]:
                status = "blocked_ambiguous_alias"
            else:
                status = "unsafe_candidate"
            rows.append(
                {
                    "graph": item.get("graph_raw"),
                    "abbreviation": item.get("abbreviation"),
                    "expanded_latin": item.get("label_token"),
                    "candidate_alias": token,
                    "status": status,
                    "currently_used": token in used_labels,
                }
            )
    unmatched_watch_tokens = sorted(token for token in normalization_config["audit_watch_tokens"] if token not in matched_tokens)
    return rows, unmatched_watch_tokens


def render_occurrence_table(occurrences: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Source | GSC | Character | Label | Fields | Component | IDS | Snippet |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for occurrence in occurrences:
        lines.append(
            f"| `{occurrence['source_layer']}` | "
            f"`{occurrence.get('series_id') or ''}` | "
            f"`{occurrence.get('character') or ''}` | "
            f"`{occurrence['label']}` | "
            f"{', '.join(occurrence.get('source_fields') or [])} | "
            f"`{occurrence.get('semantic_component') or ''}` | "
            f"`{occurrence.get('ids') or ''}` | "
            f"`{(occurrence.get('snippet') or '').replace('`', '\\`')}` |"
        )
    lines.append("")
    return lines


def render_report(audit: dict[str, Any]) -> str:
    lines = [
        "# Semantic label normalization audit",
        "",
        f"- Generated at: {audit['generated_at']}",
        f"- Normalization config: `{audit['normalization_config_path']}`",
        f"- Total occurrences audited: {len(audit['occurrences'])}",
        "",
        "## Classification summary",
        "",
        "| Classification | Count |",
        "| --- | --- |",
    ]
    for classification, count in sorted(audit["summary"]["by_classification"].items()):
        lines.append(f"| `{classification}` | {count} |")
    lines.append("")

    lines.extend(
        [
            "## Blocked ambiguous aliases",
            "",
            "| Alias | Candidate canonical labels | Reason |",
            "| --- | --- | --- |",
        ]
    )
    for alias, payload in sorted(audit["blocked_aliases"].items()):
        lines.append(
            f"| `{alias}` | {', '.join(f'`{target}`' for target in payload['targets'])} | {payload.get('reason') or ''} |"
        )
    lines.append("")

    lines.extend(
        [
            "## Intentional scoped duplicate graphs",
            "",
            "| Graph | Abbreviation | Scope | Only in | Note |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for item in audit["intentional_scoped_duplicates"]:
        lines.append(
            f"| `{item['graph_raw']}` | `{item['abbreviation']}` | {item['scope']} | "
            f"{', '.join(item['only_in'])} | {item.get('note') or ''} |"
        )
    lines.append("")

    lines.extend(
        [
            "## Unsafe alias candidates produced by the old heuristic",
            "",
            "| Graph | Canonical label | Expanded Latin | Candidate alias | Status | Used now |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in audit["unsafe_alias_candidates"]:
        lines.append(
            f"| `{row['graph'] or ''}` | `{row['abbreviation'] or ''}` | `{row['expanded_latin'] or ''}` | "
            f"`{row['candidate_alias']}` | `{row['status']}` | {'yes' if row['currently_used'] else 'no'} |"
        )
    lines.append("")
    if audit["unsafe_alias_unmatched_watch_tokens"]:
        lines.append(
            "Watched tokens with no current heuristic match: "
            + ", ".join(f"`{token}`" for token in audit["unsafe_alias_unmatched_watch_tokens"])
        )
        lines.append("")

    if audit["infirm_occurrences"]:
        lines.extend(["## `infirm` occurrences", ""])
        lines.extend(render_occurrence_table(audit["infirm_occurrences"]))

    if audit["bos_occurrences"]:
        lines.extend(["## Audited `bos` occurrences", ""])
        lines.extend(render_occurrence_table(audit["bos_occurrences"]))

    if audit["blocked_occurrences"]:
        lines.extend(["## Blocked ambiguous labels in use", ""])
        lines.extend(render_occurrence_table(audit["blocked_occurrences"]))

    if audit["needs_review_occurrences"]:
        lines.extend(["## Needs-review labels in use", ""])
        lines.extend(render_occurrence_table(audit["needs_review_occurrences"]))

    if audit["placeholder_occurrences"]:
        lines.extend(["## Placeholder labels in use", ""])
        lines.extend(render_occurrence_table(audit["placeholder_occurrences"]))

    if audit["missing_occurrences"]:
        lines.extend(["## Missing labels in use", ""])
        lines.extend(render_occurrence_table(audit["missing_occurrences"]))

    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit semantic-component label normalization across hand, curated, integrated, and validation layers.")
    parser.add_argument("--current-tex", default=DEFAULT_CURRENT_TEX)
    parser.add_argument("--pilot-tex", default=DEFAULT_PILOT_TEX)
    parser.add_argument("--current-entries", default=DEFAULT_CURRENT_ENTRIES)
    parser.add_argument("--current-semantics", default=DEFAULT_CURRENT_SEMANTICS)
    parser.add_argument("--curation-dir", default=DEFAULT_CURATION_DIR)
    parser.add_argument("--integrated-series-dir", default=DEFAULT_INTEGRATED_SERIES_DIR)
    parser.add_argument("--ids", default=DEFAULT_IDS)
    parser.add_argument("--json-out", default=DEFAULT_JSON_OUT)
    parser.add_argument("--report-out", default=DEFAULT_REPORT_OUT)
    parser.add_argument("--alias-config", default=DEFAULT_ALIAS_CONFIG)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    normalization_config = semantic_label_normalization.load_normalization_config(Path(args.alias_config))
    semantic_inventory = json.loads(Path(args.current_semantics).read_text(encoding="utf-8"))
    canonical_index = semantic_label_normalization.build_canonical_index(semantic_inventory["items"])
    ids_map = build_semantic_evidence.load_ids_map(Path(args.ids))

    occurrences: list[dict[str, Any]] = []
    occurrences.extend(
        flatten_tex_occurrences(
            entries=load_entries_from_tex(Path(args.current_tex)),
            source_layer="current_main_tex",
            source_path=args.current_tex,
            semantic_inventory=semantic_inventory,
            ids_map=ids_map,
            canonical_index=canonical_index,
            normalization_config=normalization_config,
        )
    )
    occurrences.extend(
        flatten_tex_occurrences(
            entries=load_entries_from_tex(Path(args.pilot_tex)),
            source_layer="earlier_pilot_tex",
            source_path=args.pilot_tex,
            semantic_inventory=semantic_inventory,
            ids_map=ids_map,
            canonical_index=canonical_index,
            normalization_config=normalization_config,
        )
    )
    occurrences.extend(
        flatten_tex_occurrences(
            entries=load_entries_from_json(Path(args.current_entries)),
            source_layer="current_tex_entries_json",
            source_path=args.current_entries,
            semantic_inventory=semantic_inventory,
            ids_map=ids_map,
            canonical_index=canonical_index,
            normalization_config=normalization_config,
        )
    )

    curation_dir = Path(args.curation_dir)
    for path in sorted(curation_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        occurrences.extend(
            flatten_candidate_occurrences(
                container=data,
                source_layer="curation_json",
                source_path=str(path),
                json_prefix="root",
                canonical_index=canonical_index,
                normalization_config=normalization_config,
                ids_map=ids_map,
            )
        )

    occurrences.extend(
        flatten_integrated_series_occurrences(
            series_dir=Path(args.integrated_series_dir),
            semantic_inventory=semantic_inventory,
            ids_map=ids_map,
            canonical_index=canonical_index,
            normalization_config=normalization_config,
        )
    )

    for validation_path in DEFAULT_VALIDATION_TEX:
        occurrences.extend(
            flatten_validation_tex_occurrences(
                path=Path(validation_path),
                canonical_index=canonical_index,
                normalization_config=normalization_config,
            )
        )

    unsafe_alias_candidates, unmatched_watch_tokens = build_unsafe_alias_audit(
        semantic_inventory,
        occurrences,
        normalization_config,
    )

    intentional_scoped_duplicates = [
        item
        for item in semantic_inventory["items"]
        if item.get("duplicate_graph_status") == "intentional_scoped_duplicate"
    ]

    audit = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "normalization_config_path": normalization_config["path"],
        "blocked_aliases": normalization_config["blocked_aliases"],
        "intentional_scoped_duplicates": intentional_scoped_duplicates,
        "unsafe_alias_candidates": unsafe_alias_candidates,
        "unsafe_alias_unmatched_watch_tokens": unmatched_watch_tokens,
        "summary": summarize_occurrences(occurrences),
        "occurrences": occurrences,
        "infirm_occurrences": [occurrence for occurrence in occurrences if occurrence["label"] == "infirm"],
        "bos_occurrences": [occurrence for occurrence in occurrences if occurrence["label"] == "bos"],
        "blocked_occurrences": [
            occurrence for occurrence in occurrences if occurrence["classification"] == "blocked_ambiguous_alias"
        ],
        "needs_review_occurrences": [
            occurrence for occurrence in occurrences if occurrence["classification"] == "needs_review"
        ],
        "placeholder_occurrences": [
            occurrence for occurrence in occurrences if occurrence["classification"] == "placeholder"
        ],
        "missing_occurrences": [
            occurrence for occurrence in occurrences if occurrence["classification"] == "missing_from_inventory"
        ],
    }

    json_out = Path(args.json_out)
    report_out = Path(args.report_out)
    json_out.parent.mkdir(parents=True, exist_ok=True)
    report_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_out.write_text(render_report(audit), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
