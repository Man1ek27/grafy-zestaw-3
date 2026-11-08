"""Macierz odległości między wszystkimi parami wierzchołków (zadanie 3)."""

from networkx import Graph

from .dijkstra import dijkstra


def distance_matrix(graph: Graph) -> list[list[float]]:
    """Wiersz s − 1 to tablica ds z dijkstra(G, w, s) dla kolejnych s = 1..n.

    Element [w − 1][k − 1] to długość najkrótszej ścieżki z w do k.
    """
    rows = []
    for s in sorted(graph.nodes()):
        ds, _ = dijkstra(graph, s)
        rows.append([ds[v] for v in sorted(graph.nodes())])
    return rows
