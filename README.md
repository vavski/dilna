# dílna

Nastavení Claude Code pro člověka, který má vedle sebe patnáct malých
projektů. Žádný z nich není dost velký, aby si zasloužil pozornost.
Dohromady jsou dost velké na to, aby se v nich ztratil.

Ráno se zeptáš `/kontrola` a dostaneš odpověď na tři otázky:

- **Který projekt hnije?** Popis stavu tvrdí něco, co přestalo platit.
- **Co zmizí, když shoří disk?** Data, která nejsou nikde jinde.
- **Co teče ven?** Osobní údaje ve složce, kterou nekryje `.gitignore`.

Nic to neopravuje. Výstupem je seznam kroků, seřazený podle toho, co se
stane, když se to neudělá.

---

## Rychlý start

```bash
git clone <adresa-tohoto-repozitare> dilna
cd dilna
claude
```

Při prvním spuštění se Claude Code zeptá, jestli má povolit MCP servery
z `.mcp.json`. Odsouhlas je — bez nich část kontroly nepoběží.

Pak:

```
/kontrola
```

Bez dalšího nastavení to zkontroluje ukázkový vzorek `priklad/` — tři
smyšlené projekty, každý s jinou zabudovanou chybou. Na skutečnou dílnu
to pustíš takhle:

```bash
# Windows PowerShell
$env:DILNA_ROOT = "C:\moje\dilna"

# macOS a Linux
export DILNA_ROOT=~/dilna
```

### Co je potřeba mít

| | Na co | Ověřeno |
|---|---|---|
| Claude Code | vlastně všechno | |
| Python 3.10+ | hooky, stavový řádek, skripty ve skillech | 3.14.3 |
| Node.js 18+ | MCP servery `soubory` a `pamet` (přes `npx`) | 24.15.0 |
| `uv` | MCP servery `git` a `web` (přes `uvx`) | 0.12.2 |
| git | bez něj polovina kontroly nemá co číst | 2.54 |

Verze ve třetím sloupci jsou ty, na kterých je to odzkoušené. Nižší
nejspíš taky projdou, ale netvrdím to.

---

## Co v tom je

Žádný plugin ani marketplace. Všechno leží v souborech v tomhle
repozitáři a dá se přečíst.

```
.mcp.json                   pět MCP serverů
.claude/
├── settings.json           oprávnění, hooky, stavový řádek
├── agents/                 pět subagentů
├── skills/                 pět skillů
├── commands/               tři slash příkazy
├── hooks/                  tři hooky
├── output-styles/          styl odpovědí
├── mcp/kniha.py            vlastní MCP server nad historií nálezů
└── statusline.py           stavový řádek
priklad/                    ukázkový vzorek, tři smyšlené projekty
testy/zkousky.py            dvacet zkoušek, ověří to výše
docs/                       proč je to udělané takhle
```

### MCP servery

| Server | K čemu | Odkud |
|---|---|---|
| `soubory` | čtení projektů mimo pracovní složku | `@modelcontextprotocol/server-filesystem` |
| `git` | historie projektu bez pouštění příkazů | `mcp-server-git` |
| `web` | dohledání, jestli je závislost ještě živá | `mcp-server-fetch` |
| `pamet` | co jsme o projektech zjistili minule | `@modelcontextprotocol/server-memory` |
| `kniha` | historie nálezů z minulých kontrol | **vlastní**, `.claude/mcp/kniha.py` |

`kniha` je ten, kvůli kterému to má smysl pouštět opakovaně. Bez historie
je kontrola fotka. S ní je vidět, jestli se dílna zlepšuje — a hlavně
který nález tam visí potřetí, protože to není nález, ale rozhodnutí.

### Subagenti

Každý se ptá na jednu otázku a nic neopravuje. Běží souběžně, takže
kontrola patnácti projektů je minuty, ne hodina.

| Agent | Otázka | Model |
|---|---|---|
| `revizor-stavu` | Rozešel se popis se skutečností? | Sonnet |
| `hlidac-udaju` | Odešly by osobní údaje při pushnutí? | Sonnet |
| `zalohar` | Co zmizí, když shoří disk? | Haiku |
| `krehka-mista` | Co se rozbije, až to poběží samo? | Sonnet |
| `pisar` | Jak to napsat, aby to někdo přečetl? | Opus |

Modely nejsou nastavené náhodně. `zalohar` jen čte výstup gitu a porovnává
seznamy — na to je Haiku dost a je mnohonásobně levnější. `pisar` naopak
skládá dohromady výstupy všech ostatních a rozhoduje, co je dnes důležité;
tam se úspora vrátí jako report, který nikdo nepřečte.

### Skilly

| Skill | Kdy se pustí |
|---|---|
| `kontrola-dilny` | „zkontroluj dílnu", „co mi hnije" |
| `novy-projekt` | „založ projekt", „začínám novou věc" |
| `anonymizace` | „ukliď to, ať to můžu ukázat" |
| `stav-md` | „ulož, kde jsme skončili" |
| `psani-pro-cloveka` | při psaní jakéhokoliv výstupu ven |

Dva z nich mají vlastní skripty, které dělají mechanickou práci mimo
model — hledání údajů a zakládání projektu. Model se pak rozhoduje nad
výsledkem, místo aby ručně prohledával soubory.

### Hooky

Hooky jsou jediná část nastavení, která platí, i když na ni model
zapomene. Proto v nich je to, co se nesmí stát nikdy.

| Hook | Kdy | Co dělá |
|---|---|---|
| `osobni_udaje.py` | před zápisem souboru | zastaví zápis rodného čísla, DIČ nebo IBANu |
| `git_ochrana.py` | před příkazem v shellu | zastaví `git add -f`, `push --force`, `reset --hard`; a commit, který má v indexu datový soubor |
| `stav_pripominka.py` | na začátku sezení | vypíše projekty, kde je popis stavu pozadu |

---

## Jak to vypadá

Hook zastaví zápis dřív, než se stane:

```
$ echo '{"tool_input":{"file_path":"seznam.md","content":"Emil Fiala, 691128/7788"}}' \
    | python .claude/hooks/osobni_udaje.py

ZÁPIS ZASTAVEN — v obsahu jsou osobní údaje.
Soubor: seznam.md
Nalezeno: rodné číslo (691128/7788)
```

Začátek sezení nad ukázkovým vzorkem:

```
Stav dílny (priklad):
STAV.md je pozadu za skutečnou prací:
  - fakturace (o 97 dnů)
Bez STAV.md: newsletter
Datová složka bez pravidla v .gitignore:
  - fakturace/data
```

Hledání údajů:

```
$ python .claude/skills/anonymizace/scripts/najdi_udaje.py priklad --vse

Prošlo 9 souborů, 22 nálezů.

rodné číslo (5×)
  priklad\fakturace\data\odberatele.csv:2  900*******4 [vypadá smyšleně]
  ...
```

---

## Jak si ověřit, že to funguje

```bash
python testy/zkousky.py
```

Dvacet zkoušek přes hooky, stavový řádek, skener osobních údajů a MCP
server. Trvá to pár vteřin a nepotřebuje to běžící Claude Code.

```
Hook osobni_udaje.py
  PROSLO   rodne cislo zastavi zapis
  PROSLO   cislo faktury projde
  PROSLO   vzorek pod priklad/ projde
  PROSLO   DIC zastavi zapis
...
Vsechny zkousky prosly.
```

Subagenty zkoušky nepokrývají — ti potřebují běžící Claude Code a jejich
odpověď se pokaždé liší. Testovat se dá jen to, co má pevný výstup.

---

## Ukázkový vzorek

`priklad/` jsou tři smyšlené projekty, na kterých se dá všechno vyzkoušet
bez vlastní dílny. **Všechna data v něm jsou vymyšlená.**

| Projekt | Zabudovaná chyba |
|---|---|
| `fakturace` | složka s daty mimo `.gitignore`, `STAV.md` o tři měsíce pozadu |
| `newsletter` | bez `STAV.md`, skript tiše polyká chyby, cesta natvrdo |
| `web-vizitka` | žádná — má projít bez nálezu |

Podrobnosti a jejich vysvětlení v [`priklad/README.md`](priklad/README.md).

---

## Čemu nevěřit

Poctivý seznam toho, co jsem neodzkoušel nebo co má známou hranici.

- **Odzkoušené na Windows 11 s Pythonem 3.14.** Cesty v hoocích jsou
  psané přenositelně a `subprocess` se volá bez shellu, takže by to na
  macOS a Linuxu mělo projít — ale netvrdím, že to tam běželo.
- **Čas změny souboru se klonováním ztratí.** Proto se `stav_pripominka`
  dívá i na datum napsané v hlavičce `STAV.md`. U projektu, který
  hlavičku nemá, po klonování nepozná nic.
- **Hledání údajů čte jen text.** Údaj v obrázku nebo v naskenovaném PDF
  mine úplně. Když projekt pracuje se skeny, kontrola textu nestačí.
- **Vzorek pod `priklad/` nejsou git repozitáře**, protože leží uvnitř
  tohohle repozitáře. Agenti `zalohar` a `revizor-stavu` proto na vzorku
  hlásí chybějící správu verzí. Na skutečné dílně se to nestane.
- **`kniha` a `pamet` si zakládají soubory v `.dilna/`** při prvním
  použití. Ta složka je v `.gitignore` — historie nálezů je jen tvoje.
- **`kniha` je vlastní server, ne převzatý.** Původně tam byl
  `mcp-server-sqlite`, ale ten je opuštěný a při startu spadne na
  funkci, která v dnešní verzi knihovny neexistuje. Vlastní server
  stojí jen na standardní knihovně, takže ho nemá co rozbít — zato
  za něj ručím sám. Odzkoušený je handshake, výpis nástrojů, zápis
  nálezu, odmítnutí špatného vstupu a rozpoznání téhož nálezu mezi běhy.

---

## Proč zrovna takhle

Rozhodnutí a jejich důvody jsou v [`docs/rozhodnuti.md`](docs/rozhodnuti.md).
Nejkratší verze:

**Hooky dělají to, co se nesmí stát nikdy. Skilly dělají to, co se má
stát obvykle.** Instrukce v souboru je doporučení — model ji může
přehlédnout, když má hlavu jinde. Hook je závora. Proto v hoocích není
nic o stylu psaní a ve skillech nic o osobních údajích.

**Kontrola nesmí opravovat.** Zjišťování a oprava jsou dvě práce s jiným
rizikem. Kontrola, která během čtení něco přepíše, se přestane pouštět.

**Report má mít tři položky, ne třicet.** Kontrola, která najde třicet
věcí, se přečte jednou. Proto `pisar` třídí podle důsledku a zbytek
nechává v knize na příště.


