---
name: novy-projekt
description: Založí v dílně nový projekt se vším, co má mít od první minuty — STAV.md, CLAUDE.md, .gitignore a git. Použij při „založ projekt", „začínám novou věc", „potřebuju složku na X". Zabrání tomu, aby projekt vznikl bez pravidel a doháněl je pak měsíce.
---

# Nový projekt v dílně

Většina nepořádku v dílně vzniká v první hodině projektu. Složka se založí
narychlo, `.gitignore` se dopíše až po prvním commitu s daty a `STAV.md`
nevznikne nikdy. Tenhle skill to udělá naopak.

## Postup

### 1. Zeptej se na tři věci, ne na víc

- **Jak se to jmenuje?** Krátce, malými písmeny, spojovníky místo mezer.
- **K čemu to je?** Jedna věta. Půjde do `STAV.md` i do `CLAUDE.md`.
- **Budou tam citlivá data?** Když ano, zeptej se, ve které složce budou
  ležet, a ta půjde do `.gitignore` dřív, než tam něco přistane.

Na nic dalšího se neptej. Jazyk, licenci a strukturu si projekt vyrobí sám,
až bude vědět, co je zač.

### 2. Zkontroluj jméno proti dílně

Než složku založíš, ověř, že název ještě neexistuje a že nekoliduje
s číslováním, které dílna používá. **Existující projekt nikdy nepřečíslovávej,
abys udělal místo** — cesty na něj ukazují odjinud a přejmenování je tiše
utne. Přidej nové číslo nebo nech mezeru.

### 3. Založ

```bash
python .claude/skills/novy-projekt/scripts/zaloz.py <nazev> --popis "<jedna věta>" [--data <slozka>]
```

Skript založí složku, čtyři soubory a git repozitář s prvním commitem.
Když složka existuje, skončí chybou a nic nepřepíše.

### 4. Řekni, co zbývá uživateli

Skript nedělá dvě věci schválně, protože obě jsou nevratné nebo něco stojí:

- **vzdálený repozitář** — `gh repo create` se ptá na veřejný/soukromý
- **řádek v rozcestníku dílny** — kam projekt patří, ví jen uživatel

Obojí nabídni, ale nedělej sám.

## Co vznikne

```
<nazev>/
├── STAV.md        pět sekcí, viz skill stav-md
├── CLAUDE.md      co agent o projektu musí vědět
├── README.md      pro člověka, ne pro agenta
├── .gitignore     včetně datové složky, když byla zadaná
└── .git/          jeden commit „prazdny projekt"
```

## CLAUDE.md nového projektu

Drž ho krátký. Není to popis projektu — od toho je README. Je to seznam
věcí, kvůli kterým by agent udělal škodu, kdyby je nevěděl.

Nejdůležitější sekce je **„Co se tu nesmí"**. Když nevíš, co do ní napsat,
napiš aspoň tohle a doplň to, jakmile projekt narazí:

```markdown
## Co se tu nesmí

- Commitovat cokoliv ze složky `<datová složka>`.
- Obcházet .gitignore přes `git add -f`.
- Psát do kódu nebo do testů skutečná jména a údaje.
```

## Čemu se vyhnout

- **Zakládat projekt „na zkoušku" bez gitu.** Zkouška se za tři týdny
  změní v ostrý provoz a historie chybí.
- **Odkládat .gitignore.** Když do složky s daty přistane první soubor
  dřív než pravidlo, je to už jen otázka času.
- **Kopírovat strukturu z jiného projektu.** Zdědíš i jeho balast.
