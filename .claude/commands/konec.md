---
description: Zapíše, kde jsme skončili — aktualizuje STAV.md projektu, na kterém se právě pracovalo.
argument-hint: "[projekt, nebo nic pro aktuální]"
allowed-tools: Read, Glob, Grep, Edit, Write, Bash(git *)
---

Aktualizuj `STAV.md` podle skillu `stav-md`.

Projekt: `$1` — když je prázdný, vezmi ten, ve kterém jsme v tomhle sezení
opravdu měnili soubory. Když se pracovalo na víc projektech, zeptej se
který, nebo aktualizuj všechny a řekni, že jsi to udělal.

Postup:

1. Přečti celý `STAV.md`, než začneš psát.
2. Zjisti, co se doopravdy stalo: `git log` od poslední aktualizace,
   změněné soubory, co jsme v sezení viděli běžet.
3. Přepiš pět sekcí podle skillu. Do „Co funguje dnes" dej **jen to,
   co jsme viděli fungovat** — ne to, co je napsané.
4. Do „Čemu nevěřit" doplň, co jsme cestou zjistili, že je křehké.
5. Přepiš datum v hlavičce.

Nakonec vypiš rozdíl proti původnímu stavu ve třech odrážkách — co
přibylo, co se přesunulo, co zmizelo. Celý soubor do odpovědi nekopíruj.
