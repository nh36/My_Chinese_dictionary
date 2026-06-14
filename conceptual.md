# conceptual.md — conceptual brief for the Chinese dictionary project

This file explains the intellectual purpose of the dictionary and the editorial logic behind the current LaTeX. It is meant to be read together with `AGENTS.md`. `AGENTS.md` tells a coding agent how to handle the repository safely; this file explains what the project is trying to do and why its structure matters.

## 1. What this project is

This is not an ordinary Chinese dictionary organized by modern pronunciation, radical, stroke count, or English gloss. It is a dictionary of Chinese characters in transliteration, organized around the structure of the Chinese writing system and the historical phonology that this structure preserves.

The central object is the `xiéshēng` 諧聲 / 形聲 series: a set of characters that share a phonetic element, where the graphic element points not to an exact modern reading but to a historically meaningful range of pronunciation. The dictionary tries to make that information explicit. Each entry should show:

1. the head graph or phonetic element;
2. the paragraph/series number from Schuessler's *Minimal Old Chinese and Later Han Chinese: A Companion to Grammata Serica Recensa*;
3. the abstract phonetic value assigned to the series or subseries in Nathan Hill's transcription;
4. each character belonging to the series or subseries;
5. the character's graphic structure, especially semantic component plus phonetic component;
6. the Middle Chinese reading in Nathan Hill's Indological transcription;
7. source identifiers, especially GSR item numbers where available;
8. notes where the `xiéshēng` analysis, graphic structure, reading, or subseries membership is uncertain.

The larger purpose is to replace the implicit knowledge of a specialist with an explicit, inspectable representation. A reader should be able to see why a character is placed in a series, what the semantic element contributes graphically, what phonetic abstraction the series supports, and where the analysis depends on judgement.

## 2. Why the project is organized by `xiéshēng` series

The Chinese script contains many characters whose graphic structure combines a semantic component and a phonetic component. The phonetic component does not normally predict a character's exact Middle Chinese or modern reading. It points to a historically earlier pattern shared across a series.

For example, a phonetic element may tell us that a group of characters belongs to the same broad rhyme domain, while leaving voicing, aspiration, prefixal material, tone-producing suffixes, or the type A/type B distinction unspecified. In other cases the phonetic element may be more precise. The point of the dictionary is to record these differences directly rather than hiding them behind modern character forms.

The current LaTeX therefore has a hierarchy:

- a broad subsection, such as `-ay` or `-a`, representing a major phonological/rhyme domain in Nathan's working transcription;
- paragraph entries headed by a Schuessler-style number and a head graph;
- top-level members of the phonetic series;
- nested subseries introduced when a derived graph itself becomes a phonetic element or when the series splits into a more precise phonological subgroup;
- deeper nested subseries where another graphic or phonological split is needed.

The nested LaTeX is not merely presentational. A nested `itemize` often means that one graph within a phonetic series has become a new phonetic base for a subgroup. The coding agent must therefore treat nesting as scholarly data.

## 3. Numbering: what the paragraph numbers mean

The paragraph headings in the current LaTeX use numbers such as `18-01`, `01-30`, and `10-03`. These are not arbitrary local entry numbers, and they are not the same thing as GSR item numbers such as `0060a` or `0001f`.

The paragraph numbers follow Schuessler's *Companion to Grammata Serica Recensa* (`GSC`). The first part identifies the GSC rime section; the second part identifies the phonetic series within that section. This lets the dictionary inherit the conceptual organization of Schuessler's companion while still presenting Nathan's own transcription and analysis.

Keep these identifiers distinct:

- `GSC series number`, e.g. `01-30`, used in the LaTeX paragraph heading.
- `GSR item number`, e.g. `0060a`, often found in comments after individual readings.
- `Unicode code point`, e.g. `U+99AC`, a character identity.
- `source row number`, from spreadsheets or extracted tables.

A future data model should store all of these separately.

## 4. The two transcription systems used here

The dictionary uses two of Nathan Hill's transcription systems. They must not be replaced with Baxter's ASCII forms, pinyin, IPA, or any modern-language spelling.

### 4.1 Middle Chinese transcription

Middle Chinese forms in the dictionary are given in Nathan's Indological transcription, as described in `Hill ar 2023 transcription(1).pdf`.

This system is a transcription of the Middle Chinese categories, not a claim about exact phonetic pronunciation. The methodological point is important: the transcription should preserve the philological categories without prematurely turning them into an IPA-style reconstruction. This is why a coding agent must not silently “normalize” forms into another system.

Some practical consequences:

- Middle Chinese forms are usually in `\textit{...}` in the LaTeX.
- These are attested/transcribed Middle Chinese forms and should not be starred.
- Baxter-style ASCII forms may occur in comments, e.g. `%ngjoX`, and should be preserved as source or cross-reference data, not promoted over Nathan's forms.
- Characters such as `ṅ`, `ḫ`, `ṣ`, `ẓ`, `ṭ`, `ḍ`, `ṇ`, `ś`, `ź`, `ñ`, and the special glottal stop marker must be preserved exactly.
- If a form appears both as Nathan MC and Baxter/Sagart-style MC, store the two fields separately, e.g. `mc_nwh` and `mc_bs`.

A coding agent should never guess a Middle Chinese form. It should copy from `main.tex` when present, import from the spreadsheet only into a separate field, and report disagreements.

### 4.2 Old Chinese / character-transcription system

The dictionary also uses Nathan's transcription of Chinese characters as graphic-phonological objects, described in `Hill ar 2015 Transcription of Chinese.pdf`.

The basic idea is to render the phonetic and semantic information encoded in a character into Roman letters. In a phonetic compound, the phonetic element is represented by an abstract phonetic value; semantic components are represented by abbreviated Latin labels and their graphic relationship to the phonetic element is indicated typographically.

This is why the current LaTeX contains forms such as:

```tex
{\large{qay}}
{\large{\textsuperscript{hom·}qay}}
{\large{\textsuperscript{bamb:}qay}}
{\large{qay:qay}}
{\large{k\textoverset{a}{a}y}}
{\large{q\textoverset{b}{a}y}}
{\large{pa₂}}
```

These are not decorative strings. They encode analysis. The coding agent should preserve them, parse them cautiously, and avoid converting them to plain text unless the conversion is reversible.

## 5. Semantic component notation

The semantic labels are Latin abbreviations, e.g. `hom`, `arb`, `bamb`, `dic`, `or`, `tum`, `herb`, `gem`, `met`, `aq`, `cor`, `man`, `carn`, `vest`, and many others listed in the `Semantic components` section of `main.tex`.

The use of Latin is deliberate. It avoids giving modern Mandarin, modern English, or a modern kaishu character a false epistemological priority in the transcription. The label is a label for a graphic semantic component, not a translation of the word written by the whole character.

The punctuation around semantic labels encodes graphic arrangement. The precise current conventions in `main.tex` must be documented before being automated, but the broad pattern is:

- a semantic label before the phonetic value, often as `\textsuperscript{label·}phonetic`, usually means that the semantic component is graphically before or to the left of the phonetic component;
- a semantic label before the phonetic value with a colon, as in `\textsuperscript{bamb:}qay`, often marks a different spatial relation, such as a component above the phonetic;
- a semantic label after the phonetic value, as in `phonetic\textsuperscript{·label}` or `phonetic\textsuperscript{:label}`, marks a relation where the semantic component follows, lies to the right, below, surrounds, or otherwise attaches after the phonetic base;
- doubled or chained notation, such as `qay:qay` or `pa₂\textsuperscript{:digit}`, is part of the analysis and should not be simplified.

Do not infer a final universal rule from one example. Before making a parser, make a report of all semantic-label strings and punctuation patterns actually used in `main.tex`. The parser should retain the raw LaTeX alongside any structured interpretation.

## 6. What the abstract phonetic values are doing

The form attached to a head graph or subseries is an abstraction from the readings of the characters in that series. It is not simply one character's reconstructed Old Chinese word.

The abstraction asks: what phonological information does this phonetic component make available?

Depending on the series, the answer may include:

- a rhyme or coda;
- a broad place of articulation;
- a manner of articulation;
- aspiration or lack of aspiration;
- voicing, or deliberate abstraction away from voicing;
- type A/type B behavior;
- labialization or medial material;
- a more precise subseries value when the graphic material justifies it.

Often the top-level series gives a broad common denominator, while a nested subseries gives a narrower value. For instance, the series headed by 父 has a broad `pa` value, while 布 and 甫 appear as derived subseries with their own values. Under 甫 there are further subseries such as 浦, 捕, 尃, and 旉. The hierarchy is the analysis.

When the coding agent proposes or checks an abstraction, it should ask:

1. What readings are actually attested for the members?
2. Which features are common across the whole set?
3. Which features are limited to a subgroup?
4. Does the graphic structure support making that subgroup into a subseries?
5. Is a reading irregular, late, borrowed, analogical, or otherwise not a good basis for redefining the whole series?
6. Is the uncertainty best represented as a note rather than as a forced decision?

## 7. Why the LaTeX looks the way it does

The current LaTeX is dense because it is trying to print a compact scholarly dictionary, not because it is careless.

Important LaTeX features and their purpose:

- `XeLaTeX` is necessary because the document uses Chinese characters, rare glyphs, Tibetan and Burmese fonts, and phonological symbols with diacritics.
- `BabelStone Han` is used for Chinese because rare and non-BMP characters matter.
- `Charis SIL`, `FreeSerif`, and related fonts support specialist phonetic symbols.
- `\textoversetlarge{number}{head}` places the GSC paragraph number above the head graph.
- `\textoverset{...}{...}` is used inside phonological notation and must not be flattened casually.
- `\textunderset{...}{...}` may also encode meaningful notation and should be preserved.
- `\textsuperscript{...}` is used for semantic components and other analytic annotations.
- `\textit{...}` normally marks Middle Chinese forms.
- `%` comments often contain pinyin, Baxter/Sagart MC forms, GSR numbers, or editorial reminders. They are data, not disposable comments.
- `spacing{0.7}` and `multicols` serve the compact printed dictionary format.
- PNG images represent rare glyphs where direct Unicode/font rendering is unsafe or unavailable. Do not replace them automatically.

The code is therefore both typesetting and data. A future workflow should separate data from rendering, but until that is done the LaTeX must be treated as the authority for Nathan's hand-checked editorial decisions.

## 8. The conceptual workflow for adding or checking a series

A coding agent should work series by series. Do not try to generate the whole dictionary in one pass.

### Step 1: choose the next GSC series

Start from Schuessler's GSC numbering. Select a series such as `01-30` or `18-01`. Record the GSC section, head graph, and expected rime category.

Create or update one structured record for the series. The record should know its place in the GSC order and its place in the printed LaTeX order.

### Step 2: gather candidate characters

Use all available sources, but keep their evidence separate:

- existing `main.tex` entries;
- Schuessler GSC series membership and rime section;
- Baxter-Sagart/GSR-order reconstructions from `Reconstructions in GSR order.pdf`;
- `Mand2MC2009-06-08 copy.ods` for pinyin, Nathan MC, Baxter/Sagart MC, GSR, and dictionary references;
- `声符级别-2022.06.07.xlsx` for phonetic component, phonetic level, secondary phonetic component, fanqie, rhyme, tone, OC initial/rhyme, and related fields;
- traditional and modern dictionaries for graphic structure, especially where the semantic and phonetic components are not obvious.

The agent should produce a candidate list with provenance. It should not silently accept every candidate as a member.

### Step 3: identify graphic structure

For each character, identify the structure in terms of semantic component and phonetic component.

Questions to answer:

- What is the visible semantic component?
- What is the phonetic component?
- Is the phonetic component the head graph, a derived graph, or a deeper subseries graph?
- Does the character have more than one plausible analysis?
- Does the kaishu form obscure an earlier relationship?
- Does the analysis depend on Shuowen, GSR, Schuessler, Hanyu Da Zidian, the `声符级别` spreadsheet, or Nathan's judgement?

The data model should allow multiple proposed analyses, with one selected analysis and notes explaining uncertainty.

### Step 4: sort into series, subseries, and sub-subseries

After the graphic analysis, organize the characters hierarchically.

Use the hierarchy only when it says something real. A subgroup should normally be created when:

- a member graph has become a phonetic component for other characters;
- the subgroup shares a narrower phonological abstraction;
- the subgroup is graphically coherent;
- treating it as flat would obscure the history of the series.

Do not make a subgroup merely because a list is long. Conversely, do not flatten an existing nested group merely because nesting makes parsing harder.

### Step 5: abstract the phonetic value

For the whole series and for each subseries, compare the readings and determine what is common.

Possible outputs:

- a broad root-like value, e.g. `ṅa`, `pa`, `qay`;
- a marked subtype, e.g. a value using `\textoverset{a}{...}` or `\textoverset{b}{...}`;
- a numbered distinction such as `pa₂` when multiple related phonetic values need separation;
- a note saying that no confident abstraction is yet possible.

The abstraction should not mechanically average readings. It should reflect how the graphic series functions. For irregular or late developments, preserve the evidence but do not let a single anomalous reading redefine the whole series without a note.

### Step 6: enter character-level readings

For each character, record:

- character or image reference;
- pinyin comment if available;
- Nathan MC form;
- Baxter/Sagart MC form if available;
- GSR item number if available;
- Unicode code point;
- gloss, if imported from Baxter-Sagart or another source;
- semantic label and graphic relation;
- phonetic/subseries parent;
- notes.

Multiple readings of the same character must be preserved. Do not merge them unless Nathan explicitly decides they are the same dictionary item.

### Step 7: render LaTeX from structured data

Only after a series is represented in structured data should the agent attempt to render LaTeX. The generated LaTeX should match the current style:

- paragraph heading with `\textoversetlarge{GSC}{head}`;
- series value in `\large{...}` or `\Large{...}` as appropriate;
- characters followed by semantic-phonetic transcription and italic Middle Chinese;
- comments or generated comments preserving pinyin, source forms, and GSR numbers;
- nested `itemize` reflecting the subseries hierarchy;
- notes as prose after the entry when needed.

Generated output should first go to a sample file, not overwrite `main.tex`.

### Step 8: review and conflict reporting

Every addition or change should be reviewable. The agent should produce reports such as:

- characters in Schuessler/GSR but missing from the LaTeX entry;
- characters in the LaTeX entry but absent from a source list;
- MC discrepancies between `main.tex` and the spreadsheet;
- conflicting phonetic-component assignments;
- missing semantic labels;
- entries where the graphic structure is uncertain;
- entries with no GSR number;
- rare glyphs that require images.

The report should present evidence, not make silent corrections.

## 9. Suggested data model concepts

The agent should eventually distinguish at least these entities.

### `Series`

A GSC-numbered phonetic series.

Fields:

- `gsc_id`, e.g. `01-30`;
- `gsc_section`, e.g. `01`;
- `head_graph`, as character or image;
- `printed_section`, e.g. `-a`;
- `series_transcription`, e.g. `ṅa`;
- `source_refs`;
- `notes`;
- `subseries`.

### `Subseries`

A nested phonetic subgroup.

Fields:

- `id`;
- `parent_id`;
- `head_graph`;
- `display_graph`;
- `subseries_transcription`;
- `basis`, e.g. `derived phonetic`, `graphic split`, `phonological split`, `uncertain`;
- `notes`;
- `members`.

### `CharacterReading`

One character with one reading and one analysis.

Fields:

- `char` or `image_ref`;
- `unicode`;
- `pinyin`;
- `mc_nwh`;
- `mc_bs`;
- `oc_bs` if imported;
- `gsr`;
- `gloss`;
- `semantic_label`;
- `semantic_relation_raw`;
- `semantic_relation_interpreted`;
- `phonetic_parent`;
- `latex_transcription_raw`;
- `source_refs`;
- `status`, e.g. `hand_checked`, `imported`, `needs_review`;
- `notes`.

### `SourceRef`

A reference to a source and location.

Fields:

- `source_file`;
- `source_type`, e.g. `main_tex`, `ods`, `xlsx`, `pdf`, `dictionary`;
- `row`, `page`, `line`, or `tex_line`;
- `field_name`;
- `value_raw`.

## 10. What counts as success

The successful project is a dictionary that remains Nathan's scholarly dictionary but is no longer trapped in hand-written LaTeX.

A good coding-agent outcome would let Nathan:

- choose a GSC series;
- see all candidate characters and source evidence;
- check or revise the graphic analysis;
- accept or revise the series/subseries hierarchy;
- check the abstract phonetic value;
- generate the corresponding LaTeX;
- compare the generated LaTeX with the existing hand-written entry;
- produce a consistent PDF without losing the typographic compactness of the current version.

The agent should aim for a workflow in which the computer handles inventory, import, cross-checking, report generation, and LaTeX rendering, while Nathan remains responsible for the scholarly decisions.

## 11. What the agent must not do

Do not turn the project into a pinyin dictionary.

Do not turn it into a Unicode character database with no phonetic hierarchy.

Do not flatten nested entries.

Do not replace Nathan's Middle Chinese transcription with Baxter ASCII or IPA.

Do not replace the character-transcription system with pinyin, English, or ordinary kaishu components.

Do not assume every semantic component label is a translation.

Do not treat comments in `main.tex` as disposable.

Do not silently resolve discrepancies between sources.

Do not remove rare glyph images simply because a font on the agent's machine happens to render the character.

Do not force an analysis where Nathan has left a note of uncertainty.

## 12. First conceptual task for the agent

Before coding a generator, the agent should produce a conceptual inventory of the existing LaTeX.

The first report should answer:

1. What GSC series are already present?
2. What printed subsections are already present?
3. What semantic labels are used?
4. What semantic-relation punctuation patterns are used?
5. What `\textoverset` patterns occur inside phonetic transcriptions?
6. What entries contain nested `itemize` groups?
7. What entries contain explicit uncertainty notes?
8. What entries use images rather than direct characters?
9. Which comments contain pinyin, Baxter/Sagart MC, GSR identifiers, or other data?

Only after this report exists should the agent try to convert entries into structured data.

## 13. Working rule

When in doubt, preserve the raw LaTeX, add structured interpretation beside it, and write a note. The aim is to make the scholarly reasoning visible, not to hide it behind automation.
