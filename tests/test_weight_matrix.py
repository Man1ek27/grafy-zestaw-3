import pytest

from graph_cli.random_graph import random_connected_graph
from graph_cli.weight_matrix import parse_weight_matrix, serialize_weight_matrix

from helpers import load


def test_slides_example_edges():
    graph = load("slides-7.txt")
    assert graph.number_of_edges() == 11
    assert graph[2][7]["weight"] == 1
    assert graph[1][6]["weight"] == 9
    assert not graph.has_edge(1, 3)


def test_roundtrip_of_random_graph():
    graph = random_connected_graph(9, 0.5, seed=4)
    text = serialize_weight_matrix(graph)
    again = parse_weight_matrix(text)
    assert sorted(again.edges(data="weight")) == sorted(graph.edges(data="weight"))
    assert serialize_weight_matrix(again) == text


def test_columns_are_aligned():
    text = serialize_weight_matrix(parse_weight_matrix("2\n0 10\n10 0\n"))
    assert text == "2\n 0 10\n10  0\n"


@pytest.mark.parametrize(
    "text",
    [
        "",
        "0\n",
        "2\n0 1\n",  # za mało wierszy
        "2\n0 1\n1 0 0\n",  # wiersz za długi
        "2\n0 1\n2 0\n",  # niesymetryczna
        "2\n1 1\n1 0\n",  # pętla
        "2\n0 -1\n-1 0\n",  # ujemna waga
        "2\n0 a\na 0\n",  # nie liczba
    ],
)
def test_invalid_matrices(text):
    with pytest.raises(ValueError):
        parse_weight_matrix(text)
