"""If you're going to perform recursion, you need to use recursion."""


def loop_reverse(string: str) -> str:
    """
    Reverse a string using a loop or string slicing.

    loop_reverse("hey") => "yeh"
    loop_reverse("aaa") => "aaa"
    loop_reverse("") => ""
    loop_reverse("1") => "1"

    :param string: input string
    :return: reversed input string
    """
    if not string:
        return ''
    return string[::-1]


def recursive_reverse(string: str) -> str:
    """
    Reverse a string using recursion.

    recursive_reverse("hey") => "yeh"
    recursive_reverse("aaa") => "aaa"
    recursive_reverse("") => ""
    recursive_reverse("1") => "1"

    :param string: input string
    :return: reversed input string
    """
    if len(string) <= 1:
        return string
    return recursive_reverse(string[1:]) + string[0]


def loop_sum(num: int) -> int:
    """
    Calculate the sum of all numbers up to 'num' (including 'num') using a loop.

    loop_sum(0) => 0
    loop_sum(3) => 6
    loop_sum(5) => 15

    :param num: the last number to add to the sum.
    :return: sum of integers from 0 up to given number.
    """
    sum = 0
    for i in range(num + 1):
        sum += i
    return sum


def recursive_sum(num: int) -> int:
    """
    Calculate the sum of all numbers up to 'num' (including 'num') using recursion.

    loop_sum(0) => 0
    loop_sum(3) => 6
    loop_sum(5) => 15

    :param num: the last number to add to the sum.
    :return: sum of integers from 0 up to given number.
    """
    if num == 0:
        return 0
    return num + recursive_sum(num - 1)


def loop_factorial(num: int) -> int:
    """
    Calculate the factorial of an integer 'num' using a loop.

    loop_factorial(0) => 1
    loop_factorial(5) => 120
    loop_factorial(7) => 5040
    loop_factorial(-1) => -1
    loop_factorial(-5) => -1

    :param num: integer from which the factorial should be calculated.
    :return: factorial of given number
    """
    if num < 0:
        return -1
    elif num == 1:
        return 1
    result = 1
    for i in range(1, num + 1):
        result *= i
    return result


def recursive_factorial(num: int) -> int:
    """
    Calculate the factorial of an integer 'num' using recursion.

    loop_factorial(0) => 1
    loop_factorial(5) => 120
    loop_factorial(7) => 5040
    loop_factorial(-1) => -1
    loop_factorial(-5) => -1

    :param num: integer from which the factorial should be calculated.
    :return: factorial of given number
    """
    if num < 0:
        return -1
    elif num == 0:
        return 1
    return num * recursive_factorial(num - 1)


def check_palindrome(string: str) -> bool:
    """
    Check if the input 'string' is a palindrome using recursion.

    A palindrome is a word that is spelled exactly the same way when read regularly
    or in reverse.

    check_palindrome("kirik") => True
    check_palindrome("horror") => False
    check_palindrome("0546450") => True
    check_palindrome("-") => True
    check_palindrome("") => True

    :param string: string argument
    :return: boolean. True if 'string' is a palindrome, False otherwise
    """
    if len(string) <= 1:
        return True
    return check_palindrome(string[1:-1]) if string[0] == string[-1] else False


def check_for_prime(num: int, i=None) -> bool:
    """
    Check if input number 'num' is a prime number using recursion.

    check_for_prime(0) => False
    check_for_prime(1) => False
    check_for_prime(997) => True

    Solution
    :param num: integer to be checked
    :param i: used to check if 'num' is a multiple of some integer.
    :return: boolean. True if 'num' is prime, False otherwise
    """
    if num < 2:
        return False
    if i is None:
        i = 2
    if i * i > num:
        return True
    if num % i == 0:
        return False
    return check_for_prime(num, i + 1)


def replace(input_string: str, char_to_replace: str, new_string: str) -> str:
    """
    Replace all occurrences of some specific character 'char_to_replace' in string 'input_string' with 'new_string'.

    Argument 'new_string' can be any length, 'char_to_replace' must be of length 1.
    If length of 'char_to_replace' is not equal to 1, return "Length of char_to_replace must be one character!".
    If 'input_string' is an emtpy string, return "".

    Solution must be recursive!

    replace("", "", "") => "Length of char_to_replace must be one character!"
    replace("", "6", "9") => ""
    replace("hello ", " ", " world!") => "hello world!"
    replace("aabitsamees", "e", "E") => "aabitsamEEs"
    replace("randOMSTRing123", "n", "mgm") => "ramgmdOMSTRimgmg123"
    replace("WhatStringIsThis???", "", "ii") => "Length of char_to_replace must be one character!"
    replace("WhatStringIsThis???", "in", "i") => "Length of char_to_replace must be one character!"


    :param input_string: input string
    :param char_to_replace: character, whose occurences will be replaced
    :param new_string: string of characters that will replace all occurences of 'char_to_replace'
    :return: input string with all 'char_to_replace' characters replaced with 'new_string'-s
    """
    if len(char_to_replace) != 1:
        return "Length of char_to_replace must be one character!"

    if not input_string:
        return ''

    if input_string[0] == char_to_replace:
        return new_string + replace(input_string[1:], char_to_replace, new_string)
    return input_string[0] + replace(input_string[1:], char_to_replace, new_string)


def fibonacci(num: int, fib_list=None) -> list | None:
    """
    Return a list of length 'num' of Fibonacci numbers using recursion.

    If 'num' is less than zero, return None.
    If 'num' is less than two return a list of the initial two Fibonacci numbers.

    fibonacci(-1) => None
    fibonacci(0) => [0, 1]
    fibonacci(1) => [0, 1]
    fibonacci(9) => [0, 1, 1, 2, 3, 5, 8, 13, 21]

    :param num: integer. The length of the list of Fibonacci numbers to return
    :param fib_list: used to pass the currently computed list on numbers
    :return: list of the first 'num' Fibonacci numbers
    """
    if num < 0:
        return None
    if num < 2:
        return [0, 1]
    if fib_list is None:
        fib_list = [0, 1]
    if len(fib_list) < num:
        next_fib = fib_list[-1] + fib_list[-2]
        fib_list.append(next_fib)
        return fibonacci(num, fib_list)
    return fib_list


def x_sum_loop(nums: list, x: int) -> int:
    """
    Given list 'nums' and a number called 'x' iteratively return sum of every x'th number in the list 'nums'.

    In this task "indexing" starts from 1, so if 'x' = 2 and 'nums' = [2, 3, 4, -9], the output should be -6 (3 + -9).
    'X' can also be negative, in that case indexing starts from the end of 'nums', see examples below.
    If 'x' is 0, the sum should be 0 as well.

    print(x_sum_loop([], 3))  # 0
    print(x_sum_loop([2, 5, 6, 0, 15, 5], 3))  # 11
    print(x_sum_loop([0, 5, 6, -5, -9, 3], 1))  # 0
    print(x_sum_loop([43, 90, 115, 500], -2))  # 158
    print(x_sum_loop([1, 2], -9))  # 0
    print(x_sum_loop([2, 3, 6], 5))  # 0
    print(x_sum_loop([6, 5, 3, 2, 9, 8, 6, 5, 4], 3))  # 15

    :param nums: list of integers
    :param x: number indicating every which num to add to sum
    :return: sum of every x'th number in the list
    """
    if not nums or x == 0:
        return 0
    total = 0
    if x > 0:
        return sum(nums[i - 1] for i in range(x, len(nums) + 1, x))
    else:
        nums = nums[::-1]
        total = 0
        for i in range(abs(x), len(nums) + 1, abs(x)):
            total += nums[i - 1]
        return total


def x_sum_recursion(nums: list, x: int) -> int:
    """
    Given list 'nums' and a number called 'x' recursively return sum of every x'th number in 'nums'.

    In this task "indexing" starts from 1, so if 'x' = 2 and 'nums' = [2, 3, 4, -9], the output should be -6 (3 + -9).
    'X' can also be negative, in that case indexing starts from the end of 'nums', see examples below.
    If 'x' is 0, the sum should be 0 as well.

    print(x_sum_recursion([], 3))  # 0
    print(x_sum_recursion([2, 5, 6, 0, 15, 5], 3))  # 11
    print(x_sum_recursion([0, 5, 6, -5, -9, 3], 1))  # 0
    print(x_sum_recursion([43, 90, 115, 500], -2))  # 158
    print(x_sum_recursion([1, 2], -9))  # 0
    print(x_sum_recursion([2, 3, 6], 5))  # 0
    print(x_sum_recursion([6, 5, 3, 2, 9, 8, 6, 5, 4], 3))  # 15

    :param nums: list of integers
    :param x: number indicating every which num to add to sum
    :return: sum of every x'th number in the list
    """
    if not nums:
        return 0
    if x == 0:
        return 0
    if x > 0:
        if x <= len(nums):
            return nums[x - 1] + x_sum_recursion(nums[x:], x)
        return 0
    if -x <= len(nums):
        return nums[x] + x_sum_recursion(nums[:x], x)
    return 0


def sum_squares(nested_list: list | int) -> int:
    """
    Write a function that sums squares of numbers in 'nested_list' using recursion.

    'nested_list' may contain additional lists.
    (Hint use the type() or isinstance() function)

    sum_squares([1, 2, 3]) -> 14
    sum_squares([[1, 2], 3]) -> sum_squares([1, 2]) + 9 -> 1 + 4 + 9 -> 14
    sum_squares([[[[[[[[[2]]]]]]]]]) -> 4

    :param nested_list: list of lists of lists of lists of lists ... and ints
    :return: sum of squares
    """
    # total = 0
    # for item in nested_list:
    #     if isinstance(item, int):
    #         total += item ** 2
    #     elif isinstance(item, list):
    #         total += sum_squares(item)
    # return total
    if isinstance(nested_list, int):
        return nested_list ** 2
    if not nested_list:
        return 0
    head, *rest = nested_list
    return sum_squares(head) + sum_squares(rest)


if __name__ == '__main__':
    # print("\nloop reverse:")
    # print(loop_reverse("hey"))  # => "yeh"
    # print(loop_reverse("aaa"))  # = > "aaa"
    # print(loop_reverse(""))  # = > ""
    # print(loop_reverse("1"))  # = > "1"
    #
    # print("\nrecursive reverse:")
    # print(recursive_reverse("hey"))  # = > "yeh"
    # print(recursive_reverse("aaa"))  # = > "aaa"
    # print(recursive_reverse(""))  # = > ""
    # print(recursive_reverse("1"))  # = > "1"
    #
    # print("\nloop sum:")
    # print(loop_sum(0))  # = > 0
    # print(loop_sum(3))  # = > 6
    # print(loop_sum(5))  # = > 15
    #
    # print("\nrecursive sum:")
    # print(loop_sum(0))  # = > 0
    # print(loop_sum(3))  # = > 6
    # print(loop_sum(5))  # = > 15
    #
    # print("\nloop factorial:")
    # print(loop_factorial(0))  # = > 1
    # print(loop_factorial(5))  # = > 120
    # print(loop_factorial(7))  # = > 5040
    # print(loop_factorial(-1))  # = > -1
    # print(loop_factorial(-5))  # = > -1
    #
    # print("\nrecursive factorial:")
    # print(recursive_factorial(0))  # = > 1
    # print(recursive_factorial(5))  # = > 120
    # print(recursive_factorial(7))  # = > 5040
    # print(recursive_factorial(-1))  # = > -1
    # print(recursive_factorial(-5))  # = > -1
    #
    # print("\ncheck palindrome:")
    # print(check_palindrome("kirik"))  # = > True
    # print(check_palindrome("horror"))  # = > False
    # print(check_palindrome("0546450"))  # = > True
    # print(check_palindrome("-"))  # = > True
    # print(check_palindrome(""))  # = > True
    #
    # print("\ncheck for prime:")
    # print(check_for_prime(0))  # = > False
    # print(check_for_prime(1))  # = > False
    # print(check_for_prime(997))  # = > True
    #
    # print("\nreplace:")
    # print(replace("", "", ""))  # = > "Length of char_to_replace must be one character!"
    # print(replace("", "6", "9"))  # = > ""
    # print(replace("hello ", " ", " world!"))  # = > "hello world!"
    # print(replace("aabitsamees", "e", "E"))  # = > "aabitsamEEs"
    # print(replace("randOMSTRing123", "n", "mgm"))  # = > "ramgmdOMSTRimgmg123"
    # print(replace("WhatStringIsThis???", "", "ii"))  # = > "Length of char_to_replace must be one character!"
    # print(replace("WhatStringIsThis???", "in", "i"))  # = > "Length of char_to_replace must be one character!"
    #
    # print("\nfibonacci:")
    # print(fibonacci(-1))  # = > None
    # print(fibonacci(0))  # = > [0, 1]
    # print(fibonacci(1))  # = > [0, 1]
    # print(fibonacci(9))  # = > [0, 1, 1, 2, 3, 5, 8, 13, 21]
    #
    print("\nx sum loop:")
    print(x_sum_loop([], 3))  # 0
    print(x_sum_loop([2, 5, 6, 0, 15, 5], 3))  # 11
    print(x_sum_loop([0, 5, 6, -5, -9, 3], 1))  # 0
    print(x_sum_loop([43, 90, 115, 500], -2))  # 158
    print(x_sum_loop([1, 2], -9))  # 0
    print(x_sum_loop([2, 3, 6], 5))  # 0
    print(x_sum_loop([6, 5, 3, 2, 9, 8, 6, 5, 4], 3))  # 15

    print("\nx sum recursion:")
    print(x_sum_recursion([], 3))  # 0
    print(x_sum_recursion([2, 5, 6, 0, 15, 5], 3))  # 11
    print(x_sum_recursion([0, 5, 6, -5, -9, 3], 1))  # 0
    print(x_sum_recursion([43, 90, 115, 500], -2))  # 158
    print(x_sum_recursion([1, 2], -9))  # 0
    print(x_sum_recursion([2, 3, 6], 5))  # 0
    print(x_sum_recursion([6, 5, 3, 2, 9, 8, 6, 5, 4], 3))  # 15

    print("\nsum squares:")
    print(sum_squares([1, 2, 3]))  # -> 14
    print(sum_squares([[1, 2], 3]))  # -> sum_squares([1, 2]) + 9 -> 1 + 4 + 9 -> 14
    print(sum_squares([[[[[[[[[2]]]]]]]]]))  # -> 4
