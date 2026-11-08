"""Najkrótsze ścieżki algorytmem Dijkstry (zadanie 2).

Funkcje init, relax i dijkstra odpowiadają algorytmom 1–3 z alg_3.pdf.
ds[v] — długość najkrótszej ścieżki z s do v (w trakcie: górne oszacowanie),
ps[v] — poprzednik v na tej ścieżce (None to NIL).
"""

import math

from networkx import Graph


def init(graph: Graph, s: int) -> tuple[dict[int, float], dict[int, int | None]]:
    """Algorytm 1: ds[v] = ∞ i ps[v] = NIL dla każdego v, a ds[s] = 0."""
    ds = {v: math.inf for v in graph.nodes()}
    ps = {v: None for v in graph.nodes()}
    ds[s] = 0
    return ds, ps


def relax(
    u: int, v: int, graph: Graph, ds: dict[int, float], ps: dict[int, int | None]
) -> None:
    """Algorytm 2: sprawdza, czy z s do v da się przejść krócej przez krawędź uv."""
    w = graph[u][v]["weight"]
    if ds[v] > ds[u] + w:
        ds[v] = ds[u] + w
        ps[v] = u


def dijkstra(graph: Graph, s: int) -> tuple[dict[int, float], dict[int, int | None]]:
    """Algorytm 3: zwraca tablice ds i ps dla wierzchołka startowego s.

    W każdym kroku wybiera „niegotowy” wierzchołek u o najmniejszym ds[u]
    (przy remisie najmniejszy numer), dodaje go do zbioru gotowych S
    i relaksuje krawędzie do jego niegotowych sąsiadów.
    """
    if s not in graph:
        raise ValueError(f"Wierzchołek startowy {s} nie istnieje w grafie.")
    if any(w < 0 for _, _, w in graph.edges(data="weight")):
        raise ValueError("Algorytm Dijkstry wymaga nieujemnych wag.")

    ds, ps = init(graph, s)
    ready = set()  # zbiór S — na początku pusty
    while len(ready) < graph.number_of_nodes():
        not_ready = [v for v in sorted(graph.nodes()) if v not in ready]
        u = min(not_ready, key=lambda v: ds[v])
        ready.add(u)
        for v in sorted(graph.neighbors(u)):
            if v not in ready:
                relax(u, v, graph, ds, ps)
    return ds, ps


def shortest_path(ps: dict[int, int | None], s: int, v: int) -> list[int]:
    """Odtwarza ścieżkę s → v, idąc po poprzednikach od v wstecz do s.

    Zwraca pustą listę, gdy v jest nieosiągalny z s.
    """
    path = [v]
    while path[-1] != s:
        previous = ps[path[-1]]
        if previous is None:
            return []
        path.append(previous)
    return path[::-1]
