"""Music."""


class Note:
    """
    Note class.

    Every note has a name and a sharpness or alteration (supported values: "", "#", "b").
    """

    def __init__(self, note: str):
        """Initialize the class.

        To make the logic a bit easier it is recommended to normalize the notes, that is, choose a sharpness
        either '#' or 'b' and use it as the main, that means the notes will be either A, A#, B, B#, C etc or
        A Bb, B, Cb, C.
        Note is a single alphabetical letter which is always uppercase.
        NB! Ab == Z#
        """
        self.original_note = note
        self.original_note_name = self.original_note[0].upper()
        self.note_name, self.sharpness, self.original_sharpness = self.normalize_note()

    def normalize_note(self):
        """Normalize note to A, A#, B, B#."""
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if 'b' in self.original_note:
            letter_index = (alphabet.index(self.original_note.replace('b', '').upper()) - 1) % len(alphabet)
            return alphabet[letter_index], '#', 'b'
        elif '#' in self.original_note:
            return alphabet[alphabet.index(self.original_note.replace('#', '').upper())], '#', '#'
        else:
            return self.original_note.upper(), '#', ''

    def __repr__(self) -> str:
        """
        Representation of the Note class.

        Return: <Note: [note]> where [note] is the note_name + sharpness if the sharpness is given, that is not "".
        Repr should display the original note and sharpness, before normalization.
        """
        return f"<Note: {self.original_note}>"

    def __eq__(self, other):
        """
        Compare two Notes.

        Return True if equal otherwise False. Used to check A# == Bb or Ab == Z#
        """
        return self.note_name == other.note_name and self.sharpness == other.sharpness

    def __hash__(self) -> int:
        """Allow a Note object to be used as a key in a dictionary. Don't change this method."""
        return hash((self.original_note, self.original_note_name, self.note_name, self.sharpness, self.original_sharpness))


class NoteCollection:
    """NoteCollection class."""

    def __init__(self):
        """
        Initialize the NoteCollection class.

        You will likely need to add something here, maybe a dict or a list?
        """
        self.notes = []

    def add(self, note: Note) -> None:
        """
        Add note to the collection.

        Check that the note is an instance of Note, if it is not, raise the built-in TypeError exception.

        :param note: Input object to add to the collection
        """
        if type(note) is Note:
            if note not in self.notes:
                self.notes.append(note)
        else:
            raise TypeError

    def pop(self, note: str) -> Note | None:
        """
        Remove and return previously added note from the collection by its name.

        If there are no elements with the given name, do not remove anything and return None.

        :param note: Note to remove
        :return: The removed Note object or None.
        """
        if note:
            for x in self.notes:
                if x.original_note == note:
                    self.notes.remove(x)
                    return x
        return

    def extract(self) -> list[Note]:
        """
        Return a list of all the notes from the collection and empty the collection itself.

        Order of the list must be the same as the order in which the notes were added.

        Example:
          collection = NoteCollection()
          collection.add(Note('A'))
          collection.add(Note('C'))
          collection.extract() # -> [<Note: A>, <Note: C>]
          collection.extract() # -> []

        In this example, the second time we use .extract() the output list is empty because we already extracted everything.

        :return: A list of all the notes that were previously in the collection.
        """
        temp_list = self.notes
        self.notes = []
        return temp_list

    @staticmethod
    def sort_sharpness(sharpness):
        """Sort by sharpness."""
        if sharpness == 'b':
            return 1
        elif sharpness == '#':
            return 3
        else:
            return 2

    def get_content(self) -> str:
        """
        Return a string that gives an overview of the contents of the collection.

        Example:
          collection = NoteCollection()
          collection.add(Note('C', '#'))
          collection.add(Note('L', 'b'))
          print(collection.get_content())

        Output in console:
           Notes:
            * C#
            * Lb

        The notes must be sorted alphabetically by name and then by sharpness, that is A, A#, B, Cb, C and so on.
        Recommendation: Use normalized note names, not just the __repr__()

        :return: Content as a string
        """
        if not self.notes:
            return "Notes:\n  Empty."
        notes_list = self.notes
        sorted_notes = sorted(notes_list, key=lambda x: (x.original_note_name.upper(), self.sort_sharpness(x.original_sharpness)))
        final_list = ['Notes:\n']
        for x in range(len(sorted_notes) - 1):
            note_str = "  * " + sorted_notes[x].original_note_name + sorted_notes[x].original_sharpness + '\n'
            final_list.append(note_str)
        final_list.append('  * ' + sorted_notes[-1].original_note)
        print(final_list)

        return ''.join(final_list)


class Chord:
    """Chord class."""

    def __init__(self, note_one: Note, note_two: Note, chord_name: str, note_three: Note = None):
        """
        Initialize chord class.

        A chord consists of 2-3 notes and their chord product (string).
        If any of the parameters are the same, raise the 'DuplicateNoteNamesException' exception.
        """
        if (
                note_one == note_two
                or note_one.original_note_name == chord_name
                or note_two.original_note_name == chord_name
                or (note_three is not None and (note_one == note_three
                                                or note_two == note_three
                                                or note_three.original_note_name == chord_name))
        ):
            raise DuplicateNoteNamesException()

            # Set chord notes
        self.note1 = note_one
        self.note2 = note_two
        self.note3 = note_three

        # Set chord name
        self.chord_name = chord_name

    def __repr__(self) -> str:
        """
        Chord representation.

        Return as: <Chord: [chord_name]> where [chord_name] is the name of the chord.
        """
        return f'<Chord: {self.chord_name}>'


class Chords:
    """Chords class."""

    def __init__(self):
        """
        Initialize the Chords class.

        Add whatever you need to make this class function.
        """
        self.chords = []

    def add(self, chord: Chord) -> None:
        """
        Determine if chord is valid and then add it to chords.

        If there already exists a chord for the given pair of components, raise the 'ChordOverlapException' exception.

        :param chord: Chord to be added.
        """
        for x in self.chords:
            if self.are_instances_equal_except_name(x, chord):
                raise ChordOverlapException()
        else:
            self.chords.append(chord)

    @staticmethod
    def are_instances_equal_except_name(chord1, chord2) -> bool:
        """Check if there are same chords existing."""
        notes1 = {chord1.note1, chord1.note2, chord1.note3}
        notes2 = {chord2.note1, chord2.note2, chord2.note3}
        return notes1 == notes2

    def get(self, first_note: Note, second_note: Note, third_note: Note = None) -> Chord | None:
        """
        Return the chord for the 2-3 notes.

        The order of the first_note and second_note and third_note is interchangeable.

        If there are no combinations for the 2-3 notes, return None

        Example:
          chords = Chords()
          chords.add(Chord(Note('A'), Note('B'), 'Amaj', Note('C')))
          print(chords.get(Note('A'), Note('B'), Note('C')))  # ->  <Chord: Amaj>
          print(chords.get(Note('B'), Note('C'), Note('A')))  # ->  <Chord: Amaj>
          print(chords.get(Note('D'), Note('Z')))  # ->  None
          chords.add(Chord(Note('c#'), Note('d#'), 'c#5'))
          print(chords.get(Note('C#'), Note('d#')))  # ->  <Chord: c#5>

        :param first_note: The first note of the chord.
        :param second_note: The second note of the chord.
        :param third_note: The third note of the chord.
        :return: Chord or None.
        """
        return None


class DuplicateNoteNamesException(Exception):
    """Raised when attempting to add a chord that has same names for notes and product."""


class ChordOverlapException(Exception):
    """Raised when attempting to add a combination of notes that are already used for another existing chord."""


if __name__ == '__main__':
    # chords = Chords()
    # chords.add(Chord(Note('A'), Note('B'), 'Amaj', Note('C')))
    # print(chords.get(Note('A'), Note('B'), Note('C')))  # ->  <Chord: Amaj>
    # print(chords.get(Note('B'), Note('C'), Note('A')))  # ->  <Chord: Amaj>
    # print(chords.get(Note('D'), Note('Z')))  # ->  None
    # chords.add(Chord(Note('c#'), Note('d#'), 'c#5'))
    # print(chords.get(Note('C#'), Note('d#')))  # ->  <Chord: c#5>
    #
    # chords = Chords()
    #
    # chord1 = Chord(Note('A'), Note('C#'), 'Amaj', Note('E'))
    # print(chord1)
    # chord2 = Chord(Note('E'), Note('G'), 'Emin', note_three=Note('B'))
    # print(chord2)
    # chord3 = Chord(Note('E'), Note('B'), 'E5')
    # print(chord3)
    #
    # chords.add(chord1)
    # chords.add(chord2)
    # chords.add(chord3)
    #
    # print(chords.get(Note('e'), Note('b')))  # -> <Chord: E5>

    try:
        wrong_chord = Chord(Note('E'), Note('A'), 'E')
        print('Did not raise, not working as intended.')
    except DuplicateNoteNamesException:
        print('Raised DuplicateNoteNamesException, working as intended!')

    try:
        wrong_chord = Chord(Note('A'), Note('e'), 'E')
        print(Chord(Note('A'), Note('e'), 'E'))
        print('Did not raise, not working as intended.')
    except DuplicateNoteNamesException:
        print('Raised DuplicateNoteNamesException, working as intended!')

    # try:
    #     chords.add(Chord(Note('E'), Note('B'), 'Emaj7add9'))
    #     print('Did not raise, not working as intended.')
    # except ChordOverlapException:
    #     print('Raised ChordOverlapException, working as intended!')
