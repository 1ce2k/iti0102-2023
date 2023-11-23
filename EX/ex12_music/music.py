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
        self.note_name, self.sharpness = self.normalize_note()

    def normalize_note(self):
        """Normalize note to A, A#, B, B#."""
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if 'b' in self.original_note:
            letter_index = (alphabet.index(self.original_note.replace('b', '').upper()) - 1) % len(alphabet)
            return alphabet[letter_index], '#'
        elif '#' in self.original_note:
            return alphabet[alphabet.index(self.original_note.replace('#', '').upper())], '#'
        else:
            return self.original_note.upper(), '#'

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
        return ''


if __name__ == '__main__':
    note_one = Note('a')  # yes, lowercase
    note_two = Note('C')
    note_three = Note('Eb')
    not1 = Note("A#")
    not2 = Note("Bb")
    print('test if note1 == note2')
    print(not1, not2, not1 == not2)  # <Note: A#> <Note: Bb> True
    collection = NoteCollection()
    print()

    print('test for repr of notes')
    print(note_one)  # <Note: A>
    print(note_two)
    print(note_three)  # <Note: Eb>
    print()

    collection.add(note_one)
    collection.add(note_two)

    print('test of get_content')
    print(collection.get_content())
    # Notes:
    #   * A
    #   * C
    print()

    print('test of extract')
    print(collection.extract())  # [<Note: A>,<Note: C>]
    print(collection.get_content())
    # Notes:
    #  Empty
    print()

    collection.add(note_one)
    collection.add(note_two)
    collection.add(note_three)
    print('test of add')
    print(collection.notes)
    print()

    print('test of pop')
    print(collection.pop('a') == note_one)  # True
    print(collection.notes)
    print(collection.pop('Eb') == note_three)  # True
