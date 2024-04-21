import pathlib
from enum import Enum
from typing import Any, Optional, Union

from pydantic import BaseModel, Field

KIND_MAPPING = {
    "preview": "audio",
    "song": {".ogg": "audio", ".mp3": "audio", ".opus": "audio", ".init": "metadata"},
    "guitar": "audio",
    "rhythm": "audio",
    "bass": "audio",
    "keys": "audio",
    "drums": "audio",
    "vocals": "audio",
    "crowd": "audio",
    "other": "other",
    "notes": "notes",
}


class ChartFileType(str, Enum):
    PREVIEW = "preview"
    SONG = "song"
    GUITAR = "guitar"
    RHYTHM = "rhythm"
    BASS = "bass"
    KEYS = "keys"
    DRUMS = "drums"
    VOCALS = "vocals"
    CROWD = "crowd"
    OTHER = "other"
    NOTES = "notes"


class FileExtension(str, Enum):
    INI = ".ini"
    OGG = ".ogg"
    MP3 = ".mp3"
    OPUS = ".opus"
    CHART = ".chart"
    MID = ".mid"


class FileKind(str, Enum):
    NOTES = "notes"
    AUDIO = "audio"
    IMAGE = "image"
    METADATA = "metadata"
    OTHER = "other"


class FileType(BaseModel):
    kind: FileKind
    extension: FileExtension


class ChartFile(BaseModel):
    path: Union[str, pathlib.Path]
    file_type: FileType
    chart_type: ChartFileType
    data: Any | None = Field(None)


class ChartSong(BaseModel):
    title: str
    artist: str
    path: Union[str, pathlib.Path]
    guitar: Optional[list[ChartFile]] = Field(None)
    song: Optional[list[ChartFile]] = Field(None)
    notes: Optional[list[ChartFile]] = Field(None)
    preview: Optional[list[ChartFile]] = Field(None)
