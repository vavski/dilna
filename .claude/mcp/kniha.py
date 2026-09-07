#!/usr/bin/env python3
"""MCP server: kniha nalezu z kontrol dilny.

Drzi historii toho, co kontrola nasla, aby slo poznat dve veci, ktere
z jednoho behu videt nejsou: nalez, ktery tu visi potreti (a je to tedy
rozhodnuti, ne nalez), a nalez, ktery zmizel (coz je jedine misto, kde
je videt pohyb).

Postavene na SQLite a na standardni knihovne. Zadna zavislost, takze
nema co prestat fungovat pri aktualizaci neceho jineho - mluvi JSON-RPC
pres stdin a stdout primo.

Pouziti (spousti Claude Code podle .mcp.json):
    python .claude/mcp/kniha.py --db .dilna/kniha.db
"""

import argparse
import json
import re
import sqlite3
import sys
from datetime import date
from pathlib import Path

VERZE_PROTOKOLU = "2025-06-18"
JMENO = "kniha"

ZAVAZNOSTI = ("kriticke", "vazne", "k_zvazeni")
DRUHY = ("stav", "udaje", "zaloha", "krehkost")


# --- Databaze --------------------------------------------------------------

SCHEMA = """
CREATE TABLE IF NOT EXISTS nalezy (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  bezel     TEXT NOT NULL,
  projekt   TEXT NOT NULL,
  druh      TEXT NOT NULL,
  zavaznost TEXT NOT NULL,
  popis     TEXT NOT NULL,
  otisk     TEXT NOT NULL,
  vyreseno  TEXT
);
CREATE INDEX IF NOT EXISTS nalezy_otisk ON nalezy (otisk);
CREATE INDEX IF NOT EXISTS nalezy_bezel ON nalezy (bezel);
"""


def otevri(cesta: Path) -> sqlite3.Connection:
    cesta.parent.mkdir(parents=True, exist_ok=True)
    spojeni = sqlite3.connect(cesta)
    spojeni.row_factory = sqlite3.Row
    spojeni.executescript(SCHEMA)
    spojeni.commit()
    return spojeni


def spocitej_otisk(druh: str, projekt: str, popis: str) -> str:
    """Podle ceho se pozna, ze jde o tentyz nalez jako minule.

    Cisla a data se z popisu vyhazuji - jinak by se stejny problem
    tvaril pokazde jako novy jen proto, ze se posunul radek v souboru.
    """
    holy = re.sub(r"\d+", "", popis.lower())
    holy = re.sub(r"\s+", " ", holy).strip()[:40]
    return druh + "|" + projekt + "|" + holy


# --- Nastroje --------------------------------------------------------------

def zapis_nalez(db, projekt, druh, zavaznost, popis, bezel=None):
    if druh not in DRUHY:
        raise ValueError("druh musi byt jeden z " + str(DRUHY))
    if zavaznost not in ZAVAZNOSTI:
        raise ValueError("zavaznost musi byt jedna z " + str(ZAVAZNOSTI))

    bezel = bezel or date.today().isoformat()
    otisk = spocitej_otisk(druh, projekt, popis)
    db.execute(
        "INSERT INTO nalezy (bezel, projekt, druh, zavaznost, popis, otisk) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (bezel, projekt, druh, zavaznost, popis, otisk),
    )
    db.commit()
    return {"zapsano": True, "otisk": otisk, "bezel": bezel}


def pretrvavajici(db, min_behu=3):
    radky = db.execute(
        "SELECT projekt, druh, popis, COUNT(DISTINCT bezel) AS behu, "
        "       MIN(bezel) AS poprve, otisk "
        "FROM nalezy WHERE vyreseno IS NULL "
        "GROUP BY otisk HAVING behu >= ? ORDER BY poprve",
        (min_behu,),
    ).fetchall()
    return {
        "poznamka": "Nalez, ktery tu je ponekolikate, neni nalez, ale "
                    "rozhodnuti. Zeptej se, jestli ma z kontroly zmizet.",
        "nalezy": [dict(r) for r in radky],
    }


def zmizele(db, bezel=None):
    """Nalezy z minuleho behu, ktere v tomhle behu uz nejsou."""
    dnes = bezel or date.today().isoformat()
    minuly = db.execute(
        "SELECT MAX(bezel) AS b FROM nalezy WHERE bezel < ?", (dnes,)
    ).fetchone()["b"]

    if not minuly:
        return {"minuly_beh": None, "zmizele": []}

    radky = db.execute(
        "SELECT projekt, druh, popis, otisk FROM nalezy "
        "WHERE bezel = ? AND vyreseno IS NULL AND otisk NOT IN "
        "  (SELECT otisk FROM nalezy WHERE bezel = ?)",
        (minuly, dnes),
    ).fetchall()
    return {"minuly_beh": minuly, "zmizele": [dict(r) for r in radky]}


def oznac_vyreseno(db, otisk, kdy=None):
    kdy = kdy or date.today().isoformat()
    kurzor = db.execute(
        "UPDATE nalezy SET vyreseno = ? WHERE otisk = ? AND vyreseno IS NULL",
        (kdy, otisk),
    )
    db.commit()
    return {"oznaceno": kurzor.rowcount, "kdy": kdy}


def vyvoj(db, limit=12):
    radky = db.execute(
        "SELECT bezel, "
        "  SUM(zavaznost = 'kriticke') AS kriticke, "
        "  SUM(zavaznost = 'vazne')    AS vazne, "
        "  COUNT(*)                    AS celkem "
        "FROM nalezy GROUP BY bezel ORDER BY bezel DESC LIMIT ?",
        (limit,),
    ).fetchall()
    return {"behy": [dict(r) for r in radky]}


NASTROJE = [
    {
        "name": "zapis_nalez",
        "description": (
            "Zapise jeden nalez z kontroly. Do popisu nikdy nepis osobni "
            "udaje - kniha prezije jednotlivy beh a nikdo ji necisti. "
            "Pis `rodne cislo v souboru seznam.csv`, ne samotne cislo."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "projekt": {"type": "string"},
                "druh": {"type": "string", "enum": list(DRUHY)},
                "zavaznost": {"type": "string", "enum": list(ZAVAZNOSTI)},
                "popis": {"type": "string",
                          "description": "jedna veta, bez osobnich udaju"},
                "bezel": {"type": "string",
                          "description": "datum behu RRRR-MM-DD, vychozi dnes"},
            },
            "required": ["projekt", "druh", "zavaznost", "popis"],
        },
        "fn": zapis_nalez,
    },
    {
        "name": "pretrvavajici",
        "description": (
            "Nalezy, ktere se opakuji ve vic bezich a nikdo je neresi. "
            "Tohle nejsou nalezy, ale rozhodnuti - patri ven z kontroly."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {"min_behu": {"type": "integer", "default": 3}},
        },
        "fn": pretrvavajici,
    },
    {
        "name": "zmizele",
        "description": (
            "Co bylo v minulem behu a v tomhle uz neni. Patri do reportu "
            "jako hotova vec - je to jedine misto, kde je videt pohyb."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "bezel": {"type": "string",
                          "description": "datum tohoto behu, vychozi dnes"},
            },
        },
        "fn": zmizele,
    },
    {
        "name": "oznac_vyreseno",
        "description": "Oznaci nalez za vyreseny, aby se priste nehlasil.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "otisk": {"type": "string"},
                "kdy": {"type": "string", "description": "RRRR-MM-DD"},
            },
            "required": ["otisk"],
        },
        "fn": oznac_vyreseno,
    },
    {
        "name": "vyvoj",
        "description": "Pocty nalezu po bezich. Ukaze, jestli se dilna "
                       "zlepsuje nebo zhorsuje.",
        "inputSchema": {
            "type": "object",
            "properties": {"limit": {"type": "integer", "default": 12}},
        },
        "fn": vyvoj,
    },
]

PODLE_JMENA = {n["name"]: n for n in NASTROJE}


# --- Protokol --------------------------------------------------------------

def odpoved(id_zpravy, vysledek):
    return {"jsonrpc": "2.0", "id": id_zpravy, "result": vysledek}


def chyba(id_zpravy, kod, zprava):
    return {"jsonrpc": "2.0", "id": id_zpravy,
            "error": {"code": kod, "message": zprava}}


def zpracuj(zprava, db):
    """Vrati odpoved, nebo None u oznameni, na ktera se neodpovida."""
    metoda = zprava.get("method")
    id_zpravy = zprava.get("id")

    if metoda == "initialize":
        klient = zprava.get("params", {}).get("protocolVersion")
        return odpoved(id_zpravy, {
            "protocolVersion": klient or VERZE_PROTOKOLU,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": JMENO, "version": "1.0.0"},
        })

    if metoda in ("notifications/initialized", "notifications/cancelled"):
        return None

    if metoda == "ping":
        return odpoved(id_zpravy, {})

    if metoda == "tools/list":
        return odpoved(id_zpravy, {
            "tools": [
                {k: v for k, v in n.items() if k != "fn"} for n in NASTROJE
            ]
        })

    if metoda == "tools/call":
        parametry = zprava.get("params", {}) or {}
        jmeno = parametry.get("name")
        nastroj = PODLE_JMENA.get(jmeno)

        if not nastroj:
            return chyba(id_zpravy, -32601, "Nastroj neznam: " + str(jmeno))

        try:
            vysledek = nastroj["fn"](db, **(parametry.get("arguments") or {}))
            text = json.dumps(vysledek, ensure_ascii=False, indent=2)
            return odpoved(id_zpravy, {
                "content": [{"type": "text", "text": text}]
            })
        except Exception as potiz:
            # Chybu vracime jako obsah, ne jako selhani protokolu - model
            # se z ni pak muze poucit a zavolat nastroj spravne.
            return odpoved(id_zpravy, {
                "content": [{"type": "text", "text": "Chyba: " + str(potiz)}],
                "isError": True,
            })

    if id_zpravy is None:
        return None
    return chyba(id_zpravy, -32601, "Metodu neznam: " + str(metoda))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=".dilna/kniha.db")
    argumenty = parser.parse_args()

    # Vstup se cte binarne a dekoduje rucne. Prepnuti kodovani na
    # sys.stdin zahodi, co uz je ve vyrovnavaci pameti, a prvni zprava
    # protokolu se tim ztrati - klient pak ceka na odpoved, ktera
    # nikdy neprijde. Vystup prepnout lze, ten se jeste necetl.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    db = otevri(Path(argumenty.db))

    for syrovy in sys.stdin.buffer:
        # Znacka kodovani na zacatku prvni zpravy se musi odstranit,
        # jinak se prvni radek neda rozparsovat a klient ceka na
        # odpoved, ktera nikdy neprijde. Nektere prostredi ji posila.
        radek = syrovy.decode("utf-8", errors="replace").lstrip("\ufeff").strip()
        if not radek:
            continue

        try:
            zprava = json.loads(radek)
        except json.JSONDecodeError as potiz:
            # Nerozumime radku. Mlcet by znamenalo, ze klient ceka
            # navzdy - radeji to napiseme do stderru, kde to je videt.
            sys.stderr.write("nerozumim zprave: " + str(potiz) + "\n")
            sys.stderr.flush()
            continue

        vysledek = zpracuj(zprava, db)
        if vysledek is not None:
            sys.stdout.write(json.dumps(vysledek, ensure_ascii=False) + "\n")
            sys.stdout.flush()

    return 0


if __name__ == "__main__":
    sys.exit(main())



