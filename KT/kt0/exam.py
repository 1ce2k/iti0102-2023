"""KT0."""


def add_char_into_pos(char: str, pos: int, string: str) -> str:
    """
    Return a string where a given character is added into a given position in a string.

    In the case of empty string and position 1, return the given character.

    add_char_into_pos("a", 2, "kheksa") -> "kaheksa"
    add_char_into_pos("t", 8, "kaheksa") -> "kaheksat"
    add_char_into_pos("a", 1, "mps") -> "amps"
    add_char_into_pos("a", 1, "") -> "a"
    add_char_into_pos("k", 10, "kalla") -> "kalla"

    """
    if not string and pos == 1:
        return char
    if pos - 1 <= len(string):
        return string[:pos - 1] + char + string[pos - 1:]
    return string


def nr_of_common_characters(string1: str, string2: str) -> int:
    """
    Return a number of common characters of string1 and string2.

    Do not take into account repeated characters.

    common_characters("iva", "avis") -> 3 # 'a', 'i', 'v' are common
    common_characters("saali", "pall") -> 2  # 'a', 'l' are common
    common_characters("memm", "taat") -> 0
    common_characters("memm", "") -> 0

    """
    return len(set(string1).intersection(set(string2)))


# print(nr_of_common_characters("iva", "avis")) # -> 3 # 'a', 'i', 'v' are common
# print(nr_of_common_characters("saali", "pall")) # -> 2  # 'a', 'l' are common
# print(nr_of_common_characters("memm", "taat")) # -> 0
# print(nr_of_common_characters("memm", "")) # ->0


def nr_into_num_list(nr: int, num_list: list) -> list:
    """
    Return a list of numbers where the "nr" is added into the "num_list" so that the list keep going to be sorted.

    Built-in sort methods are not allowed.

    nr_into_num_list(5, []) -> [5]
    nr_into_num_list(5, [1,2,3,4]) -> [1,2,3,4,5]
    nr_into_num_list(5, [1,2,3,4,5,6]) -> [1,2,3,4,5,5,6]
    nr_into_num_list(0, [1,2,3,4,5]) -> [0,1,2,3,4,5,]

    """
    if not num_list and nr:
        return [nr]
    index = 0
    for x in range(len(num_list)):
        if num_list[x] <= nr:
            index = x + 1
    num_list.insert(index, nr)
    return num_list


def symbol_average_position_in_words(words: list) -> dict:
    """
    Find the average position for each symbol.

    For the given text (list of words) the function has to find
    the average position for each symbol.

    If the list is: ["hello", "world"]
    then the positions for the symbols are:
    h: 0 (in the first word only)
    e: 1
    l: 2, 3, 3 (2, 3 in the first word, 3 in the second)
    o: 4, 1
    w: 0
    r: 2
    d: 4

    The average positions:
    h: 0
    e: 1
    l: 2.67
    o: 2.5
    w: 0
    r: 2
    d: 4
    Positions should be rounded to 2 places after the decimal point.

    The order of the keys in the dictionary is not important.

    symbol_average_position_in_words(["hello", "world"]) =>
    {'h': 0.0, 'e': 1.0, 'l': 2.67, 'o': 2.5, 'w': 0.0, 'r': 2.0, 'd': 4.0}

    symbol_average_position_in_words(["abc", "a", "bc", ""]) =>
    {'a': 0.0, 'b': 0.5, 'c': 1.5}

    symbol_average_position_in_words(["1", "a", "A"]) =>
    {'1': 0.0, 'a': 0.0, 'A': 0.0}

    :param words: list of words
    :return: dictionary with symbol average positions
    """
    counts = {}
    for word in words:
        for i, char in enumerate(word):
            if char not in counts:
                counts[char] = [i]
            else:
                counts[char].append(i)
    ret = {}
    for char, positions in counts.items():
        ret[char] = round(sum(positions) / len(positions), 2)
    return ret


def str_dist(string: str, sub: str) -> int:
    """
    Return the length of the largest substring which starts and ends with sub.

    Given a string and a non-empty substring sub,
    compute recursively the largest substring which starts and ends with sub and return its length.

    str_dist("catcowcat", "cat") => 9
    str_dist("catcowcat", "cow") => 3
    str_dist("cccatcowcatxx", "cat") => 9
    """
    if not string:
        return 0
    if string.startswith(sub) and string.endswith(sub):
        return len(string)
    if not string.startswith(sub):
        return str_dist(string[1:], sub)
    return str_dist(string[:-1], sub)


print(str_dist('catcowcat', 'cat'))
print(str_dist('catcowcat', 'cow'))
print(str_dist('23catcowcat343', 'cat'))
