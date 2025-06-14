"""Conversation."""
import re
import math


class Student:
    """Student class which interacts with the server."""

    def __init__(self, biggest_number: int):
        """
        Initialize Student object.

        Save the biggest number into a variable that is attainable later on.
        Create a collection of all possible results [possible_answers] <- don't rename that (can be a list or a set)
        :param biggest_number: the biggest possible number(inclusive) to guess
        NB: calculating using sets is much faster compared to lists
        """
        self.num = biggest_number
        self.possible_answers = set([x for x in range(self.num + 1)])

    def decision_branch(self, sentence: str):
        """
        Regex can and should be used here.

        :param sentence: sentence to solve
        call one of the functions bellow (within this class) and return either one of the following strings:
        if there are multiple opportunities:
        f"Possible answers are {sorted_list_of_possible_answers_in_growing_sequence}."
        if the result is certain
        f"The number I needed to guess was {final_answer}."
        """
        self.deal_with_number_type(sentence)
        if re.search(r"binary form", sentence):
            self.binary_form(sentence)
        if re.search(r"(order)", sentence):
            self.order(sentence)
        if re.search(r'decimal value: "(\d+)"', sentence):
            self.deal_with_dec_value(str(re.search(r'(\d+)', sentence).group(1)))
        if re.search(r'hex value: "\b(?:0[xX])?[\dA-Fa-f]+\b"', sentence):
            self.deal_with_hex_value(re.search(r"\b(?:0[xX])?[\dA-Fa-f]+\b", sentence).group())
        if re.search(r"equation", sentence):
            self.equation(sentence)
        if len(self.possible_answers) == 1:
            final = list(self.possible_answers)[0]
            return f"The num I needed to guess was {final}."
        sorted_list = sorted(self.possible_answers)
        return f"Possible answers are {sorted_list}."

    def binary_form(self, sentence):
        """Deal with binary form, func to make decision branch less complex."""
        if re.search(r'ones', sentence):
            self.deal_with_number_of_ones(int(re.search(r'(\d+)', sentence).group()))
        if re.search(r'zero', sentence):
            self.deal_with_number_of_zeroes(int(re.search(r"(\d+)", sentence).group()))

    def equation(self, sentence):
        """Deal with equation, func to make decision branch less complex."""
        is_bigger = not re.search(r'smaller', sentence)
        to_multiply = not re.search(r'divided', sentence)
        multiplicative = float(re.search(r'[-+]?[\d+]*\.[\d+]+', sentence).group())
        equation = re.search(r'"(.*?)"', sentence).group(1)
        self.deal_with_quadratic_equation(equation, to_multiply, multiplicative, is_bigger)

    def order(self, sentence):
        """Deal with order, func to make decision branch less complex."""
        increasing = not re.search(r'(decreasing)', sentence)
        to_be = not re.search(r"n't|not", sentence)
        self.deal_with_number_order(increasing, to_be)

    def deal_with_number_type(self, sentence):
        """Deal with number type, func to make decision branch less complex."""
        if re.search(r"(prime)", sentence):
            self.deal_with_primes(not re.search(r"not|n't", sentence))
        if re.search(r"(composite)", sentence):
            self.deal_with_composites(not re.search(r"not|n't", sentence))
        if re.search(r"(catalan)", sentence):
            self.deal_with_catalan_sequence(not re.search(r"not|n't", sentence))
        if re.search(r"(fibonacci)", sentence):
            self.deal_with_fibonacci_sequence(not re.search("not|n't", sentence))

    def intersect_possible_answers(self, update: list):
        """
        Logical AND between two sets.

        :param update: new list to be put into conjunction with self.possible_answers
        conjunction between self.possible_answers and update
        https://en.wikipedia.org/wiki/Logical_conjunction
        """
        self.possible_answers &= set(update)

    def exclude_possible_answers(self, update: list):
        """
        Logical SUBTRACTION between two sets.

        :param update: new list to be excluded from self.possible_answers
        update excluded from self.possible_answers
        """
        self.possible_answers -= set(update)

    def deal_with_number_of_zeroes(self, amount_of_zeroes: int):
        """
        Filter possible_answers to match the amount of zeroes in its binary form.

        :param amount_of_zeroes: number of zeroes in the correct number's binary form
        """
        list_of_nums = []
        for i in self.possible_answers:
            if bin(i).count('0') - 1 != amount_of_zeroes:
                list_of_nums.append(i)
        self.exclude_possible_answers(list_of_nums)

    def deal_with_number_of_ones(self, amount_of_ones: int):
        """
        Filter possible answers to match the amount of ones in its binary form.

        :param amount_of_ones: number of zeroes in the correct number's binary form
        """
        num_list = []
        for i in self.possible_answers:
            if bin(i).count('1') != amount_of_ones:
                num_list.append(i)
        self.exclude_possible_answers(num_list)

    def deal_with_primes(self, is_prime: bool):
        """
        Filter possible answers to either keep or remove all primes.

        Call find_primes_in_range to get all composite numbers in range.
        :param is_prime: boolean whether the number is prime or not
        """
        primes = find_primes_in_range(self.num)
        if is_prime:
            self.intersect_possible_answers(primes)
        else:
            self.exclude_possible_answers(primes)

    def deal_with_composites(self, is_composite: bool):
        """
        Filter possible answers to either keep or remove all composites.

        Call find_composites_in_range to get all composite numbers in range.
        :param is_composite: boolean whether the number is composite or not
        """
        composites = find_composites_in_range(self.num)
        if is_composite:
            self.intersect_possible_answers(composites)
        else:
            self.exclude_possible_answers(composites)

    def deal_with_dec_value(self, decimal_value: str):
        """
        Filter possible answers to remove all numbers that doesn't have the decimal_value in them.

        :param decimal_value: decimal value within the number like 9 in 192
        """
        self.exclude_possible_answers([x for x in self.possible_answers if decimal_value not in str(x)])

    def deal_with_hex_value(self, hex_value: str):
        """
        Filter possible answers to remove all numbers that doesn't have the decimal_value in them.

        :param hex_value: hex value within the number like e in fe2
        """
        # self.intersect_possible_answers([x for x in self.possible_answers if hex_value in str(hex(x))])
        filtered = []
        for num in self.possible_answers:
            hex_presentation = hex(num)[2:]
            if hex_value in hex_presentation:
                filtered.append(num)
        self.intersect_possible_answers(filtered)

    def deal_with_quadratic_equation(self, equation: str, to_multiply: bool, multiplicative: float, is_bigger: bool):
        """
        Filter possible answers to remove all numbers that doesn't have the decimal_value in them.

        Regex can be used here.
        Call quadratic_equation_solver with variables a, b, c.
        deal_with_dec_value should be called.
        :param equation: the quadratic equation
        :param to_multiply: whether it is necessary to multiply or divide with a given multiplicative
        :param multiplicative: the multiplicative to multiply or divide with
        :param is_bigger: to use the bigger or smaller result of the quadratic equation(min or max from [x1, x2])
        """
        solutions = quadratic_equation_solver(equation)
        if solutions:
            if to_multiply and is_bigger:
                self.deal_with_dec_value(f'{round(max(solutions) * multiplicative)}')
            elif not to_multiply and is_bigger:
                self.deal_with_dec_value(f'{round(max(solutions) / multiplicative)}')
            elif to_multiply and not is_bigger:
                self.deal_with_dec_value(f'{round(min(solutions) * multiplicative)}')
            elif not to_multiply and not is_bigger:
                self.deal_with_dec_value(f'{round(min(solutions) / multiplicative)}')

    def deal_with_fibonacci_sequence(self, is_in: bool):
        """
        Filter possible answers to either keep or remove all fibonacci numbers.

        Call find_fibonacci_numbers to get all fibonacci numbers in range.
        :param is_in: boolean whether the number is in fibonacci sequence or not
        """
        fibonacci_nums = find_fibonacci_numbers(self.num)
        if is_in:
            self.intersect_possible_answers(fibonacci_nums)
        else:
            self.exclude_possible_answers(fibonacci_nums)

    def deal_with_catalan_sequence(self, is_in: bool):
        """
        Filter possible answers to either keep or remove all catalan numbers.

        Call find_catalan_numbers to get all catalan numbers in range.
        :param is_in: boolean whether the number is in catalan sequence or not
        """
        catalan_nums = find_catalan_numbers(self.num)
        if is_in:
            self.intersect_possible_answers(catalan_nums)
        else:
            self.exclude_possible_answers(catalan_nums)

    def deal_with_number_order(self, increasing: bool, to_be: bool):
        """
        Filter possible answers to either keep or remove all numbers with wrong order.

        :param increasing: boolean whether to check is in increasing or decreasing order
        :param to_be: boolean whether the number is indeed in that order
        """
        filtered_numbers = []
        for num in self.possible_answers:
            # Convert the number to a string to check its order
            num_str = str(num)
            is_increasing = num_str == ''.join(sorted(num_str))
            is_decreasing = num_str == ''.join(sorted(num_str, reverse=True))

            if (increasing and to_be and is_increasing) or (not increasing and to_be and is_decreasing):
                filtered_numbers.append(num)
            elif (increasing and not to_be and not is_increasing) or (
                    not increasing and not to_be and not is_decreasing):
                filtered_numbers.append(num)
        self.intersect_possible_answers(filtered_numbers)


def quadratic_equation_solver(equation: str) -> None or float or tuple:
    """
    Solve the normalized quadratic equation.

    :param equation: quadratic equation
    https://en.wikipedia.org/wiki/Quadratic_formula
    :return:
    if there are no solutions, return None.
    if there is exactly 1 solution, return it.
    if there are 2 solutions, return them in a tuple, where smaller is first
    all numbers are returned as floats.
    """
    # normalize equation
    new_equation = normalize_quadratic_equation(equation)
    # find coefficients
    a, b, c = equation_coefficients(new_equation)
    # calculate discriminant
    d = b ** 2 - 4 * a * c
    # find all solutions for the equation
    if d < 0:
        return None
    if d == 0:
        if a != 0:
            x1 = -b / (2 * a)
            return x1
    if d > 0:
        if a != 0:
            x1 = (-b + math.sqrt(d)) / (2 * a)
            x2 = (-b - math.sqrt(d)) / (2 * a)
            if x2 < x1:
                return x2, x1
            elif x1 > x2:
                return x1, x2
        else:
            x1 = -c / b
            return x1


def normalize_quadratic_equation(equation: str) -> str:
    """
    Normalize the quadratic equation.

    normalize_quadratic_equation("x2 + 2x = 3") => "x2 + 2x - 3 = 0"
    normalize_quadratic_equation("0 = 3 + 1x2") => "x2 + 3 = 0"
    normalize_quadratic_equation("2x + 2 = 2x2") => "2x2 - 2x - 2 = 0"
    normalize_quadratic_equation("0x2 - 2x = 1") => "2x + 1 = 0"
    normalize_quadratic_equation("0x2 - 2x = 1") => "2x + 1 = 0"
    normalize_quadratic_equation("2x2 + 3x - 4 + 0x2 - x1 + 0x1 + 12 - 12x2 = 4x2 + x1 - 2") => "14x2 - x - 10 = 0"

    :param equation: quadratic equation to be normalized
    https://en.wikipedia.org/wiki/Quadratic_formula
    :return: normalized equation
    """
    # split equation to left and right parts
    lhs, rhs = equation.split('=')
    # calculate coefficients
    left_a, left_b, left_c = equation_coefficients(lhs)
    right_a, right_b, right_c = equation_coefficients(rhs)
    a, b, c = left_a - right_a, left_b - right_b, left_c - right_c
    # if it is needed then multiply by -1
    if a < 0:
        a, b, c = -a, -b, -c
    elif a == 0 and b < 0:
        b, c = -b, -c
    elif a == 0 and b == 0 and c < 0:
        c = -c
    # create new equation
    ret = ''
    if a == 0 and b == 0:
        return f'{c} = 0'
    if a != 0:
        ret += 'x2' if a == 1 else f'{a}x2'
    if b != 0 and a != 0:
        ret += f' {"+" if b > 0 else "-"} x' if abs(b) == 1 else f' {"+" if b > 0 else "-"} {abs(b)}x'
    if a == 0 and b != 0:
        ret += 'x' if b == 1 else f'{b}x'
    if c != 0 and (a != 0 or b != 0):
        ret += f' {"+" if c > 0 else "-"} {abs(c)}'
    ret += ' = 0'
    return ret


def find_primes_in_range(biggest_number: int) -> list:
    """
    Find all primes in range(end inclusive).

    :param biggest_number: all primes in range of biggest_number(included)
    https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
    :return: list of primes
    """
    prime = [True for _ in range(biggest_number + 1)]
    p = 2
    while p * p <= biggest_number:
        if prime[p]:
            for i in range(p * p, biggest_number + 1, p):
                prime[i] = False
        p += 1
    # Create a list of prime numbers
    primes = [p for p in range(2, biggest_number + 1) if prime[p]]
    return primes


def find_composites_in_range(biggest_number: int) -> list:
    """
    Find all composites in range(end inclusive).

    Call find_primes_in_range from this method to get all composites
    :return: list of composites
    :param biggest_number: all composites in range of biggest_number(included)
    """
    primes = find_primes_in_range(biggest_number)
    composites = []
    for i in range(2, biggest_number + 1):
        if i not in primes:
            composites.append(i)
    return composites


def find_fibonacci_numbers(biggest_number: int) -> list:
    """
    Find all Fibonacci numbers in range(end inclusive).

    Can be solved using recursion.
    :param biggest_number: all fibonacci numbers in range of biggest_number(included)
    https://en.wikipedia.org/wiki/Fibonacci_number
    :return: list of fibonacci numbers
    """
    fibonacci_sequence = []
    a, b = 0, 1
    while a <= biggest_number:
        fibonacci_sequence.append(a)
        a, b = b, a + b
    return fibonacci_sequence


def find_catalan_numbers(biggest_number: int) -> list:
    """
    Find all Catalan numbers in range(end inclusive).

    Can be solved using recursion.
    :param biggest_number: all catalan numbers in range of biggest_number(included)
    https://en.wikipedia.org/wiki/Catalan_number
    :return: list of catalan numbers
    """
    ret = []
    for x in range(biggest_number):
        catalan_number = math.factorial(2 * x) / (math.factorial(x) * math.factorial(x + 1))
        print(catalan_number)
        if catalan_number <= biggest_number:
            ret.append(int(catalan_number))
        else:
            break
    return ret


def equation_coefficients(equation: str):
    """Return equation coefficients."""
    matches_a = re.findall(regex_a, equation)
    matches_b = re.findall(regex_b, equation)
    matches_c = re.findall(regex_c, equation)
    a, b, c = 0, 0, 0
    for match_a in matches_a:
        match = match_a.replace(' ', '')
        if match == '-':
            a -= 1
        elif not match:
            a += 1
        else:
            a += int(match)
    for match_b in matches_b:
        match = match_b.replace(' ', '')
        if match == '-':
            b -= 1
        elif not match:
            b += 1
        else:
            b += int(match)
    for match_c in matches_c:
        match = match_c.replace(' ', '')
        if match == '-':
            c -= 1
        elif not match:
            c += 1
        else:
            c += int(match)
    return a, b, c


# regex pattern to find coefficients a, b, c
regex_a = r'\s*(-?\s*\d*|-)\s*x2(?![0-9])'
regex_b = r'\s*(-?\s*\d*|-)\s*x1?(?![0-9])'
regex_c = r'(?<!x)(?<!x1>)(?<!x2)\s*(-?\s*\d+)(?=\s|$)'
