# Pilot a/b subseries detection

- Pilot goal: infer handwritten subseries `a/b` marking from the MC forms attached to each subgroup.
- Current conservative rule: use the subgroup head's own MC forms as the primary signal; treat a subgroup as **b** when those forms show an `i`-medial after the onset (for example `gie`, `phiu`, `ṅiəH`), and as **a** when they do not (for example `ka`, `puH`).
- Bare `i` with zero onset is left unresolved in this pilot; it does not occur in the selected examples.

- Pilot entries reviewed: `18-01`, `01-67`
- Handwritten a/b subgroups found in those entries: 8
- Prediction matches the handwritten label in the pilot sample: 8/8

## `18-01` (可)

- Source lines: 385-512

| Head | Handwritten | Predicted | MC forms | RHS LaTeX | Note |
| --- | --- | --- | --- | --- | --- |
| 何 | `a` | `a` | `ḫa, ḫaX` | `g\textoverset{a}{a}y` | all extracted forms lack an i-medial after the onset |
| 哥 | `a` | `a` | `ka` | `k\textoverset{a}{a}y` | all extracted forms lack an i-medial after the onset |
| 奇 | `b` | `b` | `gie, kie` | `q\textoverset{b}{a}y` | all extracted forms show an i-medial or a dedicated palatal onset |

## `01-67` (父)

- Source lines: 3036-3159

| Head | Handwritten | Predicted | MC forms | RHS LaTeX | Note |
| --- | --- | --- | --- | --- | --- |
| 布 | `a` | `a` | `puH` | `p\textoverset{a}{a}` | all extracted forms lack an i-medial after the onset |
| 浦 | `a` | `a` | `phuX` | `p\textoverset{a}{a}₂` | all extracted forms lack an i-medial after the onset |
| 捕 | `a` | `a` | `buH` | `p\textoverset{a}{a}₃` | all extracted forms lack an i-medial after the onset |
| 尃 | `b` | `b` | `phiu` | `p\textoverset{b}{a}` | all extracted forms show an i-medial or a dedicated palatal onset |
| 旉 | `b` | `b` | `phiu` | `p\textoverset{b}{a}₂` | all extracted forms show an i-medial or a dedicated palatal onset |

