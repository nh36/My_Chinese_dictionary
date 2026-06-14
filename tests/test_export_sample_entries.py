from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import export_sample_entries  # noqa: E402


SAMPLE_ENTRIES = [
    {"id": "18-01", "section": "The dictionary itself", "subsection": "-ay", "head": {"type": "character"}, "start_line": 10, "end_line": 20, "line_count": 11, "chinese_characters": ["可"], "commented_pinyin": ["ke3"], "mc_forms": ["khaX"], "gsr_markers": ["0001a"], "image_refs": [], "itemize": {"block_count": 0, "max_depth": 0, "events": []}, "context_environments": [], "raw_block": "\\paragraph{...}"},
    {"id": "01-67", "section": "The dictionary itself", "subsection": "-a", "head": {"type": "character_with_image"}, "start_line": 30, "end_line": 40, "line_count": 11, "chinese_characters": ["父"], "commented_pinyin": ["fu4"], "mc_forms": ["biuX"], "gsr_markers": ["0102a"], "image_refs": ["父.png"], "itemize": {"block_count": 1, "max_depth": 1, "events": []}, "context_environments": [{"name":"multicols","arg":"2"}], "raw_block": "\\paragraph{...父...}"},
]


class ExportSampleEntriesTests(unittest.TestCase):
    def test_build_sample_payload(self) -> None:
        payload = export_sample_entries.build_sample_payload(SAMPLE_ENTRIES, ["01-67", "18-01"])

        self.assertEqual(payload["entry_ids"], ["01-67", "18-01"])
        self.assertEqual(payload["entries"][0]["id"], "01-67")
        self.assertEqual(payload["entries"][0]["source"]["tex_start_line"], 30)
        self.assertEqual(payload["entries"][1]["status"], "sample-extracted")
        self.assertEqual(payload["entries"][0]["context_environments"][0]["name"], "multicols")

    def test_write_sample_payload(self) -> None:
        payload = export_sample_entries.build_sample_payload(SAMPLE_ENTRIES, ["18-01"])

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "sample_entries.json"
            export_sample_entries.write_sample_payload(payload, output_path)

            written = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(written["entries"][0]["id"], "18-01")


if __name__ == "__main__":
    unittest.main()
