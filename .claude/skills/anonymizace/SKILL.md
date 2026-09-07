---
name: anonymizace
description: Najde v souborech české osobní údaje a nahradí je smyšlenými, které mají stejný tvar. Použij před sdílením složky, před pushnutím repozitáře, při výrobě testovacích dat a při „ukliď to, ať to můžu ukázat". Rozlišuje skutečné údaje od vymyšlených.
---

# Anonymizace

Dvě různé práce, které se často pletou:

1. **Kontrola** — je v tom něco, co nesmí ven? Zjišťuje `hlidac-udaju`.
2. **Nahrazení** — udělej z toho vzorek, který jde ukázat. To je tenhle skill.

Nahrazení nikdy nedělej na místě v ostrých datech. Pracuje se s kopií.

## Postup

### 1. Najdi

```bash
python .claude/skills/anonymizace/scripts/najdi_udaje.py <cesta>
```

Skript projde textové soubory a vypíše nálezy s cestou, řádkem a druhem.
Nic nemění. Podrobnosti o vzorech jsou v `references/vzory-cz.md`.

### 2. Rozhodni u každého nálezu

Ne všechno, co vypadá jako osobní údaj, jím je. Před nahrazením se ptej:

- Je to už teď vymyšlené? (`example.com`, `Jan Novák` v testu, `900101/1234`)
- Je to údaj o **osobě**, nebo o firmě, která ho má ve veřejném rejstříku?
- Je ten soubor vůbec určený ven?

Když si u konkrétního nálezu nejsi jistý, nahraď ho. Nahrazený vymyšlený
údaj nikoho nestojí nic; ponechaný skutečný ano.

### 3. Nahraď tvarem, ne hvězdičkami

Hvězdičky rozbijí formát a s ním i všechno, co s daty pracuje. Náhrada musí
mít **stejný tvar a stejnou délku**, aby vzorek zůstal použitelný.

| Místo | Dej |
|---|---|
| rodné číslo | `900101/1234` — datum existuje, číslo je vymyšlené |
| jméno | jméno ze seznamu níž, důsledně stejné pro stejnou osobu |
| e-mail | `jmeno.prijmeni@example.com` |
| telefon | `+420 601 000 000` až `+420 601 000 099` |
| číslo účtu | `123456789/0100` |
| adresa | `Ulice 1, 100 00 Praha 1` |
| spisová značka | `12 C 345/2024` |
| datum narození | posuň o náhodný počet dnů v rámci stejného roku |

**Jedna osoba = jedna náhrada v celém vzorku.** Když se z Nováka stane
jednou Dvořák a podruhé Svoboda, data přestanou dávat smysl a vzorek je
k ničemu. Veď si tabulku náhrad a použij ji na všechny soubory naráz.

### 4. Zkontroluj výsledek

Pusť `najdi_udaje.py` znovu na výsledek. Musí vyjít prázdný. Když ne,
buď zbyl skutečný údaj, nebo náhrada omylem trefila platný tvar — obojí
je potřeba vyřešit, ne odmávnout.

## Zásoba smyšlených jmen

Používej tahle, ať se vzorky mezi projekty nepletou. Jsou dost obyčejná
na to, aby vypadala pravdivě, a dost běžná na to, aby neukazovala na
konkrétního člověka.

`Adam Bartoš`, `Blanka Cíglerová`, `Cyril Doubek`, `Dana Effenberková`,
`Emil Fiala`, `Filip Grznár`, `Gabriela Havlová`, `Hynek Ircing`,
`Ivana Jelínková`, `Jakub Kadlec`, `Klára Lomecká`, `Lukáš Mádr`

Když test potřebuje zvláštní vlastnost — dvojité příjmení, diakritiku,
překlep z rozpoznávání textu — vymysli si ji na těchhle jménech. Nikdy
kvůli tomu nesahej po skutečném klientovi.

## Čeho se vyvarovat

- **Nahrazovat v ostrých datech.** Vždycky kopie.
- **Nahrazovat jen viditelná pole.** Údaje bývají v logu, v názvu souboru
  a v metadatech dokumentu. Projdi i názvy souborů.
- **Zapomenout na git.** Když byl údaj někdy commitnutý, nahrazení
  v pracovní složce ho z historie nesundá. To je jiný, dražší problém —
  ohlas ho a nezastírej ho.
- **Vyrobit vzorek, který je pořád rozpoznatelný.** Když v obci se sto
  obyvateli zbyde jediný právník, jméno jsi změnil zbytečně.
