# Build notes

## Current build command

```sh
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

## Current result

In this environment, the build now succeeds:

```sh
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

The successful local run still emitted a few warnings, including:

- a `biblatex` option-conflict warning;
- a `bookmark` driver warning for XeTeX;
- an `xeCJK` warning about `\CJKsfdefault`;
- a `BabelStone Han` bold-shape substitution warning;
- a `multicol` footnote-placement warning;
- one underfull `\hbox`.

## Fonts referenced by `main.tex`

- `BabelStone Han`
- `FreeSerif`
- `FreeSans`
- `FreeMono`
- `Tibetan Machine Uni`
- `Charis SIL`
- `Padauk`

These fonts are now installed and visible to XeTeX in the current environment.

## Glyph image path note

The checked-in PNG glyph assets are currently stored in `hard-character-images/`.

`main.tex` originally searched only `images/` and `../images/`. The `\graphicspath` declaration has been widened to include `hard-character-images/` first so that the current asset layout is usable without moving the scholarly source files or renaming the PNGs.

## Current repository-state notes

- `main.tex` is the current source of truth.
- `My_Chinese_dictionary.pdf` is a legacy prebuilt artifact/reference; the generated review PDF to inspect for rhyme-section breaks is `build/generated_curated_series_sample.pdf` (or open it with `python3 scripts/open_review_pdf.py`).
- The spreadsheet inputs are now present under `key references/`, and the import/comparison scripts have been run against them.
