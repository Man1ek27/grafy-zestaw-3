"""Wizualizacja na okręgu (kod z zestawu 2, rozszerzony o wagi i wyróżnione krawędzie)."""

import math
from pathlib import Path

import matplotlib.pyplot as plt
from networkx import Graph

# miejsce etykiety wagi na krawędzi, licząc od wierzchołka o mniejszym numerze;
# 0.5 (środek) dawałoby ten sam punkt dla wszystkich średnic okręgu
LABEL_POSITION = 0.35


def draw_graph(
    graph: Graph,
    output: Path,
    show: bool = False,
    highlight: list[tuple[int, int]] | None = None,
    title: str = "Wizualizacja grafu",
) -> None:
    """Rysuje graf nieskierowany z równomiernym rozmieszczeniem wierzchołków na okręgu.

    Wierzchołek 1 jest u góry, kolejne zgodnie z ruchem wskazówek zegara.
    Przy każdej krawędzi z atrybutem weight rysowana jest jej waga.
    highlight to krawędzie wyróżnione (np. drzewo rozpinające) — rysowane
    grubą niebieską linią, a pozostałe krawędzie są wtedy szare.
    """
    nodes = sorted(graph.nodes())
    n = len(nodes)

    positions = {}
    for i, node in enumerate(nodes):
        angle = math.pi / 2 - 2 * math.pi * i / n
        x = math.cos(angle)
        y = math.sin(angle)
        positions[node] = (x, y)

    highlighted = {frozenset(edge) for edge in highlight or []}

    plt.figure(figsize=(6, 6))
    plt.axis("off")
    plt.title(title)
    if positions:
        plt.scatter(*zip(*positions.values()), s=250, c="blue", zorder=3)
        for u, v in graph.edges():
            if highlight is None:
                color, width = "black", 1
            elif frozenset((u, v)) in highlighted:
                color, width = "blue", 2.5
            else:
                color, width = "darkgray", 0.8
            (x1, y1), (x2, y2) = positions[min(u, v)], positions[max(u, v)]
            plt.plot([x1, x2], [y1, y2], c=color, lw=width, zorder=1)
            if "weight" in graph[u][v]:
                plt.text(
                    x1 + LABEL_POSITION * (x2 - x1),
                    y1 + LABEL_POSITION * (y2 - y1),
                    str(graph[u][v]["weight"]),
                    fontsize=9,
                    ha="center",
                    va="center",
                    color=color,
                    bbox={"facecolor": "white", "edgecolor": "none", "pad": 1},
                    zorder=2,
                )
        for node, (x, y) in positions.items():
            plt.text(
                x,
                y,
                str(node),
                fontsize=12,
                ha="center",
                va="center",
                zorder=4,
                color="white",
                fontweight="bold",
            )

    output.parent.mkdir(parents=True, exist_ok=True)

    plt.gca().set_aspect("equal", adjustable="box")
    plt.margins(0.15)
    plt.savefig(output, bbox_inches="tight")
    if show:
        plt.show()

    plt.close()
