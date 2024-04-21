import warnings
from typing import Union

import librosa
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pretty_midi
from matplotlib.axes import Axes
from matplotlib.colors import ListedColormap
from matplotlib.figure import Figure
from pretty_midi import PrettyMIDI

warnings.filterwarnings("ignore")

LEVEL_MAPING = {
    # 'markers': (103, 127)
    # 'expert': {
    #     'pitch_lims': (95, 100),
    #     'colors': ['#000000', '#1ae81a', '#d40f15', '#f7d616', '#171ee3', '#ed652b']
    # },
    "expert": {
        "pitch_lims": (96, 100),
        "colors": ["#1ae81a", "#d40f15", "#f7d616", "#171ee3", "#ed652b"],
    },
    "hard": {
        "pitch_lims": (83, 88),
        "colors": ["#000000", "#1ae81a", "#d40f15", "#f7d616", "#171ee3", "#ed652b"],
    },
    "medium": {
        "pitch_lims": (71, 76),
        "colors": ["#000000", "#1ae81a", "#d40f15", "#f7d616", "#171ee3"],
    },
    "easy": {
        "pitch_lims": (59, 64),
        "colors": ["#000000", "#1ae81a", "#d40f15", "#f7d616"],
    },
}


def replace_notes_by_colors(
    pm: PrettyMIDI, start_pitch: int, end_pitch: int, fs: int = 100, y_axis: str = "mel"
) -> np.ndarray:
    matrix = pm.get_piano_roll(fs)[start_pitch : end_pitch + 1]
    for idx, row in enumerate(matrix):
        for index, value in enumerate(row):
            if value > 0:
                row[index] = idx
    if y_axis == "cqt_note":
        return matrix[::-1]
    else:
        return matrix


def plot_piano_roll(
    pm: PrettyMIDI,
    start_pitch: int,
    end_pitch: int,
    fs: int = 22050,
    x_axis: str = "time",
    y_axis: str = "mel",
    figsize: tuple[int, int] = (20, 4),
    cmap: ListedColormap = None,
    ax: Axes = None,
) -> Axes:
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    img = librosa.display.specshow(
        replace_notes_by_colors(pm, start_pitch, end_pitch, fs=fs, y_axis=y_axis),
        hop_length=512,
        sr=22050,
        x_axis=x_axis,
        y_axis=y_axis,
        fmin=pretty_midi.note_number_to_hz(start_pitch),
        cmap=cmap,
        ax=ax,
    )
    return ax


def plot_graph(
    graph: Union[nx.Graph, nx.DiGraph],
    node_color: list[tuple[float, float, float]],
    title: str = None,
    x_lim: tuple[int, int] = None,
    x_label: str = "Time (s)",
    y_label: str = "Note MIDI",
    with_labels: bool = False,
    node_size: int = 50,
    edge_color: str = "#dfe8e1",
    figsize: tuple[int, int] = (20, 5),
    fig_ax: tuple[Figure, Axes] = None,
    show: bool = True,
) -> Axes:
    """
    Visualiza el grafo de notas con colores únicos para cada tipo de nota.

    Args:
    graph (networkx.Graph): El grafo de notas.
    node_color (list): Lista de colores para cada nodo.
    """
    if fig_ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig, ax = fig_ax

    position = nx.get_node_attributes(graph, "position")
    nx.draw(
        graph,
        position,
        node_color=node_color,
        ax=ax,
        with_labels=with_labels,
        node_size=node_size,
        edge_color=edge_color,
    )
    if x_lim:
        ax.set_xlim(x_lim)

    ax.set_facecolor("black")
    ax.axis("off")
    fig.set_facecolor("black")

    if title is not None:
        ax.set_title(title, color="w")
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    if show:
        plt.show()

    return ax


def plot_spec(
    spec: Union[nx.Graph, nx.DiGraph],
    x_axis: str = "time",
    y_axis: str = "mel",
    title: str = None,
    x_lim: tuple[int, int] = None,
    x_label: str = "Time (s)",
    y_label: str = "Frequency (Hz)",
    figsize: tuple[int, int] = (20, 5),
    fig_ax: tuple[Figure, Axes] = None,
    show: bool = True,
) -> Axes:
    """
    Visualiza el grafo de notas con colores únicos para cada tipo de nota.

    Args:
    graph (networkx.Graph): El grafo de notas.
    node_color (list): Lista de colores para cada nodo.
    """
    if fig_ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig, ax = fig_ax

    librosa.display.specshow(spec, x_axis=x_axis, y_axis=y_axis, ax=ax)
    ax.spines["bottom"].set_color("w")
    ax.spines["top"].set_color("w")
    ax.spines["right"].set_color("w")
    ax.spines["left"].set_color("w")
    ax.xaxis.label.set_color("w")
    ax.yaxis.label.set_color("w")
    ax.tick_params(colors="w", which="both")

    if x_lim:
        ax.set_xlim(x_lim)

    ax.set_facecolor("black")
    fig.set_facecolor("black")

    if title is not None:
        ax.set_title(title, color="w")
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    if show:
        plt.show()

    return ax
