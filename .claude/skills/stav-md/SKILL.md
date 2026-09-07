---
name: stav-md
description: Konvence souboru STAV.md a jak ho po práci aktualizovat, aby po měsíci pauzy šlo navázat. Použij při „ulož, kde jsme skončili", „aktualizuj stav", na konci většího kroku a při zakládání projektu. Odpovídá na „kde jsem skončil", ne na „jak to funguje".
---

# STAV.md

Jeden soubor v každém projektu, který odpovídá na otázku **„kde jsem
skončil a co je na řadě"**. Píše se pro sebe za měsíc, ne pro cizího
člověka — od toho je README.

Nemíchej to s technickým popisem. Když projekt potřebuje vysvětlit, jak
uvnitř funguje, patří to do zvláštního souboru. `STAV.md` má zůstat krátký
dost na to, aby se dal přečíst celý.

## Pět sekcí, vždycky stejných

```markdown
# <projekt> — stav

*Aktualizováno: <D. M. RRRR>*

## Co stavíme
## Co funguje dnes
## Co zbývá
## Čeká se na
## Čemu nevěřit
```

Pořadí neměň a sekce nevynechávej. Když je sekce prázdná, napiš do ní
`Nic.` — prázdná sekce nese informaci, chybějící sekce nese pochybnost,
jestli se na to jen nezapomnělo.

### Co stavíme

Dvě až tři věty. K čemu to je a komu. Tahle sekce se skoro nemění; když
se změní, změnil se projekt a stojí to za samostatnou zmínku.

### Co funguje dnes

Jen to, co jsi **viděl fungovat**. Ne co je napsané, ne co by mělo jít.
U každé položky připiš, kdy to naposled běželo doopravdy.

Tohle je jediná sekce, kde se dá lhát nechtěně. „Import funguje" napsané
v den, kdy se psal kód, a nikdy potom nespuštěné, je nejdražší věta
v celé dílně.

### Co zbývá

Seřazené podle toho, co se má udělat dřív, ne podle velikosti. Nejvýš
sedm položek — když je jich víc, projekt nemá plán, ale seznam přání.

Každá položka začíná slovesem a dá se udělat na jedno posezení. „Dodělat
frontend" není položka.

### Čeká se na

Věci mimo tvoje ruce: odpověď od člověka, podepsaná smlouva, dodávka,
přístup. U každé napiš **od koho** a **od kdy** čekáš. Tahle sekce je
důvod, proč se STAV.md čte i po měsíci — je to jediné místo, kde se pozná,
že něco visí příliš dlouho.

### Čemu nevěřit

Nejcennější sekce a nejčastěji vynechaná. Patří sem:

- co je udělané narychlo a při zátěži se to zlomí
- co je otestované jen na jednom vzorku
- co jsi neověřil a jen předpokládáš
- kde jsou natvrdo zadané cesty a jiná lepidla

Když je tahle sekce prázdná u projektu, kde je kód, buď se lže, nebo
se na to nikdo nedíval.

## Kdy se aktualizuje

Po každém kroku, po kterém by se dalo přestat pracovat. Ne po každém
souboru a ne až na konci projektu.

Poznáš to tak, že si položíš otázku: **kdybych teď zavřel notebook na
tři týdny, našel bych v STAV.md, kde navázat?** Když ne, aktualizuj.

## Jak se aktualizuje

1. Přečti aktuální `STAV.md` **celý**, než začneš psát.
2. Projdi, co se od poslední aktualizace opravdu stalo — `git log`,
   změněné soubory, co jsi viděl běžet.
3. Přesuň hotové věci z „Co zbývá" do „Co funguje dnes". Nepiš je
   dvakrát.
4. Vyhoď z „Čeká se na" to, co dorazilo.
5. Doplň do „Čemu nevěřit", co jsi cestou zjistil. Tahle sekce jen roste,
   dokud se ta místa neopraví.
6. Přepiš datum v hlavičce.

Nikdy nedopisuj nový oddíl na konec, aby zůstala historie. Historie je
v gitu. `STAV.md` popisuje **teď**.

## Časté chyby

- **Psát tam, co se má udělat za rok.** Do „Co zbývá" patří nejbližší
  kroky, ne vize.
- **Nechat „Aktualizováno" starší, než je poslední změna souborů.**
  Právě podle toho se pozná, že se stav rozešel se skutečností.
- **Popisovat, jak to funguje.** To patří jinam.
- **Používat to jako deník.** Není to zápis z jednání, je to fotka stavu.
