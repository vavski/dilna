#!/usr/bin/env python3
"""SessionStart hook: na začátku sezení řekne, které projekty hnijí.

Nic nemění a na nic se neptá. Jen se podívá na složky v dílně a vypíše
tři věci, které se špatně hledají ručně:

  - projekt, kde se pracovalo, ale STAV.md se od té doby nesáhl
  - projekt, který STAV.md vůbec nemá
  - složka s daty, kterou nekryje žádný .gitignore

Výstup na stdout dostane model jako kontext prvního tahu.
"""

import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

for proud in (sys.stdout, sys.stderr):
    try:
        proud.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

DEN = 86400
PRAH_DNU = 14  # o kolik smí být STAV.md pozadu, než to stojí za zmínku

IGNOROVAT = {".git", ".claude", ".dilna", "node_modules", "__pycache__",
             ".venv", "venv", "dist", "build", ".pytest_cache"}

DATOVE_SLOZKY = {"data", "klient", "klienti", "podklady", "secrets"}


def koren() -> Path:
    """Kde dílna leží. Bez nastavení se použije ukázkový vzorek v repu."""
    z_prostredi = os.environ.get("DILNA_ROOT")
    if z_prostredi:
        return Path(z_prostredi).expanduser()

    projekt = os.environ.get("CLAUDE_PROJECT_DIR") or "."
    return Path(projekt) / "priklad"


HLAVICKA_DATA = re.compile(
    r"Aktualizov[aá]no:\s*(\d{1,2})\.\s*(\d{1,2})\.\s*(\d{4})"
)


def datum_z_hlavicky(stav: Path) -> float:
    """Datum z řádku `*Aktualizováno: 2. 6. 2026*` jako čas v sekundách.

    Čas změny souboru se při klonování repozitáře ztratí — všechno má
    najednou stejné stáří. Datum napsané v hlavičce přežije, takže se
    na něj díváme taky a bereme to horší z obou.
    """
    try:
        zacatek = stav.read_text(encoding="utf-8", errors="replace")[:400]
    except OSError:
        return 0.0

    shoda = HLAVICKA_DATA.search(zacatek)
    if not shoda:
        return 0.0

    den, mesic, rok = (int(c) for c in shoda.groups())
    try:
        return datetime(rok, mesic, den).timestamp()
    except ValueError:
        return 0.0


def nacti_gitignore(soubor: Path) -> set:
    """Vrátí názvy složek, které .gitignore skutečně kryje.

    Hledat název složky jako podřetězec celého souboru nestačí — slovo
    `data` se najde i ve větě „chybí tu pravidlo pro data". Proto se
    komentáře zahazují a bere se jen samotné pravidlo.
    """
    if not soubor.exists():
        return set()

    try:
        obsah = soubor.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return set()

    kryje = set()
    for radek in obsah.splitlines():
        radek = radek.split("#", 1)[0].strip()
        if not radek or radek.startswith("!"):
            continue
        kryje.add(radek.strip("/").lstrip("*").strip("/"))
    return kryje


def nejnovejsi_soubor(slozka: Path) -> float:
    """Čas poslední změny čehokoliv v projektu, mimo služební složky."""
    nejnovejsi = 0.0
    for cesta, podslozky, soubory in os.walk(slozka):
        podslozky[:] = [p for p in podslozky if p not in IGNOROVAT]
        for soubor in soubory:
            if soubor == "STAV.md":
                continue
            try:
                cas = (Path(cesta) / soubor).stat().st_mtime
            except OSError:
                continue
            nejnovejsi = max(nejnovejsi, cas)
    return nejnovejsi


def main() -> int:
    root = koren()
    if not root.is_dir():
        return 0

    ted = time.time()
    zpozdene, bez_stavu, nekryta_data = [], [], []

    for projekt in sorted(p for p in root.iterdir() if p.is_dir()):
        if projekt.name in IGNOROVAT or projekt.name.startswith("."):
            continue

        stav = projekt / "STAV.md"
        posledni_prace = nejnovejsi_soubor(projekt)

        if not stav.exists():
            if posledni_prace:
                bez_stavu.append(projekt.name)
        else:
            try:
                stav_cas = stav.stat().st_mtime
            except OSError:
                stav_cas = ted

            z_hlavicky = datum_z_hlavicky(stav)
            if z_hlavicky:
                stav_cas = min(stav_cas, z_hlavicky)

            rozdil = max(posledni_prace, ted if z_hlavicky else 0) - stav_cas
            if rozdil > PRAH_DNU * DEN:
                zpozdene.append((projekt.name, int(rozdil // DEN)))

        pravidla = nacti_gitignore(projekt / ".gitignore")
        for podslozka in projekt.iterdir():
            if podslozka.is_dir() and podslozka.name in DATOVE_SLOZKY:
                if podslozka.name not in pravidla:
                    nekryta_data.append(f"{projekt.name}/{podslozka.name}")

    if not (zpozdene or bez_stavu or nekryta_data):
        return 0

    radky = [f"Stav dílny ({root}):"]

    if zpozdene:
        radky.append("STAV.md je pozadu za skutečnou prací:")
        radky += [f"  - {jmeno} (o {dnu} dnů)" for jmeno, dnu in zpozdene]

    if bez_stavu:
        radky.append("Bez STAV.md: " + ", ".join(bez_stavu))

    if nekryta_data:
        radky.append("Datová složka bez pravidla v .gitignore:")
        radky += [f"  - {cesta}" for cesta in nekryta_data]

    radky.append(
        "Tohle je jen upozornění. Nic neopravuj, dokud o to uživatel neřekne."
    )

    print("\n".join(radky))
    return 0


if __name__ == "__main__":
    sys.exit(main())
