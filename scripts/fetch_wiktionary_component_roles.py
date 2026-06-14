from __future__ import annotations

import argparse
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_INPUT_DIR = "data/entries/curation"
DEFAULT_CACHE_DIR = "data/raw/wiktionary"
DEFAULT_REPORT_OUT = "reports/wiktionary_component_validation.md"


def fetch_wiktionary_wikitext(character: str, cache_dir: Path) -> str | None:
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / f"{ord(character):05X}.json"
    if cache_path.exists():
        payload = json.loads(cache_path.read_text(encoding="utf-8"))
        if payload.get("wikitext"):
            return payload.get("wikitext")

    url = (
        "https://en.wiktionary.org/w/index.php?title="
        + urllib.parse.quote(character)
        + "&action=raw"
    )
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 CopilotCLI/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            wikitext = response.read().decode("utf-8", "replace")
    except Exception:
        cache_path.write_text(json.dumps({"character": character, "wikitext": None}, ensure_ascii=False), encoding="utf-8")
        return None
    cache_path.write_text(json.dumps({"character": character, "wikitext": wikitext}, ensure_ascii=False), encoding="utf-8")
    time.sleep(0.1)
    return wikitext


def parse_han_compound_template(wikitext: str | None) -> dict[str, Any] | None:
    if not wikitext:
        return None
    marker = "{{Han compound|"
    index = wikitext.find(marker)
    if index == -1:
        return None
    end = wikitext.find("}}", index)
    if end == -1:
        return None
    template = wikitext[index + 2 : end]  # keep content without leading {{
    parts = template.split("|")
    if len(parts) < 3 or parts[0] != "Han compound":
        return None

    positional: list[str] = []
    named: dict[str, str] = {}
    for part in parts[1:]:
        if "=" in part:
            key, value = part.split("=", 1)
            named[key] = value
        else:
            positional.append(part)

    semantic_components: list[str] = []
    phonetic_components: list[str] = []
    for index, component in enumerate(positional, start=1):
        role = named.get(f"c{index}")
        if role == "s":
            semantic_components.append(component)
        elif role == "p":
            phonetic_components.append(component)

    return {
        "template_raw": "{{" + template + "}}",
        "positional_components": positional,
        "named_args": named,
        "semantic_components": semantic_components,
        "phonetic_components": phonetic_components,
    }


def enrich_entry(entry: dict[str, Any], cache_dir: Path) -> dict[str, Any]:
    for candidate in entry.get("proposed_additions", []):
        wikitext = fetch_wiktionary_wikitext(candidate["character"], cache_dir)
        han_compound = parse_han_compound_template(wikitext)
        candidate["wiktionary_validation"] = {
            "available": wikitext is not None,
            "han_compound": han_compound,
        }
    return entry


def render_report(entries: list[dict[str, Any]]) -> str:
    total_candidates = sum(len(entry.get("proposed_additions", [])) for entry in entries)
    available = sum(
        1
        for entry in entries
        for candidate in entry.get("proposed_additions", [])
        if candidate.get("wiktionary_validation", {}).get("available")
    )
    explicit = sum(
        1
        for entry in entries
        for candidate in entry.get("proposed_additions", [])
        if candidate.get("wiktionary_validation", {}).get("han_compound")
        and candidate["wiktionary_validation"]["han_compound"].get("semantic_components")
        and candidate["wiktionary_validation"]["han_compound"].get("phonetic_components")
    )

    lines = [
        "# Wiktionary component validation",
        "",
        f"- Proposed additions checked: {total_candidates}",
        f"- Pages fetched / cached successfully: {available}",
        f"- Additions with explicit Han-compound semantic/phonetic roles: {explicit}",
        "",
        "| GSC | Character | Wiktionary page | Explicit semantic/phonetic roles | Semantic components | Phonetic components |",
        "| --- | --- | --- | --- | --- | --- |",
    ]

    for entry in entries:
        for candidate in entry.get("proposed_additions", []):
            validation = candidate.get("wiktionary_validation", {})
            han = validation.get("han_compound") or {}
            lines.append(
                f"| `{entry['id']}` | {candidate['character']} | "
                f"{'yes' if validation.get('available') else 'no'} | "
                f"{'yes' if han.get('semantic_components') and han.get('phonetic_components') else 'no'} | "
                f"{', '.join(han.get('semantic_components', []))} | "
                f"{', '.join(han.get('phonetic_components', []))} |"
            )

    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fetch Wiktionary Han-compound evidence for curated pilot additions.")
    parser.add_argument("--input-dir", default=DEFAULT_INPUT_DIR)
    parser.add_argument("--cache-dir", default=DEFAULT_CACHE_DIR)
    parser.add_argument("--report-out", default=DEFAULT_REPORT_OUT)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    input_dir = Path(args.input_dir)
    cache_dir = Path(args.cache_dir)
    entries: list[dict[str, Any]] = []
    for path in sorted(input_dir.glob("*.json")):
        entry = json.loads(path.read_text(encoding="utf-8"))
        entry = enrich_entry(entry, cache_dir)
        path.write_text(json.dumps(entry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        entries.append(entry)
    report_path = Path(args.report_out)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_report(entries), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
