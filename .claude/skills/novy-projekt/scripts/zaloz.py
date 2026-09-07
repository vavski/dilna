#!/usr/bin/env python3
"""Založí nový projekt v dílně se všemi soubory, které má mít od začátku.

Použití:
    python zaloz.py nazev --popis "K čemu to je" [--data data] [--kde CESTA]

Nic nepřepisuje. Když složka existuje, skončí chybou a nesáhne na nic.
"""

import argparse
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

PLATNY_NAZEV = re.compile(r"^[a-z0-9][a-z0-9_-]{1,48}$")

ZAKLADNI_GITIGNORE = """# Prostředí a závislosti
.venv/
venv/
node_modules/
__pycache__/
*.pyc

# Klíče a přístupy — tohle ven nesmí nikdy
.env
.env.*
*.pem
*.key
credentials.json
token.json
client_secret*.json

# Výstupy a dočasné soubory
dist/
build/
*.log
.DS_Store
Thumbs.db
"""


def dnes_cesky() -> str:
    """Datum ve tvaru `7. 9. 2026`. Ručně, protože %-d na Windows není."""
    d = date.today()
    return f"{d.day}. {d.month}. {d.year}"


def stav_md(nazev: str, popis: str) -> str:
    return f"""# {nazev} — stav

*Aktualizováno: {dnes_cesky()}*

## Co stavíme

{popis}

## Co funguje dnes

Nic. Projekt právě vznikl.

## Co zbývá

- Rozhodnout, jestli to má vůbec smysl stavět.

## Čeká se na

Nic.

## Čemu nevěřit

Zatím není čemu — v projektu není žádný kód.
"""


def claude_md(nazev: str, popis: str, datova_slozka: str | None) -> str:
    zakaz = [
        "- Obcházet `.gitignore` přes `git add -f`.",
        "- Psát do kódu, do testů ani do komentářů skutečná jména a údaje. "
        "Používej smyšlená.",
    ]
    if datova_slozka:
        zakaz.insert(0, f"- Commitovat cokoliv ze složky `{datova_slozka}/`.")

    return f"""# {nazev}

{popis}

Stav projektu je v `STAV.md`. Popis pro člověka je v `README.md`.

## Co se tu nesmí

{chr(10).join(zakaz)}

## Co agent o projektu musí vědět

Zatím nic zvláštního. Doplň sem první věc, na kterou projekt narazí —
typicky vnější závislost, kterou nejde poznat z kódu.
"""


def readme(nazev: str, popis: str) -> str:
    return f"""# {nazev}

{popis}

## K čemu to je

*(Doplň, až bude co ukázat.)*

## Jak to spustit

*(Doplň.)*
"""


def spust_git(slozka: Path) -> str:
    """Založí repozitář a první commit. Vrátí popis výsledku pro výpis."""
    kroky = [
        ["git", "init", "--quiet"],
        ["git", "add", "."],
        ["git", "commit", "--quiet", "-m", "prazdny projekt"],
    ]
    for krok in kroky:
        vysledek = subprocess.run(
            krok, cwd=slozka, capture_output=True, text=True
        )
        if vysledek.returncode != 0:
            return f"git selhal na `{' '.join(krok)}`: {vysledek.stderr.strip()[:200]}"
    return "git založen, jeden commit"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("nazev", help="malá písmena, spojovníky místo mezer")
    parser.add_argument("--popis", required=True, help="jedna věta, k čemu to je")
    parser.add_argument(
        "--data",
        help="název složky s citlivými daty; půjde rovnou do .gitignore",
    )
    parser.add_argument(
        "--kde",
        default=".",
        help="kořen dílny (výchozí: aktuální složka)",
    )
    argumenty = parser.parse_args()

    if not PLATNY_NAZEV.match(argumenty.nazev):
        print(
            f"Název `{argumenty.nazev}` neprojde. Chci malá písmena, číslice, "
            "spojovník nebo podtržítko, 2 až 49 znaků.",
            file=sys.stderr,
        )
        return 1

    slozka = Path(argumenty.kde) / argumenty.nazev
    if slozka.exists():
        print(
            f"`{slozka}` už existuje. Nic jsem nepřepsal — vyber jiný název "
            "nebo tu složku nejdřív ukliď.",
            file=sys.stderr,
        )
        return 1

    slozka.mkdir(parents=True)

    ignorovat = ZAKLADNI_GITIGNORE
    if argumenty.data:
        ignorovat += (
            f"\n# Data projektu — do gitu nepatří\n{argumenty.data}/\n"
        )
        (slozka / argumenty.data).mkdir(exist_ok=True)
        (slozka / argumenty.data / ".gitkeep").write_text("", encoding="utf-8")

    soubory = {
        "STAV.md": stav_md(argumenty.nazev, argumenty.popis),
        "CLAUDE.md": claude_md(argumenty.nazev, argumenty.popis, argumenty.data),
        "README.md": readme(argumenty.nazev, argumenty.popis),
        ".gitignore": ignorovat,
    }
    for jmeno, obsah in soubory.items():
        (slozka / jmeno).write_text(obsah, encoding="utf-8")

    vysledek_gitu = spust_git(slozka)

    print(f"Založeno: {slozka}")
    for jmeno in soubory:
        print(f"  {jmeno}")
    if argumenty.data:
        print(f"  {argumenty.data}/ (v .gitignore)")
    print(f"  {vysledek_gitu}")
    print()
    print("Zbývá tobě:")
    print("  - založit vzdálený repozitář, když ho projekt má mít")
    print("  - přidat řádek do rozcestníku dílny")

    return 0


if __name__ == "__main__":
    sys.exit(main())
