"""TK5."""


def make_ends(nums: list) -> list:
    """
    Given an array of ints, return a new array length 2 containing the first and last elements from the original array.

    The original array will be length 1 or more.

    make_ends([1, 2, 3]) → [1, 3]
    make_ends([1, 2, 3, 4]) → [1, 4]
    make_ends([7, 4, 6, 2]) → [7, 2]

    :param nums: List of integers.
    :return: List with the first and the last element from the input list.
    """
    if len(nums) == 1:
        return [nums[0], nums[0]]
    return [nums[0], nums[-1]]


def near_ten(nr: int) -> bool:
    """
    Given a non-negative number "num", return True if num is within 2 of a multiple of 10.

    near_ten(0) →  True
    near_ten(3) →  False
    near_ten(10) →  True
    near_ten(23) →  False
    near_ten(198) →  True

    :param nr: non-negative integer.
    :return: True if num is within 2 of a multiple of 10.
    """
    remainder = nr % 10
    return remainder <= 2 or remainder >= 8


def combo_string(s1: str, s2: str) -> str:
    """
    Return a new string of the form short + long + short.

    Given 2 strings, a and b, return a string of the form short+long+short,
    with the shorter string on the outside and the longer string on the inside.
    The strings will not be the same length, but they may be empty (length 0).

    combo_string('Hello', 'hi') → 'hiHellohi'
    combo_string('hi', 'Hello') → 'hiHellohi'
    combo_string('aaa', 'b') → 'baaab'

    :param s1:
    :param s2:
    :return:
    """
    if len(s1) > len(s2):
        return s2 + s1 + s2
    else:
        return s1 + s2 + s1


def min_diff(nums: list):
    """
    Find the smaller diff between the first and the last element.

    Diff is a distance (non-negative number) between a value of an element and a value of the element at position of original element value.
    Take diffs for both the first and the last element, return the smaller diff.

    If one index is out of range, then return the diff of other element.
    If both indices are out of range, return -1.

    min_diff([1, 2, 3, 4, 5, 3]) => 1
    min_diff([1, 3, 3, 4, 1, 4]) => 2
    min_diff([0, 1, 2, 0]) => 0
    min_diff([1, 100, 102, 2]) => 99

    min_diff([1, 2, 3]) => 1
    min_diff([79, 2, 0]) => 79
    min_diff([123, 0, 122]) => -1

    :param nums: List of integers.
    :return: Min diff
    """

    if not nums:
        return -1  # Return -1 if the list is empty

    first_value = nums[0]
    last_value = nums[-1]

    first_diff = abs(first_value - nums[first_value]) if 0 <= first_value < len(nums) else -1
    last_diff = abs(last_value - nums[last_value]) if 0 <= last_value < len(nums) else -1

    if first_diff == -1 and last_diff == -1:
        return -1
    elif first_diff == -1:
        return last_diff
    elif last_diff == -1:
        return first_diff
    return min(first_diff, last_diff)


print(min_diff([1,2,3,4,5,3]))
print(min_diff([1,3,3,4,1,4]))
print(min_diff([0,1,2,0]))
print(min_diff([1,100,102,2]))
print(min_diff([1,2,3]))
print(min_diff([79,2,0]))
print(min_diff([123,0,122]))


def word_numeration(words: list) -> list:
    """
    For a given list of string, add numeration for every string.

    The input list consists of strings. For every element in the input list,
    the output list adds a numeration after the string.
    The format is as follows: #N, where N starts from 1.
    String comparison should be case-insensitive.
    The case of symbols in string itself in output list should remain the same as in input list.

    The output list has the same amount of elements as the input list.
    For every element in the output list, "#N" is added, where N = 1, 2, 3, ...

    word_numeration(["tere", "tere", "tulemast"]) => ["tere#1", "tere#2", "tulemast#1"]
    word_numeration(["Tere", "tere", "tulemast"]) => ["Tere#1", "tere#2", "tulemast#1"]
    word_numeration(["Tere", "tere", "tulemast", "no", "tere", "TERE"]) => ["Tere#1", "tere#2", "tulemast#1", "no#1", "tere#3", "TERE#4"]

    :param words: A list of strings.
    :return: List of string with numeration.
    """
    pass
