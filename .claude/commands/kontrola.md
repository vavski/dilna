---
description: Projde všechny projekty v dílně a napíše report — co hnije, co není zazálohované, kde utíkají údaje.
argument-hint: "[cesta k dílně, nebo nic pro výchozí]"
allowed-tools: Read, Glob, Grep, Bash(git *), Task, Write
---

Spusť kontrolu dílny podle skillu `kontrola-dilny`.

Kořen dílny: `$1` — když je prázdný, použij `DILNA_ROOT`, a když není ani
ten, tak složku `priklad/` v tomhle projektu.

Než začneš, vypiš jedním řádkem, kolik projektů budeš kontrolovat a kde.
Pak jeď podle skillu: čtyři agenti na projekt naráz, porovnání s knihou,
report od `pisar`a, zápis nálezů zpátky do knihy.

Nic neopravuj. Na konci se zeptej, jestli má něco z reportu opravit hned.
