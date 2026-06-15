from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_PACKET_DIR = "data/series_packets"
DEFAULT_OUTPUT_DIR = "data/entries/curation"
DEFAULT_IDS = [
    "04-04",
    "02-01",
    "02-32",
    "02-25",
    "03-32",
    "38-03",
    "04-30",
    "03-49",
    "03-57",
    "03-65",
    "04-02",
    "04-12",
    "12-01",
    "05-16",
    "07-14",
    "08-14",
    "08-19",
    "12-10",
    "04-26",
    "04-29",
    "12-08",
    "12-25",
    "11-12",
    "13-22",
    "13-47",
    "13-45",
    "14-14",
    "14-18",
    "16-15",
    "16-20",
    "16-01",
    "16-14",
    "26-38",
    "27-08",
    "32-16",
    "33-30",
    "24-21",
    "24-23",
    "25-15",
    "25-17",
    "25-19",
    "26-27",
    "26-14",
    "28-11",
    "28-15",
    "29-41",
    "24-01",
    "09-01",
    "09-25",
    "09-17",
    "16-06",
    "16-33",
    "03-38",
    "13-32",
    "07-25",
    "07-29",
    "07-08",
    "07-12",
    "04-61",
    "10-39",
    "34-23",
    "32-40",
    "35-01",
    "35-21",
    "18-18",
    "21-01",
    "01-01",
    "01-51",
    "01-43",
]


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
        "mc_resolution": candidate.get("mc_resolution"),
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
        "entry_hierarchy": packet.get("entry_hierarchy"),
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
