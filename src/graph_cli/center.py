"""Centrum grafu i centrum minimax na podstawie macierzy odległości (zadanie 4).

Obie funkcje zwracają parę (numer wierzchołka, wartość). Przy remisie
wybierany jest wierzchołek o najmniejszym numerze.
"""


def graph_center(dist: list[list[float]]) -> tuple[int, float]:
    """Wierzchołek o najmniejszej sumie odległości do pozostałych."""
    sums = [sum(row) for row in dist]
    best = sums.index(min(sums))
    return best + 1, sums[best]


def minimax_center(dist: list[list[float]]) -> tuple[int, float]:
    """Wierzchołek o najmniejszej odległości do najdalszego wierzchołka."""
    farthest = [max(row) for row in dist]
    best = farthest.index(min(farthest))
    return best + 1, farthest[best]
