# MC disagreement analysis

- Candidate additions with at least one MC-disagreement signal: 269

## Category counts

| Category | Count |
| --- | ---: |
| `mand2mc-multiple` | 254 |
| `mand2mc-extra-vs-bs` | 70 |
| `bs-gsr-multiple` | 52 |
| `bs-not-in-mand2mc` | 17 |

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
| `02-32` | 藉 | `mand2mc-multiple, bs-gsr-multiple` | dziaeH; dziek | dzjaeH; dzjek |  |  | 0798b' |
| `02-32` | 踖 | `mand2mc-multiple` | dziek; tshiak; tshiek; tsiek |  |  |  | 0798k |
| `02-32` | 借 | `mand2mc-multiple, bs-gsr-multiple` | tsiaeH; tsiek | tsjaeH; tsjek |  |  | 0798u |
| `02-32` | 蜡 | `mand2mc-multiple` | dẓaeH; tshiəH |  |  |  | 0798y |
| `03-32` | 倘 | `mand2mc-multiple` | thaṅ; thaṅX; chiaṅX |  |  |  | 0725k |
| `03-32` | 賞 | `mand2mc-multiple, mand2mc-extra-vs-bs` | śiaṅ; śiaṅX | syangX |  | syang | 0725n |
| `03-32` | 當 | `mand2mc-multiple, bs-gsr-multiple` | taṅ; taṅH | tang; tangH |  |  | 0725q |
| `03-32` | 償 | `mand2mc-multiple` | jiaṅ; jiaṅH |  |  |  | 0725y |
| `03-38` | 愓 | `mand2mc-multiple, bs-gsr-multiple` | daṅX; śiaṅ | dangX; syang |  |  | 0720e' |
| `03-38` | 𥏫 | `mand2mc-multiple` | śiaṅ; tshiaṅ |  |  |  | 0720i' |
| `03-38` | 盪 | `mand2mc-multiple` | daṅX; thaṅH |  |  |  | 0720n' |
| `03-38` | 蕩 | `mand2mc-multiple, mand2mc-extra-vs-bs` | daṅH; daṅX | dangH |  | dangX | 0720p' |
| `03-38` | 湯 | `mand2mc-multiple, bs-gsr-multiple` | śiaṅ; thaṅ | syang; thang |  |  | 0720z |
| `03-49` | 將 | `mand2mc-multiple, bs-gsr-multiple, mand2mc-extra-vs-bs` | tshiaṅ; tsiaṅ; tsiaṅH | tsjang; tsjangH |  | tshjang | 0727f |
| `03-49` | 藏 | `mand2mc-multiple, bs-gsr-multiple` | dzaṅ; dzaṅH | dzang; dzangH |  |  | 0727g' |
| `03-49` | 裝 | `mand2mc-multiple` | tṣiaṅ; tṣiaṅH |  |  |  | 0727i' |
| `03-57` | 方 | `mand2mc-multiple, mand2mc-extra-vs-bs` | baṅ; piaṅ; piaṅX | pjang |  | bang; pjangX | 0740a |
| `03-57` | 旁 | `mand2mc-multiple, mand2mc-extra-vs-bs` | baṅ; paeṅ | bang |  | paeng | 0740f' |
| `03-57` | 舫 | `mand2mc-multiple, bs-gsr-multiple` | paṅH; piaṅH | pangH; pjangH |  |  | 0740g |
| `03-57` | 放 | `mand2mc-multiple, bs-gsr-multiple` | piaṅH; piaṅX | pjangH; pjangX |  |  | 0740i |
| `03-57` | 枋 | `mand2mc-multiple, mand2mc-extra-vs-bs` | piaeṅH; piaṅ | pjaengH |  | pjang | 0740k |
| `03-57` | 傍 | `mand2mc-multiple, bs-gsr-multiple` | baṅ; baṅH | bang; bangH |  |  | 0740m' |
| `03-57` | 騯 | `mand2mc-multiple` | baeṅ; baṅ |  |  |  | 0740n' |
| `03-57` | 蒡 | `mand2mc-multiple, mand2mc-extra-vs-bs` | baṅ; paeṅ | bang |  | paeng | 0740r' |
| `03-65` | 詤 | `mand2mc-multiple, bs-gsr-multiple` | xwaṅ; xwaṅX | xwang; xwangX |  |  | 0742f' |
| `03-65` | 㡃 | `mand2mc-multiple` | maṅ; xwaṅ |  |  |  | 0742h' |
| `03-65` | 忘 | `mand2mc-multiple, bs-gsr-multiple` | miaṅ; miaṅH | mjang; mjangH |  |  | 0742i |
| `03-65` | 芒 | `mand2mc-multiple, bs-gsr-multiple, mand2mc-extra-vs-bs` | maṅ; miaṅ; xwaṅ; xwaṅX | mang; xwangX |  | mjang; xwang | 0742k |
| `03-65` | 望 | `bs-gsr-multiple, bs-not-in-mand2mc` | miaṅH | mjang; mjangH | mjang |  | 0742m |
| `04-02` | 咳 | `mand2mc-multiple, mand2mc-extra-vs-bs` | həy; khəyH | khojH |  | hoj | 0937g |
| `04-02` | 侅 | `mand2mc-multiple` | kəy; ṅəyH |  |  |  | 0937j |
| `04-02` | 絯 | `mand2mc-multiple` | heayX; kəy |  |  |  | 0937n |
| `04-02` | 劾 | `mand2mc-multiple, bs-gsr-multiple` | həyH; hok | hojH; hok |  |  | 0937x |
| `04-04` | 其 | `mand2mc-multiple, mand2mc-extra-vs-bs` | gi; ki; kiH | gi |  | ki; kiH | 0952a |
| `04-04` | 萁 | `mand2mc-multiple` | gi; ki |  |  |  | 0952m |
| `04-04` | 諆 | `mand2mc-multiple` | khi; ki |  |  |  | 0952n |
| `04-04` | 綦 | `mand2mc-multiple, bs-gsr-multiple` | gi; giH | gi; giH |  |  | 0952z |
| `04-04` | 丌 | `bs-not-in-mand2mc` |  | gi | gi |  | 0952a |
| `04-26` | 等 | `mand2mc-multiple, mand2mc-extra-vs-bs` | təyX; təṅX | tongX |  | tojX | 0961i' |
| `04-29` | 等 | `mand2mc-multiple, mand2mc-extra-vs-bs` | təyX; təṅX | tongX |  | tojX | 0961i' |
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
| `07-25` | 泚 | `mand2mc-multiple, mand2mc-extra-vs-bs` | tsheyX; tshieX | tshjeX |  | tshejX | 0358h |
| `07-25` | 玼 | `mand2mc-multiple` | tsheyX; tshieX |  |  |  | 0358i |
| `07-25` | 訾 | `mand2mc-multiple` | tsie; tsieX; zie |  |  |  | 0358k |
| `07-25` | 訿 | `mand2mc-multiple` | tsie; tsieX; zie |  |  |  | 0358l |
| `07-25` | 骴 | `mand2mc-multiple` | dzie; dzieH |  |  |  | 0358q |
| `07-25` | 眥 | `mand2mc-multiple` | dzeyH; dzieH |  |  |  | 0358s |
| `07-25` | 觜 | `mand2mc-multiple` | tsie; tsiwe |  |  |  | 0358t |
| `07-25` | 柴 | `mand2mc-multiple, mand2mc-extra-vs-bs` | dzieH; dẓea; tsieH | dzrea |  | dzjeH; tsjeH | 0358x |
| `07-29` | 裨 | `mand2mc-multiple` | byie; pyie |  |  |  | 0874e |
| `07-29` | 髀 | `mand2mc-multiple` | beyX; pyieX |  |  |  | 0874f |
| `07-29` | 綼 | `mand2mc-multiple` | bek; byie; byiek; byit |  |  |  | 0874g |
| `07-29` | 埤 | `mand2mc-multiple` | byie; byieX |  |  |  | 0874k |
| `07-29` | 蠯 | `mand2mc-multiple` | beaṅX; byie |  |  |  | 0874v |
| `07-29` | 鞞 | `mand2mc-multiple` | peṅX; pyieX |  |  |  | 0874x |
| `09-01` | 頸 | `mand2mc-multiple, bs-gsr-multiple` | gyieṅ; kyieṅX | gjieng; kjiengX |  |  | 0831n |
| `09-01` | 輕 | `mand2mc-multiple, mand2mc-extra-vs-bs` | khyieṅ; khyieṅH | khjieng |  | khjiengH | 0831o |
| `09-01` | 鑋 | `mand2mc-multiple` | kheṅH; khyieṅ |  |  |  | 0831p |
| `09-01` | 牼 | `mand2mc-multiple, bs-gsr-multiple` | heaṅ; kheaṅ | heang; kheang |  |  | 0831q |
| `09-17` | 廷 | `mand2mc-multiple` | deṅ; deṅH |  |  |  | 0835d |
| `09-17` | 聽 | `mand2mc-multiple, bs-gsr-multiple` | theṅ; theṅH | theng; thengH |  |  | 0835d' |
| `09-17` | 庭 | `mand2mc-multiple` | deṅ; theṅH |  |  |  | 0835h |
| `09-17` | 挺 | `mand2mc-multiple` | deṅX; theṅX |  |  |  | 0835i |
| `09-17` | 蜓 | `mand2mc-multiple` | deṅX; denX |  |  |  | 0835n |
| `09-17` | 珽 | `mand2mc-multiple` | theṅ; theṅX |  |  |  | 0835p |
| `09-17` | 酲 | `mand2mc-multiple` | ḍieṅ; ṭhieṅ |  |  |  | 0835v |
| `09-17` | 郢 | `bs-not-in-mand2mc` |  | yengX | yengX |  | 835 |
| `09-25` | 生 | `bs-gsr-multiple, bs-not-in-mand2mc` | ṣaeṅ | sraeng; srjaeng | srjaeng |  | 0812a |
| `09-25` | 腥 | `mand2mc-multiple` | seṅ; seṅH |  |  |  | 0812a' |
| `09-25` | 醒 | `mand2mc-multiple` | seṅ; seṅH; seṅX |  |  |  | 0812b' |
| `09-25` | 青 | `mand2mc-multiple, mand2mc-extra-vs-bs` | tseṅ; tsheṅ | tsheng |  | tseng | 0812c' |
| `09-25` | 菁 | `mand2mc-multiple` | tseṅ; tsieṅ |  |  |  | 0812f' |
| `09-25` | 請 | `mand2mc-multiple, bs-gsr-multiple` | dzieṅ; tshieṅX | dzjeng; tshjengX |  |  | 0812k' |
| `09-25` | 綪 | `mand2mc-multiple` | tshenH; tṣeaṅ |  |  |  | 0812t' |
| `09-25` | 星 | `mand2mc-multiple, mand2mc-extra-vs-bs` | dzieṅ; seṅ | seng |  | dzjeng | 0812x |
| `09-25` | 猩 | `mand2mc-multiple` | seṅ; ṣaeṅ |  |  |  | 0812z |
| `11-12` | 韣 | `mand2mc-multiple` | duwk; jiəwk; ciəwk |  |  |  | 1224k |
| `11-12` | 䪅 | `mand2mc-multiple` | jiəwk; ciəwk |  |  |  | 1224l |
| `11-12` | 濁 | `bs-not-in-mand2mc, mand2mc-extra-vs-bs` | ṭaewk | draewk | draewk | traewk | 1224p |
| `11-12` | 屬 | `mand2mc-multiple, bs-gsr-multiple` | jiəwk; ciəwk | dzyowk; tsyowk |  |  | 1224s |
| `12-01` | 控 | `mand2mc-multiple, mand2mc-extra-vs-bs` | khaewṅH; khuwṅH | khuwngH |  | khaewngH | 1172a' |
| `12-01` | 跫 | `mand2mc-multiple` | giəwṅ; khaewṅ |  |  |  | 1172f' |
| `12-01` | 空 | `mand2mc-multiple, bs-gsr-multiple, mand2mc-extra-vs-bs` | khuwṅ; khuwṅH; khuwṅX | khuwng; khuwngX |  | khuwngH | 1172h |
| `12-01` | 虹 | `mand2mc-multiple, mand2mc-extra-vs-bs` | ḫuwṅ; kaewṅH | kaewngH |  | huwng | 1172j |
| `12-01` | 矼 | `mand2mc-multiple` | kaewṅ; khuwṅH |  |  |  | 1172x |
| `12-01` | 悾 | `mand2mc-multiple` | khaewṅ; khuwṅ; khuwṅH |  |  |  | 1172z |
| `12-08` | 重 | `mand2mc-multiple, bs-gsr-multiple, bs-not-in-mand2mc` | ḍiəwṅ; ḍiəwṅX | drjowng; drjowngH; drjowngX | drjowngH |  | 1188a |
| `12-08` | 憧 | `mand2mc-multiple` | ḍaewṅH; chiəwṅ |  |  |  | 1188b' |
| `12-08` | 湩 | `mand2mc-multiple` | ṭiəwṅH; tuwṅH |  |  |  | 1188c |
| `12-08` | 罿 | `mand2mc-multiple` | duwṅ; chiəwṅ |  |  |  | 1188c' |
| `12-08` | 種 | `mand2mc-multiple, bs-gsr-multiple` | ciəwṅH; ciəwṅX | tsyowngH; tsyowngX |  |  | 1188d |
| `12-08` | 撞 | `mand2mc-multiple, bs-gsr-multiple` | ḍaewṅ; ḍaewṅH | draewng; draewngH |  |  | 1188f' |
| `12-08` | 穜 | `mand2mc-multiple` | ḍiəwṅ; duwṅ |  |  |  | 1188t |
| `12-25` | 唪 | `mand2mc-multiple` | buwṅX; puwṅX |  |  |  | 1197d' |
| `12-25` | 䋽 | `mand2mc-multiple` | paewṅX; puwṅX |  |  |  | 1197l |
| `12-25` | 夆 | `mand2mc-multiple` | biəwṅ; phiəwṅ |  |  |  | 1197m |
| `12-25` | 逢 | `mand2mc-multiple, mand2mc-extra-vs-bs` | biəwṅ; buwṅ | bjowng |  | buwng | 1197o |
| `12-25` | 縫 | `mand2mc-multiple, bs-gsr-multiple` | biəwṅ; biəwṅH | bjowng; bjowngH |  |  | 1197x |
| `12-25` | 奉 | `mand2mc-multiple, bs-gsr-multiple` | biəwṅX; phiəwṅX | bjowngX; phjowngX |  |  | 1197z |
| `13-32` | 脩 | `mand2mc-multiple, mand2mc-extra-vs-bs` | siuw; yuw; yuwX | sjuw |  | yuw; yuwX | 1077e |
| `13-32` | 條 | `mand2mc-multiple, mand2mc-extra-vs-bs` | dew; thew | dew |  | thew | 1077f |
| `13-32` | 翛 | `mand2mc-multiple` | sew; śiuwk |  |  |  | 1077l |
| `13-45` | 翏 | `mand2mc-multiple, mand2mc-extra-vs-bs` | liewH; lyiwH; liuwH | ljuwH |  | ljewH; ljiwH | 1069a |
| `13-45` | 鏐 | `mand2mc-multiple` | lyiw; liuw |  |  |  | 1069b |
| `13-45` | 摎 | `mand2mc-multiple, bs-gsr-multiple` | kyiw; liuw | kjiw; ljuw |  |  | 1069g |
| `13-45` | 勠 | `mand2mc-multiple` | liuw; liuwH; liuwk |  |  |  | 1069j |
| `13-45` | 瘳 | `mand2mc-multiple, mand2mc-extra-vs-bs` | lew; ṭhiuw | trhjuw |  | lew | 1069k |
| `13-45` | 蓼 | `mand2mc-multiple` | lewX; liuwk |  |  |  | 1069p |
| `13-45` | 膠 | `mand2mc-multiple, bs-gsr-multiple` | kaew; kaewX | kaew; kaewX |  |  | 1069s |
| `16-01` | 嚆 | `mand2mc-multiple` | haew; haewH |  |  |  | 1129b' |
| `16-01` | 藃 | `mand2mc-multiple` | haewk; hawH |  |  |  | 1129c' |
| `16-01` | 膏 | `mand2mc-multiple, bs-gsr-multiple` | kaw; kawH | kaw; kawH |  |  | 1129i |
| `16-01` | 槁 | `mand2mc-multiple` | kawX; khawX |  |  |  | 1129j |
| `16-01` | 槀 | `mand2mc-multiple` | kawX; khawX |  |  |  | 1129k |
| `16-01` | 㪣 | `mand2mc-multiple` | khaew; khaewH |  |  |  | 1129s |
| `16-01` | 熇 | `mand2mc-multiple` | hak; həwk |  |  |  | 1129u |
| `16-01` | 翯 | `mand2mc-multiple, mand2mc-extra-vs-bs` | ḫaewk; haewk | haewk |  | xaewk | 1129v |
| `16-01` | 嗃 | `mand2mc-multiple` | haewk; ḫak |  |  |  | 1129x |
| `16-01` | 稿 | `bs-not-in-mand2mc` |  | kawX | kawX |  | 1129f |
| `16-06` | 咬 | `mand2mc-multiple` | qaew; kaew; ṅaewX |  |  |  | 1166g |
| `16-06` | 校 | `mand2mc-multiple` | ḫaew; ḫaewH; ḫaewX; kaewH; kaewX |  |  |  | 1166i |
| `16-06` | 絞 | `mand2mc-multiple, mand2mc-extra-vs-bs` | ḫaew; kaewX | kaewX |  | haew | 1166k |
| `16-06` | 鉸 | `bs-not-in-mand2mc` |  | kaewX | kaewX |  | 1166 |
| `16-14` | 僥 | `mand2mc-multiple` | kewX; ṅew |  |  |  | 1164b |
| `16-14` | 膮 | `mand2mc-multiple` | hew; hewX |  |  |  | 1164g |
| `16-14` | 磽 | `mand2mc-multiple` | khaew; khewX |  |  |  | 1164i |
| `16-14` | 墝 | `mand2mc-multiple` | khaew; khewX |  |  |  | 1164j |
| `16-14` | 繞 | `mand2mc-multiple, bs-gsr-multiple` | ñiewH; ñiewX | nyewH; nyewX |  |  | 1164k |
| `16-14` | 橈 | `mand2mc-multiple, bs-gsr-multiple` | ṇaewH; ñiew | nraewH; nyew |  |  | 1164p |
| `16-14` | 撓 | `mand2mc-multiple, mand2mc-extra-vs-bs` | ṇaewX; haw | nraewX |  | xaw | 1164s |
| `16-15` | 刀 | `mand2mc-multiple, mand2mc-extra-vs-bs` | taw; tew | taw |  | tew | 1131a |
| `16-15` | 召 | `mand2mc-multiple, bs-gsr-multiple` | ḍiewH; jiewX | drjewH; dzyewX |  |  | 1131e |
| `16-15` | 怊 | `mand2mc-multiple` | ṭhiew; chiew |  |  |  | 1131i |
| `16-15` | 昭 | `mand2mc-multiple, mand2mc-extra-vs-bs` | jiew; ciew; ciewX | tsyew |  | dzyew; tsyewX | 1131m |
| `16-15` | 弨 | `mand2mc-multiple` | chiew; chiewX |  |  |  | 1131s |
| `16-20` | 銚 | `mand2mc-multiple` | dew; thew; tshiew |  |  |  | 1145h |
| `16-20` | 佻 | `mand2mc-multiple` | dew; dewX; thew |  |  |  | 1145n |
| `16-20` | 挑 | `mand2mc-multiple, bs-gsr-multiple, mand2mc-extra-vs-bs` | dewX; thaw; thew | dewX; thew |  | thaw | 1145o |
| `16-20` | 窕 | `mand2mc-multiple` | dewX; thew |  |  |  | 1145q |
| `16-20` | 咷 | `mand2mc-multiple` | daw; thewH |  |  |  | 1145t |
| `16-20` | 駣 | `mand2mc-multiple` | daw; dawX |  |  |  | 1145z |
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
| `24-23` | 儃 | `mand2mc-multiple` | jien; thanX |  |  |  | 0148c |
| `24-23` | 襢 | `mand2mc-multiple, bs-gsr-multiple, mand2mc-extra-vs-bs` | danX; ṭienH; ṭienX | trjenH; trjenX |  | danX | 0148g |
| `24-23` | 皽 | `mand2mc-multiple` | ṭienX; cienX |  |  |  | 0148h |
| `24-23` | 邅 | `mand2mc-multiple` | ḍienX; ṭienX |  |  |  | 0148i |
| `24-23` | 饘 | `mand2mc-multiple, bs-gsr-multiple` | cien; cienX | tsyen; tsyenX |  |  | 0148m |
| `24-23` | 羴 | `bs-not-in-mand2mc` |  | syen | syen |  | 0148q |
| `25-15` | 遠 | `mand2mc-multiple, mand2mc-extra-vs-bs` | ḫiwənH; ḫiwənX | hjwonX |  | hjwonH | 0256f |
| `25-15` | 睘 | `mand2mc-multiple, mand2mc-extra-vs-bs` | giwieṅ; hwaen | hwaen |  | gjwieng | 0256h |
| `25-15` | 還 | `mand2mc-multiple, bs-gsr-multiple` | hwaen; ziwen | hwaen; zjwen |  |  | 0256k |
| `25-15` | 懁 | `mand2mc-multiple` | ḫwaen; hiwien; hwenH |  |  |  | 0256x |
| `26-38` | 匕 | `bs-not-in-mand2mc, mand2mc-extra-vs-bs` | pyiyH | pjijX | pjijX | pjijH | 0566a |
| `26-38` | 批 | `mand2mc-multiple` | bet; phey |  |  |  | 0566a' |
| `26-38` | 膍 | `mand2mc-multiple` | bey; byiy |  |  |  | 0566f' |
| `26-38` | 比 | `mand2mc-multiple, bs-gsr-multiple, mand2mc-extra-vs-bs` | byiy; byiyH; pyiyH; pyiyX | pjijH; pjijX |  | bjij; bjijH | 0566g |
| `26-38` | 牝 | `mand2mc-multiple, bs-gsr-multiple` | byiyX; byinX | bjijX; bjinX |  |  | 0566i |
| `26-38` | 庀 | `mand2mc-multiple` | phyieX; phyiyX |  |  |  | 0566k |
| `26-38` | 疕 | `mand2mc-multiple` | phyieX; phyiyX; pyiyX |  |  |  | 0566l |
| `26-38` | 妣 | `mand2mc-multiple, bs-gsr-multiple` | pyiyH; pyiyX | pjijH; pjijX |  |  | 0566n |
| `26-38` | 庇 | `mand2mc-multiple, bs-gsr-multiple` | pyiy; pyiyH | pjij; pjijH |  |  | 0566p |
| `26-38` | 仳 | `mand2mc-multiple` | biyX; byiy; phyiyX |  |  |  | 0566s |
| `26-38` | 紕 | `mand2mc-multiple` | byie; byiyH; pey; phyie; phyiy |  |  |  | 0566t |
| `27-08` | 誹 | `mand2mc-multiple, mand2mc-extra-vs-bs` | piɨy; piɨyH | pj+j |  | pj+jH | 0579g |
| `27-08` | 騑 | `mand2mc-multiple` | phiɨy; piɨy |  |  |  | 0579k |
| `27-08` | 菲 | `mand2mc-multiple` | biɨyH; phiɨy; phiɨyX |  |  |  | 0579l |
| `27-08` | 蜚 | `mand2mc-multiple, mand2mc-extra-vs-bs` | biɨyH; piɨyX | pj+jX |  | bj+jH | 0579r |
| `27-08` | 陫 | `mand2mc-multiple` | biɨyH; biɨyX |  |  |  | 0579s |
| `28-11` | 推 | `mand2mc-multiple, mand2mc-extra-vs-bs` | thwəy; chiwiy | thwoj |  | tsyhwij | 0575a' |
| `28-11` | 唯 | `mand2mc-multiple` | tshwiyX; yiwiy; yiwiyX |  |  |  | 0575i |
| `28-11` | 蓷 | `mand2mc-multiple` | thwəy; chiwiy |  |  |  | 0575i' |
| `28-11` | 蜼 | `mand2mc-multiple` | lwiyX; yiwiyH |  |  |  | 0575q |
| `32-16` | 稹 | `mand2mc-multiple, mand2mc-extra-vs-bs` | denH; cin; cinX | tsyinX |  | denH; tsyin | 0375b |
| `32-16` | 縝 | `mand2mc-multiple, mand2mc-extra-vs-bs` | cin; cinX | tsyin |  | tsyinX | 0375c |
| `32-16` | 鎮 | `mand2mc-multiple, mand2mc-extra-vs-bs` | ṭin; ṭinH; ṭinX | trinH |  | trin; trinX | 0375f |
| `32-16` | 顛 | `mand2mc-multiple, mand2mc-extra-vs-bs` | den; ten | ten |  | den | 0375m |
| `32-16` | 瑱 | `mand2mc-multiple` | thenH; ṭinH |  |  |  | 0375p |
| `32-16` | 填 | `mand2mc-multiple, mand2mc-extra-vs-bs` | den; denX | den |  | denX | 0375u |
| `33-30` | 分 | `mand2mc-multiple, bs-gsr-multiple` | biunH; piun | bjunH; pjun |  |  | 0471a |
| `33-30` | 忿 | `mand2mc-multiple` | phiunH; phiunX |  |  |  | 0471g |
| `33-30` | 扮 | `mand2mc-multiple` | biun; biunX |  |  |  | 0471l |
| `33-30` | 頒 | `mand2mc-multiple, mand2mc-extra-vs-bs` | biun; paen | paen |  | bjun | 0471p |
| `33-30` | 朌 | `bs-not-in-mand2mc, mand2mc-extra-vs-bs` | biun | paen | paen | bjun | 0471q, 0471y |
| `33-30` | 肦 | `mand2mc-multiple` | biun; paen |  |  |  | 0471y |
| `34-23` | 捘 | `mand2mc-multiple` | tswəyH; tswonH |  |  |  | 0468f' |
| `34-23` | 㕙 | `mand2mc-multiple` | tshwin; tswinH |  |  |  | 0468s |
| `34-23` | 焌 | `mand2mc-multiple` | tswinH; tswonH |  |  |  | 0468u |
| `35-01` | 去 | `mand2mc-multiple, mand2mc-extra-vs-bs` | khiəH; khiəX | khjoH |  | khjoX | 0642a |
| `35-01` | 呿 | `mand2mc-multiple` | khiə; khiəH |  |  |  | 0642c |
| `35-01` | 麮 | `mand2mc-multiple` | khiəH; khiəX |  |  |  | 0642f |
| `35-01` | 胠 | `mand2mc-multiple` | khiaep; khiə |  |  |  | 0642g |
| `35-01` | 蓋 | `mand2mc-multiple, mand2mc-extra-vs-bs` | hap; kayH | kajH |  | hap | 0642q |
| `35-01` | 葢 | `mand2mc-multiple` | hap; kayH |  |  |  | 0642r |
| `35-01` | 溘 | `mand2mc-multiple` | khap; khop |  |  |  | 0642u |
| `35-01` | 磕 | `mand2mc-multiple` | khaeyH; khap |  |  |  | 0642v |
| `35-21` | 去 | `mand2mc-multiple, mand2mc-extra-vs-bs` | khiəH; khiəX | khjoH |  | khjoX | 0642a |
| `35-21` | 呿 | `mand2mc-multiple` | khiə; khiəH |  |  |  | 0642c |
| `35-21` | 麮 | `mand2mc-multiple` | khiəH; khiəX |  |  |  | 0642f |
| `35-21` | 胠 | `mand2mc-multiple` | khiaep; khiə |  |  |  | 0642g |
| `35-21` | 蓋 | `mand2mc-multiple, mand2mc-extra-vs-bs` | hap; kayH | kajH |  | hap | 0642q |
| `35-21` | 葢 | `mand2mc-multiple` | hap; kayH |  |  |  | 0642r |
| `35-21` | 溘 | `mand2mc-multiple` | khap; khop |  |  |  | 0642u |
| `35-21` | 磕 | `mand2mc-multiple` | khaeyH; khap |  |  |  | 0642v |
| `38-03` | 衿 | `mand2mc-multiple` | gimH; kim |  |  |  | 0651g |
| `38-03` | 坅 | `mand2mc-multiple` | khimX; ṅimX |  |  |  | 0651i |
| `38-03` | 含 | `mand2mc-multiple, bs-gsr-multiple` | hom; homH | hom; homH |  |  | 0651l' |
| `38-03` | 頷 | `mand2mc-multiple, mand2mc-extra-vs-bs` | homX; ṅomX | homX |  | ngomX | 0651n' |
| `38-03` | 黔 | `mand2mc-multiple` | gim; giem |  |  |  | 0651r |
| `38-03` | 陰 | `mand2mc-multiple, mand2mc-extra-vs-bs` | qim; qimH | 'im |  | 'imH | 0651y |
| `38-03` | 唫 | `mand2mc-multiple` | gimX; khim; ṅim |  |  |  | 0652g |
