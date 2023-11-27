"""Music."""
import re


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
        self.__alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.note_name = self.find_note(note)

    def __repr__(self) -> str:
        """
        Representation of the Note class.

        Return: <Note: [note]> where [note] is the note_name + sharpness if the sharpness is given, that is not "".
        Repr should display the original note and sharpness, before normalization.
        """
        return f"<Note: {self.note_name}>"

    def __eq__(self, other):
        """
        Compare two Notes.

        Return True if equal otherwise False. Used to check A# == Bb or Ab == Z#
        """
        return self.note_name == other

    def find_alphabet_index(self, char: str) -> int:
        """Return index of char from alphabet."""
        alphabet_str = re.search(char, self.__alphabet)
        return alphabet_str.start()

    def find_note(self, note: str) -> str:
        """Normalize note."""
        note_pattern = r'([A-Z])(#|b)?'
        note_match = re.match(note_pattern, note, re.IGNORECASE)
        letter, sharpness = note_match.groups()
        letter = letter.upper()
        if not sharpness:
            return letter
        alphabet_index = self.find_alphabet_index(letter)
        if sharpness == 'b':
            alphabet_index = (alphabet_index - 1) % len(self.__alphabet)
            sharpness = '#'
        return self.__alphabet[alphabet_index] + sharpness


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
        if not isinstance(note, Note):
            raise TypeError("Value is not of type Note.")
        if note not in self.notes:
            self.notes.append(note)

    def dump(self, notes: list[Note]):
        """Help func."""
        for note in notes:
            self.add(note)

    def pop(self, note: str) -> Note | None:
        """
        Remove and return previously added note from the collection by its name.

        If there are no elements with the given name, do not remove anything and return None.

        :param note: Note to remove
        :return: The removed Note object or None.
        """
        note_to_remove = Note(note)
        res = [x for x in self.notes if x == note_to_remove]
        if res:
            result = res[0]
            self.notes.remove(result)
            return result

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
        temp_list = self.notes.copy()
        self.notes = []
        return temp_list

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
        unique_notes = {note.note_name for note in self.notes}
        header = 'Notes:'
        if unique_notes:
            sorted_notes = sorted(unique_notes)
            components = [header] + sorted_notes
            separator = '\n  * '
        else:
            components = [header, 'Empty.']
            separator = '\n  '
        return separator.join(components)


class Chord:
    """Chord class."""

    def __init__(self, note_one: Note, note_two: Note, chord_name: str, note_three: Note = None):
        """
        Initialize chord class.

        A chord consists of 2-3 notes and their chord product (string).
        If any of the parameters are the same, raise the 'DuplicateNoteNamesException' exception.
        """
        unique_notes = NoteCollection()
        self.notes = [note for note in [note_one, note_two, note_three] if note is not None]
        unique_notes.dump(self.notes)

        len_not_matching = len(unique_notes.extract()) != len(self.notes)
        name_in_notes = all([note.note_name != chord_name for note in self.notes])
        if len_not_matching or not name_in_notes:
            raise DuplicateNoteNamesException()

        self.name = chord_name

    def __repr__(self) -> str:
        """
        Chord representation.

        Return as: <Chord: [chord_name]> where [chord_name] is the name of the chord.
        """
        return f'<Chord: {self.name}>'

    def __eq__(self, other):
        """Check if chords are equal."""
        return {note.note_name for note in self.notes} == other


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
        if not isinstance(chord, Chord):
            raise TypeError("Value not a type of Chord.")
        elif chord in self.chords:
            raise ChordOverlapException()
        self.chords.append(chord)

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
        input_notes = {note.note_name for note in [first_note, second_note, third_note] if note is not None}
        matching_chords = [chord for chord in self.chords if chord == input_notes]
        if matching_chords:
            return matching_chords[0]


class DuplicateNoteNamesException(Exception):
    """Raised when attempting to add a chord that has same names for notes and product."""


class ChordOverlapException(Exception):
    """Raised when attempting to add a combination of notes that are already used for another existing chord."""


if __name__ == '__main__':
    chords = Chords()
    chords.add(Chord(Note('A'), Note('B'), 'Amaj', Note('C')))
    print(chords.get(Note('A'), Note('B'), Note('C')))  # ->  <Chord: Amaj>
    print(chords.get(Note('B'), Note('C'), Note('A')))  # ->  <Chord: Amaj>
    print(chords.get(Note('D'), Note('Z')))  # ->  None
    chords.add(Chord(Note('c#'), Note('d#'), 'c#5'))
    print(chords.get(Note('C#'), Note('d#')))  # ->  <Chord: c#5>
