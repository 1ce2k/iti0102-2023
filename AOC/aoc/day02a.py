"""AOC DAY 2 part A."""

import re

red_max, green_max, blue_max = 12, 13, 14
red_min, green_min, blue_min = 0, 0, 0

with open('../day2/data.txt', 'r') as file:
    input_data = file.readlines()


def count_possible_games_by_max_values():
    """Count possible games."""
    count = 0
    for line in input_data:
        id = int(re.search(r'Game (\d+)', line).group(1))
        red_cubes = count_max_cubes(r'(\d+) red', line)
        green_cubes = count_max_cubes(r'(\d+) green', line)
        blue_cubes = count_max_cubes(r'(\d+) blue', line)
        if red_cubes <= red_max and green_cubes <= green_max and blue_cubes <= blue_max:
            count += id
    return count


def count_max_cubes(pattern, line):
    """Count max amount of cubes per time during game were shown."""
    return max([int(x) for x in re.findall(pattern, line)])


print(count_possible_games_by_max_values())
