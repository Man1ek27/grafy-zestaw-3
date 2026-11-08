import networkx as nx
import pytest

from graph_cli.components import is_connected
from graph_cli.mst import kruskal
from graph_cli.random_graph import random_connected_graph

from helpers import load, weighted


def total(tree):
    return sum(w for _, _, w in tree)


def test_slides_example():
    # slajd 21: krawędzie (1,7), (1,2), (1,4), (1,6), (4,6) są pomijane (cykl)
    tree = kruskal(load("slides-7.txt"))
    assert tree == [(2, 7, 1), (2, 4, 2), (1, 5, 3), (2, 5, 4), (3, 6, 4), (5, 6, 4)]
    assert total(tree) == 18


def test_figure_2_from_input_3():
    tree = kruskal(load("input-12.txt"))
    edges = {(u, v) for u, v, _ in tree}
    assert edges == {
        (1, 2), (1, 3), (2, 4), (4, 7), (5, 7), (7, 10),
        (5, 8), (6, 8), (6, 9), (9, 11), (11, 12),
    }  # fmt: skip
    assert total(tree) == 26


@pytest.mark.parametrize("seed", range(20))
def test_random_graphs(seed):
    graph = random_connected_graph(12, 0.35, seed=seed)
    tree = kruskal(graph)
    n = graph.number_of_nodes()
    assert len(tree) == n - 1
    spanning = weighted(tree, n)
    assert is_connected(spanning)  # n − 1 krawędzi i spójny ⇒ drzewo
    assert all(graph[u][v]["weight"] == w for u, v, w in tree)
    expected = nx.minimum_spanning_tree(graph).size(weight="weight")
    assert total(tree) == expected


def test_edges_are_added_in_non_decreasing_weight_order():
    tree = kruskal(random_connected_graph(15, 0.5, seed=1))
    weights = [w for _, _, w in tree]
    assert weights == sorted(weights)


def test_tree_is_its_own_spanning_tree():
    graph = weighted([(1, 2, 7), (2, 3, 1), (2, 4, 9)])
    assert sorted(kruskal(graph)) == [(1, 2, 7), (2, 3, 1), (2, 4, 9)]


def test_cycle_drops_heaviest_edge():
    graph = weighted([(1, 2, 1), (2, 3, 2), (3, 4, 3), (4, 1, 10)])
    assert kruskal(graph) == [(1, 2, 1), (2, 3, 2), (3, 4, 3)]


def test_single_vertex():
    assert kruskal(weighted([], n=1)) == []


def test_disconnected_graph_is_rejected():
    with pytest.raises(ValueError):
        kruskal(weighted([(1, 2, 1), (3, 4, 1)]))
