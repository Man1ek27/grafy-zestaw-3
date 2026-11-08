import pytest

from graph_cli.components import is_connected
from graph_cli.random_graph import random_connected_graph


@pytest.mark.parametrize("seed", range(20))
def test_graph_is_connected_and_weights_are_in_range(seed):
    graph = random_connected_graph(10, 0.3, seed=seed)
    assert sorted(graph.nodes()) == list(range(1, 11))
    assert is_connected(graph)
    weights = [w for _, _, w in graph.edges(data="weight")]
    assert all(isinstance(w, int) and 1 <= w <= 10 for w in weights)


@pytest.mark.parametrize("seed", range(10))
def test_gnl_model_has_exact_edge_count(seed):
    graph = random_connected_graph(12, edges=19, seed=seed)
    assert graph.number_of_edges() == 19
    assert is_connected(graph)


def test_same_seed_gives_same_graph_and_weights():
    first = random_connected_graph(8, 0.4, seed=5)
    second = random_connected_graph(8, 0.4, seed=5)
    assert sorted(first.edges(data="weight")) == sorted(second.edges(data="weight"))


def test_all_weights_from_1_to_10_appear():
    graph = random_connected_graph(30, 1.0, seed=0)
    assert {w for _, _, w in graph.edges(data="weight")} == set(range(1, 11))


def test_single_vertex_graph():
    graph = random_connected_graph(1, seed=0)
    assert list(graph.nodes()) == [1]
    assert graph.number_of_edges() == 0


def test_tree_with_minimum_number_of_edges():
    graph = random_connected_graph(6, edges=5, seed=2)
    assert graph.number_of_edges() == 5
    assert is_connected(graph)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"n": 0},
        {"n": -3},
        {"n": 5, "edges": 3},  # za mało krawędzi na graf spójny
        {"n": 4, "edges": 7},  # więcej niż 4·3/2 = 6 krawędzi
        {"n": 4, "probability": 1.5},
        {"n": 5, "probability": 0.0},  # nigdy nie wyjdzie spójny
    ],
)
def test_invalid_parameters(kwargs):
    with pytest.raises(ValueError):
        random_connected_graph(**kwargs, seed=0)
