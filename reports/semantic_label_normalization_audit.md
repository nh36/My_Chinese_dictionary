# Semantic label normalization audit

- Generated at: 2026-06-23T09:34:44.272287+00:00
- Normalization config: `data/semantic_components/semantic_aliases.json`
- Total occurrences audited: 15783

## Classification summary

| Classification | Count |
| --- | --- |
| `canonical` | 15640 |
| `explicit_alias` | 67 |
| `needs_review` | 76 |

## Blocked ambiguous aliases

| Alias | Candidate canonical labels | Reason |
| --- | --- | --- |
| `bos` | `bos`, `grunn` | Blocked as an inferred alias because bos is canonical for 牛, but also appears parenthetically in 犛 grunn(iens). |
| `den` | `dent`, `molar` | Blocked because it can refer to dent/tooth material or surface from molar/dens explanations. |
| `dens` | `dent`, `molar` | Blocked because it can refer to dent/tooth material or surface from molar/dens explanations. |
| `os` | `or`, `oss` | Blocked because it can refer to 口/or or 骨/oss. |

## Intentional scoped duplicate graphs

| Graph | Abbreviation | Scope | Only in | Note |
| --- | --- | --- | --- | --- |
| `田` | `forn` | only_in | 盧 | Same visible graph as 田/ager, but different semantic label and restricted use. |

## Unsafe alias candidates produced by the old heuristic

| Graph | Canonical label | Expanded Latin | Candidate alias | Status | Used now |
| --- | --- | --- | --- | --- | --- |
| `田` | `ager` | `ager` | `ag` | `explicit_alias` | yes |
| `髟` | `crin` | `crin(is)` | `cri` | `explicit_alias` | yes |
| `刀` | `cult` | `cult(er)` | `cul` | `explicit_alias` | yes |
| `齒` | `dent` | `(dens), dent(is)` | `den` | `blocked_ambiguous_alias` | no |
| `齒` | `dent` | `(dens), dent(is)` | `dens` | `blocked_ambiguous_alias` | no |
| `龍` | `dracon` | `(draco), dracon(is)` | `draco` | `unsafe_candidate` | no |
| `犛` | `grunn` | `(bos) grunn(iens)` | `bos` | `blocked_ambiguous_alias` | yes |
| `手` | `man` | `man(us)` | `manu` | `explicit_alias` | yes |
| `牙` | `molar` | `molar(is dens)` | `den` | `blocked_ambiguous_alias` | no |
| `牙` | `molar` | `molar(is dens)` | `dens` | `blocked_ambiguous_alias` | no |
| `口` | `or` | `(os,) or(is)` | `os` | `blocked_ambiguous_alias` | no |
| `骨` | `oss` | `(os,) oss(is)` | `os` | `blocked_ambiguous_alias` | no |
| `戶` | `ost` | `ost(ium)` | `os` | `blocked_ambiguous_alias` | no |
| `足` | `ped` | `(pes,) ped(is)` | `pes` | `unsafe_candidate` | no |
| `示` | `spirit` | `spirit(us)` | `spir` | `explicit_alias` | yes |
| `土` | `terr` | `terr(a)` | `ter` | `explicit_alias` | yes |

Watched tokens with no current heuristic match: `can`

## `infirm` occurrences

| Source | GSC | Character | Label | Fields | Component | IDS | Snippet |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `current_main_tex` | `18-08` | `痑` | `infirm` | raw_block | `疒` | `⿸疒多` | `{{\textsuperscript{infirm·}}\large{lay}},` |
| `current_main_tex` | `18-13` | `瘥` | `infirm` | raw_block | `疒` | `⿸疒差` | `{\large{{\textsuperscript{infirm·}}tsay₂}},` |
| `current_main_tex` | `18-16` | `疲` | `infirm` | raw_block | `疒` | `⿸疒皮` | `{\large{\textsuperscript{infirm·}pay}},` |
| `current_main_tex` | `19-21` | `痤` | `infirm` | raw_block | `疒` | `⿸疒坐` | `{\large{{\textsuperscript{infirm·}}tsoy}},` |
| `current_main_tex` | `01-28` | `瘀` | `infirm` | raw_block | `疒` | `⿸疒於` | `{\large{{\textsuperscript{infirm·}}a}},` |
| `current_main_tex` | `01-38` | `瘏` | `infirm` | raw_block | `疒` | `⿸疒者` | `{\large{{\textsuperscript{infirm·}}ta}},` |
| `current_main_tex` | `01-57` | `疽` | `infirm` | raw_block | `疒` | `⿸疒且` | `{\large{{\textsuperscript{infirm·}}tsa}},` |
| `current_main_tex` | `01-67` | `痡` | `infirm` | raw_block | `疒` | `⿸疒甫` | `{\large{{\textsuperscript{infirm·}}pa₂}},` |
| `current_main_tex` | `10-01` | `痀` | `infirm` | raw_block | `疒` | `⿸疒句` | `{\large{{\textsuperscript{infirm·}}ko}},` |
| `earlier_pilot_tex` | `18-08` | `痑` | `infirm` | raw_block | `疒` | `⿸疒多` | `{{\textsuperscript{infirm·}}\large{lay}},` |
| `earlier_pilot_tex` | `18-13` | `瘥` | `infirm` | raw_block | `疒` | `⿸疒差` | `{\large{{\textsuperscript{infirm·}}tsay₂}},` |
| `earlier_pilot_tex` | `18-16` | `疲` | `infirm` | raw_block | `疒` | `⿸疒皮` | `{\large{\textsuperscript{infirm·}pay}},` |
| `earlier_pilot_tex` | `19-21` | `痤` | `infirm` | raw_block | `疒` | `⿸疒坐` | `{\large{{\textsuperscript{infirm·}}tsoy}},` |
| `earlier_pilot_tex` | `01-28` | `瘀` | `infirm` | raw_block | `疒` | `⿸疒於` | `{\large{{\textsuperscript{infirm·}}a}},` |
| `earlier_pilot_tex` | `01-38` | `瘏` | `infirm` | raw_block | `疒` | `⿸疒者` | `{\large{{\textsuperscript{infirm·}}ta}},` |
| `earlier_pilot_tex` | `01-57` | `疽` | `infirm` | raw_block | `疒` | `⿸疒且` | `{\large{{\textsuperscript{infirm·}}tsa}},` |
| `earlier_pilot_tex` | `01-67` | `痡` | `infirm` | raw_block | `疒` | `⿸疒甫` | `{\large{{\textsuperscript{infirm·}}pa₂}},` |
| `earlier_pilot_tex` | `10-01` | `痀` | `infirm` | raw_block | `疒` | `⿸疒句` | `{\large{{\textsuperscript{infirm·}}ko}},` |
| `current_tex_entries_json` | `18-08` | `痑` | `infirm` | raw_block | `疒` | `⿸疒多` | `{{\textsuperscript{infirm·}}\large{lay}},` |
| `current_tex_entries_json` | `18-13` | `瘥` | `infirm` | raw_block | `疒` | `⿸疒差` | `{\large{{\textsuperscript{infirm·}}tsay₂}},` |
| `current_tex_entries_json` | `18-16` | `疲` | `infirm` | raw_block | `疒` | `⿸疒皮` | `{\large{\textsuperscript{infirm·}pay}},` |
| `current_tex_entries_json` | `19-21` | `痤` | `infirm` | raw_block | `疒` | `⿸疒坐` | `{\large{{\textsuperscript{infirm·}}tsoy}},` |
| `current_tex_entries_json` | `01-28` | `瘀` | `infirm` | raw_block | `疒` | `⿸疒於` | `{\large{{\textsuperscript{infirm·}}a}},` |
| `current_tex_entries_json` | `01-38` | `瘏` | `infirm` | raw_block | `疒` | `⿸疒者` | `{\large{{\textsuperscript{infirm·}}ta}},` |
| `current_tex_entries_json` | `01-57` | `疽` | `infirm` | raw_block | `疒` | `⿸疒且` | `{\large{{\textsuperscript{infirm·}}tsa}},` |
| `current_tex_entries_json` | `01-67` | `痡` | `infirm` | raw_block | `疒` | `⿸疒甫` | `{\large{{\textsuperscript{infirm·}}pa₂}},` |
| `current_tex_entries_json` | `10-01` | `痀` | `infirm` | raw_block | `疒` | `⿸疒句` | `{\large{{\textsuperscript{infirm·}}ko}},` |
| `curation_json` | `01-01` | `痼` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒固` | `痼	%gù
{\large{\textsuperscript{infirm·}k\textoverset{a}{a}}},
\textit{kuH};	%49` |
| `curation_json` | `02-40` | `瘼` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒莫` | `瘼	%mo4
{\large{\textsuperscript{infirm·}mak}},
\textit{mak};	%0802q` |
| `curation_json` | `03-38` | `瘍` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒昜` | `瘍	%yang2 / yáng
{\large{\textsuperscript{infirm·}laṅ}},
\textit{yaṅ};	%0720s` |
| `curation_json` | `03-39` | `痒` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒羊` | `痒	%yang2 / yang3 / yáng
{\large{\textsuperscript{infirm·}qaṅ}},
\textit{yaṅ};	%0732i
\textit{yaṅX};
\textit{ziaṅ};` |
| `curation_json` | `03-39` | `癢` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒養` | `癢	%yang3 / yǎng
{\large{\textsuperscript{infirm·}g\textoverset{b}{a}ṅ}},
\textit{yaṅX};	%0732r` |
| `curation_json` | `03-48` | `瘡` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒倉` | `瘡	%chuang1 / chuāng
{\large{\textsuperscript{infirm·}tsaṅ}},
\textit{tṣhiaṅ};	%0703n` |
| `curation_json` | `04-17` | `痏` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒有` | `痏	%wei3
{\large{\textsuperscript{infirm·}quy₃}},
\textit{ḫwiyX};	%0995x` |
| `curation_json` | `04-26` | `痔` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒寺` | `痔	%zhi4
{\large{\textsuperscript{infirm·}ty₂}},
\textit{ḍiX};	%0961t` |
| `curation_json` | `04-29` | `痔` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒寺` | `痔	%zhi4
{\large{\textsuperscript{infirm·}ty₆}},
\textit{ḍiX};	%0961t` |
| `curation_json` | `07-25` | `疵` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒此` | `疵	%ci1
{\large{\textsuperscript{infirm·}tse}},
\textit{dzie};	%0358p` |
| `curation_json` | `10-37` | `瘦` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒叟` | `瘦	%shou4
{\large{\textsuperscript{infirm·}  *su₂}},
\textit{ṣiuwH};	%1097i` |
| `curation_json` | `12-08` | `𤺄` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒童` | `𤺄	%zhong3
{\large{\textsuperscript{infirm·}toṅ₂}},
\textit{jiəwṅX};	%1188d'` |
| `curation_json` | `12-10` | `痛` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒甬` | `痛	%tong4 / tòng
{\large{\textsuperscript{infirm·}loṅ₂}},
\textit{thuwṅH};	%1185q` |
| `curation_json` | `13-45` | `瘳` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒翏` | `瘳	%chou1 / chōu
{\large{\textsuperscript{infirm·}riw}},
\textit{lew};	%1069k
\textit{ṭhiuw};` |
| `curation_json` | `16-24` | `療` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒尞` | `療	%liao2
{\large{\textsuperscript{infirm·}rew₂}},
\textit{liewH};	%1151f` |
| `curation_json` | `16-33` | `痟` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒肖` | `痟	%xiao1
{\large{\textsuperscript{infirm·}sew₃}},
\textit{siew};	%1149k` |
| `curation_json` | `20-01` | `瘈` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒契` | `瘈	%ji4 / zhi4 / jì / zhì
{\large{\textsuperscript{infirm·}ket₂}},
\textit{kyieyH};	%0279g
\textit{cieyH};` |
| `curation_json` | `21-26` | `癘` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒萬` | `癘	%li4
{\large{\textsuperscript{infirm·}man}},
\textit{lieyH};	%0340d` |
| `curation_json` | `23-17` | `㾓` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒肙` | `㾓	%yuan1
{\large{\textsuperscript{infirm·}quen}},
\textit{qiwien};	%0228d` |
| `curation_json` | `24-21` | `癉` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒單` | `癉	%duo4? / dan3
{\large{\textsuperscript{infirm·}tar}},
\textit{taH};	%0147l
\textit{tanX};` |
| `curation_json` | `24-23` | `𤺺` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒亶` | `𤺺	%dan3
{\large{\textsuperscript{infirm·}tan}},
\textit{tanX};	%0148b` |
| `curation_json` | `25-01` | `痯` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒官` | `痯	%guan3
{\large{\textsuperscript{infirm·}kuan}},
\textit{kwanX};	%0157g` |
| `curation_json` | `26-27` | `癠` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒齊` | `癠	%ji4
{\large{\textsuperscript{infirm·}tsy₃}},
\textit{dzey};	%0593k
\textit{dzeyH};
\textit{dzeyX};` |
| `curation_json` | `26-38` | `疕` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒匕` | `疕	%bi3
{\large{\textsuperscript{infirm·}piy}},
\textit{phyieX};	%0566l
\textit{phyiyX};
\textit{pyiyX};` |
| `curation_json` | `28-01` | `瘣` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒鬼` | `瘣	%lei3
{\large{\textsuperscript{infirm·}ʔuy}},
\textit{hwəyX};	%0569h` |
| `curation_json` | `31-20` | `瘁` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒卒` | `瘁	%cui4
{\large{\textsuperscript{infirm·}tsut}},
\textit{dzwiyH};	%0490k` |
| `curation_json` | `32-16` | `瘨` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒真` | `瘨	%dian1
{\large{\textsuperscript{infirm·}tin}},
\textit{ten};	%0375l` |
| `curation_json` | `32-40` | `痻` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒昏` | `痻	%min2
{\large{\textsuperscript{infirm·}miṅ₂}},
\textit{menX};	%0457f, 0457r
\textit{mwən};
\textit{min};
\textit{hwən};` |
| `curation_json` | `33-15` | `疹` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒㐱` | `疹	%zhen4 / zhèn
{\large{\textsuperscript{infirm·}tyn}},
\textit{ṭhinH};	%0453j` |
| `curation_json` | `36-12` | `痁` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒占` | `痁	%shan1
{\large{\textsuperscript{infirm·}tem}},
\textit{śiem};	%0618j
\textit{śiemH};
\textit{temH};` |
| `integrated_series_curated_entry` | `01-01` | `痼` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒固` | `痼	%gù
{\large{\textsuperscript{infirm·}k\textoverset{a}{a}}},
\textit{kuH};	%49` |
| `integrated_series_hand_entry` | `01-28` | `瘀` | `infirm` | raw_block | `疒` | `⿸疒於` | `{\large{{\textsuperscript{infirm·}}a}},` |
| `integrated_series_hand_entry` | `01-38` | `瘏` | `infirm` | raw_block | `疒` | `⿸疒者` | `{\large{{\textsuperscript{infirm·}}ta}},` |
| `integrated_series_hand_entry` | `01-57` | `疽` | `infirm` | raw_block | `疒` | `⿸疒且` | `{\large{{\textsuperscript{infirm·}}tsa}},` |
| `integrated_series_hand_entry` | `01-67` | `痡` | `infirm` | raw_block | `疒` | `⿸疒甫` | `{\large{{\textsuperscript{infirm·}}pa₂}},` |
| `integrated_series_curated_entry` | `02-40` | `瘼` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒莫` | `瘼	%mo4
{\large{\textsuperscript{infirm·}mak}},
\textit{mak};	%0802q` |
| `integrated_series_curated_entry` | `03-38` | `瘍` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒昜` | `瘍	%yang2 / yáng
{\large{\textsuperscript{infirm·}laṅ}},
\textit{yaṅ};	%0720s` |
| `integrated_series_curated_entry` | `03-39` | `痒` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒羊` | `痒	%yang2 / yang3 / yáng
{\large{\textsuperscript{infirm·}qaṅ}},
\textit{yaṅ};	%0732i
\textit{yaṅX};
\textit{ziaṅ};` |
| `integrated_series_curated_entry` | `03-39` | `癢` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒養` | `癢	%yang3 / yǎng
{\large{\textsuperscript{infirm·}g\textoverset{b}{a}ṅ}},
\textit{yaṅX};	%0732r` |
| `integrated_series_curated_entry` | `03-48` | `瘡` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒倉` | `瘡	%chuang1 / chuāng
{\large{\textsuperscript{infirm·}tsaṅ}},
\textit{tṣhiaṅ};	%0703n` |
| `integrated_series_curated_entry` | `04-17` | `痏` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒有` | `痏	%wei3
{\large{\textsuperscript{infirm·}quy₃}},
\textit{ḫwiyX};	%0995x` |
| `integrated_series_curated_entry` | `04-26` | `痔` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒寺` | `痔	%zhi4
{\large{\textsuperscript{infirm·}ty₂}},
\textit{ḍiX};	%0961t` |
| `integrated_series_curated_entry` | `04-29` | `痔` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒寺` | `痔	%zhi4
{\large{\textsuperscript{infirm·}ty₆}},
\textit{ḍiX};	%0961t` |
| `integrated_series_curated_entry` | `07-25` | `疵` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒此` | `疵	%ci1
{\large{\textsuperscript{infirm·}tse}},
\textit{dzie};	%0358p` |
| `integrated_series_hand_entry` | `10-01` | `痀` | `infirm` | raw_block | `疒` | `⿸疒句` | `{\large{{\textsuperscript{infirm·}}ko}},` |
| `integrated_series_curated_entry` | `10-37` | `瘦` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒叟` | `瘦	%shou4
{\large{\textsuperscript{infirm·}  *su₂}},
\textit{ṣiuwH};	%1097i` |
| `integrated_series_curated_entry` | `12-08` | `𤺄` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒童` | `𤺄	%zhong3
{\large{\textsuperscript{infirm·}toṅ₂}},
\textit{jiəwṅX};	%1188d'` |
| `integrated_series_curated_entry` | `12-10` | `痛` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒甬` | `痛	%tong4 / tòng
{\large{\textsuperscript{infirm·}loṅ₂}},
\textit{thuwṅH};	%1185q` |
| `integrated_series_curated_entry` | `13-45` | `瘳` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒翏` | `瘳	%chou1 / chōu
{\large{\textsuperscript{infirm·}riw}},
\textit{lew};	%1069k
\textit{ṭhiuw};` |
| `integrated_series_curated_entry` | `16-24` | `療` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒尞` | `療	%liao2
{\large{\textsuperscript{infirm·}rew₂}},
\textit{liewH};	%1151f` |
| `integrated_series_curated_entry` | `16-33` | `痟` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒肖` | `痟	%xiao1
{\large{\textsuperscript{infirm·}sew₃}},
\textit{siew};	%1149k` |
| `integrated_series_hand_entry` | `18-08` | `痑` | `infirm` | raw_block | `疒` | `⿸疒多` | `{{\textsuperscript{infirm·}}\large{lay}},` |
| `integrated_series_hand_entry` | `18-13` | `瘥` | `infirm` | raw_block | `疒` | `⿸疒差` | `{\large{{\textsuperscript{infirm·}}tsay₂}},` |
| `integrated_series_hand_entry` | `18-16` | `疲` | `infirm` | raw_block | `疒` | `⿸疒皮` | `{\large{\textsuperscript{infirm·}pay}},` |
| `integrated_series_hand_entry` | `19-21` | `痤` | `infirm` | raw_block | `疒` | `⿸疒坐` | `{\large{{\textsuperscript{infirm·}}tsoy}},` |
| `integrated_series_curated_entry` | `20-01` | `瘈` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒契` | `瘈	%ji4 / zhi4 / jì / zhì
{\large{\textsuperscript{infirm·}ket₂}},
\textit{kyieyH};	%0279g
\textit{cieyH};` |
| `integrated_series_curated_entry` | `21-26` | `癘` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒萬` | `癘	%li4
{\large{\textsuperscript{infirm·}man}},
\textit{lieyH};	%0340d` |
| `integrated_series_curated_entry` | `23-17` | `㾓` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒肙` | `㾓	%yuan1
{\large{\textsuperscript{infirm·}quen}},
\textit{qiwien};	%0228d` |
| `integrated_series_curated_entry` | `24-21` | `癉` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒單` | `癉	%duo4? / dan3
{\large{\textsuperscript{infirm·}tar}},
\textit{taH};	%0147l
\textit{tanX};` |
| `integrated_series_curated_entry` | `24-23` | `𤺺` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒亶` | `𤺺	%dan3
{\large{\textsuperscript{infirm·}tan}},
\textit{tanX};	%0148b` |
| `integrated_series_curated_entry` | `25-01` | `痯` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒官` | `痯	%guan3
{\large{\textsuperscript{infirm·}kuan}},
\textit{kwanX};	%0157g` |
| `integrated_series_curated_entry` | `26-27` | `癠` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒齊` | `癠	%ji4
{\large{\textsuperscript{infirm·}tsy₃}},
\textit{dzey};	%0593k
\textit{dzeyH};
\textit{dzeyX};` |
| `integrated_series_curated_entry` | `26-38` | `疕` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒匕` | `疕	%bi3
{\large{\textsuperscript{infirm·}piy}},
\textit{phyieX};	%0566l
\textit{phyiyX};
\textit{pyiyX};` |
| `integrated_series_curated_entry` | `28-01` | `瘣` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒鬼` | `瘣	%lei3
{\large{\textsuperscript{infirm·}ʔuy}},
\textit{hwəyX};	%0569h` |
| `integrated_series_curated_entry` | `31-20` | `瘁` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒卒` | `瘁	%cui4
{\large{\textsuperscript{infirm·}tsut}},
\textit{dzwiyH};	%0490k` |
| `integrated_series_curated_entry` | `32-16` | `瘨` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒真` | `瘨	%dian1
{\large{\textsuperscript{infirm·}tin}},
\textit{ten};	%0375l` |
| `integrated_series_curated_entry` | `32-40` | `痻` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒昏` | `痻	%min2
{\large{\textsuperscript{infirm·}miṅ₂}},
\textit{menX};	%0457f, 0457r
\textit{mwən};
\textit{min};
\textit{hwən};` |
| `integrated_series_curated_entry` | `33-15` | `疹` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒㐱` | `疹	%zhen4 / zhèn
{\large{\textsuperscript{infirm·}tyn}},
\textit{ṭhinH};	%0453j` |
| `integrated_series_curated_entry` | `36-12` | `痁` | `infirm` | render_latex, transliteration_latex | `疒` | `⿸疒占` | `痁	%shan1
{\large{\textsuperscript{infirm·}tem}},
\textit{śiem};	%0618j
\textit{śiemH};
\textit{temH};` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}mak}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}laṅ}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}qaṅ}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}g\textoverset{b}{a}ṅ}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}tsaṅ}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}quy₃}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}ty₂}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}ty₆}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}tse}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}  *su₂}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}toṅ₂}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}loṅ₂}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}riw}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}rew₂}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}sew₃}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}ket₂}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}man}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}quen}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}tar}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}tan}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}kuan}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}tsy₃}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}piy}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}ʔuy}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}tsut}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}tin}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}miṅ₂}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}tyn}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}tem}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}k\textoverset{a}{a}}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{{\textsuperscript{infirm·}}ta}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{{\textsuperscript{infirm·}}tsa}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{{\textsuperscript{infirm·}}tsoy}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}k\textoverset{a}{a}}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{{\textsuperscript{infirm·}}a}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{{\textsuperscript{infirm·}}ta}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{{\textsuperscript{infirm·}}tsa}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{{\textsuperscript{infirm·}}pa₂}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}mak}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}laṅ}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}qaṅ}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}g\textoverset{b}{a}ṅ}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}tsaṅ}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}quy₃}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}ty₂}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}ty₆}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}tse}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{{\textsuperscript{infirm·}}ko}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}  *su₂}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}toṅ₂}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}loṅ₂}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}riw}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}rew₂}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}sew₃}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{{\textsuperscript{infirm·}}\large{lay}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{{\textsuperscript{infirm·}}tsay₂}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}pay}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{{\textsuperscript{infirm·}}tsoy}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}ket₂}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}man}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}quen}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}tar}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}tan}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}kuan}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}tsy₃}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}piy}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}ʔuy}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}tsut}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}tin}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}miṅ₂}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}tyn}},` |
| `validation_tex` | `` | `` | `infirm` | line | `` | `` | `{\large{\textsuperscript{infirm·}tem}},` |

## Audited `bos` occurrences

| Source | GSC | Character | Label | Fields | Component | IDS | Snippet |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `curation_json` | `03-57` | `牥` | `bos` | render_latex, transliteration_latex | `牛` | `⿰牛方` | `牥	%fang1
{\large{\textsuperscript{bos·}paṅ}},
\textit{piaṅ};	%0740l` |
| `curation_json` | `04-26` | `特` | `bos` | render_latex, transliteration_latex | `牛` | `⿰牛寺` | `特	%te4 / tè
{\large{\textsuperscript{bos·}ty₂}},
\textit{dək};	%0961h'` |
| `curation_json` | `04-29` | `特` | `bos` | render_latex, transliteration_latex | `牛` | `⿰牛寺` | `特	%te4 / tè
{\large{\textsuperscript{bos·}ty₆}},
\textit{dək};	%0961h'` |
| `curation_json` | `09-01` | `牼` | `bos` | render_latex, transliteration_latex | `牛` | `⿰牛巠` | `牼	%keng1 / kēng
{\large{\textsuperscript{bos·}leṅ}},
\textit{heaṅ};	%0831q
\textit{kheaṅ};` |
| `curation_json` | `09-25` | `牲` | `bos` | render_latex, transliteration_latex | `牛` | `⿰牛生` | `牲	%sheng1
{\large{\textsuperscript{bos·}tseṅ₂}},
\textit{ṣaeṅ};	%0812e` |
| `curation_json` | `14-14` | `犢` | `bos` | render_latex, transliteration_latex | `牛` | `⿰牛賣` | `犢	%du2 / dú
{\large{\textsuperscript{bos·}me}},
\textit{duwk};	%1023l` |
| `curation_json` | `16-01` | `犒` | `bos` | render_latex, transliteration_latex | `牛` | `⿰牛高` | `犒	%kao4 / kào
{\large{\textsuperscript{bos·}kaw}},
\textit{khawH};	%1129l` |
| `curation_json` | `25-11` | `㹖` | `bos` | render_latex, transliteration_latex | `牛` | `⿰牛豢` | `㹖	%huan4
{\large{\textsuperscript{bos·}k\textoverset{a}{o}n}},
\textit{ḫwanH};	%0226p` |
| `curation_json` | `26-38` | `牝` | `bos` | render_latex, transliteration_latex | `牛` | `⿰牛匕` | `牝	%pin4 / pìn
{\large{\textsuperscript{bos·}piy}},
\textit{byiyX};	%0566i
\textit{byinX};` |
| `curation_json` | `32-05` | `牽` | `bos` | render_latex, transliteration_latex | `牛` | `⿱⿱亠⿻幺冖牛` | `牽	%qian1 / qiān
{\large{quin\textsuperscript{˸bos}}},
\textit{khen};	%0366k` |
| `curation_json` | `33-20` | `牣` | `bos` | render_latex, transliteration_latex | `牛` | `⿰牛刃` | `牣	%ren4
{\large{\textsuperscript{bos·}nyn}},
\textit{ñinH};	%0456d` |
| `curation_json` | `34-18` | `犉` | `bos` | render_latex, transliteration_latex | `牛` | `⿰牛享` | `犉	%run2
{\large{\textsuperscript{bos·}tur₃}},
\textit{ñiwin};	%0464m` |
| `integrated_series_curated_entry` | `03-57` | `牥` | `bos` | render_latex, transliteration_latex | `牛` | `⿰牛方` | `牥	%fang1
{\large{\textsuperscript{bos·}paṅ}},
\textit{piaṅ};	%0740l` |
| `integrated_series_curated_entry` | `04-26` | `特` | `bos` | render_latex, transliteration_latex | `牛` | `⿰牛寺` | `特	%te4 / tè
{\large{\textsuperscript{bos·}ty₂}},
\textit{dək};	%0961h'` |
| `integrated_series_curated_entry` | `04-29` | `特` | `bos` | render_latex, transliteration_latex | `牛` | `⿰牛寺` | `特	%te4 / tè
{\large{\textsuperscript{bos·}ty₆}},
\textit{dək};	%0961h'` |
| `integrated_series_curated_entry` | `09-01` | `牼` | `bos` | render_latex, transliteration_latex | `牛` | `⿰牛巠` | `牼	%keng1 / kēng
{\large{\textsuperscript{bos·}leṅ}},
\textit{heaṅ};	%0831q
\textit{kheaṅ};` |
| `integrated_series_curated_entry` | `09-25` | `牲` | `bos` | render_latex, transliteration_latex | `牛` | `⿰牛生` | `牲	%sheng1
{\large{\textsuperscript{bos·}tseṅ₂}},
\textit{ṣaeṅ};	%0812e` |
| `integrated_series_curated_entry` | `14-14` | `犢` | `bos` | render_latex, transliteration_latex | `牛` | `⿰牛賣` | `犢	%du2 / dú
{\large{\textsuperscript{bos·}me}},
\textit{duwk};	%1023l` |
| `integrated_series_curated_entry` | `16-01` | `犒` | `bos` | render_latex, transliteration_latex | `牛` | `⿰牛高` | `犒	%kao4 / kào
{\large{\textsuperscript{bos·}kaw}},
\textit{khawH};	%1129l` |
| `integrated_series_curated_entry` | `25-11` | `㹖` | `bos` | render_latex, transliteration_latex | `牛` | `⿰牛豢` | `㹖	%huan4
{\large{\textsuperscript{bos·}k\textoverset{a}{o}n}},
\textit{ḫwanH};	%0226p` |
| `integrated_series_curated_entry` | `26-38` | `牝` | `bos` | render_latex, transliteration_latex | `牛` | `⿰牛匕` | `牝	%pin4 / pìn
{\large{\textsuperscript{bos·}piy}},
\textit{byiyX};	%0566i
\textit{byinX};` |
| `integrated_series_curated_entry` | `32-05` | `牽` | `bos` | render_latex, transliteration_latex | `牛` | `⿱⿱亠⿻幺冖牛` | `牽	%qian1 / qiān
{\large{quin\textsuperscript{˸bos}}},
\textit{khen};	%0366k` |
| `integrated_series_curated_entry` | `33-20` | `牣` | `bos` | render_latex, transliteration_latex | `牛` | `⿰牛刃` | `牣	%ren4
{\large{\textsuperscript{bos·}nyn}},
\textit{ñinH};	%0456d` |
| `integrated_series_curated_entry` | `34-18` | `犉` | `bos` | render_latex, transliteration_latex | `牛` | `⿰牛享` | `犉	%run2
{\large{\textsuperscript{bos·}tur₃}},
\textit{ñiwin};	%0464m` |
| `validation_tex` | `` | `` | `bos` | line | `` | `` | `{\large{\textsuperscript{bos·}paṅ}},` |
| `validation_tex` | `` | `` | `bos` | line | `` | `` | `{\large{\textsuperscript{bos·}ty₂}},` |
| `validation_tex` | `` | `` | `bos` | line | `` | `` | `{\large{\textsuperscript{bos·}ty₆}},` |
| `validation_tex` | `` | `` | `bos` | line | `` | `` | `{\large{\textsuperscript{bos·}leṅ}},` |
| `validation_tex` | `` | `` | `bos` | line | `` | `` | `{\large{\textsuperscript{bos·}tseṅ₂}},` |
| `validation_tex` | `` | `` | `bos` | line | `` | `` | `{\large{\textsuperscript{bos·}me}},` |
| `validation_tex` | `` | `` | `bos` | line | `` | `` | `{\large{\textsuperscript{bos·}kaw}},` |
| `validation_tex` | `` | `` | `bos` | line | `` | `` | `{\large{\textsuperscript{bos·}k\textoverset{a}{o}n}},` |
| `validation_tex` | `` | `` | `bos` | line | `` | `` | `{\large{\textsuperscript{bos·}piy}},` |
| `validation_tex` | `` | `` | `bos` | line | `` | `` | `{\large{quin\textsuperscript{˸bos}}},` |
| `validation_tex` | `` | `` | `bos` | line | `` | `` | `{\large{\textsuperscript{bos·}nyn}},` |
| `validation_tex` | `` | `` | `bos` | line | `` | `` | `{\large{\textsuperscript{bos·}tur₃}},` |
| `validation_tex` | `` | `` | `bos` | line | `` | `` | `{\large{\textsuperscript{bos·}paṅ}},` |
| `validation_tex` | `` | `` | `bos` | line | `` | `` | `{\large{\textsuperscript{bos·}ty₂}},` |
| `validation_tex` | `` | `` | `bos` | line | `` | `` | `{\large{\textsuperscript{bos·}ty₆}},` |
| `validation_tex` | `` | `` | `bos` | line | `` | `` | `{\large{\textsuperscript{bos·}leṅ}},` |
| `validation_tex` | `` | `` | `bos` | line | `` | `` | `{\large{\textsuperscript{bos·}tseṅ₂}},` |
| `validation_tex` | `` | `` | `bos` | line | `` | `` | `{\large{\textsuperscript{bos·}me}},` |
| `validation_tex` | `` | `` | `bos` | line | `` | `` | `{\large{\textsuperscript{bos·}kaw}},` |
| `validation_tex` | `` | `` | `bos` | line | `` | `` | `{\large{\textsuperscript{bos·}k\textoverset{a}{o}n}},` |
| `validation_tex` | `` | `` | `bos` | line | `` | `` | `{\large{\textsuperscript{bos·}piy}},` |
| `validation_tex` | `` | `` | `bos` | line | `` | `` | `{\large{quin\textsuperscript{˸bos}}},` |
| `validation_tex` | `` | `` | `bos` | line | `` | `` | `{\large{\textsuperscript{bos·}nyn}},` |
| `validation_tex` | `` | `` | `bos` | line | `` | `` | `{\large{\textsuperscript{bos·}tur₃}},` |

## Needs-review labels in use

| Source | GSC | Character | Label | Fields | Component | IDS | Snippet |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `curation_json` | `02-08` | `彠` | `尋` | render_latex, transliteration_latex | `尋` | `⿰尋蒦` | `彠	%huo4
{\large{\textsuperscript{尋·}quak}},
\textit{qiwak};	%0784f` |
| `curation_json` | `02-27` | `夜` | `夕` | render_latex, transliteration_latex | `夕` | `⿱亠⿰亻⿴夂丶` | `夜	%ye4 / yè
{\large{qak\textsuperscript{˸夕}}},
\textit{yaeH};	%0800j` |
| `curation_json` | `03-57` | `旁` | `同` | render_latex, transliteration_latex | `同` | `⿱⿱⿱亠丷冖方` | `旁	%pang2 / bang1 / páng
{\large{\textsuperscript{同˸}paṅ}},
\textit{baṅ};	%0740f'
\textit{paeṅ};` |
| `curation_json` | `04-61` | `丕` | `一` | render_latex, transliteration_latex | `一` | `⿱不一` | `丕	%pi1 / pī
{\large{py\textsuperscript{˸一}}},
\textit{phiy};	%0999k` |
| `curation_json` | `14-02` | `麴` | `麥` | render_latex, transliteration_latex | `麥` | `⿰麥匊` | `麴	%qu1
{\large{\textsuperscript{麥·}kuk}},
\textit{khiuwk};	%1017i` |
| `curation_json` | `16-39` | `瓢` | `瓜` | render_latex, transliteration_latex | `瓜` | `⿰票瓜` | `瓢	%piao2 / piáo
{\large{pew₂\textsuperscript{·瓜}}},
\textit{byiew};	%1157k` |
| `curation_json` | `20-13` | `藝` | `云` | render_latex, transliteration_latex | `云` | `⿱蓺云` | `藝	%yi4 / yì
{\large{ŋe\textsuperscript{˸云}}},
\textit{ṅieyH};	%0330f` |
| `curation_json` | `24-02` | `倝` | `旦` | render_latex, transliteration_latex | `旦` | `⿰𠦝人` | `倝	%gan4
{\large{\textsuperscript{旦·}kan₂}},
\textit{kanH};	%0140a` |
| `curation_json` | `24-02` | `乾` | `乙` | render_latex, transliteration_latex | `乙` | `⿰𠦝乞` | `乾	%qian2 / gan1 / gān
{\large{kan₂\textsuperscript{·乙}}},
\textit{gien};	%0140c
\textit{kan};` |
| `curation_json` | `26-15` | `豒` | `豐` | render_latex, transliteration_latex | `豐` | `⿰豐弟` | `豒	%zhi4
{\large{\textsuperscript{豐·}ly₆}},
\textit{ḍit};	%0591n` |
| `curation_json` | `29-17` | `瓞` | `瓜` | render_latex, transliteration_latex | `瓜` | `⿺瓜失` | `瓞	%die2
{\large{\textsuperscript{瓜·}lit}},
\textit{det};	%0402i` |
| `curation_json` | `30-02` | `㮣` | `朩` | render_latex, transliteration_latex | `朩` | `⿱既朩` | `㮣	%gai4
{\large{kyt₂\textsuperscript{˸朩}}},
\textit{kəyH};	%0515j` |
| `curation_json` | `30-02` | `暨` | `旦` | render_latex, transliteration_latex | `旦` | `⿱既旦` | `暨	%ji4 / jì
{\large{kyt₂\textsuperscript{˸旦}}},
\textit{giyH};	%0515o` |
| `curation_json` | `30-11` | `肆` | `镸` | render_latex, transliteration_latex | `镸` | `⿰镸聿` | `肆	%si4 / sì
{\large{\textsuperscript{镸·}ryp}},
\textit{siyH};	%0509h` |
| `curation_json` | `32-26` | `粼` | `巜` | render_latex, transliteration_latex | `巜` | `⿰粦巜` | `粼	%lin2 / lin4
{\large{ryn\textsuperscript{·巜}}},
\textit{lin};	%0387c
\textit{linH};` |
| `curation_json` | `36-14` | `燅` | `坴` | render_latex, transliteration_latex | `坴` | `⿰坴炎` | `燅	%qian2
{\large{\textsuperscript{坴·}qam}},
\textit{ziem};	%0617h` |
| `integrated_series_curated_entry` | `02-08` | `彠` | `尋` | render_latex, transliteration_latex | `尋` | `⿰尋蒦` | `彠	%huo4
{\large{\textsuperscript{尋·}quak}},
\textit{qiwak};	%0784f` |
| `integrated_series_curated_entry` | `02-27` | `夜` | `夕` | render_latex, transliteration_latex | `夕` | `⿱亠⿰亻⿴夂丶` | `夜	%ye4 / yè
{\large{qak\textsuperscript{˸夕}}},
\textit{yaeH};	%0800j` |
| `integrated_series_curated_entry` | `03-57` | `旁` | `同` | render_latex, transliteration_latex | `同` | `⿱⿱⿱亠丷冖方` | `旁	%pang2 / bang1 / páng
{\large{\textsuperscript{同˸}paṅ}},
\textit{baṅ};	%0740f'
\textit{paeṅ};` |
| `integrated_series_curated_entry` | `04-61` | `丕` | `一` | render_latex, transliteration_latex | `一` | `⿱不一` | `丕	%pi1 / pī
{\large{py\textsuperscript{˸一}}},
\textit{phiy};	%0999k` |
| `integrated_series_curated_entry` | `14-02` | `麴` | `麥` | render_latex, transliteration_latex | `麥` | `⿰麥匊` | `麴	%qu1
{\large{\textsuperscript{麥·}kuk}},
\textit{khiuwk};	%1017i` |
| `integrated_series_curated_entry` | `16-39` | `瓢` | `瓜` | render_latex, transliteration_latex | `瓜` | `⿰票瓜` | `瓢	%piao2 / piáo
{\large{pew₂\textsuperscript{·瓜}}},
\textit{byiew};	%1157k` |
| `integrated_series_curated_entry` | `20-13` | `藝` | `云` | render_latex, transliteration_latex | `云` | `⿱蓺云` | `藝	%yi4 / yì
{\large{ŋe\textsuperscript{˸云}}},
\textit{ṅieyH};	%0330f` |
| `integrated_series_curated_entry` | `24-02` | `倝` | `旦` | render_latex, transliteration_latex | `旦` | `⿰𠦝人` | `倝	%gan4
{\large{\textsuperscript{旦·}kan₂}},
\textit{kanH};	%0140a` |
| `integrated_series_curated_entry` | `24-02` | `乾` | `乙` | render_latex, transliteration_latex | `乙` | `⿰𠦝乞` | `乾	%qian2 / gan1 / gān
{\large{kan₂\textsuperscript{·乙}}},
\textit{gien};	%0140c
\textit{kan};` |
| `integrated_series_curated_entry` | `26-15` | `豒` | `豐` | render_latex, transliteration_latex | `豐` | `⿰豐弟` | `豒	%zhi4
{\large{\textsuperscript{豐·}ly₆}},
\textit{ḍit};	%0591n` |
| `integrated_series_curated_entry` | `29-17` | `瓞` | `瓜` | render_latex, transliteration_latex | `瓜` | `⿺瓜失` | `瓞	%die2
{\large{\textsuperscript{瓜·}lit}},
\textit{det};	%0402i` |
| `integrated_series_curated_entry` | `30-02` | `㮣` | `朩` | render_latex, transliteration_latex | `朩` | `⿱既朩` | `㮣	%gai4
{\large{kyt₂\textsuperscript{˸朩}}},
\textit{kəyH};	%0515j` |
| `integrated_series_curated_entry` | `30-02` | `暨` | `旦` | render_latex, transliteration_latex | `旦` | `⿱既旦` | `暨	%ji4 / jì
{\large{kyt₂\textsuperscript{˸旦}}},
\textit{giyH};	%0515o` |
| `integrated_series_curated_entry` | `30-11` | `肆` | `镸` | render_latex, transliteration_latex | `镸` | `⿰镸聿` | `肆	%si4 / sì
{\large{\textsuperscript{镸·}ryp}},
\textit{siyH};	%0509h` |
| `integrated_series_curated_entry` | `32-26` | `粼` | `巜` | render_latex, transliteration_latex | `巜` | `⿰粦巜` | `粼	%lin2 / lin4
{\large{ryn\textsuperscript{·巜}}},
\textit{lin};	%0387c
\textit{linH};` |
| `integrated_series_curated_entry` | `36-14` | `燅` | `坴` | render_latex, transliteration_latex | `坴` | `⿰坴炎` | `燅	%qian2
{\large{\textsuperscript{坴·}qam}},
\textit{ziem};	%0617h` |
| `validation_tex` | `` | `` | `尋` | line | `` | `` | `{\large{\textsuperscript{尋·}quak}},` |
| `validation_tex` | `` | `` | `夕` | line | `` | `` | `{\large{qak\textsuperscript{˸夕}}},` |
| `validation_tex` | `` | `` | `同` | line | `` | `` | `{\large{\textsuperscript{同˸}paṅ}},` |
| `validation_tex` | `` | `` | `一` | line | `` | `` | `{\large{py\textsuperscript{˸一}}},` |
| `validation_tex` | `` | `` | `麥` | line | `` | `` | `{\large{\textsuperscript{麥·}kuk}},` |
| `validation_tex` | `` | `` | `瓜` | line | `` | `` | `{\large{pew₂\textsuperscript{·瓜}}},` |
| `validation_tex` | `` | `` | `云` | line | `` | `` | `{\large{ŋe\textsuperscript{˸云}}},` |
| `validation_tex` | `` | `` | `乙` | line | `` | `` | `{\large{kan₂\textsuperscript{·乙}}},` |
| `validation_tex` | `` | `` | `豐` | line | `` | `` | `{\large{\textsuperscript{豐·}ly₆}},` |
| `validation_tex` | `` | `` | `瓜` | line | `` | `` | `{\large{\textsuperscript{瓜·}lit}},` |
| `validation_tex` | `` | `` | `朩` | line | `` | `` | `{\large{kyt₂\textsuperscript{˸朩}}},` |
| `validation_tex` | `` | `` | `旦` | line | `` | `` | `{\large{kyt₂\textsuperscript{˸旦}}},` |
| `validation_tex` | `` | `` | `镸` | line | `` | `` | `{\large{\textsuperscript{镸·}ryp}},` |
| `validation_tex` | `` | `` | `巜` | line | `` | `` | `{\large{ryn\textsuperscript{·巜}}},` |
| `validation_tex` | `` | `` | `坴` | line | `` | `` | `{\large{\textsuperscript{坴·}qam}},` |
| `validation_tex` | `` | `` | `瓜` | line | `` | `` | `{\large{qua{\textsuperscript{·瓜}}}},` |
| `validation_tex` | `` | `` | `χmolar` | line | `` | `` | `{\Large{與}}	{\large{{xxx\textsuperscript{χmolar}}}} = yyy,` |
| `validation_tex` | `` | `` | `舛` | line | `` | `` | `{\large{ma{\textsuperscript{·舛}}}},` |
| `validation_tex` | `` | `` | `尋` | line | `` | `` | `{\large{\textsuperscript{尋·}quak}},` |
| `validation_tex` | `` | `` | `夕` | line | `` | `` | `{\large{qak\textsuperscript{˸夕}}},` |
| `validation_tex` | `` | `` | `latebrχ` | line | `` | `` | `{\large{\textsuperscript{latebrχ}nak}} =` |
| `validation_tex` | `` | `` | `同` | line | `` | `` | `{\large{\textsuperscript{同˸}paṅ}},` |
| `validation_tex` | `` | `` | `一` | line | `` | `` | `{\large{py\textsuperscript{˸一}}},` |
| `validation_tex` | `` | `` | `dic.` | line | `` | `` | `\item 諫 kaenH < *k\textsuperscript{ˤ}r[a]nʔ-s = \textsuperscript{dic.}Kren` |
| `validation_tex` | `` | `` | `man.` | line | `` | `` | `\item 揀 keanX < *k\textsuperscript{ˤ}r[a]nʔ = \textsuperscript{man.}Kren` |
| `validation_tex` | `` | `` | `aq.` | line | `` | `` | `\item 瀾 lan, lanH < *[r]\textsuperscript{ˤ}anʔ = \textsuperscript{aq.}ran` |
| `validation_tex` | `` | `` | `ign.` | line | `` | `` | `\item 爛 lanH < *[r]\textsuperscript{ˤ}an-s = \textsuperscript{ign.}ran` |
| `validation_tex` | `` | `` | `ign.` | line | `` | `` | `\item 爤 lanH < ?*k.[r]\textsuperscript{ˤ}an = \textsuperscript{ign.}k.ran` |
| `validation_tex` | `` | `` | `dic.` | line | `` | `` | `\item 讕 lan, lanX < *g.ra:n\footnote{Zhengzhang's reconstruction.} = \textsuperscript{dic.}ran` |
| `validation_tex` | `` | `` | `arb.` | line | `` | `` | `\item 欄 lenH < *g.ra:n\footnote{\textit{ibid.}} = \textsuperscript{arb.}ran` |
| `validation_tex` | `` | `` | `aq.` | line | `` | `` | `\item 湅 lenH < *g.re:ns\footnote{\textit{ibid.}} = \textsuperscript{aq.}Kren` |
| `validation_tex` | `` | `` | `ser.` | line | `` | `` | `\item 練 lenH < *r\textsuperscript{ˤ}en-s = \textsuperscript{ser.}Kren` |
| `validation_tex` | `` | `` | `met.` | line | `` | `` | `\item 鍊 lenH < *r\textsuperscript{ˤ}en-s = \textsuperscript{met.}Kren` |
| `validation_tex` | `` | `` | `麥` | line | `` | `` | `{\large{\textsuperscript{麥·}kuk}},` |
| `validation_tex` | `` | `` | `瓜` | line | `` | `` | `{\large{pew₂\textsuperscript{·瓜}}},` |
| `validation_tex` | `` | `` | `云` | line | `` | `` | `{\large{ŋe\textsuperscript{˸云}}},` |
| `validation_tex` | `` | `` | `乙` | line | `` | `` | `{\large{kan₂\textsuperscript{·乙}}},` |
| `validation_tex` | `` | `` | `豐` | line | `` | `` | `{\large{\textsuperscript{豐·}ly₆}},` |
| `validation_tex` | `` | `` | `瓜` | line | `` | `` | `{\large{\textsuperscript{瓜·}lit}},` |
| `validation_tex` | `` | `` | `朩` | line | `` | `` | `{\large{kyt₂\textsuperscript{˸朩}}},` |
| `validation_tex` | `` | `` | `旦` | line | `` | `` | `{\large{kyt₂\textsuperscript{˸旦}}},` |
| `validation_tex` | `` | `` | `镸` | line | `` | `` | `{\large{\textsuperscript{镸·}ryp}},` |
| `validation_tex` | `` | `` | `巜` | line | `` | `` | `{\large{ryn\textsuperscript{·巜}}},` |
| `validation_tex` | `` | `` | `坴` | line | `` | `` | `{\large{\textsuperscript{坴·}qam}},` |

