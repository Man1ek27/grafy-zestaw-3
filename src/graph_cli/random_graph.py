"""Spójny graf losowy z losowymi wagami krawędzi (zadanie 1)."""

import random

from networkx import Graph

from .components import is_connected
from .generators import generate_gnl, generate_gnp

MIN_WEIGHT = 1
MAX_WEIGHT = 10


def assign_random_weights(graph: Graph, rng: random.Random) -> None:
    """Każdej krawędzi przypisuje losową wagę naturalną z przedziału [1, 10]."""
    for u, v in sorted(graph.edges()):
        graph[u][v]["weight"] = rng.randint(MIN_WEIGHT, MAX_WEIGHT)


def random_connected_graph(
    n: int,
    probability: float = 0.5,
    edges: int | None = None,
    seed: int | None = None,
    max_tries: int = 1000,
) -> Graph:
    """Losuje graf G(n, p) z zestawu 1 (albo G(n, l), gdy podano edges),
    dopóki nie wyjdzie spójny (test z zestawu 2), a potem losuje wagi.

    Każda próba dostaje nowe ziarno z generatora rng, więc to samo --seed
    zawsze daje ten sam graf i te same wagi.
    """
    if n < 1:
        raise ValueError("Graf musi mieć co najmniej jeden wierzchołek.")
    if edges is not None and edges < n - 1:
        raise ValueError(
            f"Graf spójny o {n} wierzchołkach potrzebuje co najmniej {n - 1} krawędzi."
        )

    rng = random.Random(seed)
    for _ in range(max_tries):
        try_seed = rng.randrange(2**32)
        if edges is not None:
            graph = generate_gnl(n, edges, try_seed)
        else:
            graph = generate_gnp(n, probability, try_seed)
        if is_connected(graph):
            assign_random_weights(graph, rng)
            return graph
    raise ValueError(
        f"Nie udało się wylosować spójnego grafu w {max_tries} próbach "
        "— zwiększ prawdopodobieństwo albo liczbę krawędzi."
    )
