# Kde končí nález a začíná šum

Kontrola, která najde třicet věcí, se přestane číst. Kontrola, která najde
tři a všechny tři jsou pravda, se čte pokaždé. Tenhle soubor je o té hranici.

## Test, který každý nález musí projít

Nález je jen to, na co se dá odpovědět na obě otázky:

1. **Co se stane, když se to neudělá?** Musí to jít napsat jako věta
   o důsledku, ne jako popis technického stavu.
2. **Co konkrétně se má udělat?** Musí to být jeden krok, ne směr.

Když první odpověď zní „bylo by to hezčí" nebo druhá „přepsat to lépe",
není to nález.

## Příklady

| Situace | Nález? | Proč |
|---|---|---|
| `data/leads.db` je sledovaný gitem | **ano, kritické** | při pushnutí jdou kontakty ven |
| Repozitář nemá vzdálený server | **ano, vážné** | ztráta disku = ztráta historie |
| Automat běží na plánovači a chyby jen mlčky přeskočí | **ano, vážné** | devět dní běží naprázdno a nikdo neví |
| Cesta `C:\projekty\neco` je zapsaná ve skriptu | **ano** | přesun složky to utne |
| STAV.md tvrdí „čeká se na X", X je hotové tři týdny | **ano** | posílá tě to špatným směrem |
| Funkce nemá typové anotace | ne | nikoho to dnes nestojí nic |
| Testy pokrývají 40 % kódu | ne | číslo bez důsledku |
| README by mohl být podrobnější | ne | není z toho krok |
| `node_modules` není zálohované | ne | dá se obnovit příkazem |
| Kód by šel zkrátit | ne | to je vkus, ne riziko |

## Závažnost podle času, ne podle pocitu

Neptej se „jak je to zlé". Ptej se **„jak dlouho by to bylo rozbité, než
by si toho někdo všiml"** a **„kolik to stojí, když se to stane"**.

- **Kritické** — už se to děje, nebo se to stane při nejbližším běžném
  úkonu (push, spuštění úlohy). Náklad je nevratný: data venku, ztracená
  historie, klient bez odpovědi.
- **Vážné** — stane se to při jedné konkrétní nešťastné události, která
  je pravděpodobná do půl roku. Ztráta disku, přesun složky, výpadek sítě.
- **K zvážení** — vypadá to špatně, ale nemáš důkaz. Vždycky napiš, čím
  se pochybnost odstraní.

## Duplicity

Jeden problém na pěti místech je jeden nález s pěti výskyty, ne pět nálezů.
Napiš ho jednou a přilož seznam cest. Report se tím zkrátí na třetinu.

## Co se nehlásí nikdy

- Obsah datových a klientských složek. Ani jako ukázka, ani jako důkaz.
- Nález, který si sám nedokážeš ověřit. Radši ho vynech, než abys ho
  napsal s domněnkou — jeden vymyšlený nález zabije důvěru ve všechny
  ostatní.
- Věci, na které si uživatel už třikrát řekl, že je nechce řešit. Ty patří
  do knihy jako vyřešené, ne do reportu.
