# MC disagreement analysis

- Candidate additions with at least one MC-disagreement signal: 29

## Category counts

| Category | Count |
| --- | ---: |
| `mand2mc-multiple` | 22 |
| `cross-source-mismatch` | 17 |
| `bs-gsr-multiple` | 2 |

## Current interpretation

- The rendered warning `[MC disagreement among imported sources]` is currently triggered only by the boolean `mand_bs_mc_disagreement` field.
- That boolean is set when the Mand2MC `mc_bs` set and the BS/GSR `mc_bs` set for a candidate are both non-empty and not exactly equal.
- So the current warning is deliberately coarse: it conflates true cross-source conflict with cases where one source preserves only one reading of a graph that is polyphonic in the other source.
- `mand2mc-multiple` usually means Mand2MC contains multiple MC readings for the same graph, which may reflect real polyphony rather than an error.
- `bs-gsr-multiple` means the BS/GSR PDF lists multiple MC values for the same graph.
- `cross-source-mismatch` means the Mand2MC and BS/GSR form sets are not identical for the current character packet.
- `multiple-gsr` means the same graph is tied to more than one GSR item in the imported evidence.

## Suggested resolution workflow

1. Check whether the disagreement is between multiple legitimate readings of the same graph or between truly conflicting analyses.
2. Where the disagreement matters for promotion into dictionary output, check the relevant Guangyun fanqie / entry rather than trusting either imported source blindly.
3. Preserve unresolved polyphony explicitly instead of collapsing it into one reading too early.

## Detailed cases

| GSC | Character | Categories | Mand2MC MC | BS/GSR MC | GSR values |
| --- | --- | --- | --- | --- | --- |
| `02-01` | 骼 | `mand2mc-multiple` | kaek; kak; khaeH |  | 0766c' |
| `02-01` | 胳 | `mand2mc-multiple, cross-source-mismatch` | kaek; kak | kak | 0766d |
| `02-01` | 袼 | `mand2mc-multiple, cross-source-mismatch` | kaek; kak | kaek | 0766e |
| `02-01` | 貉 | `mand2mc-multiple, cross-source-mismatch` | hak; maeH; maek | maek | 0766h |
| `02-01` | 輅 | `mand2mc-multiple` | haek; luH; ṅaeH |  | 0766n' |
| `02-01` | 珞 | `mand2mc-multiple` | lak; lek |  | 0766u |
| `02-01` | 略 | `cross-source-mismatch` | liak | ljak | 0766v |
| `02-01` | 格 | `mand2mc-multiple, cross-source-mismatch` | haek; kaek | kaek | 0766z |
| `04-30` | 眙 | `mand2mc-multiple` | ḍiṅH; ṭhiH |  | 0976a' |
| `04-30` | 始 | `cross-source-mismatch` | śiX | syiX | 0976e' |
| `04-30` | 胎 | `cross-source-mismatch` | thəy | thoj | 0976h' |
| `04-30` | 駘 | `mand2mc-multiple` | dəy; dəyX |  | 0976j' |
| `04-30` | 殆 | `cross-source-mismatch` | dəyX | dojX | 0976l' |
| `04-30` | 俟 | `mand2mc-multiple, cross-source-mismatch` | dẓiX; ẓiX | zriX | 0976m |
| `04-30` | 迨 | `cross-source-mismatch` | dəyX | dojX | 0976n' |
| `04-30` | 台 | `mand2mc-multiple, cross-source-mismatch` | thəy; yi | yi | 0976p |
| `04-30` | 佁 | `mand2mc-multiple` | ṭhiH; yiX |  | 0976t |
| `04-30` | 詒 | `mand2mc-multiple, bs-gsr-multiple, cross-source-mismatch` | dəyX; yi | dojX; yi | 0976v |
| `04-30` | 治 | `mand2mc-multiple, cross-source-mismatch` | ḍi; ḍiH | dri | 0976z |
| `18-18` | 枷 | `mand2mc-multiple` | kae; kaeH |  | 0015c |
| `38-03` | 蔭 | `cross-source-mismatch` | qimH | 'imH | 0651b' |
| `38-03` | 衿 | `mand2mc-multiple` | gimH; kim |  | 0651g |
| `38-03` | 坅 | `mand2mc-multiple` | khimX; ṅimX |  | 0651i |
| `38-03` | 含 | `mand2mc-multiple, bs-gsr-multiple` | hom; homH | hom; homH | 0651l' |
| `38-03` | 頷 | `mand2mc-multiple, cross-source-mismatch` | homX; ṅomX | homX | 0651n' |
| `38-03` | 黔 | `mand2mc-multiple` | gim; giem |  | 0651r |
| `38-03` | 吟 | `cross-source-mismatch` | ṅim | ngim | 0651s |
| `38-03` | 陰 | `mand2mc-multiple, cross-source-mismatch` | qim; qimH | 'im | 0651y |
| `38-03` | 唫 | `mand2mc-multiple` | gimX; khim; ṅim |  | 0652g |
