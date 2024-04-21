import pathlib
from typing import Union

import pretty_midi


def load_instrument(
    midi_filepath: Union[str, pathlib.Path], instrument_name: str
) -> pretty_midi.Instrument:
    # Carga el archivo MIDI utilizando pretty_midi
    midi_filepath = str(midi_filepath) if isinstance(midi_filepath, pathlib.Path) else midi_filepath
    midi = pretty_midi.PrettyMIDI(midi_filepath)

    if instrument_name is None or instrument_name not in [instrument.name for instrument in midi.instruments]:
        raise ValueError("Unknow instrument name. Please provide a valid instrument name.")

    return [
        instrument for instrument in midi.instruments
        if instrument.name == instrument_name
    ][0]
