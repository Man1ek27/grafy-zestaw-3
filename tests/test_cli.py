import pytest

from graph_cli.cli import main
from graph_cli.weight_matrix import parse_weight_matrix

from helpers import EXAMPLES

SLIDES = str(EXAMPLES / "slides-7.txt")
INPUT = str(EXAMPLES / "input-12.txt")


def run(capsys, *argv):
    code = main(list(argv))
    return code, capsys.readouterr().out


def test_random_saves_matrix_and_plot(capsys, tmp_path):
    code, out = run(
        capsys,
        "random",
        "--n",
        "8",
        "--seed",
        "1",
        "--output",
        str(tmp_path / "g.txt"),
        "--plot",
        str(tmp_path / "g.png"),
    )
    assert code == 0
    assert out.startswith("Spójny graf losowy: n = 8, m = ")
    graph = parse_weight_matrix((tmp_path / "g.txt").read_text(encoding="utf-8"))
    assert graph.number_of_nodes() == 8
    assert (tmp_path / "g.png").exists()


def test_dijkstra_output_like_listing_1(capsys):
    _, out = run(capsys, "dijkstra", "--input", INPUT)
    lines = out.splitlines()
    assert lines[0] == "START: s = 1"
    assert lines[1] == "d(1)  = 0  ==> [1]"
    assert lines[7] == "d(7)  = 8  ==> [1 - 2 - 4 - 7]"
    assert lines[12] == "d(12) = 17 ==> [1 - 2 - 5 - 8 - 6 - 9 - 11 - 12]"


def test_dijkstra_other_start_with_plot(capsys, tmp_path):
    code, out = run(
        capsys,
        "dijkstra",
        "--input",
        SLIDES,
        "--start",
        "3",
        "--plot",
        str(tmp_path / "d.png"),
    )
    assert code == 0
    assert "d(2) = 12 ==> [3 - 6 - 5 - 2]" in out
    assert (tmp_path / "d.png").exists()


def test_distances_and_center(capsys):
    _, out = run(capsys, "distances", "--input", SLIDES)
    assert out.splitlines()[1] == " 0  6 11  8  3  7  5"
    _, out = run(capsys, "center", "--input", INPUT)
    assert out == (
        "Centrum = 5 (suma odległości: 55)\n"
        "Centrum minimax = 8 (odległość od najdalszego: 9)\n"
    )


def test_mst(capsys, tmp_path):
    _, out = run(capsys, "mst", "--input", SLIDES, "--plot", str(tmp_path / "t.png"))
    assert "(2, 7)  waga 1" in out
    assert out.endswith("Suma wag: 18\n")
    assert (tmp_path / "t.png").exists()


def test_random_graph_is_printed_before_results(capsys):
    _, out = run(capsys, "center", "--n", "6", "--seed", "2")
    assert out.startswith("Wylosowany graf: n = 6")
    assert "Centrum = " in out


def test_all_tasks_on_one_random_graph(capsys, tmp_path):
    code, out = run(
        capsys, "all", "--n", "10", "--edges", "15", "--seed", "7",
        "--output", str(tmp_path / "g.txt"),
    )  # fmt: skip
    assert code == 0
    for task in range(1, 6):
        assert f"=== Zadanie {task}:" in out
    assert "Graf: n = 10, m = 15" in out
    # ten sam graf zapisany do pliku daje te same wyniki
    _, again = run(capsys, "all", "--input", str(tmp_path / "g.txt"))
    assert again == out


def test_same_seed_same_output(capsys):
    _, first = run(capsys, "all", "--n", "9", "--seed", "3")
    _, second = run(capsys, "all", "--n", "9", "--seed", "3")
    assert first == second


@pytest.mark.parametrize(
    "argv",
    [
        ["dijkstra", "--input", SLIDES, "--start", "8"],
        ["random", "--n", "5", "--edges", "2"],
        ["random", "--n", "0"],
        ["mst", "--input", "brak-pliku.txt"],
    ],
)
def test_errors_exit_with_code_1(capsys, argv):
    with pytest.raises(SystemExit) as error:
        main(argv)
    assert error.value.code == 1
    assert capsys.readouterr().err.startswith("Błąd:")


def test_disconnected_input_is_rejected(capsys, tmp_path):
    path = tmp_path / "niespojny.txt"
    path.write_text("3\n0 2 0\n2 0 0\n0 0 0\n", encoding="utf-8")
    with pytest.raises(SystemExit) as error:
        main(["center", "--input", str(path)])
    assert error.value.code == 1
    assert "spójny" in capsys.readouterr().err


@pytest.mark.parametrize(
    "argv",
    [
        ["mst", "--input", SLIDES, "--show"],  # --show bez --plot
        ["dijkstra"],  # brak źródła grafu
        ["center", "--input", SLIDES, "--n", "5"],  # dwa źródła naraz
        ["random", "--n", "5", "--edges", "6", "--probability", "0.3"],
    ],
)
def test_bad_arguments_exit_with_code_2(argv):
    with pytest.raises(SystemExit) as error:
        main(argv)
    assert error.value.code == 2
