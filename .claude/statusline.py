#!/usr/bin/env python3
"""Stavový řádek: model, větev a kolik projektů v dílně čeká na pozornost.

Claude Code pošle na stdin JSON o sezení a vezme první řádek stdoutu.
Musí to být rychlé — spouští se to při každé změně obrazovky, takže
nepouštíme nic, co by mohlo trvat déle než zlomek vteřiny.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def vetev(slozka: str) -> str:
    try:
        vysledek = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=slozka or None,
            capture_output=True,
            text=True,
            timeout=2,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    if vysledek.returncode != 0:
        return ""
    return vysledek.stdout.strip()


def ceka_na_pozornost(projekt: str) -> int:
    """Kolik podsložek dílny nemá STAV.md. Levná verze session hooku."""
    root = os.environ.get("DILNA_ROOT") or str(Path(projekt) / "priklad")
    cesta = Path(root)
    if not cesta.is_dir():
        return 0
    pocet = 0
    for polozka in cesta.iterdir():
        if polozka.is_dir() and not polozka.name.startswith("."):
            if not (polozka / "STAV.md").exists():
                pocet += 1
    return pocet


def main() -> None:
    try:
        udalost = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        udalost = {}

    model = (udalost.get("model") or {}).get("display_name", "?")
    prostor = udalost.get("workspace") or {}
    aktualni = prostor.get("current_dir") or os.getcwd()
    projekt = prostor.get("project_dir") or aktualni

    casti = [model, Path(aktualni).name]

    v = vetev(aktualni)
    if v:
        casti.append(v)

    if not (Path(projekt) / "CLAUDE.md").exists():
        casti.append("bez CLAUDE.md")

    ceka = ceka_na_pozornost(projekt)
    if ceka:
        casti.append(f"{ceka} bez STAV.md")

    print(" | ".join(casti))


if __name__ == "__main__":
    main()
