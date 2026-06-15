from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


DEFAULT_INPUT_DIR = "data/entries/curation"
DEFAULT_REPORT_OUT = "reports/series_root_resolution.md"

GSR_BASE_RE = re.compile(r"^0*(\d+)([a-z]?(?:')?)?$", re.IGNORECASE)
MC_TONE_RE = re.compile(r"([A-Za-zəɯɨʉʌɔæɑṅḫṭḍṇśźñʔːˡʳ]+)(?:X|H|B|C)$")


def split_gsr(value: str | None) -> tuple[int, str] | None:
    if not value:
        return None
    match = GSR_BASE_RE.match(str(value).strip())
    if not match:
        return None
    return int(match.group(1)), (match.group(2) or "").lower()


def strip_tone(mc_form: str | None) -> str | None:
    if not mc_form:
        return None
    match = MC_TONE_RE.match(mc_form)
    if match:
        return match.group(1)
    return mc_form


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

            mc_form = row.get("mc_nwh") or row.get("mc_bs")
            root = strip_tone(mc_form)
            if not root:
                continue
            candidates.append(
                {
                    "character": candidate["character"],
                    "gsr": row.get("gsr"),
                    "root": root,
                    "source": "head_graph_mc",
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
            "confidence": "provisional",
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
            f"{item['character']}→{item['root']} ({item['gsr']})"
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
