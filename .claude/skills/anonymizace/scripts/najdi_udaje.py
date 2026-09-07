#!/usr/bin/env python3
"""Projde soubory a vypíše, kde jsou české osobní údaje.

Nic nemění. Výstup je seznam nálezů, nad kterým se rozhoduje ručně.

Použití:
    python najdi_udaje.py <cesta> [--vse] [--json]

    --vse   vypíše i nálezy, které vypadají jako smyšlené
    --json  strojově čitelný výstup

Návratové kódy:
    0 = nic nenalezeno
    1 = nálezy jsou
    2 = chyba vstupu
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

PRESKOCIT_SLOZKY = {
    ".git", "node_modules", "__pycache__", ".venv", "venv",
    "dist", "build", ".pytest_cache", ".mypy_cache", ".idea", ".vscode",
}

TEXTOVE_PRIPONY = {
    ".txt", ".md", ".csv", ".tsv", ".json", ".yaml", ".yml", ".xml",
    ".html", ".htm", ".py", ".js", ".ts", ".jsx", ".tsx", ".sql",
    ".sh", ".ps1", ".ini", ".cfg", ".toml", ".env", ".log", ".rst",
}

MAX_VELIKOST = 5 * 1024 * 1024  # větší soubor bude spíš binárka nebo dump

# Pořadí je zároveň pořadím přednosti. Když dva vzory sednou na stejné
# místo v řádku, vyhraje ten dřívější — jinak by se `900101/1234` hlásilo
# jednou jako rodné číslo a podruhé jako číslo účtu.
VZORY = [
    ("klíč nebo token", re.compile(
        r"\b(sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{12,})\b"
        r"|-----BEGIN [A-Z ]*PRIVATE KEY-----"
    )),
    ("rodné číslo", re.compile(r"\b(\d{2})(\d{2})(\d{2})\s?/\s?(\d{3,4})\b")),
    ("IBAN", re.compile(r"\bCZ\d{2}(?:\s?\d{4}){5}\b")),
    ("DIČ", re.compile(r"\bCZ\d{8,10}\b")),
    ("číslo účtu", re.compile(r"\b\d{1,6}-?\d{2,10}/\d{4}\b")),
    ("spisová značka", re.compile(r"\b\d{1,3}\s?[A-Z]{1,3}\s?\d{1,4}/\d{4}\b")),
    ("e-mail", re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]{2,}\b")),
    ("telefon", re.compile(r"(?:\+420[\s-]?)?\b\d{3}[\s-]?\d{3}[\s-]?\d{3}\b")),
]

# Devítimístné číslo je v českém textu příliš běžné — bez předvolby nebo
# bez slova v okolí by telefon utopil report v šumu.
TELEFON_KONTEXT = re.compile(r"(tel|mobil|kontakt|telefon|gsm)", re.IGNORECASE)

# Co skoro jistě není skutečný údaj.
ZJEVNE_SMYSLENE = re.compile(
    r"example\.(com|org|net)|@test\.|@localhost|"
    r"jmeno\.prijmeni|foo|bar|lorem|xxx|000\s?000\s?000|"
    r"900101/1234|123456789/0100",
    re.IGNORECASE,
)

SMYSLENE_SLOZKY = re.compile(r"(^|[/\\])(priklad|priklady|fixtures?|tests?|"
                             r"testdata|samples?|ukazk[ay])([/\\]|$)",
                             re.IGNORECASE)


def datum_dava_smysl(shoda: re.Match) -> bool:
    """Odfiltruje faktury a verze, které mají tvar rodného čísla."""
    mesic, den = int(shoda.group(2)), int(shoda.group(3))
    if mesic > 50:
        mesic -= 50
    if mesic > 20:
        mesic -= 20
    return 1 <= mesic <= 12 and 1 <= den <= 31


def je_telefon(radek: str, shoda: re.Match) -> bool:
    """Devítimístné číslo je telefon jen s předvolbou nebo s kontextem."""
    if shoda.group(0).lstrip().startswith("+"):
        return True
    okoli = radek[max(0, shoda.start() - 25):shoda.start()]
    return bool(TELEFON_KONTEXT.search(okoli))


def zamaskuj(text: str) -> str:
    """Nález se vypisuje zkrácený — report se taky někam ukládá."""
    if len(text) <= 4:
        return "*" * len(text)
    return f"{text[:3]}{'*' * (len(text) - 4)}{text[-1]}"


def projdi_soubor(cesta: Path, v_smyslene_slozce: bool) -> list:
    try:
        if cesta.stat().st_size > MAX_VELIKOST:
            return []
        obsah = cesta.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []

    nalezy = []
    for cislo, radek in enumerate(obsah.splitlines(), start=1):
        obsazeno = []  # rozsahy, které už si vzal specifičtější vzor

        for druh, vzor in VZORY:
            for shoda in vzor.finditer(radek):
                zacatek, konec = shoda.span()

                if any(zacatek < k and z < konec for z, k in obsazeno):
                    continue

                if druh == "rodné číslo" and not datum_dava_smysl(shoda):
                    continue

                if druh == "telefon" and not je_telefon(radek, shoda):
                    continue

                obsazeno.append((zacatek, konec))
                nalezy.append({
                    "soubor": str(cesta),
                    "radek": cislo,
                    "druh": druh,
                    "ukazka": zamaskuj(shoda.group(0)),
                    "vypada_smyslene": bool(
                        v_smyslene_slozce
                        or ZJEVNE_SMYSLENE.search(shoda.group(0))
                    ),
                })
    return nalezy


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cesta", help="soubor nebo složka")
    parser.add_argument("--vse", action="store_true",
                        help="vypsat i zjevně smyšlené údaje")
    parser.add_argument("--json", action="store_true",
                        help="strojově čitelný výstup")
    argumenty = parser.parse_args()

    koren = Path(argumenty.cesta)
    if not koren.exists():
        print(f"Cesta `{koren}` neexistuje.", file=sys.stderr)
        return 2

    soubory = []
    if koren.is_file():
        soubory = [koren]
    else:
        for cesta in koren.rglob("*"):
            if not cesta.is_file():
                continue
            if any(cast in PRESKOCIT_SLOZKY for cast in cesta.parts):
                continue
            if cesta.suffix.lower() in TEXTOVE_PRIPONY or not cesta.suffix:
                soubory.append(cesta)

    nalezy = []
    for soubor in soubory:
        v_smyslene = bool(SMYSLENE_SLOZKY.search(str(soubor)))
        nalezy.extend(projdi_soubor(soubor, v_smyslene))

    if not argumenty.vse:
        nalezy = [n for n in nalezy if not n["vypada_smyslene"]]

    if argumenty.json:
        print(json.dumps(nalezy, ensure_ascii=False, indent=2))
        return 1 if nalezy else 0

    if not nalezy:
        print(f"Prošlo {len(soubory)} souborů, nic k nahrazení.")
        return 0

    podle_druhu = {}
    for nalez in nalezy:
        podle_druhu.setdefault(nalez["druh"], []).append(nalez)

    print(f"Prošlo {len(soubory)} souborů, {len(nalezy)} nálezů.\n")
    for druh in sorted(podle_druhu, key=lambda d: -len(podle_druhu[d])):
        polozky = podle_druhu[druh]
        print(f"{druh} ({len(polozky)}×)")
        for nalez in polozky[:20]:
            znacka = " [vypadá smyšleně]" if nalez["vypada_smyslene"] else ""
            print(f"  {nalez['soubor']}:{nalez['radek']}  "
                  f"{nalez['ukazka']}{znacka}")
        if len(polozky) > 20:
            print(f"  … a dalších {len(polozky) - 20}")
        print()

    return 1


if __name__ == "__main__":
    sys.exit(main())
