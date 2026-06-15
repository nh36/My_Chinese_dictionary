# My Chinese dictionary

This repository currently centers on a hand-edited XeLaTeX source, `main.tex`, for Nathan W. Hill's dictionary of Chinese characters in transliteration. The authoritative scholarly content is still in the LaTeX; the supporting tooling in this checkout is currently focused on documenting the build and inventorying the source safely.

## Repository highlights

- `main.tex` — authoritative XeLaTeX source for the dictionary
- `asia.bib` — bibliography used by the LaTeX document
- `hard-character-images/` — PNG glyph assets for rare or hard-to-render characters
- `AGENTS.md` — implementation handoff and phased pipeline plan
- `conceptual.md` — editorial and phonological rationale for the current structure

## Build

The document is intended to be built with XeLaTeX via `latexmk`:

```sh
latexmk -xelatex main.tex
```

Clean generated LaTeX build artifacts with:

```sh
latexmk -c
```

### Required tools and fonts

- `latexmk`
- `xelatex`
- `BabelStone Han`
- `FreeSerif`
- `FreeSans`
- `FreeMono`
- `Tibetan Machine Uni`
- `Charis SIL`
- `Padauk`

In the current environment, the required XeLaTeX fonts have now been installed and `latexmk -xelatex main.tex` completes successfully. See `docs/build-notes.md` for the current build status and remaining warnings.

### Python environment for the scripts

Install the script dependencies with:

```sh
python3 -m pip install -r requirements.txt
```

## Inventory tooling

Generate the current source inventory as JSON and Markdown:

```sh
python3 scripts/inventory_tex.py
```

By default this reads `main.tex` and writes:

- `data/current_tex_inventory.json`
- `reports/current_inventory.md`

Extract entry-level JSON with raw LaTeX blocks and parsed markers:

```sh
python3 scripts/extract_tex_entries.py
```

By default this writes:

- `data/current_tex_entries.json`

Generate the current TeX-derived reports:

```sh
python3 scripts/build_tex_reports.py
```

Extract the `Semantic components` section into machine-readable form:

```sh
python3 scripts/extract_semantic_components.py
```

Reuse existing TeX analyses and IDS data to enrich curation files with semantic evidence:

```sh
python3 scripts/build_semantic_evidence.py
```

Fetch cached Wiktionary `Han compound` analyses into the curation files:

```sh
python3 scripts/fetch_wiktionary_component_roles.py
```

This writes:

- `reports/tex_entries_by_gsr.md`
- `reports/tex_entries_without_gsr.md`
- `reports/rare_glyphs_and_images.md`
- `reports/semantic_labels_used_in_tex.md`
- `reports/semantic_components_inventory.md`

## Spreadsheet import tooling

Import the Mand2MC spreadsheet:

```sh
python3 scripts/import_mand2mc.py
```

Import the Shengfu spreadsheet:

```sh
python3 scripts/import_shengfu.py
```

Build the spreadsheet-backed comparison reports after the derived CSVs exist:

```sh
python3 scripts/compare_sources.py
```

Import the Baxter-Sagart GSR-order PDF:

```sh
python3 scripts/import_bs_gsr_pdf.py
```

Build the cross-source coverage model and expansion reports:

```sh
python3 scripts/build_coverage_model.py
```

Resolve provisional abstract roots for missing-series packets:

```sh
python3 scripts/resolve_series_roots.py
```

Export hand-checkable series packets for target GSC series:

```sh
python3 scripts/export_series_packets.py
```

Promote those packets into working curation files:

```sh
python3 scripts/promote_series_packets.py
```

Refresh the full pilot curation layer in the current safe order:

```sh
python3 scripts/export_series_packets.py
python3 scripts/promote_series_packets.py
python3 scripts/fetch_wiktionary_component_roles.py
python3 scripts/resolve_series_roots.py
python3 scripts/build_semantic_evidence.py
python3 scripts/render_curated_series.py
```

Analyze MC-source conflicts and hierarchy coverage for the current pilot:

```sh
python3 scripts/analyze_mc_disagreements.py
python3 scripts/analyze_hierarchy_gap.py
```

Render the curated pilot packets into a review PDF:

```sh
python3 scripts/render_curated_series.py
```

Current MC policy in the pilot pipeline:

- render Mand2MC-derived MC forms when Mand2MC has them;
- preserve BS/GSR MC evidence in the packet JSON and reports;
- investigate only the cases where a BS/GSR MC reading is absent from Mand2MC.

The import scripts write:

- `data/derived/mand2mc.csv`
- `data/derived/shengfu.csv`
- `data/derived/bs_gsr.csv`
- `reports/import_mand2mc.md`
- `reports/import_shengfu.md`
- `reports/import_bs_gsr_pdf.md`

The comparison script writes:

- `reports/mand2mc_rows_not_in_tex.md`
- `reports/tex_forms_conflicting_with_mand2mc.md`
- `reports/shengfu_groups_missing_from_tex.md`

The coverage-model script writes:

- `data/derived/character_coverage.csv`
- `data/derived/gsc_series_coverage.csv`
- `reports/gsc_series_coverage.md`
- `reports/missing_gsc_rhymes_and_series.md`
- `reports/expansion_work_queue.md`

The root-resolution step updates:

- `data/entries/curation/*.json` with `series_root_candidates` and `resolved_series_root`
- `reports/series_root_resolution.md`

The curation-packet scripts write:

- `data/series_packets/*.json`
- `reports/series_packets/*.md`
- `data/entries/curation/*.json`
- `build/generated_curated_series_sample.tex`
- `build/generated_curated_series_sample.pdf`
- `reports/generated_curated_series_sample.md`

The pilot-quality scripts write:

- `data/current_semantic_components.json`
- `reports/semantic_components_inventory.md`
- `reports/pilot_render_readiness.md`
- `reports/semantic_evidence_reuse.md`
- cached Wiktionary component evidence under `data/raw/wiktionary/`
- `reports/series_root_resolution.md`

Fetch explicit `Han compound` evidence from Wiktionary for curated pilot candidates:

```sh
python3 scripts/fetch_wiktionary_component_roles.py
```

### Python package requirements for imports

The import scripts rely on:

- `pandas`
- `openpyxl` for `.xlsx`
- `odfpy` for `.ods`

Those packages are listed in `requirements.txt`.

## Controlled sample export and rendering

Export the current representative sample entry set:

```sh
python3 scripts/export_sample_entries.py
```

Render that sample back to LaTeX:

```sh
python3 scripts/render_entries.py
```

These commands write:

- `data/entries/sample_entries.json`
- `build/generated_entries_sample.tex`
- `build/generated_main_sample.tex`
- `build/generated_main_sample.pdf` after compiling the standalone sample

See `docs/data-model.md` for the purpose and limits of the current sample format.

You can also override the paths explicitly:

```sh
python3 scripts/inventory_tex.py \
  --source main.tex \
  --json-out data/current_tex_inventory.json \
  --report-out reports/current_inventory.md
```

## Tests

Run the current test suite:

```sh
python3 -m unittest
```

Run a single test:

```sh
python3 -m unittest tests.test_inventory_tex.InventoryTexTests.test_collect_inventory_from_sample
```

The current test suite includes parser/report unit tests plus repository-specific safety checks for missing image assets and accidentally starred Middle Chinese forms.

## Source data status

The current checkout includes the LaTeX source, bibliography, reference PDFs, glyph PNGs, and the spreadsheet inputs under `key references/`.

The current data artifacts generated from those source tables are:

- `data/derived/mand2mc.csv`
- `data/derived/shengfu.csv`
- `data/derived/bs_gsr.csv`
- `data/derived/character_coverage.csv`
- `data/derived/gsc_series_coverage.csv`
- `data/series_packets/`
- `data/entries/curation/`
- `reports/import_mand2mc.md`
- `reports/import_shengfu.md`
- `reports/import_bs_gsr_pdf.md`
- `reports/mand2mc_rows_not_in_tex.md`
- `reports/tex_forms_conflicting_with_mand2mc.md`
- `reports/shengfu_groups_missing_from_tex.md`
- `reports/gsc_series_coverage.md`
- `reports/missing_gsc_rhymes_and_series.md`
- `reports/expansion_work_queue.md`
- `reports/series_packets/`
- `reports/generated_curated_series_sample.md`
- `reports/pilot_render_readiness.md`

## Pilot readiness check

After generating a new pilot, run:

```sh
python3 scripts/evaluate_pilot_render.py
```

If the report still says **not ready**, the pilot should be treated as an internal draft rather than a review-ready approximation of `main.tex`.
