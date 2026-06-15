# Skipped series requirements

This report summarizes the series that were trialed during expansion work
but not promoted into the active pilot batch because they still had unresolved
semantic, transliteration, or root-resolution problems.

The point is not that these series are impossible, but that each currently
needs one more class of information or one more piece of resolver logic before
they can be added cleanly.

## Main patterns

| Pattern | Series | What is missing |
| --- | --- | --- |
| Missing explicit semantic evidence for a small number of characters | `03-32`, `03-65`, `09-17`, `16-01`, `35-01`, `35-21` | The pipeline cannot yet assign a trustworthy semantic component to 1-2 remaining characters in each series. |
| Missing top-level root / subgroup split before transliteration can be synthesized | `03-49`, `12-08`, `12-25` | Many characters already have semantic assignments, but the root/transliteration layer still needs a better series-level analysis. |
| Multi-semantic or orthographic edge case that needs an explicit policy | `09-17`, `16-01`, `35-01`, `35-21` | Wiktionary or IDS gives a structure that the current semantic resolver does not yet interpret correctly. |

## Series-by-series

### `03-32`

- Root currently resolves, but two characters still block clean promotion:
  - `甞`
  - `𣥺`
- What is needed:
  - a way to use orthodox/variant relations like `甞` ↔ `嘗` as evidence;
  - a strategy for rare graphs with IDS but without explicit Wiktionary component analysis.

### `03-49`

- Large failure mode: **most characters already have semantic assignments, but
  many still lack transliterations/render blocks**.
- What is needed:
  - a more reliable top-level abstraction for the `爿 / 將 / 壯 / 牆` family;
  - likely an earlier subgroup split rather than one flat packet root.

### `03-65`

- Only two characters block promotion:
  - `詤`
  - `㡃`
- What is needed:
  - explicit semantic evidence around the `㠩` family;
  - either better IDS support or explicit Wiktionary/Han-etymology data.

### `09-17`

- Only `聽` blocks promotion.
- The current issue is **not** the root; it is semantic structure.
- Wiktionary gives one phonetic component (`𡈼`) and **two semantic
  components** (`耳`, `㥁`).
- What is needed:
  - a policy for multi-semantic templates, ideally stage-aware;
  - or a deterministic rule for which semantic component to privilege when
    only one can be encoded in the current transcription layer.

### `12-08`

- Many characters have semantics, but the packet still lacks a stable clean
  transliteration layer for the whole `重 / 童 / 董 ...` family.
- What is needed:
  - a better root calculation for this series;
  - likely early subgrouping before rendering.

### `12-25`

- Similar to `12-08`: many semantics exist already, but the packet still lacks
  a stable root/transliteration layer for the `丰 / 邦 / 封 / 奉 ...` family.
- What is needed:
  - a better top-level root plus subgroup structure.

### `16-01`

- Only `毫` blocks promotion.
- Wiktionary clearly gives `高 + 毛`, but the current parser does not fully use
  that template shape.
- What is needed:
  - support for Han-compound templates where the semantic partner is present
    but not already normalized into the exact one-semantic/one-phonetic form
    the resolver expects.

### `35-01` and `35-21`

- Both are currently blocked by the same unresolved character:
  - `盇`
- What is needed:
  - explicit semantic evidence for `盇`;
  - and probably a policy decision about whether these two K. 642-derived
    packets should be handled together rather than as separate clean series.

## What to research next

1. **Variant and orthodox-form relations**
   - Especially for forms like `甞`.
2. **Multi-semantic Han-compound templates**
   - Especially `聽`.
3. **Sparse or absent BS/GSR coverage for the head graph**
   - Especially `03-49`, `12-08`, and `12-25`, where root/transliteration
     resolution is the bottleneck more than semantics.
4. **Series that probably need an earlier subgroup split**
   - Again `03-49`, `12-08`, `12-25`.
5. **Characters with no explicit semantic evidence but some IDS support**
   - `𣥺`, `詤`, `㡃`, `盇`.

## Practical consequence

The skipped series are not random failures. They mostly fall into three
research buckets:

1. **semantic evidence gaps**,
2. **root / subgroup-structure gaps**,
3. **template-shape / variant-handling gaps**.

That means the next tranche of expansion work should focus less on bulk
throughput and more on these specific resolver capabilities.
