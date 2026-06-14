# AGENTS.md — coding-agent handoff for Nathan Hill's Chinese dictionary project

## Project goal

This repository is for producing Nathan Hill's Chinese dictionary in transliteration. The present state is a hand-written XeLaTeX document with supporting images and several data sources. The next stage should make the project data-driven enough that Nathan can add, check, sort, and regenerate dictionary entries without hand-editing thousands of lines of LaTeX.

The immediate goal is not to redesign the dictionary intellectually. Preserve Nathan's existing editorial decisions and notation while building tooling that makes further progress faster and safer.

## Current source files to expect

At the time of this handoff the uploaded project/data consisted of:

- `My_Chinese_dictionary.zip`
  - Contains `main.tex`, `asia.bib`, and PNG glyph images.
  - `main.tex` is about 4,020 lines and is currently the most important source of Nathan's editorial decisions.
  - It uses XeLaTeX and fonts such as `BabelStone Han`, `FreeSerif`, `FreeSans`, `FreeMono`, `Tibetan Machine Uni`, `Charis SIL`, and `Padauk`.
  - It has these major sections: `Semantic components`, `Semantics still to alphabetize`, and `The dictionary itself`.
  - The dictionary currently has subsections such as `-ay` and `-a`, and around 127 `\paragraph` entries.
  - Rare glyphs are sometimes inserted through PNG files such as `U+26760.png`, `U+27D2A.png`, `甫.png`, `布.png`, `父.png`, and related files.
- `Mand2MC2009-06-08 copy.ods`
  - Spreadsheet with a Mandarin-to-Middle-Chinese mapping.
  - Main sheet is `Feuil1` with roughly 9,261 rows.
  - Columns include character, `pinyin`, `MC (NWH)`, `MC (B&S)`, `GSR`, `漢語大字典`, `廣韻`, and an unnamed final column.
  - `Feuil2` contains correction or uncertainty notes for individual forms.
- `声符级别-2022.06.07.xlsx`
  - Spreadsheet on phonophoric / sound-symbol level data.
  - Main sheet is `Sheet1` with roughly 18,657 rows.
  - Main columns include `序号`, `字`, `声符`, `声符级别`, `次級聲符`, `應注`, `反切`, `声`, `韵`, `调`, `呼`, `来源`, `韵部`, `上古声`, `上古韵`, `上古音节`, notes, original sequence, and rhyme annotations.
- `Reconstructions in GSR order.pdf`
  - Baxter-Sagart Old Chinese reconstruction table, version of 20 February 2011, ordered by *Grammata Serica Recensa* number.
  - Columns include character, pinyin, MC, analyzed MC, OC, gloss, GSR, and Unicode.
  - Treat the PDF as an important reference source, but prefer machine-readable extraction only when it can be validated. Do not silently import OCR errors.

## Non-negotiable scholarly conventions

- Preserve Nathan's existing notation unless Nathan explicitly asks for a change.
- Do not silently correct Chinese characters, Middle Chinese forms, Old Chinese forms, GSR numbers, semantic labels, or glosses.
- Middle Chinese forms are attested forms and should not be starred.
- Use an asterisk only at the beginning of reconstructed forms, never at the end and never surrounding the form.
- Use Baxter & Sagart forms and conventions carefully. If an automated import conflicts with Nathan's hand-edited `main.tex`, flag the conflict instead of overwriting Nathan's version.
- Preserve Unicode exactly. Normalize only when the normalization policy is explicit and tested. Be especially careful with non-BMP characters and rare Chinese glyphs.
- Do not convert between simplified and traditional Chinese unless a task explicitly asks for it.
- Keep Nathan's Latin semantic-component labels, including abbreviations such as `hom`, `arb`, `bamb`, `dic`, `or`, `tum`, `herb`, `gem`, etc.
- Preserve the distinction between semantic prefixes/suffixes and phonological/root material. For example, structures like `\textsuperscript{hom·}qay`, `qay\textsuperscript{·dehab}`, and `qay:qay` are meaningful and should not be flattened without a reversible representation.

## Immediate coding-agent mission

Build a safe, incremental pipeline around the current LaTeX rather than doing a destructive rewrite.

### Phase 0: make the current project reproducible

1. Unpack `My_Chinese_dictionary.zip` into the repository root, unless the files are already present.
2. Add a `README.md` with minimal build instructions.
3. Try to compile `main.tex` with XeLaTeX, preferably via `latexmk -xelatex main.tex`.
4. Record exact build errors in `docs/build-notes.md`.
5. If missing fonts prevent compilation, do not change the document content. Add font-installation notes and optionally a local development fallback that is clearly marked as a fallback.
6. Do not remove packages such as `tabu` merely because they are old. First get a faithful build, then modernize separately if needed.

Definition of done for Phase 0: a fresh checkout can either compile the existing document or fails with documented, actionable dependency errors.

### Phase 1: inventory and preserve the hand-written dictionary

Create scripts that inspect `main.tex` without changing it.

Suggested files:

- `scripts/inventory_tex.py`
- `scripts/extract_tex_entries.py`
- `data/current_tex_inventory.json`
- `data/current_tex_entries.json`

The extractor should capture at least:

- section and subsection context, e.g. `-ay`, `-a`;
- paragraph heading number, e.g. `18-01`, `01-30`;
- head character or image reference;
- raw LaTeX body for the entry;
- all Chinese characters found in the entry;
- commented pinyin values, e.g. `%wu3`;
- Middle Chinese forms in `\textit{...}`;
- GSR-like comments, e.g. `%0001a`;
- image references;
- nested `itemize` structures if possible.

Keep raw LaTeX alongside parsed fields. The first parser does not need to understand everything, but it must never discard content.

Definition of done for Phase 1: the script can regenerate a JSON inventory and reports counts of sections, subsections, entries, images, Chinese characters, MC forms, and GSR markers.

### Phase 2: load the external data sources into stable tables

Create import scripts for the two spreadsheets and, if feasible, a validated extraction of the PDF table.

Suggested files:

- `scripts/import_mand2mc.py`
- `scripts/import_shengfu.py`
- `scripts/import_bs_gsr_pdf.py` only if extraction is reliable
- `data/derived/mand2mc.parquet` or `.csv`
- `data/derived/shengfu.parquet` or `.csv`
- `data/derived/bs_gsr.csv` only after validation

Requirements:

- Use UTF-8 output.
- Preserve original column names in a raw layer.
- Add normalized helper columns separately rather than replacing original columns.
- Keep source row numbers.
- Keep all rows, including rows with missing pinyin or missing GSR.
- Validate row counts.
- Write an import report for each source in `reports/`.
- For the PDF, spot-check extraction against visible pages before trusting it. Tables with rare glyphs and phonological symbols are easy to corrupt.

Definition of done for Phase 2: the imports can be rerun from scratch and produce stable row counts and summary reports.

### Phase 3: build cross-reference reports, not automatic rewrites

Before generating any new dictionary entries, build reports that help Nathan see what is missing or inconsistent.

Suggested reports:

- `reports/tex_entries_by_gsr.md`
- `reports/tex_entries_without_gsr.md`
- `reports/mand2mc_rows_not_in_tex.md`
- `reports/tex_forms_conflicting_with_mand2mc.md`
- `reports/shengfu_groups_missing_from_tex.md`
- `reports/rare_glyphs_and_images.md`
- `reports/semantic_labels_used_in_tex.md`

Important policy: all conflict reports should show both sides and avoid choosing a winner automatically.

Definition of done for Phase 3: Nathan can open Markdown reports and decide which entries to add, check, or correct.

### Phase 4: introduce a canonical data model

Once the inventory and reports are stable, introduce a small canonical data format. YAML is probably easiest for Nathan to read and edit; SQLite or Parquet can be used for derived data.

A possible entry schema:

```yaml
id: "01-30"
section: "-a"
head:
  type: character
  value: "午"
root: "ṅa"
items:
  - char: "午"
    pinyin: "wu3"
    transliteration_latex: "ṅa"
    mc_nwh: "ṅuX"
    mc_bs: "nguX"
    gsr: "0060a"
    semantic:
      position: none
      label: null
    source:
      tex_line: null
      mand2mc_row: null
      shengfu_row: null
    notes: []
  - char: "仵"
    pinyin: "wu3"
    transliteration_latex: "{\\textsuperscript{hom·}}ṅa"
    mc_nwh: "ṅuH"
    mc_bs: "nguH"
    gsr: "0060f"
    semantic:
      position: prefix
      label: "hom"
    notes: []
raw_latex: "..."
status: hand_checked
```

This schema is only a starting point. Improve it after extracting real entries, especially because the existing LaTeX uses nested groupings and equations such as `=`, `:`, semantic prefixes, semantic suffixes, and vowel annotations with `\textoverset{...}{...}`.

Definition of done for Phase 4: a sample of 10 varied entries can be represented losslessly enough that the generated LaTeX is visually and textually comparable to the hand-written version.

### Phase 5: generate LaTeX from data, but only for a controlled subset

Add a generator, e.g. `scripts/render_entries.py`, that can render selected YAML entries back to LaTeX.

Start with a tiny subset:

- `可`
- `午`
- one entry using an image glyph
- one entry with nested `itemize`
- one entry with semantic suffix notation
- one entry with multiple MC readings for the same character

Do not replace the entire `main.tex` at once. Generate a separate file such as:

- `build/generated_entries_sample.tex`
- `build/generated_main_sample.tex`

Then compare against the original.

Definition of done for Phase 5: there is a documented sample showing original LaTeX, generated LaTeX, and any deliberate differences.

## Suggested repository layout

```text
.
├── AGENTS.md
├── README.md
├── main.tex
├── asia.bib
├── images/                  # optional target location for PNG glyphs
├── data/
│   ├── raw/                 # original spreadsheets/PDF if licensing permits
│   ├── derived/             # generated CSV/Parquet/JSON
│   └── entries/             # future hand-editable YAML entries
├── scripts/
│   ├── inventory_tex.py
│   ├── extract_tex_entries.py
│   ├── import_mand2mc.py
│   ├── import_shengfu.py
│   ├── compare_sources.py
│   └── render_entries.py
├── reports/
├── docs/
│   ├── build-notes.md
│   ├── notation.md
│   └── data-model.md
└── tests/
```

## Testing requirements

Add tests as soon as scripts exist. Useful tests include:

- Unicode round-trip tests for non-BMP characters.
- Parsing tests for `\textoversetlarge`, `\textoverset`, `\textsuperscript`, `\textit`, and `\includegraphics`.
- Row-count tests for spreadsheet imports.
- Snapshot tests for selected generated LaTeX entries.
- A test that no MC form is accidentally prefixed with `*`.
- A test that reconstructed forms, where represented as reconstructions, have any asterisk only at the beginning.
- A test that every referenced image exists.
- A test that every generated file includes a warning header saying it is generated and should not be hand-edited.

## Practical implementation notes

- Python is a good default for the tooling.
- Use `openpyxl` for `.xlsx` files.
- Use `pandas` with `odfpy` or another reliable reader for `.ods` files.
- Use `regex` rather than plain `re` where Unicode character classes are helpful.
- Use `lxml`, `BeautifulSoup`, or explicit tokenization only if simple regex parsing becomes too brittle.
- Avoid building a full LaTeX parser unless necessary. A conservative extractor that preserves raw blocks is safer.
- Treat `%` comments in `main.tex` as data. They often hold pinyin, Baxter-Sagart MC, GSR numbers, or reminders.
- Preserve line endings and encodings.
- Prefer generated reports over in-place edits.

## What not to do

- Do not replace `main.tex` with generated output until Nathan has approved the generator on a meaningful sample.
- Do not silently change notation to a different reconstruction system.
- Do not use OCR output from the PDF as if it were clean data.
- Do not delete rare-glyph PNGs because a system font appears to contain the character.
- Do not reformat the whole LaTeX file as a first step. It will make scholarly diffs impossible to review.
- Do not create a web app unless Nathan specifically asks for one. The first deliverable is a reliable scholarly data/build pipeline.
- Do not hide conflicts by taking the most recent source automatically. Show conflicts in reports.

## First concrete task list for the agent

1. Create the repository layout above without moving scholarly content unnecessarily.
2. Unpack the zip if needed and ensure `main.tex`, `asia.bib`, and the PNGs are present.
3. Write `docs/build-notes.md` after attempting a XeLaTeX build.
4. Write `scripts/inventory_tex.py` and generate `reports/current_inventory.md`.
5. Write import scripts for the `.ods` and `.xlsx` files and generate row-count reports.
6. Write a comparison report aligning `main.tex` entries with `Mand2MC` by character plus GSR where possible.
7. Stop and summarize what is currently hand-authored, what is available in source data, and what is missing.

## Expected first pull request

The first pull request should contain infrastructure and reports only:

- `README.md`
- `docs/build-notes.md`
- `scripts/inventory_tex.py`
- `scripts/import_mand2mc.py`
- `scripts/import_shengfu.py`
- `reports/current_inventory.md`
- `reports/import_mand2mc.md`
- `reports/import_shengfu.md`
- minimal tests

It should not contain wholesale changes to `main.tex`.

## Guiding principle

Make Nathan faster by making the existing dictionary inspectable, searchable, and regenerable in small controlled pieces. The project needs a reliable pipeline and conflict reports before it needs a grand rewrite.
