from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_PACKET_DIR = "data/series_packets"
DEFAULT_OUTPUT_DIR = "data/entries/curation"
DEFAULT_IDS = ["02-01", "38-03", "04-30", "18-18", "01-01", "01-43"]


def load_packet(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def summarize_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "character": candidate["character"],
        "in_tex": candidate["in_tex"],
        "mand2mc_count": len(candidate["mand2mc_rows"]),
        "bs_gsr_count": len(candidate["bs_gsr_rows"]),
        "shengfu_character_count": len(candidate["shengfu_character_rows"]),
        "shengfu_component_count": len(candidate["shengfu_component_rows"]),
        "mand_bs_mc_disagreement": candidate["mand_bs_mc_disagreement"],
        "mand2mc_rows": candidate["mand2mc_rows"],
        "bs_gsr_rows": candidate["bs_gsr_rows"],
        "shengfu_character_rows": candidate["shengfu_character_rows"],
        "shengfu_component_rows": candidate["shengfu_component_rows"],
    }


def promote_packet(packet: dict[str, Any]) -> dict[str, Any]:
    candidate_characters = packet["candidate_characters"]
    proposed_additions = [item for item in candidate_characters if not item["in_tex"]]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "id": packet["gsc_id"],
        "status": "machine-curated-pilot",
        "packet_kind": packet["packet_kind"],
        "schuessler": packet["schuessler"],
        "coverage": packet["coverage"],
        "tex_entry": packet["tex_entry"],
        "candidate_source_strategy": packet["candidate_source_strategy"],
        "candidate_source_tokens": packet["candidate_source_tokens"],
        "proposed_additions": [summarize_candidate(item) for item in proposed_additions],
        "all_candidates": [summarize_candidate(item) for item in candidate_characters],
        "notes": [
            "Machine-promoted from a series packet; not yet hand-checked.",
            "Use this file as the staging area for editorial decisions before any merge into main.tex.",
        ],
    }


def write_promoted_entry(entry: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"{entry['id']}.json").write_text(
        json.dumps(entry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Promote series packets into curated entry JSON files.")
    parser.add_argument("--packet-dir", default=DEFAULT_PACKET_DIR)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--ids", nargs="+", default=DEFAULT_IDS)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    for gsc_id in args.ids:
        packet = load_packet(Path(args.packet_dir) / f"{gsc_id}.json")
        promoted = promote_packet(packet)
        write_promoted_entry(promoted, Path(args.output_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
