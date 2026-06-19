# Integrated semantic components

- Current semantic source: `main.tex`
- Earlier pilot semantic source: `key references/My_Chinese_dictionary/main.tex`
- Normalization config: `data/semantic_components/semantic_aliases.json`
- Integrated items: 186
- Items present in both sources: 186
- Current-only items: 0
- Pilot-only items: 0
- Entry-form aliases matched to canonical semantic rows: 6
- Blocked ambiguous aliases configured: 4
- Blocked ambiguous aliases used in entries: 0
- Needs-review labels used in entries: 0
- Placeholder labels used in entries: 0
- Duplicate abbreviations with multiple graphs: 0
- Duplicate graphs with true conflicts: 0
- Intentional scoped duplicate graphs: 1
- Ambiguous abbreviations used in entries: 0
- Abbreviations used in entries but missing from the semantic list: 0

## Entry-form aliases matched to canonical semantic rows

`ag`, `cri`, `cul`, `manu`, `spir`, `ter`

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

## Integrated inventory

| Graph | Abbr. | Expanded Latin | Notes | Scope | Only in | Duplicate graph | Note | Entry-form aliases | Used in dictionary | Provenance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `辛` | `acr` | `acr(is)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `黹` | `acu` | `acu(laria)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `尚` | `adhuc` | `adhuc` | (shàng) - / (still, yet, even, still more) | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `田` | `ager` | `ager` |  | general |  |  |  | `ag` | yes | current_main_tex, earlier_pilot |
| `白` | `alb` | `alb(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `高` | `alt` | `alt(us)` |  | general |  |  |  |  | no | current_main_tex, earlier_pilot |
| `辵` | `amb` | `amb(ulo)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `黽` | `amph` | `amph(ibium)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `古` | `antiqu` | `antiqu(us)` | (gǔ) - / (ancient, old) | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `弓` | `arc` | `arc(us)` | (gōng) - / (bow) | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `水` | `aq` | `aq(ua)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `耒` | `aratr` | `aratr(um)` | (lěi) - / (plow) | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `木` | `arb` | `arb(or)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `耳` | `aur` | `aur(is)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `鳥` | `av` | `av(is)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `竹` | `bamb` | `bamb(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `須` | `barb` | `barb(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `\symbol{"268DE}` | `barbil` | `barbil(ia)` |  | general |  |  |  |  | no | current_main_tex, earlier_pilot |
| `豸` | `best` | `best(ia)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `牛` | `bos` | `bos` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `尸` | `cadaver` | `cadaver` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `犬` | `can` | `can(is)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `首` | `cap` | `cap(ut)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `匚` | `caps` | `caps(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `肉` | `carn` | `carn(is)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `厂` | `caut` | `caut(es)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `穴` | `cav` | `cav(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `鹿` | `cerv` | `cerv(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `止` | `cess` | `cess(o)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `申` | `tend` | `tend(o)` |  | general |  |  |  |  | yes | current_main_tex, current_main_tex, earlier_pilot, earlier_pilot |
| `單` | `cicad` | `cicad(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `雚` | `ciconia` | `ciconia` | (in 飌) | only_in | 飌 |  |  |  | no | current_main_tex, earlier_pilot |
| `丹` | `cinnabar` | `cinnabar(is)` | (in 彤) | only_in | 彤 |  |  |  | no | current_main_tex, earlier_pilot |
| `囗` | `cla` | `cla(usum)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `尢` | `claud` | `claud(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `思` | `cogit` | `cogit(o)` | (sī) - / (to think, to ponder) | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `丘/丠` | `coll` | `coll(is)` |  | general |  |  |  |  | no | current_main_tex, earlier_pilot |
| `貝` | `conch` | `conch(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `心` | `cor` | `cor` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `革` | `cori` | `cori(um)` | (gé) - / (leather, to reform, to revolutionize) | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `角` | `corn` | `corn(u)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `身` | `corp` | `corp(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `髟` | `crin` | `crin(is)` |  | general |  |  |  | `cri` | yes | current_main_tex, earlier_pilot |
| `刀` | `cult` | `cult(er)` |  | general |  |  |  | `cul` | yes | current_main_tex, earlier_pilot |
| `走` | `curr` | `curr(o)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `鬼` | `daemon` | `daemon` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `欠` | `dehab` | `dehab(eo)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `去` | `depart` | `depart(ire)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `齒` | `dent` | `(dens), dent(is)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `又` | `dextr` | `dextr(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `言` | `dic` | `dic(o)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `音` | `son` | `son(us)` |  | general |  |  |  |  | yes | current_main_tex, current_main_tex, earlier_pilot, earlier_pilot |
| `寸` | `digit` | `digit(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `舍` | `dom` | `dom(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `龍` | `dracon` | `(draco), dracon(is)` | (in 龏) | only_in | 龏 |  |  |  | no | current_main_tex, earlier_pilot |
| `甘` | `dulc` | `dulc(is)` | (in 甞) | only_in | 甞 |  |  |  | yes | current_main_tex, earlier_pilot |
| `食` | `ed` | `ed(o)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `行` | `eo` | `eo` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `象` | `elephant` | `elephant(us)` | (xiàng) - | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `馬` | `equ` | `equ(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `出` | `ex` | `ex(ire)` |  | general |  |  |  |  | no | current_main_tex, earlier_pilot |
| `頁` | `fac` | `fac(ies)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `女` | `fem` | `fem(ina)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `攴` | `fer` | `fer(io)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `勹` | `flect` | `flect(o)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `子` | `fili` | `fili(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `臤` | `firm` | `firm(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `川` | `fluvi` | `fluvi(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `田` | `forn` | `forn(us)` | (only in 盧) | only_in | 盧 | intentional_scoped_duplicate | Same visible graph as 田/ager, but different semantic label and restricted use. |  | no | current_main_tex, earlier_pilot |
| `\symbol{"2201C}` | `fov` | `fov(ere)` | (only in 筑) | only_in | 筑 |  |  |  | no | current_main_tex, earlier_pilot |
| `黃` | `galb` | `galb(inus)` | (only in 黈?) | only_in | 黈? |  |  |  | no | current_main_tex, earlier_pilot |
| `仌` | `glac` | `glac(ies)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `玉` | `gem` | `gem(ma)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `屮` | `germ` | `germ(en)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `癶` | `grad` | `grad(us)` |  | general |  |  |  |  | no | current_main_tex, earlier_pilot |
| `禾` | `gran` | `gran(um)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `犛` | `grunn` | `(bos) grunn(iens)` | (only in 斄) | only_in | 斄 |  |  |  | no | current_main_tex, earlier_pilot |
| `旨` | `gust` | `gust(us)` | (in 嘗) | only_in | 嘗 |  |  |  | yes | current_main_tex, earlier_pilot |
| `戈` | `hallebard` | `hallebard(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `殳` | `hast` | `hast(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `艸` | `herb` | `herb(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `人` | `hom` | `hom(o)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `矛` | `iacul` | `iacul(um)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `火` | `ign` | `ign(is)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `疒` | `infirm` | `infirm(itas)` | (recovered from entry usage) | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `兮` | `io` | `io` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `誩` | `iurg` | `iurg(ium)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `敕` | `iuss` | `iuss(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `石` | `lap` | `lap(is)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `匸` | `latebr` | `latebr(a)` |  | general |  |  |  |  | no | current_main_tex, earlier_pilot |
| `广` | `lax` | `lax(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `斤` | `libra` | `libra` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `舌` | `lingu` | `lingu(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `巾` | `lint` | `lint(eum)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `月` | `luna` | `luna` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `光` | `lux` | `lux` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `大` | `magn` | `magn(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `歹` | `mal` | `mal(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `手` | `man` | `man(us)` |  | general |  |  |  | `manu` | yes | current_main_tex, earlier_pilot |
| `男` | `masc` | `masc(ulus)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `午` | `meridi` | `meridi(es)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `金` | `met` | `met(allum)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `黍` | `mil` | `mil(ium)` | (only in 黎?) | only_in | 黎? |  |  |  | no | current_main_tex, earlier_pilot |
| `牙` | `molar` | `molar(is dens)` |  | general |  |  |  |  | no | current_main_tex, earlier_pilot |
| `山` | `mon` | `mon(s)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `鼠` | `rod` | `rod(entia)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `鼻` | `nas` | `nas(um)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `网` | `nass` | `nass(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `非` | `ne` | `ne` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `舟` | `nav` | `nav(is)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `黑` | `niger` | `niger` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `旡` | `non` | `non` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `監` | `observ` | `observ(o)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `舛` | `obs` | `obs(isto)` |  | general |  |  |  |  | no | current_main_tex, earlier_pilot |
| `目` | `ocul` | `ocul(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `鬲` | `olla` | `olla` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `米` | `oryz` | `oryz(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `口` | `or` | `(os,) or(is)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `骨` | `oss` | `(os,) oss(is)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `戶` | `ost` | `ost(ium)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `羊` | `ov` | `ov(is)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `帛` | `pann` | `pann(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `幺` | `parv` | `parv(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `亠` | `pav` | `pav(ilio)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `步` | `pass` | `pass(us)` |  | general |  |  |  |  | no | current_main_tex, earlier_pilot |
| `隹` | `passer` | `passer` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `足` | `ped` | `(pes,) ped(is)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `皮` | `pell` | `pell(is)` | (in 皽) | only_in | 皽 |  |  |  | yes | current_main_tex, earlier_pilot |
| `毛` | `pil` | `pil(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `聿` | `pincern` | `pincern(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `魚` | `pis` | `pis(cis)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `民` | `pleb` | `pleb(s)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `羽` | `plum` | `plum(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `雨` | `pluv` | `pluv(ia)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `豕` | `porc` | `porc(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `門` | `port` | `port(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `可` | `poss` | `poss(um)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `玄` | `profund` | `profund(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `卜` | `prognosc` | `prognosc(ere)` | (in 鼑) | only_in | 鼑 |  |  |  | yes | current_main_tex, earlier_pilot |
| `廴` | `progred` | `progred(ior)` | (in 廷) | only_in | 廷 |  |  |  | yes | current_main_tex, earlier_pilot |
| `鬥` | `pugn` | `pugn(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `方` | `quadr` | `quadr(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `支` | `ram` | `ram(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `赤` | `ruf` | `ruf(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `矢` | `sagit` | `sagit(ta)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `鹵` | `sal` | `sal(is)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `血` | `sangu` | `sangu(is)` | \item 章 sculp(ō) (in 贛) | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `戊` | `secur` | `secur(is)` | (in 戚) | only_in | 戚 |  |  |  | yes | current_main_tex, earlier_pilot |
| `片` | `segm` | `segm(entum)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `老` | `sen` | `sen(ex)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `糸` | `ser` | `ser(icum)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `虫` | `serp` | `serp(ens)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `林` | `silv` | `silv(a)` | (lín) - / (forest) | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `日` | `sol` | `sol` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `卩` | `sign` | `sign(o)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `㝱` | `somn` | `somn(ium)` | (méi) - | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `晶` | `splend` | `splend(or)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `示` | `spirit` | `spirit(us)` |  | general |  |  |  | `spir` | yes | current_main_tex, earlier_pilot |
| `立` | `sto` | `sto` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `鼓` | `tabur` | `tabur` | (only in 鼛?) | only_in | 鼛? |  |  |  | yes | current_main_tex, earlier_pilot |
| `宀` | `tect` | `tect(um)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `瓦` | `teg` | `teg(ula)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `亯` | `templ` | `templ(um)` | (in 䈞) | only_in | 䈞 |  |  |  | no | current_main_tex, earlier_pilot |
| `丮` | `ten` | `ten(eo)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `土` | `terr` | `terr(a)` |  | general |  |  |  | `ter` | yes | current_main_tex, earlier_pilot |
| `龠` | `tibia` | `tibia` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `虍` | `tigr` | `tigr(is)` | (hū) - / (tiger) | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `鼎` | `trip` | `trip(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `斗` | `trull` | `trull(a)` | (dǒu) - / (dipper, ladle) | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `爾` | `tu` | `tu` | (you, your) | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `阜` | `tum` | `tum(ulus)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `壴` | `tympan` | `tympan(um)` | (zhù) - | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `邑` | `urb` | `urb(s)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `熊` | `urs` | `urs(us)` |  | general |  |  |  |  | no | current_main_tex, earlier_pilot |
| `箕` | `vann` | `vann(us)` |  | general |  |  |  |  | no | current_main_tex, earlier_pilot |
| `皿` | `vas` | `vas(um)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `車` | `vehic` | `vehic(ulum)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `來` | `veni` | `veni(ō)` |  | general |  |  |  |  | no | current_main_tex, earlier_pilot |
| `胃` | `ventri` | `ventri(culus)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `風` | `vent` | `vent(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `衣` | `vest` | `vest(imentum)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `㫃` | `vex` | `vex(illum)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `里` | `vic` | `vic(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `見` | `vid` | `vid(eo)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `酉` | `vin` | `vin(um)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `力` | `virt` | `virt(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
