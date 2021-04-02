import enum


class Note:
    def __init__(self, name: str):
        self.name = name

    def key(self):
        return self.name[0]

    def key_order_diff(self, other: 'Note'):
        return ord(self.key()) - ord(other.key())

    def is_sharp(self):
        return len(self.name) > 1 and self.name[1] == '#'

    def is_flat(self):
        return len(self.name) > 1 and self.name[1] == 'b'

    def is_plain(self):
        return len(self.name) == 1

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"

    def __le__(self, other: 'Note'):
        return self.__eq__(other) or self.__lt__(other)

    def __eq__(self, other):
        if not isinstance(other, Note):
            return False
        # D == D
        if self.name == other.name:
            return True
        # C# == Db
        if self.key_order_diff(other) == -1 and self.is_sharp() and other.is_flat():
            return True
        # Db == C#
        if self.key_order_diff(other) == 1 and self.is_flat() and other.is_sharp():
            return True
        return False

    def __lt__(self, other):
        if self.key() == other.key():
            # D <= D# or D <= Db
            if self.is_plain():
                return True if other.is_sharp() else False
            # D# <= D or Db <= D
            return False if self.is_sharp() else True
        return True if self.key_order_diff(other) < 0 else False

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __sub__(self, other: 'Note'):
        if not isinstance(other, Note):
            raise RuntimeError

        if self.is_flat():
            self_pos = _get_pos(self, CHROMATIC_NOTES_WITH_FLATS)
        else:
            self_pos = _get_pos(self, CHROMATIC_NOTES_WITH_SHARPS)

        if other.is_flat():
            other_pos = _get_pos(other, CHROMATIC_NOTES_WITH_FLATS)
        else:
            other_pos = _get_pos(other, CHROMATIC_NOTES_WITH_SHARPS)

        semitones = self_pos - other_pos
        # Scale repeats with high pitch
        if semitones < 0:
            semitones = len(CHROMATIC_NOTES_WITH_SHARPS) + semitones

        interval = Intervals.SEMITONES_TO_INTERVALS.get(semitones)
        if interval:
            return interval

        return Interval(name='custom', semitones=semitones)


class Notes:
    C = Note("C")
    C_SHARP = Note("C#")
    D_FLAT = Note("Db")
    D = Note("D")
    D_SHARP = Note("D#")
    E_FLAT = Note("Eb")
    E = Note("E")
    F = Note("F")
    F_SHARP = Note("F#")
    G_FLAT = Note("Gb")
    G = Note("G")
    G_SHARP = Note("G#")
    A_FLAT = Note("Ab")
    A = Note("A")
    A_SHARP = Note("A#")
    B_FLAT = Note("B#")
    B = Note("B")


class IntervalType(enum.Enum):
    CONSONANT = "consonat"
    DISSONANT = "dissonant"


class Interval:
    def __init__(self, name: str, semitones: int, interval_type: 'IntervalType' = None, ratio: str = None):
        self.name = name
        self.semitones = semitones
        self.type = interval_type
        self.ratio = ratio

    def __eq__(self, other: 'Interval'):
        if not isinstance(other, Interval):
            return False
        return self.name == other.name and self.semitones == other.semitones and self.type == other.type and self.ratio == other.ratio

    def __str__(self):
        return f"{self.name}({self.semitones})"

    def __repr__(self):
        return f"{self.name}({self.semitones})"


class Intervals:
    TONE = Interval("tone", 2)
    SEMITONE = Interval("semitone", 1)
    UNISON = Interval("unison", 0, interval_type=IntervalType.CONSONANT, ratio="1:1")
    MINOR_SECOND = Interval("minor-second", 1, interval_type=IntervalType.DISSONANT, ratio="16:15")
    MAJOR_SECOND = Interval("major-second", 2, interval_type=IntervalType.DISSONANT, ratio="9:8")
    MINOR_THIRD = Interval("minor-third", 3, interval_type=IntervalType.CONSONANT, ratio="6:5")
    MAJOR_THIRD = Interval("major-third", 4, interval_type=IntervalType.CONSONANT, ratio="5:4")
    PERFECT_FOURTH = Interval("perfect-fourth", 5, interval_type=IntervalType.CONSONANT, ratio="4:3")
    AUGMENTED_FOURTH = Interval("augmented-fourth", 6, interval_type=IntervalType.DISSONANT, ratio="45:32")
    TRITONE = Interval("tritone", 6, interval_type=IntervalType.DISSONANT, ratio="45:32")
    PERFECT_FIFTH = Interval("perfect-fifth", 7, interval_type=IntervalType.CONSONANT, ratio="3:2")
    MINOR_SIXTH = Interval("minor-sixth", 8, interval_type=IntervalType.CONSONANT, ratio="8:5")
    MAJOR_SIXTH = Interval("major-sixth", 9, interval_type=IntervalType.CONSONANT, ratio="5:3")
    MINOR_SEVENTH = Interval("minor-seventh", 10, interval_type=IntervalType.DISSONANT, ratio="9:5")
    MAJOR_SEVENTH = Interval("major-seventh", 11, interval_type=IntervalType.DISSONANT, ratio="15:8")
    OCTAVE = Interval("octave", 12, interval_type=IntervalType.CONSONANT, ratio="2:1")
    SEMITONES_TO_INTERVALS = {
        0: UNISON,
        1: MINOR_SECOND, 2: MAJOR_SECOND, 3: MINOR_THIRD, 4: MAJOR_THIRD, 5: PermissionError, 6: TRITONE,
        7: PERFECT_FIFTH, 8: MINOR_SIXTH, 9: MAJOR_SIXTH, 10: MAJOR_SEVENTH, 12: OCTAVE
    }


class Scale:
    def __init__(self, name: str, intervals: '[Interval]'):
        self.name = name
        self.intervals = intervals

    def interval_len(self):
        return len(self.intervals)

    def scale_len(self):
        return len(self.intervals) + 1

    def __eq__(self, other: 'Scale'):
        if not isinstance(other, Scale):
            return False

        return self.name == other.name and self.intervals == other.intervals


class Scales:
    IONIAN = Scale("ionian",
                   [Intervals.TONE, Intervals.TONE, Intervals.SEMITONE, Intervals.TONE, Intervals.TONE, Intervals.TONE,
                    Intervals.SEMITONE])
    MAJOR = Scale("major",
                  [Intervals.TONE, Intervals.TONE, Intervals.SEMITONE, Intervals.TONE, Intervals.TONE, Intervals.TONE,
                   Intervals.SEMITONE])
    DORIAN = Scale("dorian", [Intervals.TONE, Intervals.SEMITONE, Intervals.TONE, Intervals.TONE, Intervals.TONE,
                              Intervals.SEMITONE,
                              Intervals.TONE])
    PHRYGIAN = Scale("phrygian",
                     [Intervals.SEMITONE, Intervals.TONE, Intervals.TONE, Intervals.TONE, Intervals.SEMITONE,
                      Intervals.TONE,
                      Intervals.TONE])
    LYDIAN = Scale("lydian",
                   [Intervals.TONE, Intervals.TONE, Intervals.TONE, Intervals.SEMITONE, Intervals.TONE, Intervals.TONE,
                    Intervals.SEMITONE])
    MIXOLYDIAN = Scale("mixolydian",
                       [Intervals.TONE, Intervals.TONE, Intervals.SEMITONE, Intervals.TONE, Intervals.TONE,
                        Intervals.SEMITONE,
                        Intervals.TONE])
    AEOLIAN = Scale("aeolian", [Intervals.TONE, Intervals.SEMITONE, Intervals.TONE, Intervals.TONE, Intervals.SEMITONE,
                                Intervals.TONE,
                                Intervals.TONE])
    MINOR = Scale("minor", [Intervals.TONE, Intervals.SEMITONE, Intervals.TONE, Intervals.TONE, Intervals.SEMITONE,
                            Intervals.TONE,
                            Intervals.TONE])
    LOCRIAN = Scale("locrian", [Intervals.TONE, Intervals.SEMITONE, Intervals.TONE, Intervals.TONE, Intervals.SEMITONE,
                                Intervals.TONE,
                                Intervals.TONE])


CHROMATIC_NOTES_WITH_SHARPS = [Notes.C, Notes.C_SHARP, Notes.D, Notes.D_SHARP, Notes.E, Notes.F, Notes.F_SHARP, Notes.G,
                               Notes.G_SHARP, Notes.A, Notes.A_SHARP, Notes.B]
CHROMATIC_NOTES_WITH_FLATS = [Notes.C, Notes.D_FLAT, Notes.D, Notes.E_FLAT, Notes.E, Notes.F, Notes.G_FLAT, Notes.G,
                              Notes.A_FLAT, Notes.A, Notes.B_FLAT, Notes.B]


class ScaleDegree:
    def __init__(self, degree: int, octave: int = 1):
        self.degree = degree
        self.octave = octave

    def get_pos(self, scale: Scale):
        return ((self.octave - 1) * scale.interval_len()) + self.degree

    def __eq__(self, other: 'ScaleDegree'):
        if not isinstance(other, ScaleDegree):
            return False

        return self.degree == other.degree and self.octave == other.octave


class ScaleNote:
    def __init__(self, note: 'Note', scale_degree: 'ScaleDegree', scale: Scale):
        self.note = note
        self.scale_degree = scale_degree
        self.scale = scale
        self.pos = self.scale_degree.get_pos(self.scale)

    def __eq__(self, other: 'ScaleNote'):
        if not isinstance(other, ScaleNote):
            return False

        return self.note == other.note and self.scale_degree == other.scale_degree and self.scale == other.scale

    def __str__(self):
        if self.pos <= self.scale_degree.degree:
            return f"{self.note.name}({self.scale_degree.degree})"
        return f"{self.note.name}({self.pos}/{self.scale_degree.degree})"

    def __repr__(self):
        if self.pos <= self.scale_degree.degree:
            return f"{self.note.name}({self.scale_degree.degree})"
        return f"{self.note.name}({self.pos}/{self.scale_degree.degree})"


def get_notes(scale=Scales.MAJOR, key=Notes.C, sharps=True, octaves=1, with_intervals=False, filter_pos=None,
              combine_intervals=True) -> '[ScaleNote]':
    chromatic_notes = CHROMATIC_NOTES_WITH_SHARPS if sharps else CHROMATIC_NOTES_WITH_FLATS
    chromatic_notes_len = len(chromatic_notes)

    notes = [ScaleNote(key, ScaleDegree(1, 1), scale)]
    curr = key
    pos = _get_pos(curr, chromatic_notes)
    for octave in range(octaves):
        for i, interval in enumerate(scale.intervals):
            next_pos = (pos + interval.semitones) % chromatic_notes_len
            if with_intervals:
                notes.append(interval)
            next_note = chromatic_notes[next_pos]
            scale_degree = ScaleDegree(1, octave + 2) if next_note == key else ScaleDegree(i + 2, octave + 1)
            notes.append(ScaleNote(next_note, scale_degree, scale))
            pos = next_pos

    if filter_pos:
        notes = list(filter(
            lambda scale_note: isinstance(scale_note,
                                          Interval) or scale_note.pos in filter_pos, notes))
        # Trim intervals from front and end of the list
        while notes:
            if isinstance(notes[0], ScaleNote):
                break
            notes.pop(0)
        while notes:
            if isinstance(notes[len(notes) - 1], ScaleNote):
                break
            notes.pop(len(notes) - 1)

        # Combine simple tones and semitones
        if combine_intervals:
            i = 0
            while i < len(notes) - 1:
                if not isinstance(notes[i], Interval):
                    i += 1
                    continue
                semitones = 0
                while i < len(notes) - 1 and isinstance(notes[i], Interval):
                    semitones = notes.pop(i).semitones
                notes.insert(i, Intervals.SEMITONES_TO_INTERVALS[semitones])
                i += 1
    return notes


def _get_pos(note_to_find, notes):
    for i, note in enumerate(notes):
        if note_to_find == note:
            return i
    raise RuntimeError(f"{note_to_find} not found in {notes}")


class ChordType(enum.Enum):
    MAJOR = "major"
    MINOR = "minor"
    DIMINISHED = "diminshed"
    AUGMENTED = "agumented"
    SEVENTH = "seventh"
    MAJOR_SEVENTH = "major-seventh"
    NINTH = "ninth"
    MAJOR_NINTH = "major-ninth"
    MINOR_NINTH = "minor-ninth"


class Chord:
    CHORD_TYPE_TO_INTERVALS = {
        ChordType.MAJOR: [Intervals.MAJOR_THIRD, Intervals.MINOR_THIRD],
        ChordType.MINOR: [Intervals.MINOR_THIRD, Intervals.MAJOR_THIRD],
        ChordType.DIMINISHED: [Intervals.MINOR_THIRD, Intervals.MINOR_THIRD],
        ChordType.AUGMENTED: [Intervals.MAJOR_THIRD, Intervals.MAJOR_THIRD],
        ChordType.SEVENTH: [Intervals.MAJOR_THIRD, Intervals.MINOR_THIRD, Intervals.MINOR_THIRD],
        ChordType.MAJOR_SEVENTH: [Intervals.MAJOR_THIRD, Intervals.MINOR_THIRD, Intervals.MAJOR_THIRD],
        ChordType.NINTH: [Intervals.MAJOR_THIRD, Intervals.MINOR_THIRD, Intervals.MINOR_THIRD, ScaleDegree(2, 2)],
        ChordType.MINOR_NINTH: [Intervals.MINOR_THIRD, Intervals.MAJOR_THIRD, Intervals.MINOR_THIRD, ScaleDegree(2, 2)]
    }

    def __init__(self, key=Notes.C, chord_type=ChordType.MAJOR, sharps=True):
        self.key = key
        self.scale = Scales.MAJOR
        self.chord_type = chord_type
        self.sharps = sharps
        curr_note = key
        notes = [key]
        for val in Chord.CHORD_TYPE_TO_INTERVALS[chord_type]:
            if isinstance(val, Interval):
                next_note = self._get_next_note_from_interval(curr_note, val)
            elif isinstance(val, ScaleDegree):
                next_note = self._get_next_note_from_scale_degree(val)
            else:
                raise RuntimeError
            notes.append(next_note)
            curr_note = next_note
        self.notes = notes

    def _get_next_note_from_interval(self, note: 'Note', interval):
        chromatic_notes = CHROMATIC_NOTES_WITH_SHARPS if self.sharps else CHROMATIC_NOTES_WITH_FLATS
        pos = _get_pos(note, chromatic_notes)
        next_pos = pos + interval.semitones
        next_pos %= len(chromatic_notes)
        return chromatic_notes[next_pos]

    def _get_next_note_from_scale_degree(self, scale_degree: 'ScaleDegree'):
        notes = get_notes(self.scale, self.key, self.sharps)
        return notes[scale_degree.degree - 1].note

    def get_relative_minor(self):
        chords = get_chords(self.key, self.sharps)
        return chords[5]

    @staticmethod
    def get_from_notes(notes: '[Note]'):
        notes = list(filter(lambda x: isinstance(x, Note), notes))
        if not notes:
            return

        intervals = []
        for i in range(len(notes) - 1):
            intervals.append(notes[i + 1] - notes[i])

        for key, value in Chord.CHORD_TYPE_TO_INTERVALS.items():
            if value == intervals:
                return Chord(key=notes[0], chord_type=key)

    def __eq__(self, other: 'Chord'):
        if not isinstance(other, Chord):
            return False

        return self.key == other.key and self.chord_type == other.chord_type

    def __str__(self):
        return f"{self.key}{self._get_symbol_from_type()}({self.notes})"

    def __repr__(self):
        return f"{self.key}{self._get_symbol_from_type()}({self.notes})"

    def _get_symbol_from_type(self):
        if self.chord_type == ChordType.MAJOR:
            return ""
        if self.chord_type == ChordType.MINOR:
            return "m"
        if self.chord_type == ChordType.SEVENTH:
            return "7"
        if self.chord_type == ChordType.DIMINISHED:
            return "dim"
        if self.chord_type == ChordType.AUGMENTED:
            return "aug"
        if self.chord_type == ChordType.MAJOR_SEVENTH:
            return "Maj7"
        if self.chord_type == ChordType.NINTH:
            return "9"
        if self.chord_type == ChordType.MAJOR_NINTH:
            return "Maj9"
        if self.chord_type == ChordType.MINOR_NINTH:
            return "m9"
        raise RuntimeError


def get_chords(key=Notes.C, sharps=True):
    scale_notes = get_notes(Scales.MAJOR, key, sharps)
    return [Chord(key=scale_notes[0].note, chord_type=ChordType.MAJOR),
            Chord(key=scale_notes[1].note, chord_type=ChordType.MINOR),
            Chord(key=scale_notes[2].note, chord_type=ChordType.MINOR),
            Chord(key=scale_notes[3].note, chord_type=ChordType.MAJOR),
            Chord(key=scale_notes[4].note, chord_type=ChordType.MAJOR),
            Chord(key=scale_notes[5].note, chord_type=ChordType.MINOR),
            Chord(key=scale_notes[6].note, chord_type=ChordType.DIMINISHED)]


def get_chords_for_scale(scale=Scales.MAJOR, key=Notes.C, sharps=True):
    if scale == Scales.MAJOR:
        return get_chords(key=key, sharps=True)

    chords = []
    for i in range(1, 8):
        notes = get_notes(scale=scale, key=key, octaves=2, filter_pos=[i, i + 2, i + 4])
        chords.append(Chord.get_from_notes(convert_scale_notes_to_notes(notes)))

    return chords


def get_harmonic_scale(key=Notes.C, sharps=True):
    scale_notes = get_notes(Scales.MAJOR, key, sharps)
    return [Chord(key=scale_notes[4].note, chord_type=ChordType.SEVENTH),
            Chord(key=scale_notes[0].note, chord_type=ChordType.MAJOR),
            Chord(key=scale_notes[3].note, chord_type=ChordType.MAJOR),
            Chord(key=scale_notes[6].note, chord_type=ChordType.DIMINISHED),
            Chord(key=scale_notes[2].note, chord_type=ChordType.SEVENTH),
            Chord(key=scale_notes[5].note, chord_type=ChordType.MINOR),
            Chord(key=scale_notes[1].note, chord_type=ChordType.MINOR)]


def arrange_harmonic_degrees_in_harmonic_scale(chords: '[Chord]'):
    chords = list(filter(lambda x: isinstance(x, Chord), chords))
    if len(chords) != 7:
        raise RuntimeError("harmonic scale only support 7 degrees")

    return [Chord(key=chords[4].key, chord_type=ChordType.SEVENTH),
            chords[0],
            chords[3],
            chords[6],
            Chord(key=chords[2].key, chord_type=ChordType.SEVENTH),
            chords[5],
            chords[1]]


def convert_scale_notes_to_notes(scale_notes: '[ScaleNote]'):
    scale_notes = list(filter(lambda x: isinstance(x, ScaleNote), scale_notes))
    return list(map(lambda x: x.note, scale_notes))
