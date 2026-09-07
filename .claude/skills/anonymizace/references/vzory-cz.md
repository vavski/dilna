# České osobní údaje — vzory a jejich úskalí

Referenční tabulka k `najdi_udaje.py`. Každý vzor má svůj způsob, jak
selhat. Kdo je zná, ušetří si falešné poplachy i přehlédnutí.

## Rodné číslo

```
\b(\d{2})(\d{2})(\d{2})\s?/\s?(\d{3,4})\b
```

Tvar je `RRMMDD/XXXX`. Čtyřmístná koncovka se používá od roku 1954,
starší čísla mají tři.

**Falešné poplachy:** čísla faktur, verze a měřítka mají stejný tvar.
Odfiltruj je kontrolou, že prostřední dvojice dává platný měsíc — ženám
se přičítá 50, a od roku 2004 při vyčerpání kapacity dne dalších 20.
Takže platné hodnoty měsíce jsou `01–12`, `21–32`, `51–62` a `71–82`.

**Nekontroluj dělitelnost jedenácti.** U čísel vydaných do roku 1954
neplatí a vyřadila bys tím skutečné údaje starších klientů.

**Přehlédnutí:** rodné číslo bez lomítka (`9001011234`) vzor nechytí.
Když pracuješ s exportem z cizího systému, prohlédni jeden vzorek ručně,
než se spolehneš na hledání.

## DIČ a IČO

```
DIČ:  \bCZ\d{8,10}\b
IČO:  \b\d{8}\b   ← jen v okolí slov IČO, IC, firma, dodavatel
```

DIČ fyzické osoby často obsahuje rodné číslo. **Nález DIČ ve tvaru
`CZ` + 9 nebo 10 číslic ber jako nález rodného čísla**, ne jako údaj
o firmě.

IČO samo o sobě je veřejné a nálezem být nemusí. Osmimístné číslo bez
kontextu je ale nejčastěji něco úplně jiného, proto se hledá jen v okolí
klíčových slov.

## Číslo účtu

```
klasické: \b\d{1,6}-?\d{2,10}/\d{4}\b
IBAN:     \bCZ\d{2}(?:\s?\d{4}){5}\b
```

Klasický tvar se plete se spisovou značkou a s datem. Rozliší je kód
banky na konci — čtyři číslice z uzavřeného seznamu (`0100`, `0300`,
`0600`, `0710`, `0800`, `2010`, `3030`, `5500`, `6210`, `6800`, `2700`,
a další). Když poslední skupina není platný kód banky, nejspíš to není účet.

## E-mail a telefon

```
e-mail:  \b[\w.+-]+@[\w-]+\.[\w.]{2,}\b
telefon: (?:\+420[\s-]?)?\b\d{3}[\s-]?\d{3}[\s-]?\d{3}\b
```

Devítimístné číslo je v českém textu velmi časté — bankovní účty, IČO,
identifikátory. **Telefon hlas jen tehdy, když má předvolbu, nebo když
kolem něj stojí slovo `tel`, `mobil`, `kontakt`.** Jinak utopíš report
v šumu.

Pracovní e-mail zveřejněný na webu kanceláře je jiná kategorie než
soukromý e-mail klienta. Vzor je nerozliší — rozhodni to sám.

## Spisová značka

```
\b\d{1,3}\s?[A-Z]{1,3}\s?\d{1,4}/\d{4}\b
```

Například `12 C 345/2024`. Sama o sobě není osobní údaj, ale ve spojení
s čímkoliv dalším ukazuje na konkrétní řízení a konkrétní lidi.
**Ve veřejném vzorku ji nahrazuj vždycky.**

## Klíče a tokeny

```
sk-[A-Za-z0-9]{16,}       API klíč
ghp_[A-Za-z0-9]{20,}      GitHub token
AKIA[0-9A-Z]{12,}         AWS
-----BEGIN ... PRIVATE KEY-----
```

Tohle nejsou osobní údaje, ale patří sem, protože se hledají ve stejném
průchodu a mají stejný osud — nesmí ven.

**Nález klíče se neanonymizuje, klíč se zneplatní.** Nahradit ho v souboru
nestačí, protože ten původní pořád funguje. Ohlas to jako věc k okamžitému
řešení, ne k nahrazení.

## Co žádný vzor nechytí

- **Jména.** Na české jméno neexistuje spolehlivý vzor. Hledají se
  seznamem nejčastějších příjmení, nebo se prostě přečte vzorek.
- **Adresy.** Totéž. Pomůže hledat PSČ (`\b\d{3}\s?\d{2}\b`) a číst okolí.
- **Údaj v obrázku nebo v naskenovaném PDF.** Textové hledání ho mine
  úplně. Když projekt pracuje se skeny, kontrola textu nestačí a je
  potřeba to říct nahlas.
- **Kombinace, která identifikuje sama.** „Advokátka v Kašperských Horách
  s dcerou na gymnáziu" neobsahuje žádný osobní údaj a přesto ukazuje
  na jednoho člověka. Tohle pozná jen člověk.
