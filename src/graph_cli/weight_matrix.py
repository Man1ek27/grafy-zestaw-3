"""Macierz wag: wczytywanie i zapis grafu ważonego.

Format jak macierz sąsiedztwa z zestawu 1, ale zamiast 1 stoi waga krawędzi,
a 0 oznacza brak krawędzi.
"""

from networkx import Graph


def format_matrix(rows: list[list[int]]) -> str:
    """Wiersze macierzy z kolumnami wyrównanymi do najszerszej liczby."""
    width = max((len(str(x)) for row in rows for x in row), default=1)
    return "".join(" ".join(f"{x:>{width}}" for x in row) + "\n" for row in rows)


def weight_rows(graph: Graph) -> list[list[int]]:
    """Macierz wag jako lista wierszy; w[u - 1][v - 1] to waga krawędzi uv."""
    n = graph.number_of_nodes()
    rows = [[0] * n for _ in range(n)]
    for u, v, weight in graph.edges(data="weight"):
        rows[u - 1][v - 1] = weight
        rows[v - 1][u - 1] = weight
    return rows


def serialize_weight_matrix(graph: Graph) -> str:
    """Pierwsza linia: liczba wierzchołków n, potem n wierszy macierzy wag."""
    return f"{graph.number_of_nodes()}\n" + format_matrix(weight_rows(graph))


def parse_weight_matrix(text: str) -> Graph:
    """Wczytuje graf z macierzy wag (odwrotność serialize_weight_matrix)."""
    lines = text.splitlines()
    if not lines:
        raise ValueError("Plik z macierzą wag jest pusty.")

    n = int(lines[0])
    if n < 1:
        raise ValueError("Liczba wierzchołków musi być dodatnia.")
    matrix = [list(map(int, line.split())) for line in lines[1:]]
    if len(matrix) != n or any(len(row) != n for row in matrix):
        raise ValueError(f"Macierz musi mieć rozmiar {n}x{n}.")

    for i in range(n):
        if matrix[i][i] != 0:
            raise ValueError("Graf prosty nie może mieć pętli.")
        for j in range(n):
            if matrix[i][j] < 0:
                raise ValueError("Wagi krawędzi nie mogą być ujemne.")
            if matrix[i][j] != matrix[j][i]:
                raise ValueError("Macierz musi być symetryczna.")

    graph = Graph()
    graph.add_nodes_from(range(1, n + 1))
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] > 0:
                graph.add_edge(i + 1, j + 1, weight=matrix[i][j])
    return graph
