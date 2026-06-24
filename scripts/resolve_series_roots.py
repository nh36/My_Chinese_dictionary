from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


DEFAULT_INPUT_DIR = "data/entries/curation"
DEFAULT_REPORT_OUT = "reports/series_root_resolution.md"
DEFAULT_HEAD_SUPPLEMENT = "data/series_root_head_supplement.json"

GSR_BASE_RE = re.compile(r"^0*(\d+)([a-z]?(?:')?)?$", re.IGNORECASE)
VOWEL_RE = re.compile(r"[aeiouəɨɯ]")
OC_ALT_RE = re.compile(r"\s*\{.*$")
OC_CLEAN_RE = re.compile(r"[\[\]\(\)<>]")
OC_BRACED_ALT_RE = re.compile(r"\{([^}]*)\}")


def split_gsr(value: str | None) -> tuple[int, str] | None:
    if not value:
        return None
    match = GSR_BASE_RE.match(str(value).strip())
    if not match:
        return None
    return int(match.group(1)), (match.group(2) or "").lower()


def extract_primary_oc_form(oc_bs: str | None) -> str | None:
    if not oc_bs:
        return None
    text = str(oc_bs).strip()
    primary = OC_ALT_RE.sub("", text).lstrip("*").strip()
    alt_match = OC_BRACED_ALT_RE.search(text)
    if primary.startswith(("ˤ", "ʔ", "a", "e", "i", "o", "u", "ə", "ɨ", "ɯ")) and alt_match:
        alt = alt_match.group(1).lstrip("*").strip()
        if alt:
            primary = alt
    primary = OC_CLEAN_RE.sub("", primary)
    return primary or None


def strip_oc_prefixes(oc_form: str, *, mode: str = "broad") -> str:
    form = oc_form.replace("‧", ".")
    if mode == "node":
        if "." in form:
            prefix, stem = form.rsplit(".", 1)
            form = ("s" if prefix.rstrip().endswith(("s", "S")) else "") + stem
    else:
        form = form.split(".")[-1]
    while form.startswith(("C", "N")) and len(form) > 1:
        form = form[1:]
    match = VOWEL_RE.search(form)
    if match is None:
        return form
    onset = form[: match.start()]
    rhyme = form[match.start() :]
    if "-" in onset:
        if mode == "node":
            prefix, stem = onset.rsplit("-", 1)
            onset = ("s" if prefix.rstrip().endswith(("s", "S")) else "") + stem
        else:
            onset = onset.split("-")[-1]
    return onset + rhyme


def split_onset_rhyme(oc_form: str) -> tuple[str, str] | None:
    match = VOWEL_RE.search(oc_form)
    if match is None:
        return None
    return oc_form[: match.start()], oc_form[match.start() :]


def normalize_onset(onset: str, *, mode: str = "broad") -> str:
    if not onset:
        return ""
    original = onset
    onset = onset.replace("ʳ", "r").replace("ˡ", "l")
    onset = onset.replace("ˤ", "").replace("̥", "")
    aspirated = "ʰ" in onset or "ʰ" in original
    onset = onset.replace("ʰ", "")
    if "ʷ" in onset:
        labialized = True
        onset = onset.replace("ʷ", "")
    else:
        labialized = False
    has_medial_r = "r" in onset[1:] if len(onset) > 1 else False
    if mode != "node" and len(onset) > 1:
        onset = onset[0] + onset[1:].replace("r", "")

    s_prefix_affricate = False
    if mode == "node":
        s_prefix_affricate = onset.startswith(("st", "sd"))
        if onset.startswith("ŋ"):
            base = "ŋ"
        elif onset.startswith(("ts", "dz")) or s_prefix_affricate:
            base = "ts"
        elif onset.startswith(("ɢ", "ɡ", "g")):
            base = "g"
        elif onset.startswith(("q", "ʔ")):
            base = "q"
        elif onset.startswith(("k", "x")):
            base = "k"
        elif onset.startswith(("t", "d")):
            base = "t"
        elif onset.startswith("n"):
            base = "n"
        elif onset.startswith("m"):
            base = "m"
        elif onset.startswith(("p", "b")):
            base = "p"
        elif onset.startswith(("s", "z", "ś", "ʃ")):
            base = "s"
        elif onset.startswith("l"):
            base = "l"
        elif onset.startswith("r"):
            base = "r"
        else:
            base = onset
    elif "ŋ" in onset:
        base = "ṅ"
    elif "ts" in onset or "dz" in onset:
        base = "ts"
    elif onset.startswith(("q", "ɢ")):
        base = "q"
    elif onset.startswith(("k", "g", "x")):
        base = "k"
    elif onset.startswith(("t", "d", "l̥")):
        base = "t"
    elif onset.startswith("n"):
        base = "n"
    elif onset.startswith("m"):
        base = "m"
    elif onset.startswith(("p", "b")):
        base = "p"
    elif onset.startswith(("s", "z", "ś", "ʃ")):
        base = "s"
    elif onset.startswith("l"):
        base = "l"
    elif onset.startswith("r"):
        base = "r"
    else:
        base = onset

    if labialized and base in {"k", "q"}:
        base = base + "u"
    if mode == "node" and aspirated and base in {"k", "q", "t", "p", "ts", "s"} and not (s_prefix_affricate and base == "ts"):
        base = base + "h"
    if mode == "node" and has_medial_r and not base.endswith("r") and base not in {"r", "l", "n", "m"}:
        base = base + "r"
    return base


def normalize_rhyme(rhyme: str, *, mode: str = "broad") -> tuple[str, str]:
    broad = rhyme.replace("-", "")
    broad = broad.rstrip("ʔs")
    broad = broad.replace("ˤ", "").replace("̠", "")
    if not broad:
        return "", ""
    if broad.endswith("j"):
        broad = broad[:-1]
        glide = "y"
    elif broad.endswith("w"):
        broad = broad[:-1]
        glide = "w"
    else:
        glide = ""

    coda = ""
    if broad.endswith("ŋ"):
        broad = broad[:-1]
        coda = "ṅ"
    elif broad.endswith("ɡ"):
        broad = broad[:-1]
        coda = "k"
    elif broad.endswith("b"):
        broad = broad[:-1]
        coda = "p"
    elif broad.endswith("d"):
        broad = broad[:-1]
        coda = "t"
    elif broad.endswith(("k", "m", "n", "r", "t", "p")):
        coda = broad[-1]
        broad = broad[:-1]

    if "ə" in broad or "ɨ" in broad or "ɯ" in broad:
        vowel = "y"
    elif "a" in broad:
        vowel = "a"
    elif "o" in broad:
        vowel = "o"
    elif "e" in broad:
        vowel = "e"
    elif "i" in broad:
        vowel = "i"
    elif "u" in broad:
        vowel = "u"
    else:
        vowel = broad or ""

    if glide and vowel == "y" and glide == "y":
        return vowel, coda
    if glide:
        return vowel + glide, coda
    return vowel, coda


def derive_oc_root(oc_bs: str | None, *, mode: str = "broad") -> str | None:
    primary = extract_primary_oc_form(oc_bs)
    if primary is None:
        return None
    stripped = strip_oc_prefixes(primary, mode=mode)
    parts = split_onset_rhyme(stripped)
    if parts is None:
        return None
    onset, rhyme = parts
    normalized_onset = normalize_onset(onset, mode=mode)
    normalized_vowel, normalized_coda = normalize_rhyme(rhyme, mode=mode)
    root = normalized_onset + normalized_vowel + normalized_coda
    return root or None


def load_head_supplement(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"heads": {}, "supplemental_shengfu_rows": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {
        "heads": data.get("heads") or {},
        "supplemental_shengfu_rows": data.get("supplemental_shengfu_rows") or {},
    }


def entry_gsc_id(entry: dict[str, Any]) -> str | None:
    return (
        entry.get("id")
        or entry.get("gsc_id")
        or (entry.get("schuessler") or {}).get("gsc_id")
    )


def get_head_supplement(
    entry: dict[str, Any],
    head_supplement: dict[str, Any] | None,
) -> dict[str, Any] | None:
    if not head_supplement:
        return None
    gsc_id = entry_gsc_id(entry)
    if not gsc_id:
        return None
    return (head_supplement.get("heads") or {}).get(gsc_id)


def merge_supplemental_shengfu_rows(
    entry: dict[str, Any],
    head_supplement: dict[str, Any] | None,
) -> dict[str, Any]:
    if not head_supplement:
        return entry
    gsc_id = entry_gsc_id(entry)
    if not gsc_id:
        return entry
    rows_by_character = (head_supplement.get("supplemental_shengfu_rows") or {}).get(gsc_id) or {}
    if not rows_by_character:
        return entry
    candidate_map = {candidate["character"]: candidate for candidate in entry.get("proposed_additions", [])}
    for character, supplemental_rows in rows_by_character.items():
        candidate = candidate_map.get(character)
        if candidate is None:
            continue
        existing_rows = candidate.get("shengfu_character_rows") or []
        seen = {
            json.dumps(row, ensure_ascii=False, sort_keys=True)
            for row in existing_rows
        }
        for row in supplemental_rows:
            key = json.dumps(row, ensure_ascii=False, sort_keys=True)
            if key in seen:
                continue
            existing_rows.append(row)
            seen.add(key)
        candidate["shengfu_character_rows"] = existing_rows
    return entry


def build_head_supplement_candidate(head_data: dict[str, Any] | None) -> dict[str, Any] | None:
    if not head_data:
        return None
    oc_bs = head_data.get("oc_bs")
    if not oc_bs and head_data.get("oc_syllable"):
        oc_bs = f"*{head_data['oc_syllable']}"
    root = head_data.get("root") or derive_oc_root(oc_bs, mode="broad")
    if not root:
        return None
    return {
        "character": head_data.get("character"),
        "gsr": head_data.get("gsr"),
        "oc_bs": oc_bs,
        "root": root,
        "source": "head_graph_supplement",
    }


def derive_root_candidates(
    entry: dict[str, Any],
    *,
    head_supplement: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    if entry.get("packet_kind") != "missing_series":
        return []

    header_tokens = {
        int(token)
        for token in entry.get("schuessler", {}).get("k_tokens", [])
        if str(token).isdigit()
    }
    candidates: list[dict[str, Any]] = []

    for candidate in entry.get("proposed_additions", []):
        rows = candidate.get("mand2mc_rows", []) + candidate.get("bs_gsr_rows", [])
        matched_header_token = False
        for row in rows:
            parts = split_gsr(row.get("gsr"))
            if parts is None:
                continue
            digits, suffix = parts
            if digits not in header_tokens or suffix not in {"", "a"}:
                continue
            matched_header_token = True

            oc_bs = row.get("oc_bs")
            root = derive_oc_root(oc_bs, mode="broad")
            if not root:
                continue
            candidates.append(
                {
                    "character": candidate["character"],
                    "gsr": row.get("gsr"),
                    "oc_bs": oc_bs,
                    "root": root,
                    "source": "head_graph_oc_bs",
                }
            )
        if not matched_header_token:
            continue
        for row in candidate.get("shengfu_character_rows", []):
            oc_syllable = row.get("oc_syllable")
            if not oc_syllable:
                continue
            root = derive_oc_root(f"*{oc_syllable}", mode="broad")
            if not root:
                continue
            candidates.append(
                {
                    "character": candidate["character"],
                    "gsr": None,
                    "oc_bs": f"*{oc_syllable}",
                    "root": root,
                    "source": "head_graph_oc_shengfu",
                }
            )

    supplement_candidate = build_head_supplement_candidate(get_head_supplement(entry, head_supplement))
    if supplement_candidate is not None:
        candidates.append(supplement_candidate)

    deduped: dict[str, dict[str, Any]] = {}
    for item in candidates:
        existing = deduped.get(item["root"])
        if existing is None:
            deduped[item["root"]] = {
                **item,
                "support_count": 1,
                "supporting_sources": [item["source"]],
            }
            continue
        existing["support_count"] = existing.get("support_count", 1) + 1
        supporting_sources = existing.setdefault("supporting_sources", [])
        if item["source"] not in supporting_sources:
            supporting_sources.append(item["source"])
    values = list(deduped.values())
    if any(item["gsr"] and split_gsr(item["gsr"]) and split_gsr(item["gsr"])[1] == "a" for item in values):
        values = [
            item
            for item in values
            if item["gsr"] and split_gsr(item["gsr"]) and split_gsr(item["gsr"])[1] == "a"
        ]
    return values


def derive_packet_root_consensus(entry: dict[str, Any]) -> dict[str, Any] | None:
    roots_by_character: dict[str, list[tuple[str | None, str]]] = {}
    for candidate in entry.get("proposed_additions", []):
        values: list[tuple[str | None, str]] = []
        for row in candidate.get("bs_gsr_rows", []):
            root = derive_oc_root(row.get("oc_bs"), mode="broad")
            if root:
                values.append((row.get("oc_bs"), root))
        if values:
            roots_by_character[candidate["character"]] = values
    if len(roots_by_character) < 2:
        return None
    deduped_roots: dict[str, tuple[str | None, str]] = {}
    for values in roots_by_character.values():
        for oc_bs, root in values:
            deduped_roots.setdefault(root, (oc_bs, root))
    if len(deduped_roots) != 1:
        root_counts: dict[str, int] = {}
        root_examples: dict[str, str | None] = {}
        for values in roots_by_character.values():
            local_roots = {root for _, root in values}
            for root in local_roots:
                root_counts[root] = root_counts.get(root, 0) + 1
                root_examples.setdefault(root, next((oc for oc, candidate_root in values if candidate_root == root), None))
        ranked = sorted(root_counts.items(), key=lambda item: (-item[1], item[0]))
        if ranked and ranked[0][1] > 1 and (len(ranked) == 1 or ranked[0][1] > ranked[1][1]):
            root = ranked[0][0]
            return {
                "root": root,
                "source": "packet_bs_majority",
                "character": None,
                "oc_bs": root_examples.get(root),
                "confidence": "provisional-oc",
                "supporting_characters": ranked[0][1],
            }
        return None
    oc_bs, root = next(iter(deduped_roots.values()))
    return {
        "root": root,
        "source": "packet_bs_consensus",
        "character": None,
        "oc_bs": oc_bs,
        "confidence": "provisional-oc",
        "supporting_characters": len(roots_by_character),
    }


def derive_packet_shengfu_consensus(entry: dict[str, Any]) -> dict[str, Any] | None:
    roots_by_character: dict[str, set[str]] = {}
    for candidate in entry.get("proposed_additions", []):
        roots: set[str] = set()
        for row in candidate.get("shengfu_character_rows", []):
            oc_syllable = row.get("oc_syllable")
            if not oc_syllable:
                continue
            root = derive_oc_root(f"*{oc_syllable}", mode="broad")
            if root:
                roots.add(root)
        if roots:
            roots_by_character[candidate["character"]] = roots
    if len(roots_by_character) < 2:
        return None

    root_counts: dict[str, int] = {}
    for roots in roots_by_character.values():
        for root in roots:
            root_counts[root] = root_counts.get(root, 0) + 1
    ranked = sorted(root_counts.items(), key=lambda item: (-item[1], item[0]))
    if not ranked:
        return None
    if ranked[0][1] <= 1 or (len(ranked) > 1 and ranked[0][1] <= ranked[1][1]):
        return None
    return {
        "root": ranked[0][0],
        "source": "packet_shengfu_majority",
        "character": None,
        "oc_bs": None,
        "confidence": "provisional-oc",
        "supporting_characters": ranked[0][1],
    }


def resolved_root_from_candidate(
    candidate: dict[str, Any],
    *,
    source: str | None = None,
) -> dict[str, Any]:
    resolved = {
        "root": candidate["root"],
        "source": source or candidate["source"],
        "character": candidate["character"],
        "oc_bs": candidate.get("oc_bs"),
        "confidence": "provisional-oc",
    }
    if candidate.get("support_count"):
        resolved["support_count"] = candidate["support_count"]
    if candidate.get("supporting_sources"):
        resolved["supporting_sources"] = candidate["supporting_sources"]
    return resolved


def resolve_root(
    entry: dict[str, Any],
    *,
    head_supplement: dict[str, Any] | None = None,
    candidates: list[dict[str, Any]] | None = None,
) -> dict[str, Any] | None:
    if candidates is None:
        candidates = derive_root_candidates(entry, head_supplement=head_supplement)
    if not candidates:
        return derive_packet_root_consensus(entry) or derive_packet_shengfu_consensus(entry)
    if len(candidates) == 1:
        return resolved_root_from_candidate(candidates[0])
    schuessler_tokens = [
        int(token)
        for token in entry.get("schuessler", {}).get("k_tokens", [])
        if str(token).isdigit()
    ]
    if len(schuessler_tokens) > 1:
        primary_token = schuessler_tokens[0]
        for candidate in candidates:
            parts = split_gsr(candidate.get("gsr"))
            if parts and parts[0] == primary_token:
                return resolved_root_from_candidate(candidate, source="merged_packet_primary_head")
    ranked = sorted(
        candidates,
        key=lambda item: (-item.get("support_count", 1), item["root"]),
    )
    top_support = ranked[0].get("support_count", 1)
    next_support = ranked[1].get("support_count", 1) if len(ranked) > 1 else 0
    if top_support > 1 and top_support > next_support:
        return resolved_root_from_candidate(ranked[0], source="head_graph_supported_root")
    return derive_packet_root_consensus(entry) or derive_packet_shengfu_consensus(entry)


def apply_root_resolution(
    entry: dict[str, Any],
    *,
    head_supplement: dict[str, Any] | None = None,
) -> dict[str, Any]:
    entry = merge_supplemental_shengfu_rows(entry, head_supplement)
    candidates = derive_root_candidates(entry, head_supplement=head_supplement)
    entry["series_root_candidates"] = candidates
    entry["resolved_series_root"] = resolve_root(entry, head_supplement=head_supplement, candidates=candidates)
    head_data = get_head_supplement(entry, head_supplement)
    if head_data and entry.get("resolved_series_root"):
        entry["resolved_series_root"].setdefault("head_gloss", head_data.get("gloss"))
        entry["resolved_series_root"].setdefault("head_note", head_data.get("note"))
    return entry


def render_report(entries: list[dict[str, Any]]) -> str:
    missing_entries = [entry for entry in entries if entry.get("packet_kind") == "missing_series"]
    lines = [
        "# Series root resolution",
        "",
        f"- Missing-series packets inspected: {len(missing_entries)}",
        f"- Packets with at least one root candidate: {sum(1 for entry in missing_entries if entry.get('series_root_candidates'))}",
        f"- Packets with a single resolved provisional root: {sum(1 for entry in missing_entries if entry.get('resolved_series_root'))}",
        "",
        "| GSC | Root candidates | Resolved root | Source |",
        "| --- | --- | --- | --- |",
    ]
    for entry in missing_entries:
        candidates = "; ".join(
            f"{item['character']}→{item['root']} [{item.get('oc_bs', '')}] ({item['gsr']})"
            for item in entry.get("series_root_candidates", [])
        )
        resolved = entry.get("resolved_series_root") or {}
        lines.append(
            f"| `{entry['id']}` | {candidates} | `{resolved.get('root', '')}` | `{resolved.get('source', '')}` |"
        )
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build provisional root candidates for missing GSC series.")
    parser.add_argument("--input-dir", default=DEFAULT_INPUT_DIR)
    parser.add_argument("--report-out", default=DEFAULT_REPORT_OUT)
    parser.add_argument("--head-supplement", default=DEFAULT_HEAD_SUPPLEMENT)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    input_dir = Path(args.input_dir)
    head_supplement = load_head_supplement(Path(args.head_supplement))
    entries: list[dict[str, Any]] = []
    for path in sorted(input_dir.glob("*.json")):
        entry = json.loads(path.read_text(encoding="utf-8"))
        entry = apply_root_resolution(entry, head_supplement=head_supplement)
        path.write_text(json.dumps(entry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        entries.append(entry)
    report_path = Path(args.report_out)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_report(entries), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
