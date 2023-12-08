"""AOC DAY 1 part A."""


def trebuchet(file) -> int:
    """Return sum of numbers."""
    with open(file, 'r') as file:
        data = file.readlines()
        print(data)
    data[-1] = data[-1] + '\n'
    numbers = []
    for line in data:
        print(line)
        res = find_first_digit(line) + find_last_digit(line)
        print(res)
        numbers.append(int(res))
    return sum(numbers)


def find_last_digit(s):
    """Find last digit."""
    for x in s[::-1]:
        if x.isdigit():
            return x


def find_first_digit(s):
    """Find last digit."""
    for x in s:
        if x.isdigit():
            return x
