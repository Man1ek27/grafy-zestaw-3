# Formaty wejścia i wyjścia

Pliki mają kodowanie UTF-8. Wierzchołki są numerowane od 1 do n.
Graf jest nieskierowany, bez pętli i wielokrotnych krawędzi, a każda krawędź
ma dodatnią wagę całkowitą.

## Macierz wag (`--input`, `--output`)

Format jak macierz sąsiedztwa z zestawu 1, ale zamiast 1 stoi waga krawędzi.
Pierwsza linia zawiera liczbę wierzchołków n, potem n wierszy po n liczb:

- w[u][v] > 0 — krawędź uv o wadze w[u][v],
- w[u][v] = 0 — brak krawędzi.

Macierz musi być symetryczna, mieć zera na przekątnej i nieujemne wartości;
graf podany przez `--input` musi być spójny. Liczby oddziela dowolna liczba
spacji, więc wyrównane kolumny z `--output` można wczytać z powrotem.

```text
7
0 8 0 9 3 9 5
8 0 0 2 4 0 1
0 0 0 0 0 4 0
9 2 0 0 0 9 0
3 4 0 0 0 4 0
9 0 4 9 4 0 0
5 1 0 0 0 0 0
```

To jest plik `examples/slides-7.txt` — graf ze slajdów do zestawu 3.

## Wyjście tekstowe

- Graf (zad. 1) — nagłówek z n i m oraz macierz wag:

  ```text
  Graf: n = 7, m = 11
  Macierz wag (0 — brak krawędzi):
  ```

- Najkrótsze ścieżki (zad. 2) — jak listing 1 z `input_3.pdf`:

  ```text
  START: s = 1
  d(1) = 0  ==> [1]
  d(2) = 6  ==> [1 - 7 - 2]
  ```

- Macierz odległości (zad. 3) — n wierszy po n liczb, kolumny wyrównane.
- Centrum (zad. 4) — jak listing 3 z `input_3.pdf`:

  ```text
  Centrum = 5 (suma odległości: 30)
  Centrum minimax = 5 (odległość od najdalszego: 8)
  ```

- Minimalne drzewo rozpinające (zad. 5) — krawędzie `(u, v)  waga w`
  w kolejności dodawania i `Suma wag: …`.

## Rysunki PNG

- Wierzchołki leżą na okręgu, wierzchołek 1 u góry, kolejne zgodnie z ruchem
  wskazówek zegara (jak w zestawach 1 i 2).
- Waga krawędzi jest napisana na krawędzi, bliżej wierzchołka o mniejszym numerze
  (na środku etykiety wszystkich średnic okręgu nachodziłyby na siebie).
- `random` — wszystkie krawędzie czarne.
- `dijkstra` — pogrubione niebieskie krawędzie najkrótszych ścieżek z s,
  pozostałe szare.
- `mst` i `all` — pogrubione niebieskie krawędzie drzewa, pozostałe szare.

Katalogi wyjściowe są tworzone automatycznie; istniejące pliki są nadpisywane.
