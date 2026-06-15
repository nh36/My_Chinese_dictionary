from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


DEFAULT_INPUT_DIR = "data/entries/curation"
DEFAULT_REPORT_OUT = "reports/mc_disagreement_analysis.md"


def dedupe(values: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def classify_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    mand_forms = dedupe([row.get("mc_nwh") for row in candidate.get("mand2mc_rows", []) if row.get("mc_nwh")])
    bs_forms = dedupe([row.get("mc_bs") for row in candidate.get("bs_gsr_rows", []) if row.get("mc_bs")])
    gsr_values = dedupe(
        [row.get("gsr") for row in candidate.get("mand2mc_rows", []) if row.get("gsr")]
        + [row.get("gsr") for row in candidate.get("bs_gsr_rows", []) if row.get("gsr")]
    )

    categories: list[str] = []
    if len(mand_forms) > 1:
        categories.append("mand2mc-multiple")
    if len(bs_forms) > 1:
        categories.append("bs-gsr-multiple")
    if mand_forms and bs_forms and set(mand_forms) != set(bs_forms):
        categories.append("cross-source-mismatch")
    if len(gsr_values) > 1:
        categories.append("multiple-gsr")

    return {
        "character": candidate["character"],
        "categories": categories,
        "mand_forms": mand_forms,
        "bs_forms": bs_forms,
        "gsr_values": gsr_values,
    }


def analyze_entries(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for entry in entries:
        for candidate in entry.get("proposed_additions", []):
            analyzed = classify_candidate(candidate)
            if not analyzed["categories"]:
                continue
            analyzed["gsc_id"] = entry["id"]
            analyzed["candidate"] = candidate
            results.append(analyzed)
    return results


def render_report(results: list[dict[str, Any]]) -> str:
    category_counter = Counter(category for item in results for category in item["categories"])
    lines = [
        "# MC disagreement analysis",
        "",
        f"- Candidate additions with at least one MC-disagreement signal: {len(results)}",
        "",
        "## Category counts",
        "",
        "| Category | Count |",
        "| --- | ---: |",
    ]
    for category, count in category_counter.most_common():
        lines.append(f"| `{category}` | {count} |")

    lines.extend(
        [
            "",
            "## Current interpretation",
            "",
            "- The rendered warning `[MC disagreement among imported sources]` is currently triggered only by the boolean `mand_bs_mc_disagreement` field.",
            "- That boolean is set when the Mand2MC `mc_bs` set and the BS/GSR `mc_bs` set for a candidate are both non-empty and not exactly equal.",
            "- So the current warning is deliberately coarse: it conflates true cross-source conflict with cases where one source preserves only one reading of a graph that is polyphonic in the other source.",
            "- `mand2mc-multiple` usually means Mand2MC contains multiple MC readings for the same graph, which may reflect real polyphony rather than an error.",
            "- `bs-gsr-multiple` means the BS/GSR PDF lists multiple MC values for the same graph.",
            "- `cross-source-mismatch` means the Mand2MC and BS/GSR form sets are not identical for the current character packet.",
            "- `multiple-gsr` means the same graph is tied to more than one GSR item in the imported evidence.",
            "",
            "## Suggested resolution workflow",
            "",
            "1. Check whether the disagreement is between multiple legitimate readings of the same graph or between truly conflicting analyses.",
            "2. Where the disagreement matters for promotion into dictionary output, check the relevant Guangyun fanqie / entry rather than trusting either imported source blindly.",
            "3. Preserve unresolved polyphony explicitly instead of collapsing it into one reading too early.",
            "",
            "## Detailed cases",
            "",
            "| GSC | Character | Categories | Mand2MC MC | BS/GSR MC | GSR values |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )

    for item in results:
        lines.append(
            f"| `{item['gsc_id']}` | {item['character']} | `{', '.join(item['categories'])}` | "
            f"{'; '.join(item['mand_forms'])} | {'; '.join(item['bs_forms'])} | {', '.join(item['gsr_values'])} |"
        )

    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze current MC disagreement cases in curated entries.")
    parser.add_argument("--input-dir", default=DEFAULT_INPUT_DIR)
    parser.add_argument("--report-out", default=DEFAULT_REPORT_OUT)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    entries = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(Path(args.input_dir).glob("*.json"))
    ]
    report = render_report(analyze_entries(entries))
    Path(args.report_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.report_out).write_text(report, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
