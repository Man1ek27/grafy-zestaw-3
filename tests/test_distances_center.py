import networkx as nx
import pytest

from graph_cli.center import graph_center, minimax_center
from graph_cli.distances import distance_matrix
from graph_cli.random_graph import random_connected_graph

from helpers import INPUT_DISTANCES, SLIDES_DISTANCES, load, weighted


def test_slides_distance_matrix_and_centers():
    dist = distance_matrix(load("slides-7.txt"))
    assert dist == SLIDES_DISTANCES
    # slajd 14: sumy 40 33 61 41 30 41 36, najdalsze 11 12 13 13 8 9 13
    assert graph_center(dist) == (5, 30)
    assert minimax_center(dist) == (5, 8)


def test_listings_2_and_3_from_input_3():
    dist = distance_matrix(load("input-12.txt"))
    assert dist == INPUT_DISTANCES
    assert graph_center(dist) == (5, 55)
    assert minimax_center(dist) == (8, 9)


@pytest.mark.parametrize("seed", range(10))
def test_random_matrix_is_symmetric_and_matches_networkx(seed):
    graph = random_connected_graph(10, 0.4, seed=seed)
    dist = distance_matrix(graph)
    expected = nx.floyd_warshall(graph)
    n = graph.number_of_nodes()
    for i in range(n):
        assert dist[i][i] == 0
        for j in range(n):
            assert dist[i][j] == dist[j][i] == expected[i + 1][j + 1]


def test_single_vertex():
    dist = distance_matrix(weighted([], n=1))
    assert dist == [[0]]
    assert graph_center(dist) == (1, 0)
    assert minimax_center(dist) == (1, 0)


def test_ties_choose_smallest_vertex():
    # ścieżka 1–2–3–4 z wagami 1: sumy 6 4 4 6, najdalsze 3 2 2 3
    dist = distance_matrix(weighted([(1, 2, 1), (2, 3, 1), (3, 4, 1)]))
    assert graph_center(dist) == (2, 4)
    assert minimax_center(dist) == (2, 2)


def test_center_and_minimax_can_differ():
    # gwiazda z długim ramieniem: 1 jest środkiem gwiazdy (min. suma),
    # ale do 5 ma daleko, więc minimax wypada na wierzchołku 2
    graph = weighted([(1, 2, 5), (1, 3, 1), (1, 4, 1), (1, 6, 1), (2, 5, 5)])
    dist = distance_matrix(graph)
    assert graph_center(dist) == (1, 18)
    assert minimax_center(dist) == (2, 6)
