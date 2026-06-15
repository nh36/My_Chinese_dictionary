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

The current curation schema now carries two additional structural layers that are meant to survive regeneration:

- `mc_resolution` on each proposed addition:
  - preserves the Mand2MC and BS/GSR MC form sets separately;
  - records whether BS/GSR has any reading absent from Mand2MC;
  - provides the `display_forms` that the pilot renderer should use.
- `entry_hierarchy` on promoted entries with existing TeX baselines:
  - stores extracted subgroup heads from nested `itemize` structure, including the inherited intermediate phonetic line;
  - provides `top_level_head` and ordered `nodes`.
- `hierarchy_assignment` on proposed additions where the current evidence is strong enough:
  - links a proposed addition either to an inherited subgroup head from `main.tex` or to another machine-generated candidate node when Shengfu or Wiktionary phonetic evidence points there;
  - leaves the addition top-level or unassigned when that evidence is not yet strong enough.

This is still an interim representation, but it is now rich enough for the renderer to keep some hand-authored hierarchy visible instead of flattening every proposed addition back to the top-level packet head.
