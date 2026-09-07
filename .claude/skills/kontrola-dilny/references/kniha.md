# Kniha nálezů

Historie kontrol v `.dilna/kniha.db`. Pracuje se s ní přes MCP server
`kniha` — vlastní server v `.claude/mcp/kniha.py`. Bez historie je
kontrola fotka; s ní je vidět, jestli se dílna zlepšuje nebo zhoršuje.

Tabulku nezakládej ani nečisti ručně. Server si ji vytvoří sám při
prvním spuštění a nabízí pět nástrojů, které pokrývají všechno, co
kontrola potřebuje.

## Nástroje

### `zapis_nalez`

Jeden řádek na nález. Volá se v kroku 5 kontroly, na konci.

| Pole | Co tam patří |
|---|---|
| `projekt` | název složky projektu |
| `druh` | `stav`, `udaje`, `zaloha` nebo `krehkost` |
| `zavaznost` | `kriticke`, `vazne` nebo `k_zvazeni` |
| `popis` | jedna věta, **bez osobních údajů** |
| `bezel` | datum běhu `RRRR-MM-DD`, výchozí dnes |

Server sám spočítá otisk, podle kterého se nález pozná mezi běhy —
vyhodí z popisu čísla a zkrátí ho. Díky tomu se tentýž problém
nepovažuje za nový jen proto, že se posunul řádek v souboru.

Špatný `druh` nebo `zavaznost` server odmítne a napíše, co čekal.
Neobcházej to vymýšlením nových hodnot; když ti nějaká chybí, patří
to do skillu, ne do dat.

### `pretrvavajici`

Nálezy, které se opakují ve třech a víc bězích a nikdo je neřeší.
Volá se v kroku 3, před psaním reportu.

Tohle nejsou nálezy, ale rozhodnutí. Do reportu je nepiš znovu —
místo toho se zeptej, jestli mají z kontroly zmizet, a když ano,
zavolej `oznac_vyreseno`.

### `zmizele`

Co bylo v minulém běhu a v tomhle už není. Patří do reportu jako
hotová věc — je to jediné místo, kde je vidět pohyb. Bez toho vypadá
každá kontrola stejně marně, i když se pracuje.

### `oznac_vyreseno`

Označí nález za vyřešený, aby se příště nehlásil. Bere otisk, který
vrátil `zapis_nalez` nebo `pretrvavajici`.

Používej to na dvě věci: na nález, který skutečně zmizel, a na nález,
o kterém uživatel řekl, že ho řešit nebude.

### `vyvoj`

Počty nálezů po bězích, od nejnovějšího. Do reportu to nepatří pokaždé —
hodí se, když se někdo ptá, jestli to pouštění vůbec k něčemu je.

## Do popisu nepatří osobní údaje

Kniha přežije jednotlivý běh a nikdo ji nečistí. Píšeš
`rodné číslo v souboru seznam.csv`, nikdy samotné číslo. Platí i pro
e-maily, jména a spisové značky.

Server to za tebe nepohlídá. Je to jediné pravidlo téhle knihy, které
stojí jen na tobě.

## Když server nenaběhne

Kontrola má běžet i bez knihy. Když se `kniha` nepřipojí, přeskoč krok 3
a krok 5, napiš do reportu jednou větou, že porovnání s minulými běhy
chybí, a pokračuj. Nezastavuj kvůli tomu celou kontrolu.
