---
description: Založí v dílně nový projekt se STAV.md, CLAUDE.md, .gitignore a gitem.
argument-hint: "<nazev-projektu> <k čemu to je>"
allowed-tools: Read, Glob, Bash(python *), Bash(git *)
---

Založ nový projekt podle skillu `novy-projekt`.

Zadání od uživatele: `$ARGUMENTS`

Z toho si vezmi název a popis. Když v zadání chybí jedno nebo druhé,
zeptej se — ale jen na to, co chybí, ne na obojí znovu.

Zeptej se navíc na jedinou věc: **budou v projektu citlivá data?** Když
ano, na kterou složku. Ta půjde do `.gitignore` dřív, než tam něco přistane.

Pak spusť `zaloz.py` a vypiš, co zbývá uživateli.
