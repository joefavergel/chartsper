import glob
import os
import pathlib

from chartsper.logging import logger
from chartsper.io import read_midi
from chartsper.schemas import ChartSong, ChartFile, KIND_MAPPING

DATASET = 'Guitar Hero World Tour'
DATAPATH = f'datalake/{DATASET}'
CHART_EXTENSIONS = ['.mp3', '.ogg', '.mid', '.chart', '.ini']


def get_paths():
    titles = {
    str(path_.parent).split('/')[-1]: path_.parent
    for path in glob.glob(os.path.join(DATAPATH, '**/**'))
    if (path_ := pathlib.Path(path)) and path_.is_file() and path_.suffix in ['.ini']
    }
    chart_file_paths = {
        name: [
            path_ for path in glob.glob(os.path.join(path, '*'))
            if (path_ := pathlib.Path(path)) and path_.is_file() and path_.suffix.lower() in CHART_EXTENSIONS]
        for name, path in titles.items()
    }
    return titles, chart_file_paths


def get_chart_song(chart_file_kinds, allowed_extensions):
    titles, chart_file_paths = get_paths()
    artist_name = 'Eagles'
    char_path = dict(filter(lambda item: item[0].startswith(artist_name), titles.items()))
    chart_name = list(char_path.keys())[0]
    artist, title = tuple(chart_name.split(' - '))

    for name, paths in dict(filter(lambda item: item[0].startswith(artist_name), chart_file_paths.items())).items():
        tmp = [path for path in paths if any(map(path.stem.startswith, chart_file_kinds)) and path.suffix.lower() in allowed_extensions]
        filtered = {
            file_kind: [
                ChartFile(**{
                    'path': path,
                    'file_type': {
                        'kind': KIND_MAPPING.get(file_kind) if file_kind != 'song' else KIND_MAPPING.get(file_kind).get(path.suffix),
                        'extension': path.suffix
                    },
                    'chart_type': file_kind
                })
                for path in tmp
                if path.stem.startswith(file_kind)
            ] for file_kind in chart_file_kinds}

    chart_song = ChartSong(title=title, artist=artist, path=char_path[list(char_path.keys())[0]], **filtered)
    return chart_song


def main():
    chart_file_kinds = ['guitar', 'song', 'notes', 'preview']
    allowed_extensions = ['.chart', '.mid', '.ogg']
    chart_song = get_chart_song(chart_file_kinds, allowed_extensions)
    # mid = read_midifile(chart_song.notes[0].path)
    mid = read_midi(chart_song.notes[0].path)

    for i, track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))
        for msg in track:
            print(msg)

    # print(mid)


if __name__ == '__main__':
    main()