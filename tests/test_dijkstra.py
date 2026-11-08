import math

import networkx as nx
import pytest

from graph_cli.dijkstra import dijkstra, init, relax, shortest_path
from graph_cli.random_graph import random_connected_graph

from helpers import load, weighted


def test_init_and_relax_like_alg_3():
    graph = weighted([(1, 2, 8), (1, 7, 5), (7, 2, 1)])
    ds, ps = init(graph, 1)
    assert ds == {1: 0, 2: math.inf, 7: math.inf}
    assert ps == {1: None, 2: None, 7: None}
    relax(1, 2, graph, ds, ps)
    relax(1, 7, graph, ds, ps)
    assert (ds[2], ps[2]) == (8, 1)
    relax(7, 2, graph, ds, ps)  # krócej przez 7: 5 + 1 < 8
    assert (ds[2], ps[2]) == (6, 7)
    relax(1, 2, graph, ds, ps)  # brak poprawy — nic się nie zmienia
    assert (ds[2], ps[2]) == (6, 7)


def test_slides_example():
    # slajd 8: wynik (ds/ps) przy każdym wierzchołku i slajd 9: ścieżki
    ds, ps = dijkstra(load("slides-7.txt"), 1)
    assert ds == {1: 0, 2: 6, 3: 11, 4: 8, 5: 3, 6: 7, 7: 5}
    assert ps == {1: None, 2: 7, 3: 6, 4: 2, 5: 1, 6: 5, 7: 1}
    assert shortest_path(ps, 1, 3) == [1, 5, 6, 3]
    assert shortest_path(ps, 1, 4) == [1, 7, 2, 4]
    assert shortest_path(ps, 1, 1) == [1]


def test_listing_1_from_input_3():
    ds, ps = dijkstra(load("input-12.txt"), 1)
    expected = {
        1: (0, [1]),
        2: (3, [1, 2]),
        3: (2, [1, 3]),
        4: (5, [1, 2, 4]),
        5: (7, [1, 2, 5]),
        6: (10, [1, 2, 5, 8, 6]),
        7: (8, [1, 2, 4, 7]),  # remis z [1, 2, 5, 7] — wygrywa pierwsza relaksacja
        8: (9, [1, 2, 5, 8]),
        9: (12, [1, 2, 5, 8, 6, 9]),
        10: (13, [1, 2, 4, 7, 10]),
        11: (14, [1, 2, 5, 8, 6, 9, 11]),
        12: (17, [1, 2, 5, 8, 6, 9, 11, 12]),
    }
    for v, (distance, path) in expected.items():
        assert ds[v] == distance
        assert shortest_path(ps, 1, v) == path


@pytest.mark.parametrize("seed", range(20))
def test_matches_networkx_on_random_graphs(seed):
    graph = random_connected_graph(12, 0.3, seed=seed)
    start = seed % 12 + 1
    ds, ps = dijkstra(graph, start)
    expected = nx.single_source_dijkstra_path_length(graph, start)
    assert ds == expected
    for v in graph.nodes():
        path = shortest_path(ps, start, v)
        assert path[0] == start and path[-1] == v
        length = sum(graph[a][b]["weight"] for a, b in zip(path, path[1:]))
        assert length == ds[v]


def test_single_vertex():
    graph = weighted([], n=1)
    ds, ps = dijkstra(graph, 1)
    assert ds == {1: 0}
    assert shortest_path(ps, 1, 1) == [1]


def test_unreachable_vertex_has_infinite_distance():
    graph = weighted([(1, 2, 4)], n=3)
    ds, ps = dijkstra(graph, 1)
    assert ds[3] == math.inf
    assert shortest_path(ps, 1, 3) == []


def test_longer_path_with_smaller_sum_wins():
    # bezpośrednia krawędź 1–3 ma wagę 10, droga 1–2–3 tylko 2
    ds, ps = dijkstra(weighted([(1, 3, 10), (1, 2, 1), (2, 3, 1)]), 1)
    assert ds[3] == 2
    assert shortest_path(ps, 1, 3) == [1, 2, 3]


def test_invalid_start_vertex():
    with pytest.raises(ValueError):
        dijkstra(load("slides-7.txt"), 8)


def test_negative_weight_is_rejected():
    with pytest.raises(ValueError):
        dijkstra(weighted([(1, 2, -1)]), 1)
