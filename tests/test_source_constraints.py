from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import extract_tex_entries  # noqa: E402


class SourceConstraintTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        source_path = ROOT / "main.tex"
        source_text = source_path.read_text(encoding="utf-8")
        cls.entries_data = extract_tex_entries.extract_entries(
            source_text, source_path=str(source_path)
        )

    def test_all_referenced_images_exist(self) -> None:
        asset_dir = ROOT / "hard-character-images"
        available = {path.name for path in asset_dir.glob("*.png")}

        missing = sorted(
            {
                image
                for entry in self.entries_data["entries"]
                for image in entry["image_refs"]
                if image not in available
            }
        )

        self.assertEqual(missing, [])

    def test_mc_forms_are_not_starred(self) -> None:
        starred_forms = sorted(
            {
                mc_form
                for entry in self.entries_data["entries"]
                for mc_form in entry["mc_forms"]
                if mc_form.startswith("*")
            }
        )

        self.assertEqual(starred_forms, [])


if __name__ == "__main__":
    unittest.main()
