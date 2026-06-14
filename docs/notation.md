# Notation and formatting requirements

This document exists to make future generated pilots comparable to `main.tex`, not merely informative.

## 1. A comparable pilot must preserve the visual grammar of entries

The current dictionary entries are not just lists of characters and MC forms. A comparable pilot should preserve, or explicitly mark as still unresolved:

1. `\paragraph{\textoversetlarge{GSC}{head}}` entry headings.
2. The abstract phonetic value in `{\large{...}}`.
3. Semantic superscripts in `\textsuperscript{...}`.
4. The punctuation inside those superscripts, because `label·`, `label:`, `·label`, and `:label` encode placement and structure.
5. Nested `itemize` blocks when a derived graph becomes a new phonetic base.
6. `%` comments carrying pinyin, GSR, and reminders.

If a generated pilot still omits items 2-4, then it is not yet comparable to the existing document, even if it contains the right characters.

## 2. Semantic superscripts are analytic content

The Latin superscripts are not glosses. They are compact structural analyses:

- `\textsuperscript{hom·}qay` typically means a semantic element before / to the left of the phonetic;
- `\textsuperscript{bamb:}qay` typically marks a different placement such as above;
- `qay\textsuperscript{·dehab}` or `qay\textsuperscript{:label}` marks a semantic element after or attached differently;
- forms such as `qay:qay`, `pa₂`, `\textoverset{...}{...}`, and `\textunderset{...}{...}` are part of the phonological analysis and must not be flattened.

## 3. Source architecture needed for new additions

For each newly proposed character, the renderer should eventually know:

1. the target GSC series;
2. one or more source GSR links;
3. the MC form(s) in Nathan’s notation;
4. the phonetic base or subseries parent;
5. the semantic component candidate;
6. the semantic abbreviation matching the `Semantic components` section;
7. the semantic placement / punctuation pattern;
8. the resulting transliteration LaTeX.

The current packet workflow gathers evidence for items 1-4 and some of 5. It does **not yet** solve 6-8 automatically.

## 4. Required architecture before a pilot counts as satisfactory

1. Parse the `Semantic components` section into a machine-readable inventory of graph-to-abbreviation mappings.
2. Build a semantic-resolution step for candidate characters:
   - identify candidate semantic component(s);
   - map them onto the inventory abbreviations;
   - choose or defer left/right/above/below placement.
   - if the semantic component is known but the inventory still has no settled Latin abbreviation, use the component itself in superscript temporarily and flag it for later abbreviation review.
3. Add explicit fields in curation JSON for:
   - `semantic_assignment.abbreviation`
   - `semantic_assignment.position`
   - `transliteration_latex`
   - `render_latex`
4. Make the pilot renderer consume those fields instead of emitting MC-only placeholders.

## 5. Acceptance rule

Do not treat a pilot as review-ready if it still relies on prose placeholders like:

- `[provisional draft ...]`
- `[proposed additions ...]`

without also supplying semantic superscripts, placement decisions, and abstract phonetic forms for the proposed new material.
