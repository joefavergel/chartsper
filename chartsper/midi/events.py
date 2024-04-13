import math

class EventRegistry:
    Events = {}
    MetaEvents = {}

    @classmethod
    def register_event(cls, event, bases):
        if (Event in bases) or (NoteEvent in bases):
            assert event.statusmsg not in cls.Events, \
                f"Event {event.name} already registered"
            cls.Events[event.statusmsg] = event
        elif (MetaEvent in bases) or (MetaEventWithText in bases):
            assert event.metacommand not in cls.MetaEvents, \
                f"Event {event.name} already registered"
            cls.MetaEvents[event.metacommand] = event
        else:
            raise ValueError(f"Unknown bases class in event type: {event.name}")


class AbstractEvent:
    # __slots__ = ['tick', 'data']
    name = "Generic MIDI Event"
    length = 0
    statusmsg = 0x0

    def __init__(self, **kw):
        if type(self.length) == int:
            defdata = [0] * self.length
        else:
            defdata = []
        self.tick = 0
        self.data = defdata
        for key in kw:
            setattr(self, key, kw[key])

    def __lt__(self, other):
        if self.tick < other.tick:
            return True
        elif self.tick > other.tick:
            return False
        return self.data < other.data

    def __eq__(self, other):
        return self.tick == other.tick and self.data == other.data

    def __baserepr__(self, keys=[]):
        keys = ['tick'] + keys + ['data']
        body = []
        for key in keys:
            val = getattr(self, key)
            keyval = f"{key}={val!r}"
            body.append(keyval)
        body = str.join(', ', body)
        return f"midi.{self.__class__.__name__}({body})"

    def __repr__(self):
        return self.__baserepr__()

class Event(AbstractEvent):
    # __slots__ = ['channel']
    name = 'Event'

    def __init__(self, **kw):
        if 'channel' not in kw:
            kw = kw.copy()
            kw['channel'] = 0
        super().__init__(**kw)

    def copy(self, **kw):
        _kw = {'channel': self.channel, 'tick': self.tick, 'data': self.data}
        _kw.update(kw)
        return self.__class__(**_kw)

    def __lt__(self, other):
        if self.tick < other.tick:
            return True
        elif self.tick > other.tick:
            return False
        return False

    def __repr__(self):
        return self.__baserepr__(['channel'])

    @classmethod
    def is_event(cls, statusmsg):
        return cls.statusmsg == (statusmsg & 0xF0)


class MetaEvent(AbstractEvent):
    statusmsg = 0xFF
    metacommand = 0x0
    name = 'Meta Event'

    @classmethod
    def is_event(cls, statusmsg):
        return statusmsg == 0xFF


class NoteEvent(Event):
    # __slots__ = ['pitch', 'velocity']
    length = 2

    @property
    def pitch(self):
        return self.data[0]

    @pitch.setter
    def pitch(self, val):
        self.data[0] = val

    @property
    def velocity(self):
        return self.data[1]

    @velocity.setter
    def velocity(self, val):
        self.data[1] = val


class NoteOnEvent(NoteEvent):
    statusmsg = 0x90
    name = 'Note On'


class NoteOffEvent(NoteEvent):
    statusmsg = 0x80
    name = 'Note Off'


class AfterTouchEvent(Event):
    statusmsg = 0xA0
    length = 2
    name = 'After Touch'

    @property
    def pitch(self):
        return self.data[0]

    @pitch.setter
    def pitch(self, val):
        self.data[0] = val

    @property
    def value(self):
        return self.data[1]

    @value.setter
    def value(self, val):
        self.data[1] = val


class ControlChangeEvent(Event):
    # __slots__ = ['control', 'value']
    statusmsg = 0xB0
    length = 2
    name = 'Control Change'

    @property
    def control(self):
        return self.data[0]

    @control.setter
    def control(self, val):
        self.data[0] = val

    @property
    def value(self):
        return self.data[1]

    @value.setter
    def value(self, val):
        self.data[1] = val


class ProgramChangeEvent(Event):
    # __slots__ = ['value']
    statusmsg = 0xC0
    length = 1
    name = 'Program Change'

    @property
    def value(self):
        return self.data[0]

    @value.setter
    def value(self, val):
        self.data[0] = val


class ChannelAfterTouchEvent(Event):
    # __slots__ = ['value']
    statusmsg = 0xD0
    length = 1
    name = 'Channel After Touch'

    @property
    def value(self):
        return self.data[1]

    @value.setter
    def value(self, val):
        self.data[1] = val


class PitchWheelEvent(Event):
    # __slots__ = ['pitch']
    statusmsg = 0xE0
    length = 2
    name = 'Pitch Wheel'

    @property
    def pitch(self):
        return ((self.data[1] << 7) | self.data[0]) - 0x2000

    @pitch.setter
    def pitch(self, pitch):
        value = pitch + 0x2000
        self.data[0] = value & 0x7F
        self.data[1] = (value >> 7) & 0x7F


class SysexEvent(Event):
    statusmsg = 0xF0
    name = 'SysEx'
    length = 'varlen'

    @classmethod
    def is_event(cls, statusmsg):
        return cls.statusmsg == statusmsg


class SequenceNumberMetaEvent(MetaEvent):
    name = 'Sequence Number'
    metacommand = 0x00
    length = 2


class MetaEventWithText(MetaEvent):
    def __init__(self, **kw):
        super().__init__(**kw)
        if 'text' not in kw:
            self.text = ''.join(chr(datum) for datum in self.data)

    def __repr__(self):
        return self.__baserepr__(['text'])


class TextMetaEvent(MetaEventWithText):
    name = 'Text'
    metacommand = 0x01
    length = 'varlen'


class CopyrightMetaEvent(MetaEventWithText):
    name = 'Copyright Notice'
    metacommand = 0x02
    length = 'varlen'


class TrackNameEvent(MetaEventWithText):
    name = 'Track Name'
    metacommand = 0x03
    length = 'varlen'


class InstrumentNameEvent(MetaEventWithText):
    name = 'Instrument Name'
    metacommand = 0x04
    length = 'varlen'


class LyricsEvent(MetaEventWithText):
    name = 'Lyrics'
    metacommand = 0x05
    length = 'varlen'


class MarkerEvent(MetaEventWithText):
    name = 'Marker'
    metacommand = 0x06
    length = 'varlen'


class CuePointEvent(MetaEventWithText):
    name = 'Cue Point'
    metacommand = 0x07
    length = 'varlen'


class ProgramNameEvent(MetaEventWithText):
    name = 'Program Name'
    metacommand = 0x08
    length = 'varlen'


class SomethingEvent(MetaEvent):
    name = 'Something'
    metacommand = 0x09


class ChannelPrefixEvent(MetaEvent):
    name = 'Channel Prefix'
    metacommand = 0x20
    length = 1


class PortEvent(MetaEvent):
    name = 'MIDI Port/Cable'
    metacommand = 0x21


class TrackLoopEvent(MetaEvent):
    name = 'Track Loop'
    metacommand = 0x2E


class EndOfTrackEvent(MetaEvent):
    name = 'End of Track'
    metacommand = 0x2F


class SetTempoEvent(MetaEvent):
    # __slots__ = ['bpm', 'mpqn']
    name = 'Set Tempo'
    metacommand = 0x51
    length = 3

    @property
    def bpm(self):
        return float(6e7) / self.mpqn

    @bpm.setter
    def bpm(self, bpm):
        self.mpqn = int(float(6e7) / bpm)

    @property
    def mpqn(self):
        assert len(self.data) == 3
        vals = [self.data[x] << (16 - (8 * x)) for x in range(3)]
        return sum(vals)

    @mpqn.setter
    def mpqn(self, val):
        self.data = [(val >> (16 - (8 * x)) & 0xFF) for x in range(3)]


class SmpteOffsetEvent(MetaEvent):
    name = 'SMPTE Offset'
    metacommand = 0x54


class TimeSignatureEvent(MetaEvent):
    # __slots__ = ['numerator', 'denominator', 'metronome', 'thirtyseconds']
    name = 'Time Signature'
    metacommand = 0x58
    length = 4

    @property
    def numerator(self):
        return self.data[0]

    @numerator.setter
    def numerator(self, val):
        self.data[0] = val

    @property
    def denominator(self):
        return 2 ** self.data[1]

    @denominator.setter
    def denominator(self, val):
        self.data[1] = int(math.log(val, 2))

    @property
    def metronome(self):
        return self.data[2]

    @metronome.setter
    def metronome(self, val):
        self.data[2] = val

    @property
    def thirtyseconds(self):
        return self.data[3]

    @thirtyseconds.setter
    def thirtyseconds(self, val):
        self.data[3] = val


class KeySignatureEvent(MetaEvent):
    # __slots__ = ['alternatives', 'minor']
    name = 'Key Signature'
    metacommand = 0x59
    length = 2

    @property
    def alternatives(self):
        d = self.data[0]
        return d - 256 if d > 127 else d

    @alternatives.setter
    def alternatives(self, val):
        self.data[0] = 256 + val if val < 0 else val

    @property
    def minor(self):
        return self.data[1]

    @minor.setter
    def minor(self, val):
        self.data[1] = val


class SequencerSpecificEvent(MetaEvent):
    name = 'Sequencer Specific'
    metacommand = 0x7F