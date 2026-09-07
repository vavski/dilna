---
name: kontrola-dilny
description: Projde všechny projekty v dílně a vrátí jeden report — co hnije, co není zazálohované, kde utíkají osobní údaje a co se rozbije, až to poběží samo. Použij při „zkontroluj dílnu", „projdi projekty", „co mi hnije", při nedělní kontrole a vždycky před tím, než se něco pushne veřejně. Neopravuje, jen zjišťuje.
---

# Kontrola dílny

Dílna je složka, ve které leží vedle sebe víc malých projektů. Každý z nich
je malý dost na to, aby se na něj zapomnělo, a jich je dohromady tolik, že
je ručně neprojdeš. Tahle kontrola to udělá za tebe.

**Nic neopravuje.** Výstupem je report a seznam kroků. Opravuje se až na
samostatný pokyn.

## Než začneš

Zjisti kořen dílny v tomhle pořadí:

1. cesta, kterou uživatel napsal v zadání
2. proměnná prostředí `DILNA_ROOT`
3. složka `priklad/` v tomhle projektu (ukázkový vzorek)

Když v kořeni nejsou žádné podsložky, řekni to a skonči. Nehádej.

## Postup

Udělej si na každý z pěti kroků položku v seznamu úkolů.

### 1. Sestav seznam projektů

Jedna podsložka = jeden projekt. Přeskoč `.git`, `.claude`, `.dilna`,
`node_modules`, `.venv` a vše, co začíná tečkou.

U každého projektu si poznamenej: název, jestli je to git repozitář,
datum posledního commitu, datum poslední změny souborů.

### 2. Rozešli specialisty

Na každý projekt pusť **čtyři agenty najednou v jedné zprávě**, ať běží
souběžně a ne za sebou:

| Agent | Na co se ptá |
|---|---|
| `revizor-stavu` | Rozešel se STAV.md se skutečností? |
| `hlidac-udaju` | Odešly by osobní údaje při pushnutí? |
| `zalohar` | Co zmizí, když shoří disk? |
| `krehka-mista` | Co se rozbije, až to poběží bez dozoru? |

U projektů, kde je jasné, že nemají co běžet samo (jen dokumenty, žádný
kód), `krehka-mista` vynech. Šetři, kde to nic nestojí.

**Nikdy nespouštěj `krehka-mista` a `hlidac-udaju` na složky, které jsou
podle `.gitignore` datové.** Data se nekontrolují, data se chrání — obsah
klientských složek do kontextu agenta nepatří.

### 3. Porovnej s minulým během

Kniha nálezů v `.dilna/kniha.db` si pamatuje minulé běhy. Zavolej
`pretrvavajici` a `zmizele` — zajímají tě dvě věci:

- **Nález, který přetrvává.** Když je stejný nález ve třech běhech po sobě,
  není to nález, ale rozhodnutí. Označ ho a zeptej se, jestli má zmizet
  z kontroly.
- **Nález, který zmizel.** Zapiš do reportu jako hotovou věc, ať je vidět
  pohyb.

Když se server `kniha` nepřipojí, tenhle krok přeskoč a napiš do
reportu jednou větou, že porovnání s minulými běhy chybí. Kvůli knize
kontrolu nezastavuj.

### 4. Nech to sepsat

Předej všechny nálezy agentovi `pisar`. Dej mu je celé — nepředžvýkávej je,
od toho je on. Report píše pro člověka, který není vývojář.

### 5. Zapiš nálezy do knihy

Na každý nález zavolej `zapis_nalez`. Do popisu piš jednu větu
**bez osobních údajů** — kniha přežije jednotlivý běh a nikdo ji nečistí.
Bez tohohle kroku nebude příště fungovat krok 3.

## Co dělá tuhle kontrolu užitečnou

Ne počet nálezů. Užitečná je tím, že **rozdělí věci na dnes a na potom**.
Když z toho vyjde seznam dvaceti položek bez pořadí, kontrola selhala,
i kdyby byl každý nález pravdivý.

Když nálezů vyjde přes deset, do reportu jdou tři nejvážnější a zbytek
jedním řádkem. Zbytek zůstane v knize a vyplave příští týden.

## Časté chyby

- **Spouštět agenty postupně.** Čtyři projekty krát čtyři agenti postupně
  je hodina čekání. Naráz jsou to minuty.
- **Opravovat během kontroly.** Kontrola zjišťuje. Oprava je jiný úkol
  s jiným rozpočtem a s jiným rizikem.
- **Číst obsah datových složek.** Tomu se vyhýbáš i za cenu horšího nálezu.
- **Hlásit balast.** `node_modules` bez zálohy není nález.

## Další čtení

- `references/kniha.md` — nástroje knihy nálezů a co do nich patří
- `references/co-je-nalez.md` — hranice mezi nálezem a šumem

