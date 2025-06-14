"""KT2."""


def switch_lasts_and_firsts(s: str) -> str:
    """
    Move last two characters to the beginning of string and first two characters to the end of string.

    When string length is smaller than 4, return reversed string.

    switch_lasts_and_firsts("ambulance") => "cebulanam"
    switch_lasts_and_firsts("firetruck") => "ckretrufi"
    switch_lasts_and_firsts("car") => "rac"

    :param s:
    :return: modified string
    """
    if not s:
        return ''
    if len(s) < 4:
        return s[::-1]
    return s[-2:] + s[2:-2] + s[:2]


def min_diff(nums: list) -> int:
    """
    Find the smallest diff between two integer numbers in the list.

    The list will have at least 2 elements.

    min_diff([1, 2, 3]) => 1
    min_diff([1, 9, 17]) => 8
    min_diff([100, 90]) => 10
    min_diff([1, 100, 1000, 1]) => 0

    :param nums: list of ints, at least 2 elements.
    :return: min diff between 2 numbers.
    """
    if len(nums) < 2:
        return 0
    nums.sort(reverse=True)
    differences = [nums[i] - nums[i + 1] for i in range(len(nums) - 1)]
    return min(differences)


def get_symbols_by_occurrences(text: str) -> dict:
    """
    Return dict where key is the occurrence count and value is a list of corresponding symbols.

    The order of the counts and the symbols is not important.

    get_symbols_by_occurrences("hello") => {1: ['e', 'o', 'h'], 2: ['l']}
    get_symbols_by_occurrences("abcaba") => {2: ['b'], 1: ['c'], 3: ['a']}
    """
    if not text:
        return {}

    final_dict = {}
    for x in text:
        num = text.count(x)
        if num not in final_dict:
            final_dict[num] = []
        if x not in final_dict[num]:
            final_dict[num].append(x)
    return final_dict


def sum_of_digits_recursion(s: str) -> int:
    """
    Return sum of all the digits.

    The input string contains different symbols.
    Sum all the digits.

    The function has to be recursive (no loops allowed).

    sum_of_digits_recursion("123") => 6
    sum_of_digits_recursion("a") => 0
    sum_of_digits_recursion("") => 0
    sum_of_digits_recursion("1-2-3-99") => 24
    """
    if not s:
        return 0
    if s[0].isdigit():
        return int(s[0]) + sum_of_digits_recursion(s[1:])
    return sum_of_digits_recursion(s[1:])


if __name__ == '__main__':
    print(switch_lasts_and_firsts("ambulance"))  # => "cebulanam"
    print(switch_lasts_and_firsts("firetruck"))  # => "ckretrufi"
    print(switch_lasts_and_firsts("car"))  # => "rac"

    print(min_diff([1, 2, 3]))  # => 1
    print(min_diff([1, 9, 17]))  # => 8
    print(min_diff([100, 90]))  # => 10
    print(min_diff([1, 100, 1000, 1]))  # => 0

    print(get_symbols_by_occurrences("hello"))  # => {1: ['e', 'o', 'h'], 2: ['l']}
    print(get_symbols_by_occurrences("abcaba"))  # => {2: ['b'], 1: ['c'], 3: ['a']}

    print(sum_of_digits_recursion("123"))  # 6
    print(sum_of_digits_recursion(""))  # 0
