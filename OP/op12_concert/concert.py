"""Concert."""
from music import NoteCollection, Chords, Chord, Note


class ChordNotInScaleException(Exception):
    """Raised when the chord is not in the key."""


class Mixer(NoteCollection):
    """
    Mixer class.

    Extends the `NoteCollection class`.
    """

    def __init__(self, chords: Chords):
        """Initialize the Mixer class"""
        super().__init__()
        self.chords = chords

    def add(self, note: Note):
        """
        Add note to the collection and check if it can combine with anything already inside.

        Use the `chords` object that was given in the constructor to determine the combinations.

        Example:
                chords = Chords()
                chords.add_chord(Chord(Note('A'), Note('B#"), 'Amin', Note('C')))
                mixer = Mixer(chords)
                mixer.add(Note('A'))
                mixer.add(Note('C'))
                mixer.add(Note('B#'))
                mixer.extract() # -> [<Chord: Amin>]

        :param note: Input object to add to collection.
        """
        if not isinstance(note, Note):
            raise TypeError()
        return [x.name for x in self.chords.chords]


    def extract(self) -> list[Note | Chord]:
        """
        Extract mixer.

        Similar as with NoteCollection but at the end insert the chords as well.
        """
        content = super().extract()
        return content

    def get_content(self) -> str:
        """
        Get content of the Mixer.

        Similar as with NoteCollection but at the end insert the 'name' of the chords too.
        """
        content = super().get_content()
        chord_names = [chord.name for chord in self.notes if isinstance(chord, Chord)]
        if chord_names:
            content += '\nChords:\n  * ' + '\n  * '.join(chord_names)
        return content


class Scale:
    """
    Scale class.

    In music there is a thing called a scale. A scale
    is a sequence of 7 notes that if played will sound good
    together. Other name for the scale is the `key`, such as
    key of A minor or alternatively A minor scale.

    Initialize the class however you like. Just keep in mind that
    you will need to store 7 notes.
    """

    def __init__(self, starting_note: Note, scale_mode: str = "maj"):
        """
        Initialize the scale.

        In this task the scale can be either a `maj` or major scale and
        `min` or minor scale.
        The starting note is the first note of the scale and you have
        to build the scale up relative to that note.
        Major scale is built like that: W W H W W W H
        Minor scale is built like that: W H W W H W W
        W - whole step
        H - half step
        At the last step the note usually goes back to the first note
        , so as a simplification you can ignore the last step so that
        the scale always includes 7 notes exactly.
        What do these mean? A whole step is for example: A -> B or A# -> B#
        A half step is for example: A -> A#. A# -> B. Gb -> G

        You don't have to consider the case where the scale starts from the end of the alphabet
        and you have to wrap back to A. So the highest start note is 'U'.

        :param starting_note: The first note of the scale
        :param scale_mode: The scale mode, either 'maj' or 'min'
        """

    def is_chord_in_scale(self, chord: Chord) -> bool:
        """
        Check if the chord is in scale.

        A chord is in the scale if all the notes of the chord are in the scale.
        :param chord: The chord to check
        :return: The boolean showing that the chord is in scale or not
        """
        return False

    def is_chord_major_or_minor(self, chord: Chord) -> str:
        """
        Return whether the chord is a major or minor chord.

        The rules are the following: big roman numeral marks major and small roman numeral marks minor chord.
        Major scale: I, ii, iii, IV V, vi, vii
        Minor scale: i, ii, III, iv, v, VI, VII.

        For the sake of the exercise let's make the logic so that the chord is major or minor based on the above rule on it's notes, that is if it has more minor notes then it is a minor chord otherwise if it has more major notes then the chord is a major note.

        :param chord: The chord to check
        :return: 'maj' if chord is major, 'min' if chord is minor, 'powerchord' if chord has same number of minor and major notes
        """

    def get_scale(self) -> list[Note]:
        """
        Get scale.

        Return the scale notes in order.
        :return: List of notes
        """


if __name__ == '__main__':
    chords = Chords()

    chord1 = Chord(Note('A'), Note('C#'), 'Amaj', Note('E'))
    chord2 = Chord(Note('E'), Note('G'), 'Emin', note_three=Note('B'))
    chord3 = Chord(Note('E'), Note('B'), 'E5')

    chords.add(chord1)
    chords.add(chord2)
    chords.add(chord3)

    # print(chords.get(Note('e'), Note('b')))  # -> <Chord: E5>

    # try:
    #     wrong_chord = Chord(Note('E'), Note('E'), 'Something else')
    #     print('Did not raise, not working as intended.')
    # except DuplicateNoteNamesException:
    #     print('Raised DuplicateNoteNamesException, working as intended!')
    #
    # try:
    #     chords.add(Chord(Note('E'), Note('B'), 'Emaj7add9'))
    #     print('Did not raise, not working as intended.')
    # except ChordOverlapException:
    #     print('Raised ChordOverlapException, working as intended!')

    mixer = Mixer(chords)
    mixer.add(Note('E'))
    # mixer.add(Note('B'))
    mixer.add(Note('c#'))

    print(mixer.extract())  # -> [<Note: C#>, <Chord: E5>]

    mixer.add(Note('E'))
    # mixer.add(Note('b'))
    mixer.add(Note('e'))
    mixer.add(Note('g'))
    # mixer.add(Note('B'))
    mixer.add(Note('C#'))

    print(mixer.extract())  # -> [<Note: C#>, <Chord: E5>, <Chord: Emin>]

    chord = Chord(Note('A'), Note('b'), "ABCmaj", Note('C'))

    scale = Scale(Note('A'), 'maj')
    print(scale.is_chord_in_scale(chord))
    # ^ -> True, because notes A, B and C are in the scale of 'A' 'maj'

    print(scale.is_chord_major_or_minor(chord))  # -> min

    chord2 = Chord(Note('A'), Note('C'), "A5")

    print(scale.is_chord_major_or_minor(chord2))  # -> powerchord

    chord3 = Chord(Note('A#'), Note('E'), 'E5')

    try:
        scale.is_chord_major_or_minor(chord3)
        print('Did not raise, not working as intended.')
    except ChordNotInScaleException:
        print('Raised ChordNotInScaleException, working as intended!')

    print(scale.get_scale())
    # -> [<Note: A>, <Note: B>, <Note: C>, <Note: C#>, <Note: D#>, <Note: E#>, <Note: F#>]
    # or
    # -> [<Note: A>, <Note: B>, <Note: C>, <Note: Db>, <Note: Eb>, <Note: Fb>, <Note: Gb>]
