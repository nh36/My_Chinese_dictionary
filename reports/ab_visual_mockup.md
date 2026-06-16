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
- `overlay-compact` is closer, but a little too small and easy to miss.
- `overlay-airy` is clearer than the current stack, but still slightly too elevated.
- `overlay-balanced` keeps the mark legible while holding it close enough to the vowel that it reads as part of the phonetic form rather than as a separate annotation.
