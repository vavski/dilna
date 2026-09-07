# Kniha nálezů

Historie kontrol v `.dilna/kniha.db`. Pracuje se s ní přes MCP server
`kniha` (sqlite). Bez historie je kontrola jen fotka; s ní je vidět, jestli
se dílna zlepšuje nebo zhoršuje.

## Založení

Když tabulka neexistuje, spusť:

```sql
CREATE TABLE IF NOT EXISTS nalezy (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  bezel       TEXT NOT NULL,          -- datum běhu, RRRR-MM-DD
  projekt     TEXT NOT NULL,
  druh        TEXT NOT NULL,          -- stav | udaje | zaloha | krehkost
  zavaznost   TEXT NOT NULL,          -- kriticke | vazne | k_zvazeni
  popis       TEXT NOT NULL,          -- jedna věta, bez osobních údajů
  otisk       TEXT NOT NULL,          -- druh + projekt + zkrácený popis
  vyreseno    TEXT                    -- datum, kdy nález zmizel
);

CREATE INDEX IF NOT EXISTS nalezy_otisk ON nalezy (otisk);
CREATE INDEX IF NOT EXISTS nalezy_bezel ON nalezy (bezel);
```

`otisk` je to, podle čeho se nález pozná mezi běhy. Skládá se z druhu,
projektu a prvních čtyřiceti znaků popisu bez čísel a dat — jinak by se
stejný problém tvářil pokaždé jako nový.

## Do popisu nepatří osobní údaje

Kniha přežije jednotlivý běh a nikdo ji nečistí. Do sloupce `popis` píšeš
`rodné číslo v souboru seznam.csv`, nikdy samotné číslo. Platí i pro
e-maily, jména a spisové značky.

## Dotazy, které se hodí

**Nálezy, které tu jsou nejmíň tři běhy a nikdo je neřeší:**

```sql
SELECT projekt, druh, popis, COUNT(*) AS beho, MIN(bezel) AS poprve
FROM nalezy
WHERE vyreseno IS NULL
GROUP BY otisk
HAVING beho >= 3
ORDER BY poprve;
```

Tohle nejsou nálezy, ale rozhodnutí. Zeptej se, jestli mají z kontroly
zmizet, a když ano, zapiš jim `vyreseno` s poznámkou.

**Co zmizelo od minulé kontroly:**

```sql
SELECT projekt, popis FROM nalezy
WHERE otisk NOT IN (SELECT otisk FROM nalezy WHERE bezel = :dnes)
  AND bezel = (SELECT MAX(bezel) FROM nalezy WHERE bezel < :dnes)
  AND vyreseno IS NULL;
```

Těmhle nastav `vyreseno` na dnešní datum a v reportu je uveď jako hotové.

**Jak se dílna vyvíjí:**

```sql
SELECT bezel,
       SUM(zavaznost = 'kriticke') AS kriticke,
       SUM(zavaznost = 'vazne')    AS vazne,
       COUNT(*)                    AS celkem
FROM nalezy
GROUP BY bezel
ORDER BY bezel DESC
LIMIT 12;
```

**Nejhorší projekt:**

```sql
SELECT projekt, COUNT(*) AS otevrenych
FROM nalezy
WHERE vyreseno IS NULL
GROUP BY projekt
ORDER BY otevrenych DESC
LIMIT 5;
```

## Úklid

Nálezy s `vyreseno` staršími než rok smaž. Kniha má sloužit rozhodování,
ne archivaci.
