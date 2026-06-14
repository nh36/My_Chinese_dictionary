# Generated sample comparison

- Sample source: `data/entries/sample_entries.json`
- Generated entry file: `build/generated_entries_sample.tex`
- Generated standalone file: `build/generated_main_sample.tex`
- Current generator behavior: the sample renderer re-emits each entry's stored `raw_latex` block and adds only the missing outer `multicols` / `spacing` wrappers required to make selected entries self-contained.
- Deliberate differences: generated-file warning headers, standalone wrapper text, and explicit outer environment wrappers when the raw entry block starts inside an already-open environment.

## Included entries

| ID | Section | Subsection | Source lines | Head type |
| --- | --- | --- | ---: | --- |
| `18-01` | The dictionary itself | -ay | 385-512 | character |
| `18-04` | The dictionary itself | -ay | 557-585 | character |
| `18-05` | The dictionary itself | -ay | 586-656 | character |
| `19-18` | The dictionary itself | -ay | 1349-1364 | image |
| `19-22` | The dictionary itself | -ay | 1404-1416 | image |
| `01-30` | The dictionary itself | -a | 2153-2190 | character |
| `01-38` | The dictionary itself | -a | 2336-2448 | character |
| `01-43` | The dictionary itself | -a | 2545-2595 | character |
| `01-57` | The dictionary itself | -a | 2805-2936 | character |
| `01-67` | The dictionary itself | -a | 3036-3159 | character_with_image |
