"""Rozešle newsletter odběratelům. Běží každé úterý na plánovači.

Ukázkový kód se třemi křehkými místy, která má najít agent
`krehka-mista`. Neopravuj je, dokud si vzorek nevyzkoušíš:

  1. cesta natvrdo — po přesunu složky přestane fungovat
  2. prázdný except — chyba odesílání zmizí beze stopy
  3. žádná kontrola, jestli už dnes běželo — dvojí spuštění pošle
     odběratelům dva stejné e-maily
"""

import csv
import smtplib
from email.mime.text import MIMEText

SEZNAM = r"C:\dilna\newsletter\data\odberatele.csv"
SERVER = "smtp.example.com"


def nacti_prijemce():
    with open(SEZNAM, encoding="utf-8") as f:
        return [radek["email"] for radek in csv.DictReader(f, delimiter=";")]


def rozeslat(predmet, telo):
    server = smtplib.SMTP(SERVER)
    odeslano = 0

    for prijemce in nacti_prijemce():
        try:
            zprava = MIMEText(telo, "plain", "utf-8")
            zprava["Subject"] = predmet
            zprava["To"] = prijemce
            server.send_message(zprava)
            odeslano += 1
        except Exception:
            pass

    server.quit()
    return odeslano


if __name__ == "__main__":
    rozeslat("Novinky", "Text newsletteru.")
