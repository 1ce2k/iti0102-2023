import re

red_max, green_max, blue_max = 12, 13, 14
red_min, green_min, blue_min = 0, 0, 0

with open('data.txt', 'r') as file:
    input_data = file.readlines()

def count_possible_games_by_max_values():
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
    return max([int(x) for x in re.findall(pattern, line)])

def is_game_possible_min_value(max_count, min_count):
    return min_count <= max_count


def min_cubes_for_game():
    count = 0
    for line in input_data:
        print(line)
        red_cubes = count_max_cubes(r'(\d+) red', line)
        green_cubes = count_max_cubes(r'(\d+) green', line)
        blue_cubes = count_max_cubes(r'(\d+) blue', line)
        count += red_cubes * green_cubes * blue_cubes
    return count

print(min_cubes_for_game())
