# Integrated semantic components

- Current semantic source: `main.tex`
- Earlier pilot semantic source: `key references/My_Chinese_dictionary/main.tex`
- Normalization config: `data/semantic_components/semantic_aliases.json`
- Integrated items: 328
- Items present in both sources: 194
- Current-only items: 35
- Pilot-only items: 0
- Entry-form aliases matched to canonical semantic rows: 0
- Blocked ambiguous aliases configured: 4
- Blocked ambiguous aliases used in entries: 0
- Needs-review labels used in entries: 0
- Placeholder labels used in entries: 0
- Duplicate abbreviations with multiple graphs: 2
- Duplicate graphs with true conflicts: 0
- Intentional scoped duplicate graphs: 1
- Ambiguous abbreviations used in entries: 0
- Abbreviations used in entries but missing from the semantic list: 0

## Blocked ambiguous aliases

| Alias | Candidate canonical labels | Reason |
| --- | --- | --- |
| `bos` | `bos`, `grunn` | Blocked as an inferred alias because bos is canonical for 牛, but also appears parenthetically in 犛 grunn(iens). |
| `den` | `dent`, `molar` | Blocked because it can refer to dent/tooth material or surface from molar/dens explanations. |
| `dens` | `dent`, `molar` | Blocked because it can refer to dent/tooth material or surface from molar/dens explanations. |
| `os` | `or`, `oss` | Blocked because it can refer to 口/or or 骨/oss. |

## Duplicate abbreviations across different graphs

| Abbreviation | Graphs |
| --- | --- |
| `discr` | `一`; `旁` |
| `prior` | `坴`; `𦰩` |

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
| `曰` | `ait` | `ait` |  | general |  |  |  |  | yes | current_main_tex |
| `永` | `aetern` | `aetern(us)` |  | general |  |  |  |  | yes | current_main_tex |
| `田` | `ager` | `ager` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `白` | `alb` | `alb(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `韋` | `alut` | `alut(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
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
| `\symbol{"268DE}` | `barbil` | `barbil(ia)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `豸` | `best` | `best(ia)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `廾` | `biman` | `biman(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `牛` | `bos` | `bos` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `尸` | `cadaver` | `cadaver` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `缶` | `cad` | `cad(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `履` | `calce` | `calce(us)` |  | general |  |  |  |  | yes | current_main_tex |
| `兀` | `calv` | `calv(us)` |  | general |  |  |  |  | yes | current_main_tex |
| `犬` | `can` | `can(is)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `首` | `cap` | `cap(ut)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `匚` | `caps` | `caps(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `肉` | `carn` | `carn(is)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `厂` | `caut` | `caut(es)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `穴` | `cav` | `cav(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `鹿` | `cerv` | `cerv(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `釆` | `cern` | `cern(ere)` |  | general |  |  |  |  | yes | current_main_tex |
| `止` | `cess` | `cess(o)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `申` | `tend` | `tend(o)` |  | general |  |  |  |  | yes | current_main_tex, current_main_tex, earlier_pilot, earlier_pilot |
| `單` | `cicad` | `cicad(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `雚` | `ciconia` | `ciconia` | (in 飌) | only_in | 飌 |  |  |  | yes | current_main_tex, earlier_pilot |
| `丹` | `cinnabar` | `cinnabar(is)` | (in 彤) | only_in | 彤 |  |  |  | yes | current_main_tex, earlier_pilot |
| `囗` | `cla` | `cla(usum)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `尢` | `claud` | `claud(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `囟` | `fontan` | `fontan(ella)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `思` | `cogit` | `cogit(o)` | (sī) - / (to think, to ponder) | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `丘/丠` | `coll` | `coll(is)` |  | general |  |  |  |  | no | current_main_tex, earlier_pilot |
| `貝` | `conch` | `conch(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `心` | `cor` | `cor` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `𤼽` | `coron` | `coron(a)` |  | general |  |  |  |  | yes | current_main_tex |
| `革` | `cori` | `cori(um)` | (gé) - / (leather, to reform, to revolutionize) | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `角` | `corn` | `corn(u)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `身` | `corp` | `corp(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `尾` | `caud` | `caud(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `髟` | `crin` | `crin(is)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `刀` | `cult` | `cult(er)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `走` | `curr` | `curr(o)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `鬼` | `daemon` | `daemon` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `欠` | `dehab` | `dehab(eo)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `去` | `depart` | `depart(ire)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `齒` | `dent` | `(dens), dent(is)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `又` | `dextr` | `dextr(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `言` | `dic` | `dic(o)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `一` | `discr` | `discr(imen)` | (only in 丕) | only_in | 丕 |  |  |  | yes | current_main_tex |
| `旁` | `discr` | `discr(imen)` | (only in 旁) | only_in | 旁 |  |  |  | yes | current_main_tex |
| `音` | `son` | `son(us)` |  | general |  |  |  |  | yes | current_main_tex, current_main_tex, earlier_pilot, earlier_pilot |
| `寸` | `digit` | `digit(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `舍` | `dom` | `dom(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `龍` | `dracon` | `(draco), dracon(is)` | (in 龏) | only_in | 龏 |  |  |  | no | current_main_tex, earlier_pilot |
| `甘` | `dulc` | `dulc(is)` | (in 甞) | only_in | 甞 |  |  |  | yes | current_main_tex, earlier_pilot |
| `八` | `dvid` | `dvid(o)` |  | general |  |  |  |  | yes | current_main_tex |
| `食` | `ed` | `ed(o)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `行` | `eo` | `eo` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `象` | `elephant` | `elephant(us)` | (xiàng) - | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `馬` | `equ` | `equ(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `出` | `ex` | `ex(ire)` |  | general |  |  |  |  | no | current_main_tex, earlier_pilot |
| `工` | `fabr` | `fabr(ica)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `頁` | `fac` | `fac(ies)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `庚` | `flagell` | `flagell(um)` |  | general |  |  |  |  | yes | current_main_tex |
| `女` | `fem` | `fem(ina)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `攴` | `fer` | `fer(io)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `勹` | `flect` | `flect(o)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `子` | `fili` | `fili(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `臤` | `firm` | `firm(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `炎` | `flamm` | `flamm(a)` |  | general |  |  |  |  | yes | current_main_tex |
| `川` | `fluvi` | `fluvi(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `𣒚` | `foll` | `foll(is)` |  | general |  |  |  |  | yes | current_main_tex |
| `嗇` | `frug` | `frug(is)` |  | general |  |  |  |  | yes | current_main_tex |
| `田` | `forn` | `forn(us)` | (only in 盧) | only_in | 盧 | intentional_scoped_duplicate | Same visible graph as 田/ager, but different semantic label and restricted use. |  | no | current_main_tex, earlier_pilot |
| `\symbol{"2201C}` | `fov` | `fov(ere)` | (only in 筑) | only_in | 筑 |  |  |  | yes | current_main_tex, earlier_pilot |
| `黃` | `galb` | `galb(inus)` | (only in 黈?) | only_in | 黈? |  |  |  | no | current_main_tex, earlier_pilot |
| `仌` | `glac` | `glac(ies)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `玉` | `gem` | `gem(ma)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `屮` | `germ` | `germ(en)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `癶` | `grad` | `grad(us)` |  | general |  |  |  |  | no | current_main_tex, earlier_pilot |
| `禾` | `gran` | `gran(um)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `㐭` | `granar` | `granar(ium)` |  | general |  |  |  |  | yes | current_main_tex |
| `犛` | `grunn` | `(bos) grunn(iens)` | (only in 斄) | only_in | 斄 |  |  |  | no | current_main_tex, earlier_pilot |
| `旨` | `gust` | `gust(us)` | (in 嘗) | only_in | 嘗 |  |  |  | yes | current_main_tex, earlier_pilot |
| `戈` | `hallebard` | `hallebard(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `殳` | `hast` | `hast(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `艸` | `herb` | `herb(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `人` | `hom` | `hom(o)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `矛` | `iacul` | `iacul(um)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `火` | `ign` | `ign(is)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `疒` | `infirm` | `infirm(itas)` | (recovered from entry usage) | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `入` | `intro` | `intro` |  | general |  |  |  |  | yes | current_main_tex |
| `己` | `ipse` | `ipse` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `兮` | `io` | `io` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `誩` | `iurg` | `iurg(ium)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `敕` | `iuss` | `iuss(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `石` | `lap` | `lap(is)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `匸` | `latebr` | `latebr(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `广` | `lax` | `lax(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `斤` | `libra` | `libra` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `系` | `lig` | `lig(amen)` |  | general |  |  |  |  | yes | current_main_tex |
| `舌` | `lingu` | `lingu(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `巾` | `lint` | `lint(eum)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `月` | `luna` | `luna` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `光` | `lux` | `lux` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `大` | `magn` | `magn(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `歹` | `mal` | `mal(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `手` | `man` | `man(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `男` | `masc` | `masc(ulus)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `巫` | `mag` | `mag(us)` |  | general |  |  |  |  | yes | current_main_tex |
| `午` | `meridi` | `meridi(es)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `金` | `met` | `met(allum)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `黍` | `mil` | `mil(ium)` | (only in 黎?) | only_in | 黎? |  |  |  | yes | current_main_tex, earlier_pilot |
| `臣` | `ministr` | `ministr(er)` |  | general |  |  |  |  | yes | current_main_tex |
| `牙` | `molar` | `molar(is dens)` |  | general |  |  |  |  | no | current_main_tex, earlier_pilot |
| `山` | `mon` | `mon(s)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `死` | `mort` | `mort(uus)` |  | general |  |  |  |  | yes | current_main_tex |
| `鼠` | `rod` | `rod(entia)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `䖵` | `insect` | `insect(a)` |  | general |  |  |  |  | yes | current_main_tex |
| `鼻` | `nas` | `nas(um)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `网` | `nass` | `nass(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `隶` | `nex` | `nex(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `非` | `ne` | `ne` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `舟` | `nav` | `nav(is)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `黑` | `niger` | `niger` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `雲` | `nimb` | `nimb(us)` |  | general |  |  |  |  | yes | current_main_tex |
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
| `宮` | `palat` | `palat(ium)` |  | general |  |  |  |  | yes | current_main_tex |
| `幺` | `parv` | `parv(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `亠` | `pav` | `pav(ilio)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `步` | `pass` | `pass(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `隹` | `passer` | `passer` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `足` | `ped` | `(pes,) ped(is)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `皮` | `pell` | `pell(is)` | (in 皽) | only_in | 皽 |  |  |  | yes | current_main_tex, earlier_pilot |
| `毛` | `pil` | `pil(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `冃` | `pile` | `pile(us)` |  | general |  |  |  |  | yes | current_main_tex |
| `聿` | `pincern` | `pincern(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `魚` | `pis` | `pis(cis)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `民` | `pleb` | `pleb(s)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `羽` | `plum` | `plum(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `雨` | `pluv` | `pluv(ia)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `豕` | `porc` | `porc(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `韭` | `porr` | `porr(um)` |  | general |  |  |  |  | yes | current_main_tex |
| `門` | `port` | `port(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `殺` | `occid` | `occid(o)` |  | general |  |  |  |  | yes | current_main_tex |
| `可` | `poss` | `poss(um)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `玄` | `profund` | `profund(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `卜` | `prognosc` | `prognosc(ere)` | (in 鼑) | only_in | 鼑 |  |  |  | yes | current_main_tex, earlier_pilot |
| `坴` | `prior` | `prior(phonogramma)` | (only in 燅) | only_in | 燅 |  |  |  | yes | current_main_tex |
| `𦰩` | `prior` | `prior(phonogramma)` | (only in 艱) | only_in | 艱 |  |  |  | yes | current_main_tex |
| `廴` | `progred` | `progred(ior)` | (in 廷) | only_in | 廷 |  |  |  | yes | current_main_tex, earlier_pilot |
| `鬥` | `pugn` | `pugn(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `方` | `quadr` | `quadr(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `支` | `ram` | `ram(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `反` | `revers` | `revers(us)` |  | general |  |  |  |  | yes | current_main_tex |
| `赤` | `ruf` | `ruf(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `屵` | `rup` | `rup(es)` |  | general |  |  |  |  | yes | current_main_tex |
| `矢` | `sagit` | `sagit(ta)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `鹵` | `sal` | `sal(is)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `㯻` | `sac` | `sac(cus)` |  | general |  |  |  |  | yes | current_main_tex |
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
| `示` | `spirit` | `spirit(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `立` | `sto` | `sto` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `鼓` | `tabur` | `tabur` | (only in 鼛?) | only_in | 鼛? |  |  |  | yes | current_main_tex, earlier_pilot |
| `宀` | `tect` | `tect(um)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `瓦` | `teg` | `teg(ula)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `亯` | `templ` | `templ(um)` | (in 䈞) | only_in | 䈞 |  |  |  | no | current_main_tex, earlier_pilot |
| `丮` | `ten` | `ten(eo)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `土` | `terr` | `terr(a)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `龠` | `tibia` | `tibia` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `虍` | `tigr` | `tigr(is)` | (hū) - / (tiger) | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `鼎` | `trip` | `trip(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `斗` | `trull` | `trull(a)` | (dǒu) - / (dipper, ladle) | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `乑` | `turb` | `turb(a)` |  | general |  |  |  |  | yes | current_main_tex |
| `爾` | `tu` | `tu` | (you, your) | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `阜` | `tum` | `tum(ulus)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `壴` | `tympan` | `tympan(um)` | (zhù) - | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `邑` | `urb` | `urb(s)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `熊` | `urs` | `urs(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `箕` | `vann` | `vann(us)` |  | general |  |  |  |  | no | current_main_tex, earlier_pilot |
| `气` | `vapor` | `vapor` |  | general |  |  |  |  | yes | current_main_tex |
| `皿` | `vas` | `vas(um)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `車` | `vehic` | `vehic(ulum)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `來` | `veni` | `veni(ō)` |  | general |  |  |  |  | no | current_main_tex, earlier_pilot |
| `胃` | `ventri` | `ventri(culus)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `風` | `vent` | `vent(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `衣` | `vest` | `vest(imentum)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `夂` | `vestig` | `vestig(ium)` |  | general |  |  |  |  | yes | current_main_tex |
| `㫃` | `vex` | `vex(illum)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `里` | `vic` | `vic(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `見` | `vid` | `vid(eo)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `酉` | `vin` | `vin(um)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `士` | `vir` | `vir` |  | general |  |  |  |  | yes | current_main_tex |
| `力` | `virt` | `virt(us)` |  | general |  |  |  |  | yes | current_main_tex, earlier_pilot |
| `面` | `vult` | `vult(us)` |  | general |  |  |  |  | yes | current_main_tex |
| `㗊` | `clam` | `clam(or)` |  | general |  |  | Many mouths; outcry or shout. |  | yes | semantic_label_supplement |
| `㢟` | `extens` | `extens(us)` |  | general |  |  | Old form of 延; extend/travel far. |  | yes | semantic_label_supplement |
| `㱃` | `bib` | `bib(it)` |  | general |  |  | To drink. |  | yes | semantic_label_supplement |
| `丂` | `halit` | `halit(us)` |  | general |  |  | Breath/exhalation. |  | yes | semantic_label_supplement |
| `丌` | `pedest` | `pedest(al)` |  | general |  |  | Pedestal. |  | yes | semantic_label_supplement |
| `丵` | `caesp` | `caesp(es)` |  | general |  |  | Tufted grass; clustered growth. |  | yes | semantic_label_supplement |
| `凡` | `lanx` | `lanx` |  | general |  |  | Tray or flat dish. |  | yes | semantic_label_supplement |
| `䀠` | `binoc` | `binoc(ulus)` |  | general |  |  | Two eyes. |  | yes | semantic_label_supplement |
| `䇂` | `falx` | `falx` |  | general |  |  | Sickle. |  | yes | semantic_label_supplement |
| `厶` | `priv` | `priv(atus)` |  | general |  |  | Private/self. |  | yes | semantic_label_supplement |
| `匕` | `cyath` | `cyath(us)` |  | general |  |  | Spoon or ladle. |  | yes | semantic_label_supplement |
| `兔` | `lepus` | `lepus` |  | general |  |  | Rabbit/hare. |  | yes | semantic_label_supplement |
| `二` | `duo` | `duo` |  | general |  |  | Two equal lines. |  | yes | semantic_label_supplement |
| `十` | `iung` | `iung(o)` |  | general |  |  | Knotted-cord / joining form. |  | yes | semantic_label_supplement |
| `𠨍` | `coram` | `coram` |  | general |  |  | Two people facing each other. |  | yes | semantic_label_supplement |
| `𠩺` | `fiss` | `fiss(ura)` |  | general |  |  | To split or rive. |  | yes | semantic_label_supplement |
| `𭚧` | `emiss` | `emiss(io)` |  | general |  |  | Bow-firing / discharge / launch. |  | yes | semantic_label_supplement |
| `覀` | `velam` | `velam(en)` |  | general |  |  | Cover/veil. |  | yes | semantic_label_supplement |
| `豈` | `perc` | `perc(ussio)` |  | general |  |  | Drum / percussion. |  | yes | semantic_label_supplement |
| `告` | `nunt` | `nunt(io)` |  | general |  |  | To tell, announce. |  | yes | semantic_label_supplement |
| `囧` | `fenestr` | `fenestr(a)` |  | general |  |  | Window-like form. |  | yes | semantic_label_supplement |
| `壺` | `urn` | `urn(a)` |  | general |  |  | Urn or pot. |  | yes | semantic_label_supplement |
| `几` | `sell` | `sell(a)` |  | general |  |  | Small stool. |  | yes | semantic_label_supplement |
| `勻` | `aequ` | `aequ(us)` |  | general |  |  | Equal / even / balanced. |  | yes | semantic_label_supplement |
| `北` | `dors` | `dors(um)` |  | general |  |  | Back; back-to-back. |  | yes | semantic_label_supplement |
| `卪` | `nod` | `nod(us)` |  | general |  |  | Joint or node. |  | yes | semantic_label_supplement |
| `危` | `peril` | `peril(um)` |  | general |  |  | Danger; peril. |  | yes | semantic_label_supplement |
| `冖` | `velum` | `velum` |  | general |  |  | Covering or canopy. |  | yes | semantic_label_supplement |
| `向` | `echo` | `echo` |  | general |  |  | Echo / resonance. |  | yes | semantic_label_supplement |
| `文` | `script` | `script(um)` |  | general |  |  | Patterned / written / tattooed form. |  | yes | semantic_label_supplement |
| `彣` | `vari` | `vari(us)` |  | general |  |  | Variegated / literary. |  | yes | semantic_label_supplement |
| `昱` | `luc` | `luc(em)` |  | general |  |  | Bright / shining. |  | yes | semantic_label_supplement |
| `旦` | `auror` | `auror(a)` |  | general |  |  | Sunrise / dawn. |  | yes | semantic_label_supplement |
| `夕` | `nox` | `nox` |  | general |  |  | Night / evening. |  | yes | semantic_label_supplement |
| `朩` | `lign` | `lign(um)` |  | general |  |  | Wood / timber. |  | yes | semantic_label_supplement |
| `谷` | `vall` | `vall(is)` |  | general |  |  | Valley. |  | yes | semantic_label_supplement |
| `皀` | `cib` | `cib(us)` |  | general |  |  | Bowl of rice / food. |  | yes | semantic_label_supplement |
| `香` | `fragr` | `fragr(ans)` |  | general |  |  | Fragrant / sweet-smelling. |  | yes | semantic_label_supplement |
| `正` | `rect` | `rect(us)` |  | general |  |  | Straight / correct. |  | yes | semantic_label_supplement |
| `比` | `comp` | `comp(ar)` |  | general |  |  | Compare / juxtapose. |  | yes | semantic_label_supplement |
| `瓜` | `cucur` | `cucur(bita)` |  | general |  |  | Gourd. |  | yes | semantic_label_supplement |
| `柬` | `leg` | `leg(o)` |  | general |  |  | Select / choose. |  | yes | semantic_label_supplement |
| `殸` | `cymb` | `cymb(alum)` |  | general |  |  | Stone chime / percussion instrument. |  | yes | semantic_label_supplement |
| `爿` | `lect` | `lect(us)` |  | general |  |  | Bed / bedboard. |  | yes | semantic_label_supplement |
| `異` | `divers` | `divers(us)` |  | general |  |  | Different / unusual. |  | yes | semantic_label_supplement |
| `盾` | `scut` | `scut(um)` |  | general |  |  | Shield. |  | yes | semantic_label_supplement |
| `習` | `exerc` | `exerc(itium)` |  | general |  |  | Practice / learn. |  | yes | semantic_label_supplement |
| `舁` | `elev` | `elev(are)` |  | general |  |  | Raise / carry. |  | yes | semantic_label_supplement |
| `色` | `color` | `color` |  | general |  |  | Color / complexion. |  | yes | semantic_label_supplement |
| `生` | `nasc` | `nasc(i)` |  | general |  |  | Life / birth / sprouting. |  | yes | semantic_label_supplement |
| `臼` | `mortar` | `mortar(ium)` |  | general |  |  | Mortar. |  | yes | semantic_label_supplement |
| `閃` | `fulg` | `fulg(or)` |  | general |  |  | Flash / sparkle. |  | yes | semantic_label_supplement |
| `華` | `flor` | `flor` |  | general |  |  | Flower / blossoming brilliance. |  | yes | semantic_label_supplement |
| `雈` | `strix` | `strix` |  | general |  |  | Owl. |  | yes | semantic_label_supplement |
| `麥` | `trit` | `trit(icum)` |  | general |  |  | Wheat. |  | yes | semantic_label_supplement |
| `麻` | `cann` | `cann(abis)` |  | general |  |  | Hemp. |  | yes | semantic_label_supplement |
| `㕣` | `palud` | `palud(is)` |  | general |  |  | Marsh or wetland between mountains. |  | yes | semantic_label_supplement |
| `㣇` | `fasc` | `fasc(is)` |  | general |  |  | Bundle / gathered mass. |  | yes | semantic_label_supplement |
| `丷` | `furc` | `furc(a)` |  | general |  |  | Forked, split-open upper form. |  | yes | semantic_label_supplement |
| `丿` | `obliq` | `obliq(uus)` |  | general |  |  | Left-falling oblique stroke. |  | yes | semantic_label_supplement |
| `乚` | `unc` | `unc(us)` |  | general |  |  | Hooked terminal stroke. |  | yes | semantic_label_supplement |
| `乙` | `uncin` | `uncin(us)` |  | general |  |  | Hooked / curving terminal graph. |  | yes | semantic_label_supplement |
| `倠` | `avis` | `avis` |  | general |  |  | Bird-like component in 雁. |  | yes | semantic_label_supplement |
| `儿` | `crur` | `crur(a)` |  | general |  |  | Leg-like human base / knees. |  | yes | semantic_label_supplement |
| `共` | `commun` | `commun(is)` |  | general |  |  | Together / common / held-up object with two hands. |  | yes | semantic_label_supplement |
| `卂` | `celer` | `celer(is)` |  | general |  |  | Swift / flying component in 迅. |  | yes | semantic_label_supplement |
| `吅` | `bivoc` | `bivoc(is)` |  | general |  |  | Two mouths / outcry. |  | yes | semantic_label_supplement |
| `呂` | `spina` | `spina` |  | general |  |  | Spine / vertebral pair. |  | yes | semantic_label_supplement |
| `喦` | `sax` | `sax(um)` |  | general |  |  | Rocky / craggy mass. |  | yes | semantic_label_supplement |
| `夸` | `glor` | `glor(ia)` |  | general |  |  | Boast / magnified form. |  | yes | semantic_label_supplement |
| `委` | `genuf` | `genuf(lectere)` |  | general |  |  | Kneeling woman / bent posture. |  | yes | semantic_label_supplement |
| `室` | `cella` | `cella` |  | general |  |  | Room / chamber / house. |  | yes | semantic_label_supplement |
| `尋` | `brach` | `brach(ium)` |  | general |  |  | Armspan / measure. |  | yes | semantic_label_supplement |
| `尺` | `regul` | `regul(a)` |  | general |  |  | Ruler / measuring rod. |  | yes | semantic_label_supplement |
| `巜` | `riv` | `riv(us)` |  | general |  |  | Stream / channel. |  | yes | semantic_label_supplement |
| `弋` | `clav` | `clav(us)` |  | general |  |  | Peg / sharp stake. |  | yes | semantic_label_supplement |
| `引` | `tract` | `tract(us)` |  | general |  |  | Draw / pull. |  | yes | semantic_label_supplement |
| `恣` | `cupi` | `cupi(dus)` |  | general |  |  | Desire / indulge oneself. |  | yes | semantic_label_supplement |
| `是` | `ver` | `ver(us)` |  | general |  |  | Right / true / correct. |  | yes | semantic_label_supplement |
| `桀` | `hero` | `heros` |  | general |  |  | Outstanding hero / valiant figure. |  | yes | semantic_label_supplement |
| `皃` | `spec` | `spec(ies)` |  | general |  |  | Appearance / visage. |  | yes | semantic_label_supplement |
| `縣` | `susp` | `susp(ensus)` |  | general |  |  | Hang / suspend. |  | yes | semantic_label_supplement |
| `臥` | `procumb` | `procumb(ere)` |  | general |  |  | Lie down / recline. |  | yes | semantic_label_supplement |
| `至` | `adven` | `adven(ire)` |  | general |  |  | Arrive / reach. |  | yes | semantic_label_supplement |
| `蜀` | `bombyx` | `bombyx` |  | general |  |  | Silkworm / insect graph. |  | yes | semantic_label_supplement |
| `豐` | `abund` | `abund(ans)` |  | general |  |  | Abundance / fullness. |  | yes | semantic_label_supplement |
| `重` | `grav` | `grav(is)` |  | general |  |  | Heavy / weight. |  | yes | semantic_label_supplement |
| `镸` | `long` | `long(us)` |  | general |  |  | Long / extended form. |  | yes | semantic_label_supplement |
| `龴` | `curv` | `curv(us)` |  | general |  |  | Curved top / hooked upper element. |  | yes | semantic_label_supplement |
| `𠂇` | `laev` | `laev(us)` |  | general |  |  | Left-hand / left-side element. |  | yes | semantic_label_supplement |
| `𠌵` | `anser` | `anser` |  | general |  |  | Goose / bird component in 鴈. |  | yes | semantic_label_supplement |
| `𠚕` | `odont` | `odont(us)` |  | general |  |  | Tooth row / dental graph. |  | yes | semantic_label_supplement |
| `𠬜` | `preh` | `preh(endere)` |  | general |  |  | Grasp / seize / entangle. |  | yes | semantic_label_supplement |
| `𠬪` | `carp` | `carp(ere)` |  | general |  |  | Pluck / pick by hand. |  | yes | semantic_label_supplement |
| `𬅟` | `desid` | `desid(erium)` |  | general |  |  | Desire / wishing heart. |  | yes | semantic_label_supplement |
| `㚣` | `mulier` | `mulier(es)` |  | general |  |  | Women / female cluster. |  | yes | semantic_label_supplement |
| `丶` | `punct` | `punct(um)` |  | general |  |  | Dot / point / marked dot. |  | yes | semantic_label_supplement |
| `叹` | `suspir` | `suspir(are)` |  | general |  |  | Sigh / exclaiming mouth. |  | yes | semantic_label_supplement |
| `吂` | `vict` | `vict(or)` |  | general |  |  | Victory / winning-abundance family. |  | yes | semantic_label_supplement |
