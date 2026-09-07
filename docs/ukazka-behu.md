# Jak vypadá jeden běh

Co se stane mezi `/kontrola` a hotovým reportem. Psané podle vzorku
`priklad/`, aby se to dalo zopakovat.

---

## Ještě před prvním slovem

Sezení se otevře a spustí se hook `stav_pripominka.py`. Nikdo ho nevolal
a model o něm neví — prostě dostane do kontextu tohle:

```
Stav dílny (priklad):
STAV.md je pozadu za skutečnou prací:
  - fakturace (o 97 dnů)
Bez STAV.md: newsletter
Datová složka bez pravidla v .gitignore:
  - fakturace/data
Tohle je jen upozornění. Nic neopravuj, dokud o to uživatel neřekne.
```

Poslední řádek tam je schválně. Bez něj má model tendenci začít
opravovat věci, na které se nikdo neptal.

Zároveň se rozjede stavový řádek:

```
Opus 5 | dilna | main | 1 bez STAV.md
```

---

## `/kontrola`

Příkaz načte skill `kontrola-dilny` a ten model provede pěti kroky.

### Krok 1 — seznam projektů

Najde `fakturace`, `newsletter`, `web-vizitka`. U každého si zjistí,
jestli je to git repozitář a kdy se v něm naposled něco měnilo.

### Krok 2 — čtyři agenti naráz

Tohle je místo, kde se rozhoduje o tom, jestli kontrola trvá minuty nebo
hodinu. Skill výslovně říká pustit je v jedné zprávě.

Na `fakturace` najde `hlidac-udaju` tohle:

```
KRITICKÉ: rodné číslo
  Soubor: priklad/fakturace/data/odberatele.csv:2
  Ukázka: 900*******4
  Sledované gitem: ne
  Co s tím: přidat `data/` do .gitignore dřív, než někdo udělá git add .
```

A `revizor-stavu` tohle:

```
ROZPOR: STAV.md tvrdí, že se čeká na účetní, ale čeká se od 28. 5.
  Napsáno:    „Čeká se na potvrzení číselné řady faktur od účetní."
  Skutečnost: hlavička je z 2. 6. 2026, od té doby žádná změna.
```

Na `newsletter` najde `krehka-mista` tři věci, z nichž nejhorší je tahle:

```
KŘEHKÉ: odeslání e-mailu selže a nikdo se to nedozví
  Kde:     priklad/newsletter/skripty/rozeslat.py:38
  Spustí to: výpadek SMTP serveru, plná schránka, špatná adresa
  Jak dlouho by to nikdo nevěděl: dokud se někdo nezeptá, proč newsletter nechodí
  Nejlevnější pojistka: vypsat počet neúspěšných odeslání na konci běhu
```

`web-vizitka` projde bez nálezu. To je taky výsledek.

### Krok 3 — porovnání s knihou

Dotaz do `.dilna/kniha.db`. Při prvním běhu je prázdná, takže se přeskočí.
Při třetím běhu vypadne třeba tohle:

```
Nález „data/ mimo .gitignore" je tu potřetí. Není to nález, ale rozhodnutí.
Má zmizet z kontroly?
```

### Krok 4 — report

`pisar` dostane všechny nálezy a udělá z nich tohle:

```markdown
# Kontrola dílny — 7. 9. 2026

Hoří jedna věc: v projektu fakturace leží rodná čísla ve složce,
kterou nekryje .gitignore.

## Udělat dnes
- Přidej `data/` do `.gitignore` v projektu fakturace
  (jinak jdou rodná čísla pěti lidí ven při nejbližším nahrání na GitHub)

## Udělat tenhle týden
- Doplň do newsletteru výpis, kolik e-mailů se nepodařilo odeslat
  (dnes se chyba ztratí a rozesílka může tiše nepracovat celé týdny)
- Přepiš cestu v newsletteru tak, aby nebyla svázaná s jedním diskem
  (po přesunu složky to přestane fungovat bez varování)

## Ví se o tom, nespěchá
- Fakturace čeká na účetní od 28. května. Buď připomeň, nebo to
  z čekání vyškrtni.
- Newsletter nemá STAV.md.

## Prošlo bez nálezu
web-vizitka
```

Report se uloží do `.dilna/reporty/2026-09-07.md`.

### Krok 5 — zápis do knihy

Jeden řádek na nález. Bez tohohle kroku by krok 3 příště neměl s čím
porovnávat.

---

## Když se model splete

Řekněme, že se rozhodne nález rovnou opravit a napíše `.gitignore`
i se seznamem odběratelů v komentáři. Zasáhne hook:

```
ZÁPIS ZASTAVEN — v obsahu jsou osobní údaje.
Soubor: .gitignore
Nalezeno: rodné číslo (900101/1234)
```

A když by chtěl commitnout se souborem dat v indexu:

```
COMMIT ZASTAVEN — v indexu jsou soubory, které vypadají jako data:
  - priklad/fakturace/data/odberatele.csv
```

Obojí je závora, ne rada. Model to nemůže přeskočit tím, že si to
rozmyslí — hook běží mimo něj.

---

## Co si z běhu odnést

Kontrola nenašla nic, co by se nedalo najít ručně. Našla to za dvě minuty
místo za odpoledne, a hlavně to seřadila — jedna věc dnes, dvě tenhle
týden, zbytek ne. To je celý rozdíl proti seznamu dvaceti nálezů, který
se přečte jednou a pak už nikdy.
