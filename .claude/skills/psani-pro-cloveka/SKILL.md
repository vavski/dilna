---
name: psani-pro-cloveka
description: Jak psát výstupy pro majitele dílny, který není vývojář — v důsledcích místo v názvech technologií, krátce a bez vaty. Použij při psaní reportu, shrnutí, návrhu, e-mailu a při „vysvětli mi to" nebo „napiš to normálně". Platí na všechny české texty, které z dílny vycházejí.
---

# Psaní pro člověka

Čtenář umí zadat práci a rozhodnout o penězích. Neumí a nechce číst
výpisy. Když text nepřečte, práce se neudělá — a to je chyba textu,
ne čtenáře.

## Jediné pravidlo, ze kterého plyne zbytek

**Piš v důsledcích, ne ve jménech technologií.**

| Ne | Ano |
|---|---|
| chybí ošetření výjimky u síťového volání | když spadne internet, automat tiše přestane běžet a nikdo se to nedozví |
| `data/leads.db` není v `.gitignore` | při nejbližším nahrání na GitHub jdou kontakty ven |
| absolutní cesta v konfiguraci | až tu složku přesuneš, přestane to fungovat a nic to neohlásí |
| chybí index nad tabulkou | při tisíci záznamech se to začne táhnout |
| STAV.md není synchronní s HEAD | popis projektu tvrdí něco, co je tři týdny hotové |

Název technologie použij jen tehdy, když ho čtenář potřebuje k tomu, aby
něco našel nebo napsal. `data/leads.db` v tabulce výš zůstává, protože
bez cesty by nevěděl, kde to je.

## Tvar

- **První věta odpovídá na otázku, se kterou čtenář přišel.** Ne kontext,
  ne postup, ne co jsi dělal.
- **Nejvýš tři věci k udělání dnes.** Když jich je víc, seřaď je a zbytek
  dej pod čáru. Seznam dvaceti položek je stejně užitečný jako žádný.
- **Každá položka začíná slovesem.** „Přesuň", „Zazálohuj", „Ověř".
- **Za položkou důsledek v závorce.** Bez něj čtenář nemá jak rozhodnout
  o pořadí.
- **Odrážky jen na seznamy.** Souvislá úvaha je věta, ne tři odrážky
  pod sebou.
- **Nadpis až od tří oddílů výš.** Nad dvěma odstavci je nadpis šum.

## Čeho se zbavit

Tyhle obraty nenesou informaci a jen prodlužují text:

`je důležité zmínit`, `stojí za zmínku`, `v neposlední řadě`,
`komplexní řešení`, `robustní`, `elegantní`, `posunout na další úroveň`,
`v dnešní době`, `jak již bylo řečeno`, `doufám, že to pomůže`,
`rád ti s tím pomůžu`, `skvělá otázka`

Stejně tak omluvy a předehry. Když jsi udělal chybu, oprav ji jednou
větou a pokračuj. Když jsi hotový, řekni to bez „myslím, že by to
snad mohlo".

## Odhady

Odhad piš jen tehdy, když ho máš z čeho udělat, a napiš, z čeho.
`Asi dvě hodiny, protože stejnou věc jsme dělali u X` je odhad.
`Pravděpodobně to nebude trvat dlouho` je vata.

Když odhad nemáš, napiš `nevím, kolik to je práce` a co bys potřeboval
zjistit. To je použitelnější než vymyšlené číslo.

## Když je zpráva špatná

Nezjemňuj a nedramatizuj. Napiš, co se stalo, co to znamená a co s tím.

> Automat devět dní neběžel. Přišel o 34 e-mailů, které se musí projít
> ručně. Příčina: přejmenovaná složka, na kterou ukazovala naplánovaná
> úloha. Opravené je to od dneška, seznam nezpracovaných e-mailů je
> v `data/dohnat.md`.

Ne „došlo k nesrovnalosti v konfiguraci". Ne „bohužel musím s politováním
oznámit".

## Test před odesláním

Přečti si první tři řádky. **Ví po nich čtenář, jestli musí něco udělat?**
Když ne, přepiš je. Zbytek textu už nikdo nečte, když ho první tři řádky
nepřesvědčí, že to má smysl.
