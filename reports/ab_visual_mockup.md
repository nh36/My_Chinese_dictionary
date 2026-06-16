# a/b superscript visual mockup

- Mockup source: handwritten snippets from `18-01` and `01-67` in `main.tex`
- Renderer: `scripts/render_ab_visual_mockup.py`
- Final mockup PDF: `build/ab_visual_mockup.pdf`

## Variants checked

1. `current-tabular` — the existing `\textoverset` tabular stack from `main.tex`
2. `overlay-compact`
3. `overlay-balanced`
4. `overlay-airy`

## Chosen variant

- `overlay-balanced`

## Reason

- The current tabular stack sits too high above the vowel and makes the `a/b` marker feel detached from the letter.
- The first lower overlay pass still let the small letter touch the main vowel visually.
- The current chosen pass raises it further than that first overlay and trims the letter slightly so it clears the vowel more decisively.
- `overlay-compact` lifts the mark, but shrinks it a little too much.
- `overlay-airy` clears the vowel, but starts to drift away from it.
- `overlay-balanced` now raises the mark enough to avoid overlap while keeping it close enough to read as part of the phonetic form rather than as a detached annotation.
