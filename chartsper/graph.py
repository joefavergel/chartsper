import pathlib
from typing import Union

import matplotlib.colors
import numpy as np
import pretty_midi
import networkx as nx

from .plot import LEVEL_MAPING


def assign_colors_to_notes(
    piano_roll: np.ndarray,
    note_to_color: dict[int, str] = None,
    level: str = None
):
    if note_to_color is None and level is None:
        raise ValueError("Please provide a note_to_color mapping or chart level to get default values.")
    elif note_to_color is None and level is not None:
        level = LEVEL_MAPING.get(level)
        note_to_color = dict(zip(range(level['pitch_lims'][0], level['pitch_lims'][1] + 1), level['colors']))
        
    if isinstance(note_to_color, dict):
        note_to_color = {note: matplotlib.colors.to_rgb(hex_) for note, hex_ in note_to_color.items()}

    return note_to_color


def replace_values_by_notes(
    piano_roll: np.ndarray,
    start_pitch: int,
    end_pitch: int,
) -> np.ndarray:
    # Crear un array de índices para asignar a cada fila del piano_roll
    indices = np.arange(start_pitch, end_pitch + 1)
    # Crear una máscara para los valores mayores que cero en el piano_roll
    mask = piano_roll > 0
    # Multiplicar la máscara por los índices para asignar las notas
    piano_roll *= mask * indices[:, np.newaxis]
    return piano_roll / 100


def create_note_graph(instrument, start_pitch, end_pitch, sr = 22050, hop_length = 512) -> nx.DiGraph:
    fs = np.ceil(sr / hop_length)

    piano_roll = replace_values_by_notes(
        instrument.get_piano_roll(fs)[start_pitch:end_pitch + 1], start_pitch, end_pitch
    ).T

    # Crea un grafo dirigido utilizando networkx
    graph = nx.DiGraph()

    note_to_color = assign_colors_to_notes(piano_roll, level='expert')

    node_color = []
    for time_step, column in enumerate(piano_roll):
        # Obtén las notas activas en este paso de tiempo
        active_notes = np.where(column > 0)[0]
        # Añade un nodo por cada nota activa en este paso de tiempo
        for idx in active_notes:
            # El nodo se representa como una tupla (pitch, tiempo)
            note = column[idx]
            node_id = f'{int(note)}_{time_step}'
            graph.add_node(node_id, position=(time_step / fs, note))
            node_color.append(note_to_color[int(note)])
            
            # Conectar con el nodo de la misma nota en el paso de tiempo anterior con un borde temporal
            # print(time_step - 1, int(note))
            if time_step > 0 and piano_roll[time_step - 1, idx] > 0:
                prev_node_id = f'{int(note)}_{time_step - 1}'
                graph.add_edge(prev_node_id, node_id, tipo='temporal')
            
            # Conectar con otros nodos activos en este paso de tiempo para formar acordes
            # Estos bordes no son temporales, así que no agregamos el atributo "tipo"
            for other_idx in active_notes:
                other_note = column[other_idx]
                if note != other_note:
                    other_node_id = f'{int(other_note)}_{time_step}'
                    graph.add_edge(node_id, other_node_id)
    
    return graph, node_color


def consolidate_notes(piano_roll, threshold=2):
    """
    Consolidate consecutive activations of the same note into a single activation if they
    are separated by less than 'threshold' number of frames.
    """
    # This is a binary mask of where notes are present
    note_ons = piano_roll > 0
    # Iterate over all possible notes
    for note in range(piano_roll.shape[0]):
        # Find indices where this note is on
        ons = np.where(note_ons[note])[0]
        if len(ons) > 1:
            # Compare each pair of consecutive ons
            for i in range(len(ons) - 1):
                if ons[i + 1] - ons[i] <= threshold:
                    # If the gap is small, consider this one sustained note
                    piano_roll[note, ons[i]:ons[i + 1]] = piano_roll[note, ons[i]]

    return piano_roll


def create_note_graph_consolidated(instrument, start_pitch, end_pitch, sr=22050, hop_length=512) -> nx.DiGraph:
    fs = np.ceil(sr / hop_length)
    piano_roll = instrument.get_piano_roll(fs)[start_pitch:end_pitch + 1]
    piano_roll = replace_values_by_notes_vec(piano_roll, start_pitch, end_pitch)

    graph = nx.DiGraph()

    # Generamos los identificadores de nodos de manera coherente y precisa.
    for note_index, midi_note in enumerate(range(start_pitch, end_pitch + 1)):
        note_states = piano_roll[note_index] > 0
        changes = np.diff(note_states.astype(int)).nonzero()[0] + 1  # ajustamos para que el cambio refleje el primer índice después del cambio

        if note_states[0]:
            changes = np.insert(changes, 0, 0)  # Si comienza con un estado activo, agregamos un cambio en el comienzo
        if note_states[-1]:
            changes = np.append(changes, len(note_states))  # Asegurarnos de cerrar la última nota

        for i in range(0, len(changes) - 1, 2):
            start_idx = changes[i]
            end_idx = changes[i + 1]
            start_time = start_idx / fs
            end_time = end_idx / fs
            node_id = f'{midi_note}_{start_time:.3f}'

            graph.add_node(node_id, position=(start_time, midi_note), duration=(end_time - start_time))

            # Conexiones para notas sostenidas
            if i > 0:  # Existe un nodo anterior en la misma pista
                prev_time = changes[i - 1] / fs
                prev_node_id = f'{midi_note}_{prev_time:.3f}'
                if graph.has_node(prev_node_id):
                    graph.add_edge(prev_node_id, node_id, type='sustain')

            # Conexiones para formar acordes
            for other_note_index, other_midi_note in enumerate(range(start_pitch, end_pitch + 1)):
                if other_midi_note != midi_note and piano_roll[other_note_index, start_idx] > 0:
                    other_start_time = start_idx / fs
                    other_node_id = f'{other_midi_note}_{other_start_time:.3f}'
                    if graph.has_node(other_node_id):
                        graph.add_edge(node_id, other_node_id, type='chord')

    return graph
