"""Interfejs terminalowy; logika grafów znajduje się w osobnych modułach.

Budowa parsera, tablica COMMANDS, main(), write_text i format_path
(format_cycle) pochodzą z zestawu 2.
"""

import argparse
from pathlib import Path

from networkx import Graph

from .center import graph_center, minimax_center
from .components import is_connected
from .dijkstra import dijkstra, shortest_path
from .distances import distance_matrix
from .mst import kruskal
from .random_graph import random_connected_graph
from .visualization import draw_graph
from .weight_matrix import (
    format_matrix,
    parse_weight_matrix,
    serialize_weight_matrix,
    weight_rows,
)


def add_random_arguments(command: argparse.ArgumentParser) -> None:
    """Parametry losowania grafu z zadania 1: G(n, p) albo G(n, l) z zestawu 1."""
    density = command.add_mutually_exclusive_group()
    density.add_argument(
        "--probability", type=float, default=0.5, help="p w G(n,p) (domyślnie 0.5)"
    )
    density.add_argument("--edges", type=int, help="liczba krawędzi — model G(n,l)")
    command.add_argument("--seed", type=int, help="ziarno losowania")


def add_graph_arguments(command: argparse.ArgumentParser) -> None:
    """Graf wejściowy: plik z macierzą wag albo losowy spójny graf z wagami."""
    source = command.add_mutually_exclusive_group(required=True)
    source.add_argument("--input", type=Path, help="plik z macierzą wag")
    source.add_argument("--n", type=int, help="liczba wierzchołków losowego grafu")
    add_random_arguments(command)


def add_start_argument(command: argparse.ArgumentParser) -> None:
    command.add_argument(
        "--start", type=int, default=1, help="wierzchołek startowy (domyślnie 1)"
    )


def add_plot_arguments(command: argparse.ArgumentParser) -> None:
    command.add_argument("--plot", type=Path, help="zapisz rysunek PNG")
    command.add_argument("--show", action="store_true", help="otwórz okno z rysunkiem")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Grafy ważone — zestaw 3")
    commands = parser.add_subparsers(dest="command", required=True)

    random = commands.add_parser("random", help="Zad. 1: spójny graf losowy z wagami")
    random.add_argument("--n", type=int, required=True, help="liczba wierzchołków")
    add_random_arguments(random)
    random.add_argument("--output", type=Path, help="zapisz macierz wag do pliku")
    add_plot_arguments(random)

    dijkstra_cmd = commands.add_parser("dijkstra", help="Zad. 2: algorytm Dijkstry")
    add_graph_arguments(dijkstra_cmd)
    add_start_argument(dijkstra_cmd)
    add_plot_arguments(dijkstra_cmd)

    distances = commands.add_parser("distances", help="Zad. 3: macierz odległości")
    add_graph_arguments(distances)

    center = commands.add_parser("center", help="Zad. 4: centrum i centrum minimax")
    add_graph_arguments(center)

    mst = commands.add_parser("mst", help="Zad. 5: minimalne drzewo rozpinające")
    add_graph_arguments(mst)
    add_plot_arguments(mst)

    everything = commands.add_parser("all", help="Zad. 1–5 na jednym grafie")
    add_graph_arguments(everything)
    add_start_argument(everything)
    everything.add_argument("--output", type=Path, help="zapisz macierz wag do pliku")
    add_plot_arguments(everything)
    return parser


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def format_path(path: list[int]) -> str:
    """Zapis ścieżki jak w przykładach: [1 - 2 - 5]."""
    return "[" + " - ".join(str(v) for v in path) + "]"


def load_graph(args: argparse.Namespace) -> Graph:
    """Wczytuje graf z macierzy wag albo losuje spójny graf z wagami (zad. 1)."""
    if args.input is not None:
        graph = parse_weight_matrix(args.input.read_text(encoding="utf-8"))
        if not is_connected(graph):
            raise ValueError("Graf musi być spójny.")
        return graph
    return random_connected_graph(args.n, args.probability, args.edges, args.seed)


def print_graph(graph: Graph, title: str = "Graf") -> None:
    print(f"{title}: n = {graph.number_of_nodes()}, m = {graph.number_of_edges()}")
    print("Macierz wag (0 — brak krawędzi):")
    print(format_matrix(weight_rows(graph)), end="")


def print_random_graph(args: argparse.Namespace, graph: Graph) -> None:
    """Wylosowany graf trzeba pokazać, żeby dało się sprawdzić dalsze wyniki."""
    if args.input is None:
        print_graph(graph, "Wylosowany graf")
        print()


def print_paths(ds: dict[int, float], ps: dict[int, int | None], s: int) -> None:
    """Wypisuje d(v) i najkrótszą ścieżkę s → v jak w listingu 1 z input_3.pdf."""
    print(f"START: s = {s}")
    label_width = max(len(f"d({v})") for v in ds)
    value_width = max(len(str(d)) for d in ds.values())
    for v in sorted(ds):
        label = f"d({v})"
        path = format_path(shortest_path(ps, s, v))
        print(f"{label:<{label_width}} = {ds[v]:<{value_width}} ==> {path}")


def print_centers(dist: list[list[float]]) -> None:
    """Wypisuje centrum i centrum minimax jak w listingu 3 z input_3.pdf."""
    vertex, total = graph_center(dist)
    print(f"Centrum = {vertex} (suma odległości: {total})")
    vertex, farthest = minimax_center(dist)
    print(f"Centrum minimax = {vertex} (odległość od najdalszego: {farthest})")


def print_mst(tree: list[tuple[int, int, int]]) -> None:
    print("Krawędzie drzewa w kolejności dodawania (algorytm Kruskala):")
    for u, v, w in tree:
        print(f"({u}, {v})  waga {w}")
    print(f"Suma wag: {sum(w for _, _, w in tree)}")


def tree_edges(tree: list[tuple[int, int, int]]) -> list[tuple[int, int]]:
    return [(u, v) for u, v, _ in tree]


def run_random(args: argparse.Namespace) -> None:
    graph = random_connected_graph(args.n, args.probability, args.edges, args.seed)
    print_graph(graph, "Spójny graf losowy")
    if args.output is not None:
        write_text(args.output, serialize_weight_matrix(graph))
    if args.plot is not None:
        draw_graph(graph, args.plot, args.show, title="Spójny graf losowy z wagami")


def run_dijkstra(args: argparse.Namespace) -> None:
    graph = load_graph(args)
    print_random_graph(args, graph)
    ds, ps = dijkstra(graph, args.start)
    print_paths(ds, ps, args.start)
    if args.plot is not None:
        # drzewo najkrótszych ścieżek: krawędź od poprzednika do każdego v
        edges = [(ps[v], v) for v in ps if ps[v] is not None]
        title = f"Najkrótsze ścieżki z s = {args.start}"
        draw_graph(graph, args.plot, args.show, edges, title)


def run_distances(args: argparse.Namespace) -> None:
    graph = load_graph(args)
    print_random_graph(args, graph)
    print("Macierz odległości:")
    print(format_matrix(distance_matrix(graph)), end="")


def run_center(args: argparse.Namespace) -> None:
    graph = load_graph(args)
    print_random_graph(args, graph)
    print_centers(distance_matrix(graph))


def run_mst(args: argparse.Namespace) -> None:
    graph = load_graph(args)
    print_random_graph(args, graph)
    tree = kruskal(graph)
    print_mst(tree)
    if args.plot is not None:
        title = "Minimalne drzewo rozpinające"
        draw_graph(graph, args.plot, args.show, tree_edges(tree), title)


def run_all(args: argparse.Namespace) -> None:
    """Cały zestaw w jednym uruchomieniu, na jednym grafie."""
    graph = load_graph(args)
    print("=== Zadanie 1: spójny graf z wagami ===")
    print_graph(graph)
    if args.output is not None:
        write_text(args.output, serialize_weight_matrix(graph))

    print("\n=== Zadanie 2: algorytm Dijkstry ===")
    ds, ps = dijkstra(graph, args.start)
    print_paths(ds, ps, args.start)

    print("\n=== Zadanie 3: macierz odległości ===")
    dist = distance_matrix(graph)
    print(format_matrix(dist), end="")

    print("\n=== Zadanie 4: centrum grafu ===")
    print_centers(dist)

    print("\n=== Zadanie 5: minimalne drzewo rozpinające ===")
    tree = kruskal(graph)
    print_mst(tree)
    if args.plot is not None:
        title = "Minimalne drzewo rozpinające"
        draw_graph(graph, args.plot, args.show, tree_edges(tree), title)


COMMANDS = {
    "random": run_random,
    "dijkstra": run_dijkstra,
    "distances": run_distances,
    "center": run_center,
    "mst": run_mst,
    "all": run_all,
}


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if getattr(args, "show", False) and args.plot is None:
        parser.error("--show wymaga --plot.")
    try:
        COMMANDS[args.command](args)
    except (ValueError, OSError) as error:
        parser.exit(1, f"Błąd: {error}\n")
    return 0
