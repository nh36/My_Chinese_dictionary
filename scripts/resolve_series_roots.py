from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


DEFAULT_INPUT_DIR = "data/entries/curation"
DEFAULT_REPORT_OUT = "reports/series_root_resolution.md"

GSR_BASE_RE = re.compile(r"^0*(\d+)([a-z]?(?:')?)?$", re.IGNORECASE)
VOWEL_RE = re.compile(r"[aeiouəɨɯ]")
OC_ALT_RE = re.compile(r"\s*\{.*$")
OC_CLEAN_RE = re.compile(r"[\[\]\(\)<>]")


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
    primary = OC_ALT_RE.sub("", str(oc_bs).strip()).lstrip("*").strip()
    primary = OC_CLEAN_RE.sub("", primary)
    return primary or None


def strip_oc_prefixes(oc_form: str) -> str:
    form = oc_form.split(".")[-1]
    match = VOWEL_RE.search(form)
    if match is None:
        return form
    onset = form[: match.start()]
    rhyme = form[match.start() :]
    if "-" in onset:
        onset = onset.split("-")[-1]
    return onset + rhyme


def split_onset_rhyme(oc_form: str) -> tuple[str, str] | None:
    match = VOWEL_RE.search(oc_form)
    if match is None:
        return None
    return oc_form[: match.start()], oc_form[match.start() :]


def normalize_onset(onset: str) -> str:
    if not onset:
        return ""
    onset = onset.replace("ˤ", "").replace("ʰ", "").replace("̥", "")
    if "ʷ" in onset:
        labialized = True
        onset = onset.replace("ʷ", "")
    else:
        labialized = False
    onset = onset.replace("r", "")

    if "ŋ" in onset:
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
        return base + "u"
    return base


def normalize_rhyme(rhyme: str) -> tuple[str, str]:
    broad = rhyme.rstrip("ʔs")
    broad = broad.replace("ˤ", "")
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
    elif broad.endswith(("k", "m", "n", "r")):
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

    if glide:
        return vowel + glide, coda
    return vowel, coda


def derive_oc_root(oc_bs: str | None) -> str | None:
    primary = extract_primary_oc_form(oc_bs)
    if primary is None:
        return None
    stripped = strip_oc_prefixes(primary)
    parts = split_onset_rhyme(stripped)
    if parts is None:
        return None
    onset, rhyme = parts
    normalized_onset = normalize_onset(onset)
    normalized_vowel, normalized_coda = normalize_rhyme(rhyme)
    root = normalized_onset + normalized_vowel + normalized_coda
    return root or None


def derive_root_candidates(entry: dict[str, Any]) -> list[dict[str, Any]]:
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
        for row in rows:
            parts = split_gsr(row.get("gsr"))
            if parts is None:
                continue
            digits, suffix = parts
            if digits not in header_tokens or suffix not in {"", "a"}:
                continue

            oc_bs = row.get("oc_bs")
            root = derive_oc_root(oc_bs)
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

    deduped: dict[str, dict[str, Any]] = {}
    for item in candidates:
        deduped.setdefault(item["root"], item)
    return list(deduped.values())


def resolve_root(entry: dict[str, Any]) -> dict[str, Any] | None:
    candidates = derive_root_candidates(entry)
    if not candidates:
        return None
    if len(candidates) == 1:
        candidate = candidates[0]
        return {
            "root": candidate["root"],
            "source": candidate["source"],
            "character": candidate["character"],
            "oc_bs": candidate.get("oc_bs"),
            "confidence": "provisional-oc",
        }
    return None


def apply_root_resolution(entry: dict[str, Any]) -> dict[str, Any]:
    entry["series_root_candidates"] = derive_root_candidates(entry)
    entry["resolved_series_root"] = resolve_root(entry)
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
    return parser


def main() -> int:
    args = build_parser().parse_args()
    input_dir = Path(args.input_dir)
    entries: list[dict[str, Any]] = []
    for path in sorted(input_dir.glob("*.json")):
        entry = json.loads(path.read_text(encoding="utf-8"))
        entry = apply_root_resolution(entry)
        path.write_text(json.dumps(entry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        entries.append(entry)
    report_path = Path(args.report_out)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_report(entries), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
