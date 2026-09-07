# dílna

Nastavení Claude Code pro člověka, který má vedle sebe patnáct malých
projektů a žádný z nich není tak velký, aby si zasloužil vlastní pozornost.
Dohromady jsou ale dost velké na to, aby se v nich ztratil.

Popis pro člověka je v `README.md`. Rozhodnutí a jejich důvody v `docs/`.

## Co se tu nesmí

- **Číst obsah datových a klientských složek.** `data/`, `klient/`,
  `podklady/`, `_spis*/` jsou zakázané v `.claude/settings.json` a to
  pravidlo se neobchází. Kontrola dílny pracuje s metadaty, ne s obsahem.
- **Psát skutečná jména a údaje kamkoliv.** Do kódu, do testů, do
  komentářů ani do ukázkových dat. Seznam smyšlených jmen je ve skillu
  `anonymizace`.
- **Obcházet hook `git_ochrana.py`.** Když blokne commit, je to proto, že
  v indexu je datový soubor. Řešení je vyndat ho, ne hook vypnout.
- **Přidávat do vzorku pod `priklad/` skutečná data.** Vzorek je veřejný.

## Jak je to poskládané

Pět MCP serverů, pět subagentů, pět skillů, tři hooky. Nic z toho není
plugin — všechno leží v souborech v tomhle repozitáři.

Když v tom něco měníš, změň i `docs/rozhodnuti.md`. Nastavení bez důvodů
se za tři měsíce nedá udržovat.

## Práce se vzorkem

`priklad/` obsahuje tři smyšlené projekty se schválně zabudovanými
chybami. **Neopravuj je.** Jsou tam proto, aby bylo na čem ukázat, co
kontrola najde. Když by je někdo opravil, ukázka přestane fungovat.

Hook `osobni_udaje.py` do `priklad/` schválně nezasahuje.

## Kořen dílny

Agenti a hooky hledají projekty v tomhle pořadí:

1. cesta zadaná v příkazu
2. proměnná prostředí `DILNA_ROOT`
3. `priklad/` v tomhle repozitáři

Nikdy nehádej, kde dílna leží. Když v kořeni nejsou podsložky, řekni to
a skonči.
