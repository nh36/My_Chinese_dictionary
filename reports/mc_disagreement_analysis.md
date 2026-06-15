# MC disagreement analysis

- Candidate additions with at least one MC-disagreement signal: 112

## Category counts

| Category | Count |
| --- | ---: |
| `mand2mc-multiple` | 104 |
| `mand2mc-extra-vs-bs` | 32 |
| `bs-gsr-multiple` | 18 |
| `bs-not-in-mand2mc` | 9 |

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
| `03-38` | 愓 | `mand2mc-multiple, bs-gsr-multiple` | daṅX; śiaṅ | dangX; syang |  |  | 0720e' |
| `03-38` | 𥏫 | `mand2mc-multiple` | śiaṅ; tshiaṅ |  |  |  | 0720i' |
| `03-38` | 盪 | `mand2mc-multiple` | daṅX; thaṅH |  |  |  | 0720n' |
| `03-38` | 蕩 | `mand2mc-multiple, mand2mc-extra-vs-bs` | daṅH; daṅX | dangH |  | dangX | 0720p' |
| `03-38` | 湯 | `mand2mc-multiple, bs-gsr-multiple` | śiaṅ; thaṅ | syang; thang |  |  | 0720z |
| `03-57` | 方 | `mand2mc-multiple, mand2mc-extra-vs-bs` | baṅ; piaṅ; piaṅX | pjang |  | bang; pjangX | 0740a |
| `03-57` | 旁 | `mand2mc-multiple, mand2mc-extra-vs-bs` | baṅ; paeṅ | bang |  | paeng | 0740f' |
| `03-57` | 舫 | `mand2mc-multiple, bs-gsr-multiple` | paṅH; piaṅH | pangH; pjangH |  |  | 0740g |
| `03-57` | 放 | `mand2mc-multiple, bs-gsr-multiple` | piaṅH; piaṅX | pjangH; pjangX |  |  | 0740i |
| `03-57` | 枋 | `mand2mc-multiple, mand2mc-extra-vs-bs` | piaeṅH; piaṅ | pjaengH |  | pjang | 0740k |
| `03-57` | 傍 | `mand2mc-multiple, bs-gsr-multiple` | baṅ; baṅH | bang; bangH |  |  | 0740m' |
| `03-57` | 騯 | `mand2mc-multiple` | baeṅ; baṅ |  |  |  | 0740n' |
| `03-57` | 蒡 | `mand2mc-multiple, mand2mc-extra-vs-bs` | baṅ; paeṅ | bang |  | paeng | 0740r' |
| `04-04` | 其 | `mand2mc-multiple, mand2mc-extra-vs-bs` | gi; ki; kiH | gi |  | ki; kiH | 0952a |
| `04-04` | 萁 | `mand2mc-multiple` | gi; ki |  |  |  | 0952m |
| `04-04` | 諆 | `mand2mc-multiple` | khi; ki |  |  |  | 0952n |
| `04-04` | 綦 | `mand2mc-multiple, bs-gsr-multiple` | gi; giH | gi; giH |  |  | 0952z |
| `04-04` | 丌 | `bs-not-in-mand2mc` |  | gi | gi |  | 0952a |
| `04-30` | 眙 | `mand2mc-multiple` | ḍiṅH; ṭhiH |  |  |  | 0976a' |
| `04-30` | 駘 | `mand2mc-multiple` | dəy; dəyX |  |  |  | 0976j' |
| `04-30` | 俟 | `mand2mc-multiple, mand2mc-extra-vs-bs` | dẓiX; ẓiX | zriX |  | dzriX | 0976m |
| `04-30` | 台 | `mand2mc-multiple, mand2mc-extra-vs-bs` | thəy; yi | yi |  | thoj | 0976p |
| `04-30` | 佁 | `mand2mc-multiple` | ṭhiH; yiX |  |  |  | 0976t |
| `04-30` | 詒 | `mand2mc-multiple, bs-gsr-multiple` | dəyX; yi | dojX; yi |  |  | 0976v |
| `04-30` | 治 | `mand2mc-multiple, mand2mc-extra-vs-bs` | ḍi; ḍiH | dri |  | driH | 0976z |
| `04-61` | 不 | `mand2mc-multiple, mand2mc-extra-vs-bs` | piuw; piuwX | pjuw |  | pjuwX | 0999a |
| `04-61` | 掊 | `mand2mc-multiple` | phuwX; puwX |  |  |  | 0999d' |
| `04-61` | 否 | `mand2mc-multiple, mand2mc-extra-vs-bs` | biyX; piyX; piuwX | pjuwX |  | bijX; pijX | 0999e |
| `04-61` | 踣 | `mand2mc-multiple` | bok; phuwH |  |  |  | 0999e' |
| `04-61` | 紑 | `mand2mc-multiple` | phiuw; phiuwX |  |  |  | 0999g |
| `04-61` | 蔀 | `mand2mc-multiple` | buwX; phuwX |  |  |  | 0999g' |
| `04-61` | 秠 | `mand2mc-multiple` | phiy; phiuw |  |  |  | 0999n |
| `04-61` | 棓 | `mand2mc-multiple` | buw; phuwX |  |  |  | 0999x |
| `07-08` | 窐 | `mand2mc-multiple` | qwae; kwey |  |  |  | 0879f |
| `07-08` | 鮭 | `mand2mc-multiple` | hea; hwae; kwey |  |  |  | 0879g |
| `07-08` | 厓 | `mand2mc-multiple, mand2mc-extra-vs-bs` | kweaH; ṅea | ngea |  | kweaH | 0879p |
| `07-08` | 哇 | `mand2mc-multiple` | hwea; hweaH |  |  |  | 0879x |
| `07-08` | 鼃 | `mand2mc-multiple, bs-gsr-multiple` | qwae; qwea; hwae; hwea | 'wae; 'wea; hwae; hwea |  |  | 0879y |
| `07-08` | 鞋 | `bs-not-in-mand2mc` |  | hea | hea |  | 879 |
| `09-25` | 生 | `bs-gsr-multiple, bs-not-in-mand2mc` | ṣaeṅ | sraeng; srjaeng | srjaeng |  | 0812a |
| `09-25` | 腥 | `mand2mc-multiple` | seṅ; seṅH |  |  |  | 0812a' |
| `09-25` | 醒 | `mand2mc-multiple` | seṅ; seṅH; seṅX |  |  |  | 0812b' |
| `09-25` | 青 | `mand2mc-multiple, mand2mc-extra-vs-bs` | tseṅ; tsheṅ | tsheng |  | tseng | 0812c' |
| `09-25` | 菁 | `mand2mc-multiple` | tseṅ; tsieṅ |  |  |  | 0812f' |
| `09-25` | 請 | `mand2mc-multiple, bs-gsr-multiple` | dzieṅ; tshieṅX | dzjeng; tshjengX |  |  | 0812k' |
| `09-25` | 綪 | `mand2mc-multiple` | tshenH; tṣeaṅ |  |  |  | 0812t' |
| `09-25` | 星 | `mand2mc-multiple, mand2mc-extra-vs-bs` | dzieṅ; seṅ | seng |  | dzjeng | 0812x |
| `09-25` | 猩 | `mand2mc-multiple` | seṅ; ṣaeṅ |  |  |  | 0812z |
| `12-01` | 控 | `mand2mc-multiple, mand2mc-extra-vs-bs` | khaewṅH; khuwṅH | khuwngH |  | khaewngH | 1172a' |
| `12-01` | 跫 | `mand2mc-multiple` | giəwṅ; khaewṅ |  |  |  | 1172f' |
| `12-01` | 空 | `mand2mc-multiple, bs-gsr-multiple, mand2mc-extra-vs-bs` | khuwṅ; khuwṅH; khuwṅX | khuwng; khuwngX |  | khuwngH | 1172h |
| `12-01` | 虹 | `mand2mc-multiple, mand2mc-extra-vs-bs` | ḫuwṅ; kaewṅH | kaewngH |  | huwng | 1172j |
| `12-01` | 矼 | `mand2mc-multiple` | kaewṅ; khuwṅH |  |  |  | 1172x |
| `12-01` | 悾 | `mand2mc-multiple` | khaewṅ; khuwṅ; khuwṅH |  |  |  | 1172z |
| `16-06` | 咬 | `mand2mc-multiple` | qaew; kaew; ṅaewX |  |  |  | 1166g |
| `16-06` | 校 | `mand2mc-multiple` | ḫaew; ḫaewH; ḫaewX; kaewH; kaewX |  |  |  | 1166i |
| `16-06` | 絞 | `mand2mc-multiple, mand2mc-extra-vs-bs` | ḫaew; kaewX | kaewX |  | haew | 1166k |
| `16-06` | 鉸 | `bs-not-in-mand2mc` |  | kaewX | kaewX |  | 1166 |
| `16-33` | 削 | `mand2mc-multiple, mand2mc-extra-vs-bs` | siak; siewH; ṣaewH | sjewH |  | sjak; sraewH | 1149c' |
| `16-33` | 揱 | `mand2mc-multiple` | sew; ṣaew; ṣaewk |  |  |  | 1149d' |
| `16-33` | 少 | `mand2mc-multiple, bs-gsr-multiple` | śiewH; śiewX | syewH; syewX |  |  | 1149e |
| `16-33` | 箾 | `mand2mc-multiple` | sew; ṣaewk |  |  |  | 1149e' |
| `16-33` | 肖 | `mand2mc-multiple, bs-gsr-multiple` | siew; siewH | sjew; sjewH |  |  | 1149g |
| `16-33` | 綃 | `mand2mc-multiple` | sew; siew |  |  |  | 1149l |
| `16-33` | 趙 | `mand2mc-multiple` | dewX; ḍiewX |  |  |  | 1149u |
| `18-18` | 枷 | `mand2mc-multiple` | kae; kaeH |  |  |  | 0015c |
| `21-01` | 匃 | `mand2mc-multiple, bs-gsr-multiple` | kayH; kat | kajH; kat |  |  | 0313a |
| `21-01` | 鶡 | `mand2mc-multiple` | hat; khat |  |  |  | 0313h |
| `21-01` | 渴 | `mand2mc-multiple, mand2mc-extra-vs-bs` | giet; khat | khat |  | gjet | 0313j |
| `21-01` | 喝 | `mand2mc-multiple` | qaeyH; hat |  |  |  | 0313k |
| `21-01` | 朅 | `mand2mc-multiple` | khiet; khiət |  |  |  | 0313m |
| `21-01` | 揭 | `mand2mc-multiple, bs-gsr-multiple` | giet; giət; khieyH; khiet; kiət | gjet; gjot; khjejH; khjet; kjot |  |  | 0313n |
| `21-01` | 楬 | `mand2mc-multiple` | giet; khaet |  |  |  | 0313o |
| `21-01` | 愒 | `mand2mc-multiple, mand2mc-extra-vs-bs` | khayH; khieyH; khiet | khjet |  | khajH; khjejH | 0313s |
| `21-01` | 餲 | `mand2mc-multiple` | qaeyH; qat; qieyH |  |  |  | 0313y |
| `24-01` | 飦 | `mand2mc-multiple, mand2mc-extra-vs-bs` | kan; kiən | kan |  | kjon | 0139m |
| `24-01` | 釬 | `mand2mc-multiple` | hanH; kan |  |  |  | 0139y |
| `24-21` | 單 | `mand2mc-multiple, bs-gsr-multiple, bs-not-in-mand2mc, mand2mc-extra-vs-bs` | tan; tanX | dzyen; tan | dzyen | tanX | 0147a |
| `24-21` | 觶 | `mand2mc-multiple, mand2mc-extra-vs-bs` | cie; cieH | tsye |  | tsyeH | 0147c' |
| `24-21` | 驒 | `mand2mc-multiple` | da; dan; ten |  |  |  | 0147d' |
| `24-21` | 鼉 | `mand2mc-multiple` | da; dan |  |  |  | 0147e' |
| `24-21` | 鱓 | `mand2mc-multiple` | da; dan |  |  |  | 0147h' |
| `24-21` | 癉 | `mand2mc-multiple` | taH; tanX |  |  |  | 0147l |
| `24-21` | 嘽 | `mand2mc-multiple, mand2mc-extra-vs-bs` | than; chienX | than |  | tsyhenX | 0147m |
| `24-21` | 彈 | `mand2mc-multiple, bs-gsr-multiple` | dan; danH | dan; danH |  |  | 0147n |
| `24-21` | 樿 | `mand2mc-multiple` | jienH; cienX |  |  |  | 0147s |
| `24-21` | 燀 | `mand2mc-multiple` | cienX; chienX |  |  |  | 0147t |
| `28-11` | 推 | `mand2mc-multiple, mand2mc-extra-vs-bs` | thwəy; chiwiy | thwoj |  | tsyhwij | 0575a' |
| `28-11` | 唯 | `mand2mc-multiple` | tshwiyX; yiwiy; yiwiyX |  |  |  | 0575i |
| `28-11` | 蓷 | `mand2mc-multiple` | thwəy; chiwiy |  |  |  | 0575i' |
| `28-11` | 蜼 | `mand2mc-multiple` | lwiyX; yiwiyH |  |  |  | 0575q |
| `34-23` | 捘 | `mand2mc-multiple` | tswəyH; tswonH |  |  |  | 0468f' |
| `34-23` | 㕙 | `mand2mc-multiple` | tshwin; tswinH |  |  |  | 0468s |
| `34-23` | 焌 | `mand2mc-multiple` | tswinH; tswonH |  |  |  | 0468u |
| `38-03` | 衿 | `mand2mc-multiple` | gimH; kim |  |  |  | 0651g |
| `38-03` | 坅 | `mand2mc-multiple` | khimX; ṅimX |  |  |  | 0651i |
| `38-03` | 含 | `mand2mc-multiple, bs-gsr-multiple` | hom; homH | hom; homH |  |  | 0651l' |
| `38-03` | 頷 | `mand2mc-multiple, mand2mc-extra-vs-bs` | homX; ṅomX | homX |  | ngomX | 0651n' |
| `38-03` | 黔 | `mand2mc-multiple` | gim; giem |  |  |  | 0651r |
| `38-03` | 陰 | `mand2mc-multiple, mand2mc-extra-vs-bs` | qim; qimH | 'im |  | 'imH | 0651y |
| `38-03` | 唫 | `mand2mc-multiple` | gimX; khim; ṅim |  |  |  | 0652g |
