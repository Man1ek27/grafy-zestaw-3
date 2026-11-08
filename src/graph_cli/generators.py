"""Samodzielne implementacje modeli G(n, l) oraz G(n, p) (kod z zestawu 1)."""

import math
import random

from networkx import Graph


# gnl - G(n, l) - losowy graf z n wierzchołkami i dokładnie l krawędziami
def generate_gnl(n: int, edges: int, seed: int | None = None) -> Graph:
    """Losuje graf z n wierzchołkami i dokładnie edges krawędziami."""
    if n < 0:
        raise ValueError("Liczba wierzchołków nie może być ujemna.")

    max_edges = n * (n - 1) // 2

    if not 0 <= edges <= max_edges:
        raise ValueError(f"Liczba krawędzi musi być od 0 do {max_edges}.")

    graph = Graph()
    graph.add_nodes_from(range(1, n + 1))
    pairs = [(u, v) for u in range(1, n + 1) for v in range(u + 1, n + 1)]
    rng = random.Random(seed)
    # wybieramy z pairs dokładnie edges krawędzi bez powtórzeń
    graph.add_edges_from(rng.sample(pairs, edges))

    return graph


# gnp - G(n, p) - losowy graf z n wierzchołkami, w którym każda możliwa krawędź jest losowana niezależnie z prawdopodobieństwem p
def generate_gnp(n: int, probability: float, seed: int | None = None) -> Graph:
    """Losuje każdą możliwą krawędź niezależnie z podanym prawdopodobieństwem."""
    if n < 0:
        raise ValueError("Liczba wierzchołków nie może być ujemna.")
    if not math.isfinite(probability) or not 0 <= probability <= 1:
        raise ValueError("Prawdopodobieństwo musi być skończoną liczbą od 0 do 1.")

    graph = Graph()
    graph.add_nodes_from(range(1, n + 1))
    rng = random.Random(seed)
    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            if rng.random() < probability:
                graph.add_edge(u, v)

    return graph
