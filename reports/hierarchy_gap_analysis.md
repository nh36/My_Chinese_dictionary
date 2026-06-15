# Hierarchy gap analysis

- This report compares the current packet model with hand-done entries that already show explicit internal hierarchy.
- The question is not whether the current pipeline can list the right characters, but whether it can represent intermediate phonetic nodes and subgroup structure.

## `18-01`

- Original TeX itemize depth: 1
- Original TeX subgroup / intermediate-phonetic nodes detected: 3
- Current packet available for direct comparison: no
- Current packet candidate count: unavailable
- Packet source layer: unavailable
- Packet candidates have explicit parent/subseries fields: no

### Detected intermediate nodes in the hand-done entry

- `{\Large{何}}	%he2` ⇒ `{\large{g\textoverset{a}{a}y}},`
- `{\Large{哥}}	%ge1` ⇒ `{\large{k\textoverset{a}{a}y}},`
- `{\Large{奇}}	%qi2` ⇒ `{\large{q\textoverset{b}{a}y}},`

### Current packet-model limitation

This entry is not yet represented by a packet file, so the current pipeline cannot even attempt a like-for-like reproduction of its hierarchy.

## `01-01`

- Original TeX itemize depth: 1
- Original TeX subgroup / intermediate-phonetic nodes detected: 5
- Current packet available for direct comparison: yes
- Current packet candidate count: 4
- Packet source layer: `curation`
- Packet candidates have explicit parent/subseries fields: yes

### Detected intermediate nodes in the hand-done entry

- `{\Large{固}}	%gu4` ⇒ `{\large{k\textoverset{a}{a}}},`
- `{\Large{胡}}	%hu2` ⇒ `{\large{g\textoverset{a}{a}}},`
- `{\Large{居}}	%ju1` ⇒ `{\large{k\textoverset{b}{a}}},`
- `{\Large{辜}}	%gu1` ⇒ `{\large{k\textoverset{a}{a}₂}},`
- `{\Large{苦}}	%ku3` ⇒ `{\large{k\textoverset{a}{a}₃}},`

### Current packet-model limitation

The packet layer can now preserve extracted subgroup heads and candidate-to-parent assignments where evidence allows, but it still needs broader packetization and better assignment coverage before every hand-done series can be reproduced like-for-like.

## `01-67`

- Original TeX itemize depth: 2
- Original TeX subgroup / intermediate-phonetic nodes detected: 5
- Current packet available for direct comparison: no
- Current packet candidate count: unavailable
- Packet source layer: unavailable
- Packet candidates have explicit parent/subseries fields: no

### Detected intermediate nodes in the hand-done entry

- `{\Large{布}}({\includegraphics[width=5mm]{布.png}})	%bu4` ⇒ `{\large{p\textoverset{a}{a}}},`
- `{\Large{甫}}({\includegraphics[width=5mm]{甫.png}})	%bu4` ⇒ `{\large{pa₂}},`
- `{\Large{浦}}` ⇒ `{\large{p\textoverset{a}{a}₂}},`
- `{\Large{捕}}	%bu3` ⇒ `{\large{p\textoverset{a}{a}₃}},`
- `{\Large{尃}}	%fu1` ⇒ `{\large{p\textoverset{b}{a}}},`

### Current packet-model limitation

This entry is not yet represented by a packet file, so the current pipeline cannot even attempt a like-for-like reproduction of its hierarchy.

## Consequence

Before broader expansion, the packet schema needs fields such as `parent_phonetic`, `subseries_root`, or `hierarchy_depth`, so that reproduced hand-done entries and newly expanded ones can preserve internal xiesheng structure instead of flattening everything to the top-level head.
