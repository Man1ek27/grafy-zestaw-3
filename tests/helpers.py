from pathlib import Path

from networkx import Graph

from graph_cli.weight_matrix import parse_weight_matrix

EXAMPLES = Path(__file__).parents[1] / "examples"


def load(name: str) -> Graph:
    return parse_weight_matrix((EXAMPLES / name).read_text(encoding="utf-8"))


def weighted(edges: list[tuple[int, int, int]], n: int | None = None) -> Graph:
    """Graf z listy (u, v, waga); n dodaje też wierzchołki izolowane 1..n."""
    graph = Graph()
    if n is not None:
        graph.add_nodes_from(range(1, n + 1))
    for u, v, w in edges:
        graph.add_edge(u, v, weight=w)
    return graph


# macierz odległości ze slajdu 12 (Grafy_3.pdf) dla grafu examples/slides-7.txt
SLIDES_DISTANCES = [
    [0, 6, 11, 8, 3, 7, 5],
    [6, 0, 12, 2, 4, 8, 1],
    [11, 12, 0, 13, 8, 4, 13],
    [8, 2, 13, 0, 6, 9, 3],
    [3, 4, 8, 6, 0, 4, 5],
    [7, 8, 4, 9, 4, 0, 9],
    [5, 1, 13, 3, 5, 9, 0],
]

# listing 2 z input_3.pdf dla grafu examples/input-12.txt
INPUT_DISTANCES = [
    [0, 3, 2, 5, 7, 10, 8, 9, 12, 13, 14, 17],
    [3, 0, 5, 2, 4, 7, 5, 6, 9, 10, 11, 14],
    [2, 5, 0, 7, 6, 9, 7, 8, 11, 12, 13, 16],
    [5, 2, 7, 0, 4, 7, 3, 6, 9, 8, 11, 13],
    [7, 4, 6, 4, 0, 3, 1, 2, 5, 6, 7, 10],
    [10, 7, 9, 7, 3, 0, 4, 1, 2, 6, 4, 7],
    [8, 5, 7, 3, 1, 4, 0, 3, 6, 5, 8, 10],
    [9, 6, 8, 6, 2, 1, 3, 0, 3, 5, 5, 8],
    [12, 9, 11, 9, 5, 2, 6, 3, 0, 8, 2, 5],
    [13, 10, 12, 8, 6, 6, 5, 5, 8, 0, 8, 5],
    [14, 11, 13, 11, 7, 4, 8, 5, 2, 8, 0, 3],
    [17, 14, 16, 13, 10, 7, 10, 8, 5, 5, 3, 0],
]
