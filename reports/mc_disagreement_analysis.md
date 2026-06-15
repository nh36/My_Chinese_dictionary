# MC disagreement analysis

- Candidate additions with at least one MC-disagreement signal: 26

## Category counts

| Category | Count |
| --- | ---: |
| `mand2mc-multiple` | 22 |
| `mand2mc-extra-vs-bs` | 9 |
| `bs-not-in-mand2mc` | 4 |
| `bs-gsr-multiple` | 2 |

## Current interpretation

- The pilot should now render Mand2MC-derived MC forms without a visible inline warning.
- `bs-not-in-mand2mc` is the only case that should force investigation: it means BS/GSR has an MC reading whose Baxter-Sagart form is absent from Mand2MC.
- `mand2mc-extra-vs-bs` is not by itself a conflict; it means Mand2MC preserves extra readings not reflected in the BS/GSR extraction.
- `mand2mc-multiple` usually means Mand2MC contains multiple MC readings for the same graph, which may reflect real polyphony rather than an error.
- `bs-gsr-multiple` means the BS/GSR PDF lists multiple MC values for the same graph.

## Suggested resolution workflow

1. Render from Mand2MC when it provides an MC form.
2. Preserve all BS/GSR rows in packet evidence even when they do not affect rendering.
3. Investigate only the cases where BS/GSR has a reading absent from Mand2MC, using Guangyun / fanqie where the discrepancy matters editorially.

## Detailed cases

| GSC | Character | Categories | Mand2MC MC | BS/GSR MC | BS not in Mand2MC | Mand2MC extra vs BS | GSR values |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `01-01` | 糊 | `bs-not-in-mand2mc` |  | hu | hu |  | 49 |
| `01-01` | 菇 | `bs-not-in-mand2mc` |  | ku | ku |  | 49 |
| `01-01` | 痼 | `bs-not-in-mand2mc` |  | kuH | kuH |  | 49 |
| `01-01` | 個 | `bs-not-in-mand2mc` |  | kaH | kaH |  | 0049f' |
| `02-01` | 骼 | `mand2mc-multiple` | kaek; kak; khaeH |  |  |  | 0766c' |
| `02-01` | 胳 | `mand2mc-multiple, mand2mc-extra-vs-bs` | kaek; kak | kak |  | kaek | 0766d |
| `02-01` | 袼 | `mand2mc-multiple, mand2mc-extra-vs-bs` | kaek; kak | kaek |  | kak | 0766e |
| `02-01` | 貉 | `mand2mc-multiple, mand2mc-extra-vs-bs` | hak; maeH; maek | maek |  | hak; maeH | 0766h |
| `02-01` | 輅 | `mand2mc-multiple` | haek; luH; ṅaeH |  |  |  | 0766n' |
| `02-01` | 珞 | `mand2mc-multiple` | lak; lek |  |  |  | 0766u |
| `02-01` | 格 | `mand2mc-multiple, mand2mc-extra-vs-bs` | haek; kaek | kaek |  | haek | 0766z |
| `04-30` | 眙 | `mand2mc-multiple` | ḍiṅH; ṭhiH |  |  |  | 0976a' |
| `04-30` | 駘 | `mand2mc-multiple` | dəy; dəyX |  |  |  | 0976j' |
| `04-30` | 俟 | `mand2mc-multiple, mand2mc-extra-vs-bs` | dẓiX; ẓiX | zriX |  | dzriX | 0976m |
| `04-30` | 台 | `mand2mc-multiple, mand2mc-extra-vs-bs` | thəy; yi | yi |  | thoj | 0976p |
| `04-30` | 佁 | `mand2mc-multiple` | ṭhiH; yiX |  |  |  | 0976t |
| `04-30` | 詒 | `mand2mc-multiple, bs-gsr-multiple` | dəyX; yi | dojX; yi |  |  | 0976v |
| `04-30` | 治 | `mand2mc-multiple, mand2mc-extra-vs-bs` | ḍi; ḍiH | dri |  | driH | 0976z |
| `18-18` | 枷 | `mand2mc-multiple` | kae; kaeH |  |  |  | 0015c |
| `38-03` | 衿 | `mand2mc-multiple` | gimH; kim |  |  |  | 0651g |
| `38-03` | 坅 | `mand2mc-multiple` | khimX; ṅimX |  |  |  | 0651i |
| `38-03` | 含 | `mand2mc-multiple, bs-gsr-multiple` | hom; homH | hom; homH |  |  | 0651l' |
| `38-03` | 頷 | `mand2mc-multiple, mand2mc-extra-vs-bs` | homX; ṅomX | homX |  | ngomX | 0651n' |
| `38-03` | 黔 | `mand2mc-multiple` | gim; giem |  |  |  | 0651r |
| `38-03` | 陰 | `mand2mc-multiple, mand2mc-extra-vs-bs` | qim; qimH | 'im |  | 'imH | 0651y |
| `38-03` | 唫 | `mand2mc-multiple` | gimX; khim; ṅim |  |  |  | 0652g |
