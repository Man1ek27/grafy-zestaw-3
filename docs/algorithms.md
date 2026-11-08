# Algorytmy i złożoność

Opis dotyczy aktualnej implementacji. n oznacza liczbę wierzchołków,
m liczbę krawędzi, a w(u, v) wagę krawędzi uv. Wierzchołki mają numery 1..n.
Graf przechowuje `networkx.Graph` (krawędzie z atrybutem `weight`, sąsiedzi);
wszystkie algorytmy z zadań są zaimplementowane samodzielnie.

## 1. Spójny graf losowy z wagami — `random_graph.py`

`random_connected_graph(n, probability, edges, seed)` składa się z programów
z poprzednich zestawów:

1. Kontrola: n ≥ 1, a dla G(n,l) l ≥ n − 1 (mniej krawędzi nie da grafu spójnego).
2. Losuje graf `generate_gnp(n, p)` albo `generate_gnl(n, l)` z zestawu 1.
3. `is_connected()` z zestawu 2 — jeśli graf jest niespójny, losuje od nowa
   (najwyżej 1000 prób, potem `ValueError`).
4. `assign_random_weights()` — każdej krawędzi (w kolejności posortowanej)
   przypisuje `rng.randint(1, 10)`.

Jeden generator `random.Random(seed)` daje ziarna kolejnych prób i wagi,
więc to samo `--seed` zawsze odtwarza ten sam graf z tymi samymi wagami.

Czas jednej próby: O(n²) dla G(n,p) i G(n,l) + O(n + m log n) test spójności.

## 2. Algorytm Dijkstry — `dijkstra.py`

Funkcje odpowiadają algorytmom 1–3 z `alg_3.pdf`:

- `init(graph, s)` — ds[v] = ∞, ps[v] = NIL (`None`) dla każdego v, ds[s] = 0.
- `relax(u, v, graph, ds, ps)` — jeśli ds[v] > ds[u] + w(u, v), to
  ds[v] ← ds[u] + w(u, v) i ps[v] ← u.
- `dijkstra(graph, s)`:
  1. `init(G, s)`, zbiór gotowych S pusty.
  2. Dopóki S nie zawiera wszystkich wierzchołków: wybiera niegotowy u
     o najmniejszym ds[u] (przy remisie najmniejszy numer) i dodaje go do S.
  3. Relaksuje krawędzie do niegotowych sąsiadów u.

Po zakończeniu ds[v] to długość najkrótszej ścieżki s → v, a ps[v] — poprzednik v
na tej ścieżce. `shortest_path(ps, s, v)` idzie od v po poprzednikach aż do s
i odwraca listę; dla wierzchołka nieosiągalnego zwraca pustą listę.

Remisy: relaksacja zmienia ds tylko przy ostrej nierówności, więc z dwóch
ścieżek tej samej długości zostaje ta znaleziona pierwsza (np. dla grafu
z `input_3.pdf`: d(7) = 8 przez [1 - 2 - 4 - 7], a nie [1 - 2 - 5 - 7]).

Algorytm wymaga nieujemnych wag — funkcja odrzuca wagę ujemną (`ValueError`).

Czas: n razy wybór minimum przez przejrzenie niegotowych wierzchołków O(n)
i łącznie 2m relaksacji → O(n² + m) = O(n²) (jak na slajdzie 10).
Pamięć: O(n) na ds, ps i S.

## 3. Macierz odległości — `distances.py`

`distance_matrix(graph)` wywołuje `dijkstra(G, s)` kolejno dla s = 1..n
(slajd 12: „dijkstra(G, w, s = 1), dijkstra(G, w, s = 2), itd.”). Wiersz s − 1
to tablica ds. Macierz jest kwadratowa, ma zera na przekątnej i jest
symetryczna, bo graf jest nieskierowany.

Czas: n · O(n²) = O(n³). Pamięć: O(n²).

## 4. Centrum grafu — `center.py`

Obie funkcje korzystają z macierzy odległości (slajd 14):

- `graph_center(dist)` — dla każdego wierzchołka suma wiersza (suma odległości
  do pozostałych); centrum to wierzchołek o najmniejszej sumie.
- `minimax_center(dist)` — dla każdego wierzchołka maksimum wiersza (odległość
  do najdalszego); centrum minimax to wierzchołek o najmniejszym maksimum.

Przy remisie wybierany jest najmniejszy numer (`list.index(min(...))`).
Czas: O(n²) na przejrzenie macierzy.

## 5. Minimalne drzewo rozpinające — `mst.py`

`kruskal(graph)` realizuje algorytm Kruskala z `alg_3.pdf` (punkt 3.2):

1. Las T zawiera wszystkie wierzchołki i żadnej krawędzi.
2. Krawędzie są sortowane według niemalejących wag, przy remisie według
   numerów wierzchołków (jak tabela na slajdzie 21).
3. Dla kolejnych krawędzi uv: `components()` z zestawu 2 numeruje drzewa lasu T;
   jeśli u i v są w różnych drzewach, krawędź nie tworzy cyklu i trafia do T.
4. Koniec, gdy T ma n − 1 krawędzi. Jeśli krawędzie się skończą wcześniej,
   graf jest niespójny (`ValueError`).

Funkcja zwraca listę (u, v, waga) w kolejności dodawania.

Czas: sortowanie O(m log m) + najwyżej m wywołań `components()` na lesie
z co najwyżej n − 1 krawędziami, każde O(n log n) → O(m · n log n).
Wersja z union-find byłaby szybsza (O(m log m)), ale ponowne użycie
oznaczania składowych z zestawu 2 jest prostsze do wytłumaczenia.

## 6. Wizualizacja — `visualization.py`

Rozszerzenie `draw_graph()` z zestawu 2. Wierzchołek i (i = 0..n−1 w kolejności
numerów) ma pozycję:

```text
kąt = π/2 − 2πi/n
x = cos(kąt), y = sin(kąt)
```

Waga krawędzi uv (u < v) jest rysowana w punkcie u + 0,35 · (v − u) — na
środku (0,5) wszystkie średnice okręgu miałyby etykietę w tym samym miejscu.
`highlight` to lista krawędzi rysowanych grubą niebieską linią (drzewo
najkrótszych ścieżek albo minimalne drzewo rozpinające); pozostałe krawędzie
są wtedy szare. Przygotowanie rysunku: O(n log n + m).
