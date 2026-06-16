from __future__ import annotations

import re
import shutil
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PDF_PATH = ROOT / "build" / "generated_curated_series_sample.pdf"
TEX_PATH = ROOT / "build" / "generated_curated_series_sample.tex"
WORD_RE = re.compile(
    r'<word xMin="([0-9.]+)" yMin="([0-9.]+)" xMax="([0-9.]+)" yMax="([0-9.]+)">([^<]+)</word>'
)
PAGE_DIM_RE = re.compile(r'width="([0-9.]+)" height="([0-9.]+)"')
ENTRY_ID_RE = re.compile(r"^\d{2}-\d{2}$")
TEX_ENTRY_ID_RE = re.compile(r"\\paragraph\{\\textoversetlarge\{(\d{2}-\d{2})\}")


def parse_pdf_layout(pdf_path: Path) -> list[dict[str, object]]:
    text = subprocess.run(
        ["pdftotext", "-bbox-layout", str(pdf_path), "-"],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    ).stdout
    pages: list[dict[str, object]] = []
    for page_index, chunk in enumerate(text.split("<page ")[1:], start=1):
        dims = PAGE_DIM_RE.search(chunk)
        if not dims:
            continue
        width, height = map(float, dims.groups())
        words = WORD_RE.findall(chunk)
        left_words = []
        right_words = []
        left_ids = []
        right_ids = []
        for x_min, y_min, x_max, y_max, word in words:
            x_center = (float(x_min) + float(x_max)) / 2
            target_words = left_words if x_center < width / 2 else right_words
            target_words.append((float(y_min), float(y_max), word))
            if ENTRY_ID_RE.fullmatch(word):
                target_ids = left_ids if x_center < width / 2 else right_ids
                target_ids.append((word, float(y_min)))
        left_ids.sort(key=lambda item: item[1])
        right_ids.sort(key=lambda item: item[1])
        pages.append(
            {
                "page_number": page_index,
                "height": height,
                "left_max_y": max((y_max for _, y_max, _ in left_words), default=0.0),
                "right_max_y": max((y_max for _, y_max, _ in right_words), default=0.0),
                "left_ids": left_ids,
                "right_ids": right_ids,
            }
        )
    return pages


def estimate_first_entry_height(page: dict[str, object], column: str) -> float | None:
    ids = page[f"{column}_ids"]  # type: ignore[index]
    max_y = page[f"{column}_max_y"]  # type: ignore[index]
    if not ids:
        return None
    ids = list(ids)  # type: ignore[assignment]
    start_y = ids[0][1]
    if len(ids) >= 2:
        return ids[1][1] - start_y
    return max_y - start_y  # type: ignore[operator]


class PilotLayoutDensityTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which("pdftotext"), "requires pdftotext")
    def test_pdf_preserves_entry_order_in_two_column_reading_order(self) -> None:
        expected_ids = TEX_ENTRY_ID_RE.findall(TEX_PATH.read_text(encoding="utf-8"))
        pages = parse_pdf_layout(PDF_PATH)
        observed_ids: list[str] = []
        for page in pages:
            observed_ids.extend(entry_id for entry_id, _ in page["left_ids"])  # type: ignore[index]
            observed_ids.extend(entry_id for entry_id, _ in page["right_ids"])  # type: ignore[index]
        self.assertEqual(observed_ids, expected_ids)

    @unittest.skipUnless(shutil.which("pdftotext"), "requires pdftotext")
    def test_later_pages_do_not_leave_half_empty_columns_when_next_short_entry_fits(self) -> None:
        pages = parse_pdf_layout(PDF_PATH)
        self.assertGreater(len(pages), 3)
        tolerance = 36.0
        for index, page in enumerate(pages[1:-1], start=1):
            page_height = page["height"]  # type: ignore[index]
            half_page = page_height / 2
            left_blank = page_height - page["left_max_y"]  # type: ignore[index]
            right_blank = page_height - page["right_max_y"]  # type: ignore[index]

            right_first_height = estimate_first_entry_height(page, "right")
            if right_first_height is not None and left_blank > half_page:
                self.assertGreater(
                    right_first_height + tolerance,
                    left_blank,
                    f"Page {page['page_number']} leaves too much blank space in the left column before a short right-column entry.",
                )

            next_left_height = estimate_first_entry_height(pages[index + 1], "left")
            if next_left_height is not None and right_blank > half_page:
                self.assertGreater(
                    next_left_height + tolerance,
                    right_blank,
                    f"Page {page['page_number']} leaves too much blank space in the right column before the next page's short left-column entry.",
                )


if __name__ == "__main__":
    unittest.main()
