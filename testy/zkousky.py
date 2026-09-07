#!/usr/bin/env python3
"""Zkousky nastaveni dilny. Spust z korene repozitare:

    python testy/zkousky.py

Prochazi hooky, stavovy radek, skener osobnich udaju a MCP server
kniha. Nekontroluje subagenty - ti potrebuji bezici Claude Code
a jejich odpoved se pokazde lisi.

Navratovy kod 0 = vse proslo, 1 = neco selhalo.
"""

import json
import subprocess
import sys
from pathlib import Path

KOREN = Path(__file__).resolve().parent.parent
PYTHON = sys.executable

selhani = []


def spust(prikaz, vstup=""):
    """Pusti prikaz s danym vstupem a vrati (kod, stdout, stderr)."""
    vysledek = subprocess.run(
        prikaz,
        cwd=KOREN,
        input=vstup.encode("utf-8"),
        capture_output=True,
        timeout=60,
    )
    return (
        vysledek.returncode,
        vysledek.stdout.decode("utf-8", errors="replace"),
        vysledek.stderr.decode("utf-8", errors="replace"),
    )


def zkouska(nazev, podminka, podrobnosti=""):
    if podminka:
        print(f"  PROSLO   {nazev}")
    else:
        print(f"  SELHALO  {nazev}")
        if podrobnosti:
            print(f"           {podrobnosti}")
        selhani.append(nazev)


def hook(jmeno, udalost):
    cesta = KOREN / ".claude" / "hooks" / jmeno
    return spust([PYTHON, str(cesta)], json.dumps(udalost, ensure_ascii=False))


# --- Hook na osobni udaje --------------------------------------------------

print("\nHook osobni_udaje.py")

kod, _, _ = hook("osobni_udaje.py", {
    "tool_input": {"file_path": "a.md", "content": "Emil Fiala, 691128/7788"}
})
zkouska("rodne cislo zastavi zapis", kod == 2, f"vratil {kod}, cekal 2")

kod, _, _ = hook("osobni_udaje.py", {
    "tool_input": {"file_path": "a.md", "content": "faktura 202599/2026"}
})
zkouska("cislo faktury projde", kod == 0, f"vratil {kod}, cekal 0")

kod, _, _ = hook("osobni_udaje.py", {
    "tool_input": {"file_path": "priklad/x.csv", "content": "691128/7788"}
})
zkouska("vzorek pod priklad/ projde", kod == 0, f"vratil {kod}, cekal 0")

kod, _, chyba = hook("osobni_udaje.py", {
    "tool_input": {"file_path": "a.md", "content": "CZ1234567890"}
})
zkouska("DIC zastavi zapis", kod == 2, f"vratil {kod}, cekal 2")


# --- Hook na git -----------------------------------------------------------

print("\nHook git_ochrana.py")

for prikaz in ("git add -f data/x.db", "git push --force", "git reset --hard"):
    kod, _, _ = hook("git_ochrana.py", {"tool_input": {"command": prikaz},
                                        "cwd": str(KOREN)})
    zkouska(f"zastavi `{prikaz}`", kod == 2, f"vratil {kod}, cekal 2")

kod, _, _ = hook("git_ochrana.py", {"tool_input": {"command": "git status"},
                                    "cwd": str(KOREN)})
zkouska("pusti `git status`", kod == 0, f"vratil {kod}, cekal 0")

kod, _, chyba = spust([PYTHON, str(KOREN / ".claude/hooks/git_ochrana.py")],
                      "tohle neni json")
zkouska("nesrozumitelny vstup pusti dal, ale nahlas",
        kod == 0 and "nerozumel" in chyba,
        f"vratil {kod}, stderr: {chyba.strip()[:60]}")


# --- Zacatek sezeni a stavovy radek ----------------------------------------

print("\nSezeni a stavovy radek")

kod, vystup, _ = hook("stav_pripominka.py", {"source": "startup"})
zkouska("najde ve vzorku zpozdeny STAV.md",
        "fakturace" in vystup, f"vystup: {vystup.strip()[:80]}")
zkouska("najde projekt bez STAV.md", "newsletter" in vystup)
zkouska("najde datovou slozku mimo .gitignore",
        "fakturace/data" in vystup)

kod, vystup, _ = spust(
    [PYTHON, str(KOREN / ".claude/statusline.py")],
    json.dumps({"model": {"display_name": "Zkouska"},
                "workspace": {"current_dir": str(KOREN),
                              "project_dir": str(KOREN)}}),
)
zkouska("stavovy radek vypise model", "Zkouska" in vystup,
        f"vystup: {vystup.strip()[:60]}")


# --- Skener osobnich udaju -------------------------------------------------

print("\nSkener osobnich udaju")

skener = str(KOREN / ".claude/skills/anonymizace/scripts/najdi_udaje.py")

kod, vystup, _ = spust([PYTHON, skener, "priklad"])
zkouska("vzorek bez --vse nic nehlasi", kod == 0,
        f"vratil {kod}, cekal 0")

kod, vystup, _ = spust([PYTHON, skener, "priklad", "--vse", "--json"])
try:
    nalezy = json.loads(vystup)
except json.JSONDecodeError:
    nalezy = []
druhy = {n["druh"] for n in nalezy}
zkouska("s --vse najde ctyri druhy udaju", len(druhy) == 4, f"nasel: {druhy}")
zkouska("kazdy nalez je zamaskovany",
        all("*" in n["ukazka"] for n in nalezy))
# Tentyz udaj nesmi vyjit jednou jako rodne cislo a podruhe jako cislo
# uctu. Dvakrat tyz udaj na jednom radku pod jednim jmenem naopak
# spravne je - napriklad e-mail v odkazu i ve viditelnem textu.
podle_hodnoty = {}
for n in nalezy:
    klic = (n["soubor"], n["radek"], n["ukazka"])
    podle_hodnoty.setdefault(klic, set()).add(n["druh"])
sporne = {k: v for k, v in podle_hodnoty.items() if len(v) > 1}
zkouska("tentyz udaj nevyjde pod dvema jmeny", not sporne,
        f"sporne: {list(sporne.items())[:2]}")


# --- MCP server kniha ------------------------------------------------------

print("\nMCP server kniha")

zpravy = "\n".join([
    json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                "params": {"protocolVersion": "2025-06-18",
                           "capabilities": {}}}),
    json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}),
    json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}),
    json.dumps({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                "params": {"name": "zapis_nalez", "arguments": {
                    "projekt": "zkouska", "druh": "vymysleny",
                    "zavaznost": "kriticke", "popis": "x"}}}),
])

db = KOREN / ".dilna" / "zkousky.db"
kod, vystup, _ = spust(
    [PYTHON, str(KOREN / ".claude/mcp/kniha.py"), "--db", str(db)], zpravy
)
odpovedi = {}
for radek in vystup.splitlines():
    try:
        z = json.loads(radek)
        odpovedi[z.get("id")] = z
    except json.JSONDecodeError:
        pass

zkouska("odpovi na initialize", 1 in odpovedi,
        f"odpovedi na: {sorted(k for k in odpovedi if k is not None)}")
zkouska("nabizi pet nastroju",
        len(odpovedi.get(2, {}).get("result", {}).get("tools", [])) == 5)
zkouska("odmitne neplatny druh nalezu",
        odpovedi.get(3, {}).get("result", {}).get("isError") is True)

db.unlink(missing_ok=True)


# --- Zaver -----------------------------------------------------------------

print()
if selhani:
    print(f"SELHALO {len(selhani)} zkousek:")
    for s in selhani:
        print(f"  - {s}")
    sys.exit(1)

print("Vsechny zkousky prosly.")
sys.exit(0)