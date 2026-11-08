# Graph CLI — Zestaw 3

Aplikacja CLI w Pythonie do pracy z grafami ważonymi: losowanie spójnego grafu
z wagami 1–10, najkrótsze ścieżki algorytmem Dijkstry, macierz odległości,
centrum i centrum minimax oraz minimalne drzewo rozpinające (algorytm Kruskala).
Wierzchołki są numerowane od 1 do n.

NetworkX przechowuje wierzchołki, krawędzie i wagi; wszystkie algorytmy z zadań
zaimplementowano samodzielnie. Matplotlib zapisuje rysunki PNG.

**Kod z poprzednich zestawów:** `generators.py` (G(n,l) i G(n,p) z zestawu 1),
`components.py` (spójne składowe z zestawu 2 — tylko `components`,
`components_r`, `is_connected`), `__main__.py`, `scripts/fix_local_import.py`
i konfiguracja projektu są przeniesione bez zmian w logice. Z zestawu 2 pochodzi
też budowa CLI (`build_parser`, `COMMANDS`, `main`, `write_text`, zapis ścieżki
`[1 - 2 - 3]`), a `visualization.py` zamiast kolorów składowych i cyklu rysuje
wagi krawędzi i wyróżnione krawędzie (drzewo).

## 1. Przygotowanie środowiska

Wymagania: Python 3.10 lub nowszy. Git jest potrzebny do commitów i hooków.

```bash
git clone https://github.com/Man1ek27/grafy-zestaw-3.git
cd grafy-zestaw-3
```

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
pre-commit install
```

Windows (Git Bash): `source .venv/Scripts/activate` zamiast `Activate.ps1`.

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
pre-commit install
```

Instalacja dodaje komendę `graph-cli`, biblioteki NetworkX i Matplotlib oraz
narzędzia developerskie Ruff, pre-commit i pytest. Jeżeli na macOS wystąpi
`ModuleNotFoundError: No module named 'graph_cli'`, wykonaj
`.venv/bin/python scripts/fix_local_import.py` (opis w README zestawu 1).

Alternatywne uruchomienie aplikacji: `python -m graph_cli`.

## 2. Dane wejściowe

Zgodnie z przykładowym wejściem zestawu 3 jedno uruchomienie pracuje na jednym
grafie. Polecenia 2–5 przyjmują go na jeden z dwóch sposobów:

- `--n N` — losowy spójny graf z wagami z zadania 1. Domyślnie model G(n,p)
  z `--probability 0.5`; `--edges L` wybiera model G(n,l). `--seed` pozwala
  odtworzyć losowanie (ten sam graf i te same wagi);
- `--input PLIK` — macierz wag (format w [docs/formats.md](docs/formats.md));
  graf musi być spójny.

Przykłady w `examples/`:

| Plik           | Opis                                                        |
| -------------- | ----------------------------------------------------------- |
| `slides-7.txt` | graf z 7 wierzchołkami ze slajdów do zestawu 3              |
| `input-12.txt` | graf z rys. 1 w przykładowym wejściu zestawu 3 (`input_3.pdf`) |

Wyniki programu dla obu plików są identyczne z wynikami w materiałach
(listingi 1–3 i rys. 2 z `input_3.pdf`, tabele ze slajdów).

## 3. Wywołania CLI

Pomoc: `graph-cli --help`, `graph-cli dijkstra --help` itd.

`--plot PLIK.png` zapisuje rysunek, a `--show` (wymaga `--plot`) otwiera okno.
`--output PLIK` zapisuje macierz wag, którą można później podać jako `--input`.

### Zadanie 1: spójny graf losowy z wagami

```bash
graph-cli random --n 8 --seed 1 --plot output/z1.png --output output/z1.txt
graph-cli random --n 12 --edges 19 --seed 3
```

```text
Spójny graf losowy: n = 8, m = 11
Macierz wag (0 — brak krawędzi):
0 0 0 0 0 5 0 0
0 0 0 0 0 2 8 0
...
```

Na rysunku przy każdej krawędzi jest jej waga.

### Zadanie 2: algorytm Dijkstry

```bash
graph-cli dijkstra --input examples/slides-7.txt --plot output/z2.png
graph-cli dijkstra --input examples/input-12.txt --start 5
graph-cli dijkstra --n 6 --seed 2
```

```text
START: s = 1
d(1) = 0  ==> [1]
d(2) = 6  ==> [1 - 7 - 2]
d(3) = 11 ==> [1 - 5 - 6 - 3]
d(4) = 8  ==> [1 - 7 - 2 - 4]
d(5) = 3  ==> [1 - 5]
d(6) = 7  ==> [1 - 5 - 6]
d(7) = 5  ==> [1 - 7]
```

`--start` (domyślnie 1) wybiera wierzchołek startowy. Dla grafu losowego
program najpierw wypisuje wylosowaną macierz wag. Na rysunku pogrubione są
krawędzie wszystkich najkrótszych ścieżek z s (drzewo poprzedników ps).

### Zadanie 3: macierz odległości

```bash
graph-cli distances --input examples/slides-7.txt
```

```text
Macierz odległości:
 0  6 11  8  3  7  5
 6  0 12  2  4  8  1
...
```

Element w wierszu w i kolumnie k to długość najkrótszej ścieżki z w do k.

### Zadanie 4: centrum i centrum minimax

```bash
graph-cli center --input examples/input-12.txt
```

```text
Centrum = 5 (suma odległości: 55)
Centrum minimax = 8 (odległość od najdalszego: 9)
```

Przy remisie wypisywany jest wierzchołek o najmniejszym numerze.

### Zadanie 5: minimalne drzewo rozpinające

```bash
graph-cli mst --input examples/slides-7.txt --plot output/z5.png
```

```text
Krawędzie drzewa w kolejności dodawania (algorytm Kruskala):
(2, 7)  waga 1
(2, 4)  waga 2
(1, 5)  waga 3
(2, 5)  waga 4
(3, 6)  waga 4
(5, 6)  waga 4
Suma wag: 18
```

Na rysunku krawędzie drzewa są grube i niebieskie, pozostałe szare (jak rys. 2
w przykładowym wejściu).

### Wszystkie zadania na jednym grafie

```bash
graph-cli all --n 12 --edges 19 --seed 3 --output output/all.txt --plot output/all.png
graph-cli all --input examples/input-12.txt --start 1
```

Wypisuje kolejno sekcje `=== Zadanie 1 ===` … `=== Zadanie 5 ===`; rysunek
pokazuje graf z wagami i wyróżnionym minimalnym drzewem rozpinającym.

Sukces kończy program kodem 0; błędy danych lub plików (np. graf niespójny,
nieistniejący wierzchołek startowy) kodem 1; błędne argumenty CLI kodem 2.
Komunikaty błędów trafiają na stderr.

## 4. Funkcje w kolejności wywoływania

### Wspólny początek

1. `main(argv=None)` w `cli.py` jest punktem wejścia komendy `graph-cli`.
2. `build_parser()` tworzy parser argparse; `add_graph_arguments()`,
   `add_random_arguments()`, `add_start_argument()` i `add_plot_arguments()`
   dodają wspólne opcje.
3. `main()` sprawdza zależność `--show` od `--plot` i wywołuje funkcję
   `run_*` z tablicy `COMMANDS`. `ValueError` i `OSError` kończą program kodem 1.
4. `load_graph(args)` przygotowuje graf: `parse_weight_matrix()` i
   `is_connected()` dla `--input` albo `random_connected_graph()` dla `--n`.
   `print_random_graph()` wypisuje graf, jeśli był losowany.

### random (zad. 1)

`run_random()` → `random_connected_graph(n, probability, edges, seed)`
w `random_graph.py`: w pętli `generate_gnp()` albo `generate_gnl()` z zestawu 1
i `is_connected()` z zestawu 2, aż graf wyjdzie spójny; potem
`assign_random_weights()`. Następnie `print_graph()`,
`serialize_weight_matrix()` + `write_text()` dla `--output` i `draw_graph()`.

### dijkstra (zad. 2)

`run_dijkstra()` → `dijkstra(graph, s)` w `dijkstra.py`: `init()`, a potem
w pętli wybór niegotowego wierzchołka o najmniejszym ds i `relax()` dla jego
niegotowych sąsiadów. `print_paths()` dla każdego v wywołuje
`shortest_path(ps, s, v)` i `format_path()`.

### distances (zad. 3)

`run_distances()` → `distance_matrix(graph)` w `distances.py`, która wywołuje
`dijkstra()` z każdego wierzchołka. Wynik wypisuje `format_matrix()`.

### center (zad. 4)

`run_center()` → `distance_matrix()` → `print_centers()`, która wywołuje
`graph_center()` i `minimax_center()` z `center.py`.

### mst (zad. 5)

`run_mst()` → `kruskal(graph)` w `mst.py`: sortowanie krawędzi po wagach
i dla każdej krawędzi `components()` z zestawu 2 na budowanym lesie.
Potem `print_mst()` i `draw_graph(..., highlight=krawędzie drzewa)`.

### all (zad. 1–5)

`run_all()` → `load_graph()` i kolejno funkcje z punktów powyżej na tym samym
grafie.

## 5. Formatowanie i testy

Ruff automatycznie formatuje pliki Pythona przy `git commit`.

```bash
ruff format .
ruff format --check .
pytest
```

Testy w `tests/` sprawdzają wyniki ze slajdów i z przykładowego wejścia
zestawu 3 (listingi 1–3, drzewo z rys. 2), porównują Dijkstrę, macierz
odległości i wagę drzewa z gotowymi algorytmami NetworkX na losowych grafach
oraz przypadki brzegowe: graf z jednym wierzchołkiem, remisy, wierzchołek
nieosiągalny, graf niespójny, błędne pliki i argumenty.

## 6. Zakres i ograniczenia

- Wybór wierzchołka o najmniejszym ds przegląda wszystkie niegotowe
  wierzchołki (bez kopca), więc Dijkstra działa w O(n² + m) — jak na slajdach.
- Kruskal sprawdza „czy krawędź łączy różne drzewa” funkcją `components()`
  z zestawu 2. To proste do wytłumaczenia, ale wolniejsze od struktury
  union-find; dla grafów z zadania w zupełności wystarcza.
- Graf jest losowany ponownie, dopóki nie wyjdzie spójny (najwyżej 1000 prób).
  Dla G(n,l) z l < n − 1 graf spójny nie istnieje — program od razu zgłasza błąd.
- Jeśli kilka wierzchołków jest centrum (albo kilka ścieżek ma tę samą długość),
  program podaje jeden wynik: wierzchołek o najmniejszym numerze, a ze ścieżek
  tę, którą algorytm znalazł pierwszą.

Opis algorytmów i złożoności: [docs/algorithms.md](docs/algorithms.md).
Formaty wejścia i wyjścia: [docs/formats.md](docs/formats.md).
