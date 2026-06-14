from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_INPUT = "data/current_tex_entries.json"
DEFAULT_OUTPUT = "data/entries/sample_entries.json"
DEFAULT_IDS = [
    "18-01",
    "18-04",
    "18-05",
    "19-18",
    "19-22",
    "01-30",
    "01-38",
    "01-43",
    "01-57",
    "01-67",
]


def load_entries(input_path: Path) -> list[dict]:
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    return payload["entries"]


def select_entries(entries: list[dict], selected_ids: list[str]) -> list[dict]:
    entries_by_id = {entry["id"]: entry for entry in entries}
    missing = [entry_id for entry_id in selected_ids if entry_id not in entries_by_id]
    if missing:
        raise ValueError(f"Sample entry IDs not found in extracted entries: {', '.join(missing)}")
    return [entries_by_id[entry_id] for entry_id in selected_ids]


def project_sample_entry(entry: dict) -> dict:
    return {
        "id": entry["id"],
        "section": entry["section"],
        "subsection": entry["subsection"],
        "head": entry["head"],
        "source": {
            "tex_start_line": entry["start_line"],
            "tex_end_line": entry["end_line"],
            "line_count": entry["line_count"],
        },
        "characters": entry["chinese_characters"],
        "commented_pinyin": entry["commented_pinyin"],
        "mc_forms": entry["mc_forms"],
        "gsr_markers": entry["gsr_markers"],
        "image_refs": entry["image_refs"],
        "itemize": entry["itemize"],
        "context_environments": entry.get("context_environments", []),
        "raw_latex": entry["raw_block"],
        "status": "sample-extracted",
    }


def build_sample_payload(entries: list[dict], selected_ids: list[str]) -> dict:
    selected_entries = select_entries(entries, selected_ids)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "entry_ids": selected_ids,
        "entries": [project_sample_entry(entry) for entry in selected_entries],
    }


def write_sample_payload(payload: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Export a controlled sample of extracted TeX entries.")
    parser.add_argument("--input", default=DEFAULT_INPUT, help="Path to current_tex_entries.json.")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Path to sample entry JSON.")
    parser.add_argument(
        "--ids",
        nargs="+",
        default=DEFAULT_IDS,
        help="Entry IDs to include in the sample.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    payload = build_sample_payload(load_entries(Path(args.input)), list(args.ids))
    write_sample_payload(payload, Path(args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
