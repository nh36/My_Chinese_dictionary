from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import hierarchy_utils

DEFAULT_TEX_ENTRIES = "data/current_tex_entries.json"
DEFAULT_GSC_IDS = ["18-01", "01-01", "01-67"]
DEFAULT_PACKET_DIR = "data/series_packets"
DEFAULT_CURATION_DIR = "data/entries/curation"
DEFAULT_REPORT_OUT = "reports/hierarchy_gap_analysis.md"


def extract_intermediate_nodes(raw_block: str) -> list[dict[str, str]]:
    return [
        {
            "character_line": node["display_line"],
            "rhs_snippet": node["rhs_snippet"],
        }
        for node in hierarchy_utils.extract_hierarchy_nodes(raw_block)
    ]


def load_packet_lookup(
    *,
    ids: list[str],
    packet_dir: Path,
    curation_dir: Path,
) -> dict[str, dict[str, Any] | None]:
    packets: dict[str, dict[str, Any] | None] = {}
    for entry_id in ids:
        curation_path = curation_dir / f"{entry_id}.json"
        packet_path = packet_dir / f"{entry_id}.json"
        if curation_path.exists():
            packets[entry_id] = {
                "source": "curation",
                "payload": json.loads(curation_path.read_text(encoding="utf-8")),
            }
        elif packet_path.exists():
            packets[entry_id] = {
                "source": "series_packet",
                "payload": json.loads(packet_path.read_text(encoding="utf-8")),
            }
        else:
            packets[entry_id] = None
    return packets


def packet_candidate_summary(packet_wrapper: dict[str, Any] | None) -> tuple[int | None, list[str], bool]:
    if packet_wrapper is None:
        return None, [], False
    payload = packet_wrapper["payload"]
    if packet_wrapper["source"] == "curation":
        candidates = payload.get("proposed_additions", [])
    else:
        candidates = payload.get("candidate_characters", [])
    candidate_keys = sorted(candidates[0].keys()) if candidates else []
    has_parent_field = any(
        "parent" in key or "subseries" in key or "hierarchy" in key for key in candidate_keys
    )
    return len(candidates), candidate_keys, has_parent_field


def render_report(
    entry_ids: list[str],
    tex_entries: dict[str, dict[str, Any]],
    packets: dict[str, dict[str, Any] | None],
) -> str:
    lines = [
        "# Hierarchy gap analysis",
        "",
        "- This report compares the current packet model with hand-done entries that already show explicit internal hierarchy.",
        "- The question is not whether the current pipeline can list the right characters, but whether it can represent intermediate phonetic nodes and subgroup structure.",
        "",
    ]

    for entry_id in entry_ids:
        entry = tex_entries[entry_id]
        packet = packets[entry_id]
        subgroup_nodes = extract_intermediate_nodes(entry["raw_block"])
        packet_candidate_count, _, has_parent_field = packet_candidate_summary(packet)
        packet_source = packet["source"] if packet else None

        lines.extend(
            [
                f"## `{entry_id}`",
                "",
                f"- Original TeX itemize depth: {entry['itemize']['max_depth']}",
                f"- Original TeX subgroup / intermediate-phonetic nodes detected: {len(subgroup_nodes)}",
                f"- Current packet available for direct comparison: {'yes' if packet else 'no'}",
                (
                    f"- Current packet candidate count: {packet_candidate_count}"
                    if packet_candidate_count is not None
                    else "- Current packet candidate count: unavailable"
                ),
                (
                    f"- Packet source layer: `{packet_source}`"
                    if packet_source
                    else "- Packet source layer: unavailable"
                ),
                f"- Packet candidates have explicit parent/subseries fields: {'yes' if has_parent_field else 'no'}",
                "",
                "### Detected intermediate nodes in the hand-done entry",
                "",
            ]
        )

        if subgroup_nodes:
            for node in subgroup_nodes:
                lines.append(f"- `{node['character_line']}` ⇒ `{node['rhs_snippet']}`")
        else:
            lines.append("- None detected by the current heuristic.")

        lines.extend(
            [
                "",
                "### Current packet-model limitation",
                "",
                (
                    "This entry is not yet represented by a packet file, so the current pipeline cannot even attempt a like-for-like reproduction of its hierarchy."
                    if packet is None
                    else "The packet layer can now preserve extracted subgroup heads and candidate-to-parent assignments where evidence allows, but it still needs broader packetization and better assignment coverage before every hand-done series can be reproduced like-for-like."
                ),
                "",
            ]
        )

    lines.extend(
        [
            "## Consequence",
            "",
            "Before broader expansion, the packet schema needs fields such as `parent_phonetic`, `subseries_root`, or `hierarchy_depth`, so that reproduced hand-done entries and newly expanded ones can preserve internal xiesheng structure instead of flattening everything to the top-level head.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compare hand-done entry hierarchy against the current packet model.")
    parser.add_argument("--tex-entries", default=DEFAULT_TEX_ENTRIES)
    parser.add_argument("--packet-dir", default=DEFAULT_PACKET_DIR)
    parser.add_argument("--curation-dir", default=DEFAULT_CURATION_DIR)
    parser.add_argument("--report-out", default=DEFAULT_REPORT_OUT)
    parser.add_argument("--ids", nargs="+", default=DEFAULT_GSC_IDS)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    entries = {
        entry["id"]: entry
        for entry in json.loads(Path(args.tex_entries).read_text(encoding="utf-8"))["entries"]
        if entry["id"] in set(args.ids)
    }
    packets = load_packet_lookup(
        ids=args.ids,
        packet_dir=Path(args.packet_dir),
        curation_dir=Path(args.curation_dir),
    )
    report = render_report(args.ids, entries, packets)
    Path(args.report_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.report_out).write_text(report, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
