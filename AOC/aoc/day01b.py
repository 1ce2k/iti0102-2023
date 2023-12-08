"""AOC DAY 1 part B."""


def trebuchet(file) -> int:
    """Return sum of numbers."""
    with open(file, 'r') as file:
        data = file.readlines()
        # print(data)
    data[-1] = data[-1] + '\n'
    numbers = []
    for line in data:
        print(line)
        res = find_first_digit(line) + find_last_digit(line, 2)
        numbers.append(int(res))

    return sum(numbers)


def find_last_digit(s, index_to_start):
    """Find last digit."""
    word_to_num = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7',
                   'eight': '8', 'nine': '9'}
    last_num = ''

    for i in range(len(s), -1, -1):
        for j in range(len(s), 0, -1):
            if s[i:j] in word_to_num.keys():
                last_num = word_to_num[s[i:j]]
                return last_num
            elif s[i:j].isdigit():
                return s[i:j]


def find_first_digit(s):
    """Find first digit."""
    word_to_num = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7',
                   'eight': '8', 'nine': '9'}
    # Get the first and last characters
    first_num = ''

    for i in range(len(s)):
        for j in range(1, len(s)):
            if s[i:j] in word_to_num.keys():
                first_num = word_to_num[s[i:j]]
                return first_num
            elif s[i:j].isdigit():
                return s[i:j]
