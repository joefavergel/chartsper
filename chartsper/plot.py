import warnings

import librosa
import numpy as np
import matplotlib.pyplot as plt
import pretty_midi
from matplotlib.axes import Axes
from matplotlib.colors import ListedColormap
from pretty_midi import PrettyMIDI

warnings.filterwarnings('ignore')

LEVEL_MAPING = {
    # 'markers': (103, 127)
    'expert': {
        'pitch_lims': (95, 100),
        'colors': ['#000000', '#1ae81a', '#d40f15', '#f7d616', '#171ee3', '#ed652b']
    },
    'hard': {
        'pitch_lims': (83, 88),
        'colors': ['#000000', '#1ae81a', '#d40f15', '#f7d616', '#171ee3', '#ed652b']
    },
    'medium': {
        'pitch_lims': (71, 76),
        'colors': ['#000000', '#1ae81a', '#d40f15', '#f7d616', '#171ee3']
    },
    'easy': {
        'pitch_lims': (59, 64),
        'colors': ['#000000', '#1ae81a', '#d40f15', '#f7d616']
    },
}


def replace_notes_by_colors(
    pm: PrettyMIDI,
    start_pitch: int,
    end_pitch: int,
    fs: int = 100,
    y_axis: str='mel'
) -> np.ndarray:
    matrix = pm.get_piano_roll(fs)[start_pitch:end_pitch + 1]
    for idx, row in enumerate(matrix):
        for index, value in enumerate(row):
            if value > 0:
                row[index] = idx
    if y_axis == 'cqt_note':
        return matrix[::-1]
    else:
        return matrix


def plot_piano_roll(
    pm: PrettyMIDI,
    start_pitch: int,
    end_pitch: int,
    fs: int = 100,
    y_axis: str='mel',
    figsize: tuple[int, int] = (20, 4),
    cmap: ListedColormap = None,
    ax: Axes = None,
) -> Axes:
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    img = librosa.display.specshow(
        replace_notes_by_colors(pm, start_pitch, end_pitch, fs=100, y_axis=y_axis),
        hop_length=1,
        sr=fs,
        x_axis='time',
        y_axis=y_axis,
        fmin=pretty_midi.note_number_to_hz(start_pitch),
        cmap=cmap,
        ax=ax
    )
    return ax
