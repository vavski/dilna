"""Načte odběratele a spočítá, co komu vyfakturovat.

Ukázkový kód. Generování PDF chybí schválně — projekt je rozdělaný,
protože takhle vypadá většina projektů v dílně.
"""

import csv
from pathlib import Path

SOUBOR = Path(__file__).parent / "data" / "odberatele.csv"


def nacti_odberatele():
    with SOUBOR.open(encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))


def spocitej_celkem(odberatele):
    return sum(int(o["castka"]) for o in odberatele)


if __name__ == "__main__":
    odberatele = nacti_odberatele()
    print(f"Odběratelů: {len(odberatele)}")
    print(f"Celkem k fakturaci: {spocitej_celkem(odberatele)} Kč")
