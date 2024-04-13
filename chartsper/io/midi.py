from collections import defaultdict, deque
from enum import Enum, auto
from dataclasses import dataclass
import os

import mido


class Instrument(Enum):
    Guitar = auto()
    Bass = auto()
    Drums = auto()
    Rhythm = auto()
    Keys = auto()
    Vocals = auto()


class Difficulty(Enum):
    Easy = auto()
    Medium = auto()
    Hard = auto()
    Expert = auto()


class NoteType(Enum):
    Normal = auto()
    Tap = auto()
    StarPower = auto()
    Open = auto()


@dataclass
class Note:
    tick: int
    note_type: NoteType
    duration: int


class Song:
    def __init__(self):
        self.tracks = defaultdict(list)
        self.bpm = 120  # Default bpm, should be updated from MIDI
        self.time_signature = (4, 4)  # Default time signature, should be updated from MIDI
    
    def add_track(self, instrument, notes):
        self.tracks[instrument].append(notes)

    def set_bpm(self, bpm):
        self.bpm = bpm

    def set_time_signature(self, numerator, denominator):
        self.time_signature = (numerator, denominator)


def read_midi(file_path):
    song = Song()
    midi = mido.MidiFile(file_path)

    for i, track in enumerate(midi.tracks):
        print(f'Track {i}: {track.name}')
        for msg in track:
            if msg.type == 'note_on':
                # Example handling of note_on message
                pass
            elif msg.type == 'set_tempo':
                # Update song BPM based on the MIDI set_tempo message
                bpm = mido.tempo2bpm(msg.tempo)
                song.set_bpm(bpm)
            elif msg.type == 'time_signature':
                # Update song time signature based on the MIDI time_signature message
                song.set_time_signature(msg.numerator, msg.denominator)

    return song
