from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

import mc_resolution


DEFAULT_INPUT_DIR = "data/entries/curation"
DEFAULT_REPORT_OUT = "reports/mc_disagreement_analysis.md"


def classify_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    resolution = candidate.get("mc_resolution") or mc_resolution.resolve_candidate_mc(candidate)
    mand_forms = resolution["mand2mc_nwh_forms"]
    bs_forms = resolution["bs_gsr_forms"]
    gsr_values = mc_resolution.dedupe(
        [row.get("gsr") for row in candidate.get("mand2mc_rows", []) if row.get("gsr")]
        + [row.get("gsr") for row in candidate.get("bs_gsr_rows", []) if row.get("gsr")]
    )

    categories: list[str] = []
    if len(mand_forms) > 1:
        categories.append("mand2mc-multiple")
    if len(bs_forms) > 1:
        categories.append("bs-gsr-multiple")
    if resolution["bs_not_in_mand2mc"]:
        categories.append("bs-not-in-mand2mc")
    if resolution["mand2mc_not_in_bs_gsr"]:
        categories.append("mand2mc-extra-vs-bs")

    return {
        "character": candidate["character"],
        "categories": categories,
        "mand_forms": mand_forms,
        "bs_forms": bs_forms,
        "gsr_values": gsr_values,
        "mc_resolution": resolution,
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
            "- The pilot should now render Mand2MC-derived MC forms without a visible inline warning.",
            "- `bs-not-in-mand2mc` is the only case that should force investigation: it means BS/GSR has an MC reading whose Baxter-Sagart form is absent from Mand2MC.",
            "- `mand2mc-extra-vs-bs` is not by itself a conflict; it means Mand2MC preserves extra readings not reflected in the BS/GSR extraction.",
            "- `mand2mc-multiple` usually means Mand2MC contains multiple MC readings for the same graph, which may reflect real polyphony rather than an error.",
            "- `bs-gsr-multiple` means the BS/GSR PDF lists multiple MC values for the same graph.",
            "",
            "## Suggested resolution workflow",
            "",
            "1. Render from Mand2MC when it provides an MC form.",
            "2. Preserve all BS/GSR rows in packet evidence even when they do not affect rendering.",
            "3. Investigate only the cases where BS/GSR has a reading absent from Mand2MC, using Guangyun / fanqie where the discrepancy matters editorially.",
            "",
            "## Detailed cases",
            "",
            "| GSC | Character | Categories | Mand2MC MC | BS/GSR MC | BS not in Mand2MC | Mand2MC extra vs BS | GSR values |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )

    for item in results:
        lines.append(
            f"| `{item['gsc_id']}` | {item['character']} | `{', '.join(item['categories'])}` | "
            f"{'; '.join(item['mand_forms'])} | {'; '.join(item['bs_forms'])} | "
            f"{'; '.join(item['mc_resolution']['bs_not_in_mand2mc'])} | "
            f"{'; '.join(item['mc_resolution']['mand2mc_not_in_bs_gsr'])} | "
            f"{', '.join(item['gsr_values'])} |"
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
