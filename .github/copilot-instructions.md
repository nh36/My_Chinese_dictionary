# Copilot instructions for this repository

## Build, test, and lint commands

- Install Python dependencies: `python3 -m pip install -r requirements.txt`
- Build the authoritative dictionary: `latexmk -xelatex main.tex`
- Clean LaTeX build artifacts: `latexmk -c`
- Run the full test suite: `python3 -m unittest`
- Run a single test: `python3 -m unittest tests.test_inventory_tex.InventoryTexTests.test_collect_inventory_from_sample`
- Run a focused pilot regression: `python3 -m unittest tests.test_pilot_regressions.PilotRegressionTests.test_current_pilot_readiness_is_ready`
- There is no repository-local lint command in the current checkout.
- `pdftotext` is required for the PDF-backed import/coverage scripts, and the XeLaTeX build depends on the fonts listed in `README.md` and `main.tex`.

- Safe TeX inspection pipeline:
  - `python3 scripts/inventory_tex.py`
  - `python3 scripts/extract_tex_entries.py`
  - `python3 scripts/build_tex_reports.py`
- Spreadsheet/PDF import pipeline:
  - `python3 scripts/import_mand2mc.py`
  - `python3 scripts/import_shengfu.py`
  - `python3 scripts/import_bs_gsr_pdf.py`
  - `python3 scripts/compare_sources.py`
  - `python3 scripts/build_coverage_model.py`
- Curated pilot refresh order:
  - `python3 scripts/export_series_packets.py`
  - `python3 scripts/promote_series_packets.py`
  - `python3 scripts/fetch_wiktionary_component_roles.py`
  - `python3 scripts/resolve_series_roots.py`
  - `python3 scripts/build_semantic_evidence.py`
  - `python3 scripts/number_phonetic_transcriptions.py`
  - `python3 scripts/render_curated_series.py`
  - `python3 scripts/evaluate_pilot_render.py`
- Integrated review build:
  - `python3 scripts/build_integrated_semantic_components.py`
  - `python3 scripts/build_integrated_series.py`
  - `python3 scripts/render_integrated_dictionary.py`
  - `latexmk -xelatex build/generated_integrated_dictionary.tex`

## High-level architecture

- `main.tex` is the authoritative hand-edited source. It combines document setup, the semantic-component inventory, and the dictionary itself; `asia.bib` and `hard-character-images/` support that build.
- `AGENTS.md` captures the safe automation workflow, and `conceptual.md` explains the scholarly model behind the current structure. Use both when a task affects parsing, series structure, or rendering.
- The conservative inspection layer reads `main.tex` without rewriting it:
  - `scripts/inventory_tex.py` inventories sections, subsections, entries, images, MC forms, comments, and nesting into `data/current_tex_inventory.json`.
  - `scripts/extract_tex_entries.py` preserves raw entry blocks plus parsed markers in `data/current_tex_entries.json`.
  - `scripts/build_tex_reports.py` turns those extracted entries into review reports instead of automatic edits.
- External source ingestion is centralized around `scripts/spreadsheet_import.py`, which loads spreadsheets while preserving original headers and adding provenance columns such as `source_row_number` and `source_sheet_name`. The importers write stable CSVs in `data/derived/` and Markdown reports in `reports/`.
- The curation layer works one GSC series at a time. `data/series_packets/` holds exported review packets, and `data/entries/curation/*.json` is the working store for curated series data, generated additions, hierarchy assignments, semantic evidence, and resolved roots.
- Shared enrichment/render helpers sit in modules such as `hierarchy_utils.py`, `mc_resolution.py`, and `semantic_label_normalization.py`. `build_semantic_evidence.py`, `resolve_series_roots.py`, and `number_phonetic_transcriptions.py` update curated entries before rendering.
- `scripts/render_curated_series.py` produces the pilot review document in `build/generated_curated_series_sample.tex`, and `scripts/evaluate_pilot_render.py` plus the pilot regression tests are the readiness gate for that generated sample.
- The integrated review layer merges three sources: current `main.tex`, the earlier pilot under `key references/My_Chinese_dictionary/main.tex`, and the active curated packets. `build_integrated_semantic_components.py` writes `data/semantic_components/integrated_semantic_components.json`, `build_integrated_series.py` writes `data/entries/integrated_series/*.json`, and `render_integrated_dictionary.py` renders the combined review document.

## Key conventions

- Treat `main.tex` as the source of truth for Nathan Hill's hand-checked decisions. Tooling should add structure and reports around it, not silently overwrite its forms, labels, or hierarchy.
- Preserve raw LaTeX alongside parsed fields. In this repository, `%` comments often carry pinyin, Baxter-style MC, GSR identifiers, and editorial notes that future tooling must keep.
- Keep identifier types separate: GSC entry IDs such as `01-30` are not GSR item IDs such as `0060a`, spreadsheet row numbers, or Unicode code points.
- Nested `itemize` blocks encode real subseries and sub-subseries structure. Do not flatten them for convenience, and keep generated subseries directly under their parent series rather than collecting them globally at the end.
- Preserve Unicode and rare-glyph PNG usage exactly. The tests expect every referenced PNG to exist in `hard-character-images/`.
- Middle Chinese forms in `\textit{...}` are attested/transcribed forms and must not be starred. The test suite treats any leading `*` on extracted MC forms as a failure.
- When spreadsheet and PDF sources disagree on MC, use Mand2MC as the rendered MC authority when it has a reading; keep BS/GSR evidence separately for reports and investigation.
- Spreadsheet importers preserve source columns and add normalized helper columns rather than normalizing in place. Follow that pattern for new imports.
- Semantic-label normalization is explicit, not heuristic: use `data/semantic_components/semantic_aliases.json` and `scripts/semantic_label_normalization.py`. Blocked or placeholder labels such as `os`, `den`, and `xxx` must not appear in authoritative or generated outputs.
- Generated TeX files should include the warning header `% GENERATED FILE - DO NOT EDIT BY HAND.`; the rendering tests check for it.
- Pilot and integrated renderers preserve Schuessler order and a measured two-column layout that tries to keep whole entries within a column. If roots or subgroup semantics change, rerun `scripts/number_phonetic_transcriptions.py` before rendering so duplicate phonetic values get renumbered consistently.
