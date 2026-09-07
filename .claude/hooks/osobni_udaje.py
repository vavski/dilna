#!/usr/bin/env python3
"""PreToolUse hook: zastaví zápis osobních údajů do souborů.

Claude Code pošle na stdin JSON o chystaném volání nástroje Write/Edit.
Když v zapisovaném obsahu najdeme české rodné číslo, DIČ nebo IBAN,
vrátíme kód 2 — Claude Code zápis neprovede a text ze stderru
dostane model jako vysvětlení, proč to neprošlo.

Návratové kódy:
  0 = v pořádku, pokračuj
  2 = zablokovat volání nástroje
"""

import json
import re
import sys
from pathlib import Path

# Aby čeština nerozbila výstup na Windows konzoli.
for proud in (sys.stdout, sys.stderr):
    try:
        proud.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# --- Vzory -----------------------------------------------------------------

RODNE_CISLO = re.compile(r"\b(\d{2})(\d{2})(\d{2})\s?/\s?(\d{3,4})\b")
DIC = re.compile(r"\bCZ\d{8,10}\b")
IBAN_CZ = re.compile(r"\bCZ\d{2}(?:\s?\d{4}){5}\b")

# Složky, kde je nález očekávaný — ukázkový vzorek pro demo a testy.
VYJIMKY = ("priklad/", "priklad\\", "/priklad/", "\\priklad\\")


def je_platne_rodne_cislo(shoda: re.Match) -> bool:
    """Odfiltruje čísla faktur a verzí, které jen vypadají jako rodné číslo.

    Nekontrolujeme dělitelnost jedenácti — u čísel vydaných do roku 1954
    neplatí a falešně negativní nález je tu horší než falešně pozitivní.
    Stačí nám, že prostředních šest číslic dává smysl jako datum.
    """
    mesic = int(shoda.group(2))
    den = int(shoda.group(3))
    # Ženám se k měsíci přičítá 50, od roku 2004 se při vyčerpání
    # kapacity dne přičítá dalších 20.
    if mesic > 50:
        mesic -= 50
    if mesic > 20:
        mesic -= 20
    return 1 <= mesic <= 12 and 1 <= den <= 31


def posbirej_text(vstup: dict) -> str:
    """Vytáhne všechen text, který se chystá zapsat, bez ohledu na nástroj."""
    kusy = [
        vstup.get("content", ""),
        vstup.get("new_string", ""),
    ]
    for uprava in vstup.get("edits", []) or []:
        kusy.append(uprava.get("new_string", ""))
    return "\n".join(k for k in kusy if isinstance(k, str))


def nacti_udalost():
    """Precte udalost ze stdin. Vrati None, kdyz ji nerozumime.

    Vstup se cte binarne a cisti od znacky kodovani - nektera prostredi
    ji na zacatek prilepi a `json` na ni spadne. Hook, ktery kvuli tomu
    tise pusti volani dal, prestane hlidat a nikdo si toho nevsimne.
    Proto se to aspon napise do stderru, kde to je videt.
    """
    syrove = sys.stdin.buffer.read()
    try:
        text = syrove.decode("utf-8", errors="replace").lstrip("\ufeff")
        return json.loads(text)
    except json.JSONDecodeError as potiz:
        sys.stderr.write("hook nerozumel vstupu a pousti volani dal: "
                         + str(potiz) + "\n")
        return None


def main() -> int:
    udalost = nacti_udalost()
    if udalost is None:
        return 0

    vstup = udalost.get("tool_input", {}) or {}
    cesta = str(vstup.get("file_path", "") or "")

    normalizovana = cesta.replace("\\", "/")
    if any(v.replace("\\", "/") in normalizovana for v in VYJIMKY):
        return 0

    text = posbirej_text(vstup)
    if not text:
        return 0

    nalezy = []

    for shoda in RODNE_CISLO.finditer(text):
        if je_platne_rodne_cislo(shoda):
            nalezy.append(f"rodné číslo ({shoda.group(0)})")

    if DIC.search(text):
        nalezy.append(f"DIČ ({DIC.search(text).group(0)})")

    if IBAN_CZ.search(text):
        nalezy.append("číslo účtu ve formátu IBAN")

    if not nalezy:
        return 0

    soubor = Path(cesta).name or "soubor"
    print(
        "ZÁPIS ZASTAVEN — v obsahu jsou osobní údaje.\n"
        f"Soubor: {soubor}\n"
        f"Nalezeno: {', '.join(dict.fromkeys(nalezy))}\n\n"
        "Než to zkusíš znovu:\n"
        "1. Nahraď údaj smyšleným (rodné číslo 900101/1234 je vymyšlené a bezpečné).\n"
        "2. Pokud jde o skutečná data, patří do složky, která je v .gitignore, "
        "ne do kódu ani do testů.\n"
        "3. Do ukázkových dat pod priklad/ tenhle hook nezasahuje.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
