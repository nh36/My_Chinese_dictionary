# Pilot acceptance and next architecture plan

## Why the last pilot was not good enough

The previous pilot improved the page layout, but it still failed the real comparison test because proposed additions were rendered mostly as:

- character;
- pinyin comment;
- MC form;
- GSR comment.

That is not enough. The hand-written dictionary also encodes semantic structure, phonetic abstraction, and component placement. Until the pilot does that too, it is still only a candidate list in dictionary clothing.

## Acceptance criteria for future pilots

A future pilot should be considered review-ready only when proposed additions have all of the following:

1. a target GSC series and head graph;
2. explicit candidate semantic component evidence;
3. a chosen semantic abbreviation from the `Semantic components` inventory;
4. an explicit placement decision (`prefix-dot`, `prefix-colon`, `suffix-dot`, `suffix-colon`, etc.);
5. a transliteration LaTeX form using the same analytic conventions as `main.tex`;
6. MC forms in Nathan’s notation;
7. GSR/source provenance preserved in comments or structured fields;
8. rendering in a block whose formatting can be compared directly to an existing entry.

If the semantic component is identified but the abbreviation inventory does not yet contain a settled Latin label for it, render the component itself in superscript temporarily instead of halting the pilot. That fallback only applies after the semantic/phonetic roles are understood.

## Current readiness check

Run:

```sh
python3 scripts/evaluate_pilot_render.py
```

This report is intentionally conservative. If it says the pilot is not ready, the output should be treated as an internal draft rather than something to ask Nathan to judge as dictionary formatting.

## Immediate architecture tasks

1. Parse and inventory semantic components (`scripts/extract_semantic_components.py`).
2. Add semantic-assignment fields to the curation files.
3. Build a resolver for abbreviation + placement decisions.
4. Teach the pilot renderer to use those semantic fields.
5. Tighten the readiness evaluator so that omission of semantic superscripts and placement becomes impossible to miss.
