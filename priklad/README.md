# Ukázkový vzorek dílny

Tři smyšlené projekty, na kterých se dá celé nastavení vyzkoušet, aniž
by bylo potřeba mít vlastní dílnu. **Všechna data tady jsou vymyšlená** —
jména, rodná čísla, e-maily i firmy. Nic z toho neodkazuje na skutečnou
osobu.

Každý projekt má schválně jinou chybu, aby bylo vidět, co která část
nastavení najde.

| Projekt | Co je na něm špatně | Kdo to najde |
|---|---|---|
| `fakturace` | složka s daty není v `.gitignore` a je v ní rodné číslo; `STAV.md` je o měsíc pozadu | `hlidac-udaju`, `revizor-stavu` |
| `newsletter` | nemá `STAV.md`, skript tiše polyká chyby, cesta je zadaná natvrdo | `krehka-mista`, hook `stav_pripominka` |
| `web-vizitka` | nic — je v pořádku | nikdo, má projít bez nálezu |

## Jak to zkusit

```bash
/kontrola
```

Nebo jen jednu část:

```bash
python .claude/skills/anonymizace/scripts/najdi_udaje.py priklad --vse
```

Přepínač `--vse` je tu potřeba schválně. Bez něj skript nálezy pod
složkou `priklad/` skryje jako smyšlené — což je správné chování při
běžné práci a nepohodlné při ukázce.

## Proč nejsou projekty gitové repozitáře

Vzorek leží uvnitř tohohle repozitáře, takže vlastní `.git` mít nemůže.
Agenti `zalohar` a `revizor-stavu` proto na vzorku hlásí, že projekt není
pod správou verzí — to je u ukázky očekávané, ne chyba.

Na skutečné dílně ukaž agentům složku přes `DILNA_ROOT`:

```bash
export DILNA_ROOT=/cesta/k/moji/dilne   # Windows: $env:DILNA_ROOT = "C:\dilna"
```
