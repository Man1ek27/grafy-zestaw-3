"""Spójne składowe (kod z zestawu 2, zadanie 3 — tylko funkcje używane tutaj)."""

from networkx import Graph


def components(graph: Graph) -> dict[int, int]:
    """Algorytm components(G) z alg_2.pdf: comp[v] to numer składowej v (od 1)."""
    comp = {v: -1 for v in graph.nodes()}
    nr = 0
    for v in sorted(graph.nodes()):
        if comp[v] == -1:
            nr += 1
            comp[v] = nr
            components_r(nr, v, graph, comp)
    return comp


def components_r(nr: int, v: int, graph: Graph, comp: dict[int, int]) -> None:
    """Przeszukiwanie w głąb od v (components_R) ze stosem zamiast rekurencji.

    Stos przechowuje iteratory sąsiadów, więc kolejność odwiedzin jest taka
    sama jak w wersji rekurencyjnej, a duży graf nie przekracza limitu rekurencji.
    """
    stack = [iter(sorted(graph.neighbors(v)))]
    while stack:
        for u in stack[-1]:
            if comp[u] == -1:
                comp[u] = nr
                stack.append(iter(sorted(graph.neighbors(u))))
                break
        else:
            stack.pop()


def is_connected(graph: Graph) -> bool:
    """Graf jest spójny, gdy ma co najwyżej jedną składową."""
    return max(components(graph).values(), default=0) <= 1
