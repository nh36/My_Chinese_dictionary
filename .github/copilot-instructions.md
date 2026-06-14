# Copilot instructions for this repository

## Build

- Primary build: `latexmk -xelatex main.tex`
- Clean generated LaTeX build artifacts: `latexmk -c`
- Run the current inventory tooling: `python3 scripts/inventory_tex.py`
- Run the current entry extractor: `python3 scripts/extract_tex_entries.py`
- Run the current TeX-derived report builder: `python3 scripts/build_tex_reports.py`
- Run the Mand2MC importer: `python3 scripts/import_mand2mc.py`
- Run the Shengfu importer: `python3 scripts/import_shengfu.py`
- Run the BS/GSR PDF importer: `python3 scripts/import_bs_gsr_pdf.py`
- Run the spreadsheet comparison reports: `python3 scripts/compare_sources.py`
- Run the coverage-model builder: `python3 scripts/build_coverage_model.py`
- Export hand-checkable series packets: `python3 scripts/export_series_packets.py`
- Promote series packets into curation files: `python3 scripts/promote_series_packets.py`
- Render curated pilot packets: `python3 scripts/render_curated_series.py`
- Export the controlled sample entries: `python3 scripts/export_sample_entries.py`
- Render the controlled sample entries: `python3 scripts/render_entries.py`
- Run the current tests: `python3 -m unittest`
- Run a single test: `python3 -m unittest tests.test_inventory_tex.InventoryTexTests.test_collect_inventory_from_sample`
- There is no repository-local lint target in the current checkout.
- `main.tex` depends on XeLaTeX and the fonts named in the preamble, especially `BabelStone Han`, `FreeSerif`, `FreeSans`, `FreeMono`, `Tibetan Machine Uni`, `Charis SIL`, and `Padauk`. Those fonts are installed in the current environment and `latexmk -xelatex main.tex` succeeds.
- Spreadsheet import tooling relies on `pandas`, `openpyxl` for `.xlsx`, and `odfpy` for `.ods`; they are declared in `requirements.txt`.

## High-level architecture

- `main.tex` is the authoritative source. It is a single, hand-edited XeLaTeX document that combines document setup, the semantic-component inventory, and the dictionary itself.
- The document has three major logical sections: `Semantic components`, `Semantics still to alphabetize`, and `The dictionary itself`.
- The dictionary section is hierarchical. It is organized first by phonological subsections such as `-ay` and `-a`, then by paragraph entries headed with `\textoversetlarge{GSC series number}{head graph}`. Those paragraph numbers are GSC series identifiers, not GSR item numbers.
- Nested `itemize` blocks inside an entry are part of the scholarly model: they mark subseries and sub-subseries, often where one derived graph becomes a new phonetic base. Do not treat that nesting as disposable formatting.
- `asia.bib` supplies bibliography data for the document. `AGENTS.md` and `conceptual.md` are the project-level guidance documents: `AGENTS.md` describes the intended safe automation workflow, while `conceptual.md` explains the editorial and phonological logic behind the current LaTeX structure.
- `scripts/inventory_tex.py` is the first safe inspection tool around the LaTeX source. It inventories sections, subsections, paragraph entries, image references, `\textit{...}` MC forms, GSR-like markers, commented pinyin, and nested `itemize` depth, then writes `data/current_tex_inventory.json` and `reports/current_inventory.md`.
- `scripts/extract_tex_entries.py` builds on the inventory pass and writes `data/current_tex_entries.json`. Each extracted entry retains section/subsection context, line ranges, head data, raw LaTeX block/body, Chinese characters, commented pinyin, MC forms, GSR-like markers, image references, and itemize-depth events.
- `scripts/build_tex_reports.py` generates report files from the extracted entry data. The current tex-only reports are `reports/tex_entries_by_gsr.md`, `reports/tex_entries_without_gsr.md`, `reports/rare_glyphs_and_images.md`, and `reports/semantic_labels_used_in_tex.md`.
- `scripts/import_mand2mc.py` and `scripts/import_shengfu.py` are the spreadsheet-ingestion entry points. They preserve raw sheet columns, add explicit `source_row_number` / `source_sheet_name`, append normalized helper columns, and write CSV plus Markdown import reports.
- `scripts/import_bs_gsr_pdf.py` imports `key references/Reconstructions in GSR order.pdf` via `pdftotext -layout` into `data/derived/bs_gsr.csv` and writes `reports/import_bs_gsr_pdf.md`.
- In the current checkout, the real spreadsheet source files live under `key references/`, and the importer defaults are pointed there.
- `scripts/compare_sources.py` consumes `data/current_tex_entries.json` plus derived CSVs and generates spreadsheet-backed comparison reports (`mand2mc_rows_not_in_tex.md`, `tex_forms_conflicting_with_mand2mc.md`, and `shengfu_groups_missing_from_tex.md`).
- `scripts/build_coverage_model.py` combines TeX entries, Mand2MC, Shengfu, BS/GSR, and the Schuessler PDF series universe to produce `data/derived/character_coverage.csv`, `data/derived/gsc_series_coverage.csv`, and the expansion reports `gsc_series_coverage.md`, `missing_gsc_rhymes_and_series.md`, and `expansion_work_queue.md`.
- `scripts/export_series_packets.py` turns one or more target GSC series into hand-checkable curation packets in `data/series_packets/` and `reports/series_packets/`.
- `scripts/promote_series_packets.py` promotes those packets into working series files under `data/entries/curation/`.
- `scripts/render_curated_series.py` renders curated pilot packets into a review document in `build/generated_curated_series_sample.tex` / `.pdf`.
- `scripts/export_sample_entries.py` builds a curated representative sample from `data/current_tex_entries.json` and writes `data/entries/sample_entries.json`.
- `scripts/render_entries.py` renders that sample back to `build/generated_entries_sample.tex` and `build/generated_main_sample.tex` with explicit generated-file warnings.
- The checked-in reference PDFs and spreadsheet inputs live under `key references/`. The active importer defaults point at `key references/Mand2MC2009-06-08 copy.ods`, `key references/声符级别-2022.06.07.xlsx`, and `key references/Reconstructions in GSR order.pdf`.
- Rare glyphs are a mixed asset model: many characters are direct Unicode in `main.tex`, but some heads and members are PNGs included with `\includegraphics`. The checked-in glyph assets are currently in `hard-character-images/`, and `main.tex` now includes that directory in `\graphicspath`.

## Key conventions

- Treat `main.tex` as the source of truth for Nathan Hill's hand-checked editorial decisions. Do not silently overwrite its forms, labels, or structure from external data.
- Preserve Nathan Hill's transcription systems exactly. Middle Chinese forms normally appear in `\textit{...}` and are attested/transcribed forms, so they should **not** be starred. If other systems appear in comments or future imports, keep them in separate fields instead of normalizing over Nathan's form.
- Preserve Unicode and specialist diacritics exactly, especially non-BMP Chinese characters and forms such as `ṅ`, `ḫ`, `ṭ`, `ḍ`, `ṇ`, `ś`, `ź`, and `ñ`. Do not replace rare-glyph PNGs with Unicode or a different font automatically.
- Treat LaTeX comments as data. In `main.tex`, `%` comments frequently carry pinyin, Baxter-style Middle Chinese, GSR numbers, and editorial notes that future tooling must preserve.
- Keep identifier types distinct. A paragraph heading like `18-01` or `01-67` is a GSC series number; inline values such as `0001a` or `0102n` are GSR-style item identifiers; future spreadsheet row numbers or Unicode code points should remain separate fields.
- Semantic-component notation is meaningful and must stay reversible. Prefix forms such as `\textsuperscript{hom·}qay`, suffix forms such as `qay\textsuperscript{·dehab}`, colon variants such as `\textsuperscript{bamb:}qay`, doubled values like `qay:qay`, numbered values like `pa₂`, and `\textoverset{...}{...}` / `\textunderset{...}{...}` forms all encode analysis, not just presentation.
- Preserve compact typesetting choices unless the task is specifically about layout. `multicols`, `spacing{0.7}`, paragraph-head macros, and inline footnotes are used to fit a dense scholarly dictionary, so avoid broad reformatting of `main.tex`.
- Prefer incremental, reviewable changes. Do not flatten nested entry structure, replace the whole LaTeX document with generated output, or rewrite the document just to make parsing easier.
- When adding tooling, keep the first pass conservative: preserve raw LaTeX alongside parsed fields, and prefer reports and inventories over automatic rewrites.
- The test suite encodes repository-specific safety rules: every referenced PNG should exist in `hard-character-images/`, and extracted Middle Chinese forms should never begin with `*`.
- The project goal now includes expansion, not only reproduction: use the coverage outputs to target missing GSC series, missing rhyme sections, and source-backed characters not yet represented in `main.tex`.
- The next working unit is a `series packet`, not a whole-document rewrite: gather all evidence for one GSC series, review it, then promote it into `data/entries/curation/` before attempting broader dictionary generation.
