"""TK2."""


def middle_value(a: int, b: int, c: int) -> int:
    """
    Return the middle value out of three values.

    The middle value is the one where there is other value which is smaller or equal
    and there is another value which is larger or equal.

    If the values are 6 2 4, then the middle value is 4.

    middle_value(6, 2, 4) => 4
    middle_value(2, 2, 4) => 2
    middle_value(2, 6, 2) => 2
    middle_value(88, 88, 88) => 88
    """
    if (b <= a <= c) or (c <= a <= b):
        return a
    elif (a <= b <= c) or (c <= b <= a):
        return b
    return c


def lucky_guess(n: int) -> bool:
    """
    Determine whether the given number gives you points for this task or not.

    The number gives you points if it is:
    * either 1, 3 or 7
    * greater or equal than -6 and smaller or equals than 121 and
      divisible by 13 (-6 and 121 are inclusive)
    * smaller than 0 and does not contain number 5 or 6

    lucky_guess(7)  # True
    lucky_guess(26)  # True
    lucky_guess(-35)  # False

    :param n: given number
    :return: boolean - points or no points
    """
    if n in {1, 3, 7}:
        return True
    elif -6 <= n <= 121 and n % 13 == 0:
        return True
    elif 0 > n and '5' not in str(n) and '6' not in str(n):
        return True
    return False


def without_end(s: str) -> str:
    """
    Given a string, return a version without the first and last char, so "Hello" yields "ell".

    The string length will be at least 2.

    without_end('Hello') → 'ell'
    without_end('java') → 'av'
    without_end('coding') → 'odin'

    :param s: String
    :return: String without first and last char.
    """
    if len(s) < 2:
        return ''
    return s[1:-1]


def non_decreasing_list(nums: list) -> bool:
    """
    Given a list of numbers.

    If given list is a non-decreasing list, return True, otherwise False.
    Non-decreasing means every next element in the list must not be smaller than the previous one.

    non_decreasing_list([0, 1, 2, 3, 98]) => True
    non_decreasing_list([50, 49]) => False
    non_decreasing_list([12, 12]) => True

    :param nums:
    :return:
    """
    if not nums:
        return True

    for i in range(1, len(nums)):
        if nums[i] < nums[i - 1]:
            return False
    return True


def max_duplicate(nums: list) -> int or None:
    """
    Return the largest element which has at least one duplicate.

    If no element has duplicate element (an element with the same value), return None.

    max_duplicate([1, 2, 3]) => None
    max_duplicate([1, 2, 2]) => 2
    max_duplicate([1, 2, 2, 1, 1]) => 2

    :param nums: List of integers
    :return: Maximum element with duplicate. None if no duplicate found.
    """
    freq_dict = {}
    for num in nums:
        if num in freq_dict:
            freq_dict[num] += 1
        else:
            freq_dict[num] = 1
    max_element = None

    for num, freq in freq_dict.items():
        if freq > 1 and (max_element is None or num > max_element):
            max_element = num
    if max_element is not None:
        return max_element
    return None
