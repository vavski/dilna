# Rozhodnutí a jejich důvody

Nastavení bez důvodů se za tři měsíce nedá udržovat — nikdo neví, jestli
je věc schválně, nebo jen zbyla. Tenhle soubor je ta chybějící část.

---

## 1. Hooky místo instrukcí tam, kde se něco nesmí stát nikdy

**Rozhodnutí:** osobní údaje a nevratné příkazy v gitu hlídají hooky.
Ve skillech o nich není ani řádka.

**Proč:** instrukce v souboru je doporučení. Model ji obvykle dodrží,
ale ne vždycky — když je kontext plný a úkol složitý, může na ni
zapomenout. Hook je závora: běží mimo model, nemá kontext a nedá se
přemluvit.

Rozdělení je proto tvrdé:

- **Hook** = co se nesmí stát nikdy, ani omylem. Rodné číslo v souboru,
  `git push --force`, commit s daty v indexu.
- **Skill** = co se má stát obvykle. Jak vypadá dobrý report, kdy
  aktualizovat stav, jak se anonymizuje.

**Co to stojí:** hook musí být rychlý a nesmí padat, jinak zablokuje
práci. Proto jsou všechny tři psané tak, že při jakékoliv nejistotě
pustí volání dál — nesrozumitelný vstup, chyba čtení, nedostupný git.
Falešně propuštěný zápis je horší než zablokovaná práce jen do té chvíle,
než hook začne blokovat i to, co je v pořádku. Pak se vypne a nehlídá nic.

---

## 2. Kontrola nikdy neopravuje

**Rozhodnutí:** všech pět agentů má zakázáno cokoliv měnit. `pisar` smí
psát jediný soubor — report.

**Proč:** zjišťování a oprava jsou dvě práce s úplně jiným rizikem.
Zjišťování se dá pustit naslepo v pátek večer. Oprava ne.

Kdyby kontrola během čtení něco opravila, přestala by se pouštět —
protože by se jí přestalo věřit. A kontrola, kterou nikdo nepouští,
je horší než žádná: vytváří dojem, že se dílna hlídá.

**Co to stojí:** dvojí práci u zjevných drobností. `.gitignore`, kterému
chybí jeden řádek, se opraví za tři vteřiny a agent to musí místo toho
napsat do reportu. Beru to — hranice, která má výjimky, není hranice.

---

## 3. Levný model na mechanickou práci

**Rozhodnutí:** `zalohar` běží na Haiku, `pisar` na Opusu, zbytek na Sonnetu.

**Proč:** `zalohar` čte výstup tří příkazů gitu a porovnává seznamy podle
pevných pravidel. Tam silnější model nic nepřidá. `pisar` naopak dostane
výstupy všech ostatních a rozhoduje, co je z dvaceti nálezů dnes důležité
a jak to napsat, aby to někdo přečetl — to je nejtěžší úkol v celém
řetězci a zároveň jediný, jehož výsledek je vidět.

**Co to stojí:** u projektu se zvláštní strukturou může `zalohar`
netrefit, co je data a co balast. Pozná se to podle nesmyslného řádku
v tabulce a dá se to opravit tím, že se mu ta složka pojmenuje v zadání.

---

## 4. Agenti běží souběžně, ne za sebou

**Rozhodnutí:** skill `kontrola-dilny` výslovně nařizuje pustit čtyři
agenty na projekt v jedné zprávě.

**Proč:** čtyři agenti krát patnáct projektů postupně je hodina čekání.
Souběžně jsou to minuty. Rozdíl mezi „pustím to a počkám" a „pustím to
a půjdu pryč" rozhoduje o tom, jestli se to bude pouštět každý týden.

**Co to stojí:** víc souběžných volání a tím i vyšší špičkovou spotřebu.
Celkově se ale nezaplatí víc — práce je stejná, jen se udělá najednou.

---

## 5. Kontext agenta se drží mimo datové složky

**Rozhodnutí:** `data/`, `klient/`, `podklady/` a `_spis*/` jsou zakázané
v oprávněních a skill to připomíná ještě jednou.

**Proč:** dvakrát. Zaprvé je zbytečné posílat klientská data do modelu,
když se kontroluje struktura a ne obsah. Zadruhé — a to je důležitější —
agent, který si obsah přečte, ho pak může nechtěně zopakovat v reportu.
Report se ukládá na disk a někdy se posílá dál.

**Co to stojí:** kontrola nepozná osobní údaj, který leží uvnitř správně
zabezpečené datové složky. To je přijatelné: tam patří. Kontroluje se to,
co je venku z ní.

---

## 6. Historie nálezů v SQLite, ne v souborech

**Rozhodnutí:** nálezy se ukládají do `.dilna/kniha.db` přes MCP server
`kniha`.

**Proč:** kontrola bez historie je fotka. Zajímavé jsou dvě věci, které
z jednoho běhu nejdou zjistit:

- **Nález, který tu je potřetí.** To už není nález, ale rozhodnutí.
  Patří ven z kontroly, ne do dalšího reportu.
- **Nález, který zmizel.** To je jediné místo, kde je vidět pohyb.

V markdownu by to šlo taky, ale porovnání by musel dělat model v každém
běhu znovu a byla by to nejdražší část kontroly. Dotaz nad tabulkou je
zadarmo.

**Co to stojí:** jeden soubor navíc, který se nesmí commitnout. Je
v `.gitignore`.

---

## 7. Ukázkový vzorek uvnitř repozitáře

**Rozhodnutí:** `priklad/` se třemi smyšlenými projekty se zabudovanými
chybami.

**Proč:** nastavení, které se nedá spustit bez toho, aby si člověk nejdřív
postavil vlastní dílnu, si nikdo nezkusí. Vzorek zkracuje cestu od
naklonování k prvnímu výsledku na jeden příkaz.

Chyby ve vzorku nejsou náhodné. Pokrývají po jedné každý druh nálezu,
který kontrola umí najít, a `web-vizitka` je tam schválně čistá — aby
bylo vidět, že kontrola umí i mlčet.

**Co to stojí:** vzorek nemůže mít vlastní git repozitáře, protože leží
uvnitř tohohle. Agenti na něm hlásí chybějící správu verzí. Je to napsané
v `priklad/README.md` i v „Čemu nevěřit".

---

## 8. Hook `osobni_udaje` do vzorku nezasahuje

**Rozhodnutí:** cesty pod `priklad/` hook přeskakuje.

**Proč:** vzorek musí obsahovat data, která vypadají jako osobní údaje —
jinak nemá kontrola co najít. Bez výjimky by se vzorek nedal ani založit,
ani upravit.

**Co to stojí:** kdyby si někdo založil skutečný projekt jménem
`priklad`, hook by ho nehlídal. Je to napsané v hlášce hooku, aby to
nebylo tiché.

---

## 9. Vlastní styl odpovědí

**Rozhodnutí:** `dilna` jako výchozí styl. Krátce, v důsledcích, bez vaty.

**Proč:** majitel dílny není vývojář. Věta „chybí ošetření výjimky
u síťového volání" mu neřekne nic. Věta „když spadne internet, automat
tiše přestane běžet a nikdo se to nedozví" mu řekne všechno včetně toho,
jak je to naléhavé.

Stejné pravidlo je i ve skillu `psani-pro-cloveka`, protože styl platí
na odpovědi v okně a skill i na soubory, které se zapisují.

**Co to stojí:** nic. Styl mění, jak se mluví, ne jak se pracuje —
a je to v něm napsané, aby to model nezaměnil.

---

## 10. Kniha nálezů je vlastní MCP server, ne převzatý

**Rozhodnutí:** `kniha` je `.claude/mcp/kniha.py` — 320 řádků nad SQLite,
jen standardní knihovna, žádná závislost.

**Proč:** původně tam byl hotový `mcp-server-sqlite`. Při prvním
skutečném spuštění se ukázalo, že je opuštěný — volá funkci, která
v dnešní verzi knihovny `mcp` neexistuje, a spadne hned po startu.
Můj test byl přitom `--help`, který skončí dřív, než se server rozjede.
Ověřil jsem, že se balík stáhne, ne že běží.

Připnout starou verzi knihovny by problém odsunulo, ne vyřešilo: za rok
by to spadlo znovu a další člověk by hledal totéž. Vlastní server nemá
co rozbít, protože nestojí na ničem, co se aktualizuje.

Vedlejší přínos: nástroje se dají pojmenovat podle toho, k čemu slouží
(`pretrvavajici`, `zmizele`), místo aby model skládal SQL. Kontrola pak
nemůže dotaz splést a skill je o třetinu kratší.

**Co to stojí:** za ten server ručím sám. Když se protokol MCP posune,
neopraví ho nikdo jiný. U dvou set řádků bez závislostí to beru.

**Co se cestou ukázalo:** server tiše zahazoval zprávy, kterým nerozuměl.
Klient by na odpověď čekal navždy a nikdo by nevěděl proč — přesně to
tiché selhání, na které je v repozitáři vlastní agent. Teď se nesrozumitelná
zpráva vypíše.

---

## Co bych udělal jinak, kdyby na to byl čas

- **Hook na konci sezení.** Když se v sezení měnily soubory a `STAV.md`
  se nesáhl, mělo by to samo připomenout `/konec`. Nedal jsem to tam,
  protože hook, který otravuje po každé drobnosti, se do týdne vypne —
  a správnou hranici jsem zatím nenašel.
- **Rozpoznání jmen.** Na jména neexistuje vzor a seznam příjmení by
  z toho udělal jinou třídu nástroje. Zatím to řeší člověk, což je
  v `anonymizace` napsané nahlas.


