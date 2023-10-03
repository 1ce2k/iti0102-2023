"""Conversation."""
import re
import math

regex_a = '.x2'
regex_b = '.x'
regex_c = '.'


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
        self.biggest_number = biggest_number
        self.possible_answers = set([all_possible_answers for all_possible_answers in range(biggest_number + 1)])

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
        primes = find_primes_in_range(self.biggest_number)
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
        composites = find_composites_in_range(self.biggest_number)
        if is_composite:
            self.intersect_possible_answers(composites)
        else:
            self.exclude_possible_answers(composites)

    def deal_with_dec_value(self, decimal_value: str):
        """
        Filter possible answers to remove all numbers that doesn't have the decimal_value in them.

        :param decimal_value: decimal value within the number like 9 in 192
        """
        self.intersect_possible_answers([x for x in self.possible_answers if decimal_value in str(x)])

    def deal_with_hex_value(self, hex_value: str):
        """
        Filter possible answers to remove all numbers that doesn't have the decimal_value in them.

        :param hex_value: hex value within the number like e in fe2
        """
        # self.intersect_possible_answers([x for x in self.possible_answers if hex_value in str(hex(x))])
        filtered = []
        pattern = r'[0-9a-fA-F]*' + hex_value + r'[0-9a-fA-F]*'
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
        normalize_equation = normalize_quadratic_equation(equation)
        solutions = quadratic_equation_solver(normalize_equation)
        if solutions is None:
            return
        elif isinstance(solutions, float):
            if is_bigger:
                self.intersect_possible_answers([x for x in self.possible_answers if x > solutions])
            else:
                self.intersect_possible_answers([x for x in self.possible_answers if x < solutions])
        elif isinstance(solutions, tuple):
            smaller, larger = solutions
            if is_bigger:
                self.intersect_possible_answers([x for x in self.possible_answers if x > larger])
            else:
                self.intersect_possible_answers([x for x in self.possible_answers if x < smaller])

    def deal_with_fibonacci_sequence(self, is_in: bool):
        """
        Filter possible answers to either keep or remove all fibonacci numbers.

        Call find_fibonacci_numbers to get all fibonacci numbers in range.
        :param is_in: boolean whether the number is in fibonacci sequence or not
        """
        fibonacci_nums = find_fibonacci_numbers(self.biggest_number)
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
        catalan_nums = find_catalan_numbers(self.biggest_number)
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
        filtered = set()
        if increasing and to_be:
            prev_num = None
            for num in sorted(self.possible_answers):
                if prev_num is None or num >= prev_num:
                    filtered.add(num)
                prev_num = num
        elif increasing and not to_be:
            prev_num = None
            for num in sorted(self.possible_answers):
                if prev_num is None or num < prev_num:
                    filtered.add(num)
                prev_num = num
        elif not increasing and to_be:
            prev_num = None
            for num in sorted(self.possible_answers, reverse=True):
                if prev_num is None or num >= prev_num:
                    filtered.add(num)
                prev_num = num
        elif not increasing and not to_be:
            prev_num = None
            for num in sorted(self.possible_answers, reverse=True):
                if prev_num is None or num < prev_num:
                    filtered.add(num)
                prev_num = num
        self.intersect_possible_answers(list(filtered))

        # self.intersect_possible_answers([x for x in self.possible_answers if x >= sorted_answers[0]])
        # self.possible_answers = '1'
        # else:
        #     self.exclude_possible_answers([x for x in self.possible_answers if x < sorted_answers[0]])
        # self.possible_answers = '2'
        # else:
        #     reversed_answers = sorted(self.possible_answers, reverse=True)
        #     if to_be:
        #         self.intersect_possible_answers([x for x in self.possible_answers if x <= self.biggest_number])
        #         self.possible_answers = '3'
        # else:
        #     self.intersect_possible_answers([x for x in self.possible_answers if x <= self.biggest_number])
        # self.possible_answers = '4'


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
    equation = equation.replace(' ', '')
    terms = re.split('([-+=])', equation)
    a, b, c, d = 0, 0, 0, 0
    for term in terms:
        if 'x2' in term:
            if term == 'x2':
                a = 1
            else:
                a = int(term.replace('x2', ''))
        elif 'x' in term:
            if terms[terms.index(term) - 1] == '+':
                if term == 'x':
                    b = 1
                else:
                    b = int(term.replace('x', ''))
            elif terms[terms.index(term) - 1] == '-':
                if term == 'x':
                    b = -1
                else:
                    b = -int(term.replace('x', ''))
        elif term.isdigit() and term != '0':
            if terms[terms.index(term) - 1] == '-':
                c = -int(term)
            elif terms[terms.index(term) - 1] == '+':
                c = int(term)
    if a != 0:
        d = b ** 2 - 4 * a * c
    x1 = 0
    x2 = 0
    if d < 0:
        return None
    if d == 0:
        if a != 0:
            x1 = - b / (2 * a)
            return float(x1)
    if d > 0:
        x1 = (-b + math.sqrt(d)) / (2 * a)
        x2 = (-b - math.sqrt(d)) / (2 * a)

    if x1 == x2:
        return x1
    res = [x1, x2]
    return min(res), max(res)


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
    equation = equation.replace('x1', 'x')
    equation = equation.replace(' ', '')
    lhs, rhs = equation.split('=')

    # init coefficient
    a, b, c = 0, 0, 0

    # split left and right parts to terms
    lhs_terms = re.split(r'([-+])', lhs)
    rhs_terms = re.split(r'([-+])', rhs)

    def process_term(term, sign):
        """Update coefficients by term."""
        nonlocal a, b, c
        if 'x2' in term:
            a += sign * (1 if term == 'x2' else int(term.replace('x2', '')))
        elif 'x' in term or 'x1' in term:
            b += sign * (1 if term in {'x'} else int(term.replace('x', '')))
        elif term.isdigit():
            c += sign * int(term)

    # left part
    sign = 1
    for term in lhs_terms:
        if term == '-':
            sign = -1
        elif term == '+':
            sign = 1
        else:
            process_term(term, sign)

    # right part
    sign = -1
    for term in rhs_terms:
        if term == '-':
            sign = 1
        elif term == '+':
            sign = -1
        else:
            process_term(term, sign)

    # if there is need to multiply by -1
    if a != 0 and a < 0:
        a, b, c = -a, -b, -c
    elif a == 0 and b < 0:
        b, c = -b, -c
    elif a == 0 and b == 0 and c < 0:
        c = -c
    # create normalized equation
    normalized_equation = ''
    if a == 0 and b == 0:
        return f'{c} = 0'
    if a != 0:
        if abs(a) == 1:
            normalized_equation += 'x2'
        else:
            normalized_equation += f'{a}x2'
    if b != 0:
        if a != 0:
            if abs(b) == 1:
                normalized_equation += f' {"+" if b >= 0 else "-"} x'
            else:
                normalized_equation += f' {"+" if b >= 0 else "-"} {abs(b)}x'
        else:
            if abs(b) == 1:
                normalized_equation += 'x'
            else:
                normalized_equation += f"{b}x"
    if c != 0:
        if a != 0 or b != 0:
            normalized_equation += f' {"+" if c >= 0 else "-"} {abs(c)}'
    normalized_equation += ' = 0'
    return normalized_equation


def find_coefficients_for_solver(equation: str) -> tuple:
    """Return coefficients for normalized equation."""
    ret = ()
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
    return [math.comb(2 * i, i) // (i + 1) for i in range(biggest_number + 1)]


if __name__ == '__main__':

    def print_regex_results(regex, f):
        """Return smth."""
        for match in re.finditer(regex, f):
            print(match.group(0))


    # f = "3x2 - 4x + 1"

    # print(print_regex_results(regex_a, f))  # 3
    # print(print_regex_results(regex_b, f))  # - 4
    # print(print_regex_results(regex_c, f))  # 1

    f2 = "3x2 + 4x + 5 - 2x2 - 7x + 4"

    print("x2")
    print_regex_results(regex_a, f2)  # 3, - 2
    print("x")
    print_regex_results(regex_b, f2)  # 4, - 7
    print("c")
    print_regex_results(regex_c, f2)  # 5, 4
