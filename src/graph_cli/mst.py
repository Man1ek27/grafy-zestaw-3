"""Minimalne drzewo rozpinające algorytmem Kruskala (zadanie 5)."""

from networkx import Graph

from .components import components


def kruskal(graph: Graph) -> list[tuple[int, int, int]]:
    """Zwraca krawędzie (u, v, waga) minimalnego drzewa rozpinającego.

    Krawędzie sortujemy według niemalejących wag (przy remisie według numerów
    wierzchołków). Krawędź uv trafia do lasu T, gdy łączy różne drzewa,
    czyli u i v leżą w różnych spójnych składowych T — sprawdza to
    components() z zestawu 2. Kończymy, gdy T ma n − 1 krawędzi.
    """
    n = graph.number_of_nodes()
    edges = sorted((w, min(u, v), max(u, v)) for u, v, w in graph.edges(data="weight"))

    forest = Graph()  # las T: na początku wszystkie wierzchołki, bez krawędzi
    forest.add_nodes_from(graph.nodes())
    tree = []
    for w, u, v in edges:
        if len(tree) == n - 1:
            break
        comp = components(forest)
        if comp[u] != comp[v]:  # różne drzewa, więc nie powstanie cykl
            forest.add_edge(u, v)
            tree.append((u, v, w))

    if len(tree) < n - 1:
        raise ValueError("Graf nie jest spójny — nie ma drzewa rozpinającego.")
    return tree
