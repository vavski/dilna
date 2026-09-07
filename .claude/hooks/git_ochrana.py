#!/usr/bin/env python3
"""PreToolUse hook: hlídá nevratné a nebezpečné příkazy v gitu.

Řeší dvě různé bolesti:

1. Nevratné příkazy (`git push --force`, `git reset --hard`, `git add -f`).
   Ty zastavíme vždy. Když je uživatel opravdu chce, spustí si je sám
   v terminálu — agent na ně sahat nemá.

2. Commit, který má v indexu soubor ze složky s daty. Tohle je ta tichá
   chyba, kterou nikdo nevidí, dokud data nejsou na GitHubu.
"""

import json
import re
import subprocess
import sys

for proud in (sys.stdout, sys.stderr):
    try:
        proud.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# --- Nevratné příkazy ------------------------------------------------------

ZAKAZANE = [
    (re.compile(r"\bgit\s+add\b[^|;&]*\s(-f|--force)\b"),
     "git add -f obchází .gitignore. Ten soubor tam nemá být schválně."),
    (re.compile(r"\bgit\s+push\b[^|;&]*\s(-f|--force|--force-with-lease)\b"),
     "git push --force přepíše historii na serveru. To musíš udělat ručně."),
    (re.compile(r"\bgit\s+reset\b[^|;&]*\s--hard\b"),
     "git reset --hard zahodí rozdělanou práci bez možnosti návratu."),
    (re.compile(r"\bgit\s+clean\b[^|;&]*\s[-a-zA-Z]*f"),
     "git clean -f maže nesledované soubory natrvalo."),
    (re.compile(r"\brm\s+-rf\s+[/~]\S*"),
     "rm -rf na kořen nebo na domovskou složku."),
]

# --- Složky, které nikdy nemají jít do commitu -----------------------------

CITLIVE_CESTY = re.compile(
    r"(^|/)(data|klient|klienti|podklady|_spis[^/]*|secrets)(/|$)"
    r"|(^|/)\.env(\.|$)"
    r"|\.(pem|key|sqlite|db)$"
)


def zkontroluj_index(cwd: str) -> list:
    """Vrátí seznam souborů v indexu, které vypadají jako data, ne jako kód."""
    try:
        vysledek = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            cwd=cwd or None,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return []

    if vysledek.returncode != 0:
        return []

    return [
        radek.strip()
        for radek in vysledek.stdout.splitlines()
        if radek.strip() and CITLIVE_CESTY.search(radek.strip())
    ]


def main() -> int:
    try:
        udalost = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    prikaz = str((udalost.get("tool_input") or {}).get("command", "") or "")
    if not prikaz:
        return 0

    for vzor, duvod in ZAKAZANE:
        if vzor.search(prikaz):
            print(
                f"PŘÍKAZ ZASTAVEN: {duvod}\n"
                f"Příkaz byl: {prikaz.strip()[:200]}\n\n"
                "Když to opravdu chceš, spusť si to sám v terminálu. "
                "Agent nevratné operace nedělá.",
                file=sys.stderr,
            )
            return 2

    if re.search(r"\bgit\s+commit\b", prikaz):
        podezrele = zkontroluj_index(udalost.get("cwd", ""))
        if podezrele:
            seznam = "\n".join(f"  - {c}" for c in podezrele[:15])
            print(
                "COMMIT ZASTAVEN — v indexu jsou soubory, které vypadají "
                "jako data, ne jako kód:\n"
                f"{seznam}\n\n"
                "Udělej tohle:\n"
                "1. `git restore --staged <soubor>` je vyndá z commitu.\n"
                "2. Přidej složku do .gitignore.\n"
                "3. Teprve pak commitni znovu.",
                file=sys.stderr,
            )
            return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
