# Data model notes

The current repository now has a controlled sample export at `data/entries/sample_entries.json`.

This sample is intentionally conservative. It does **not** try to infer a full scholarly structure beyond what is already extracted safely from `main.tex`. Each sample entry keeps:

- `id`, `section`, and `subsection`;
- `head` data, including image-backed heads where present;
- source line numbers from `main.tex`;
- extracted character, pinyin, MC, GSR, image, and itemize data;
- `raw_latex` as the loss-preserving source of truth.

The immediate purpose of this sample is to support round-trippable rendering experiments without rewriting `main.tex`. `scripts/render_entries.py` renders the selected sample entries back to:

- `build/generated_entries_sample.tex`
- `build/generated_main_sample.tex`
- `build/generated_main_sample.pdf` once the standalone sample is compiled

The current standalone sample now compiles successfully after the renderer was taught to add only the outer `multicols` / `spacing` wrappers that are missing from the selected raw entry blocks.

This is an interim representation, not the final canonical schema. A later phase can refine the sample format toward a more explicit entry model once spreadsheet-backed comparison reports are available.

## Current curation layer

The repository now also has a working `series packet` layer for expansion work:

- `data/series_packets/*.json` — machine-assembled evidence packets for target GSC series;
- `reports/series_packets/*.md` — human-readable packet summaries;
- `data/entries/curation/*.json` — promoted working series files for pilot curation;
- `build/generated_curated_series_sample.tex` / `.pdf` — a review document built from those curated packets.

These curation files are still explicitly pre-editorial. They preserve source evidence and proposed additions, but they are not yet final dictionary entries and should not be merged into `main.tex` without scholarly review.
