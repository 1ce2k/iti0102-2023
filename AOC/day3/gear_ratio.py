import re

input = """
467#..114.
#645..114.
...*......
..35..633.
"""
# output should be 467 + 645 + 35 = 1147

input_grid = [re.sub(r'[^a-zA-Z0-9.]', '#', line) for line in input.split()]
# print(input_grid)
count = 0
line_nums = []


def find_largest_number_at_index(s, index):
    max_start = index
    max_end = index
    for i in range(index, 0, -1):
        if s[i].isdigit():
            max_start -= 1
        elif not s[i].isdigit():
            break
    for i in range(index, len(s)):
        if s[i].isdigit():
            max_end += 1
        else:
            break
    if s[max_start].isdigit() and s[max_end - 1].isdigit():
        return int(s[max_start:max_end])
    elif not s[max_start].isdigit() and s[max_end - 1].isdigit():
        return int(s[max_start+1:max_end])


print(find_largest_number_at_index(input_grid[0], 2))  # 467
print(find_largest_number_at_index(input_grid[0], 8))  # 114
print(find_largest_number_at_index(input_grid[1], 1))  # 645


list_of_nums = []
for i in range(len(input_grid)):
    for x in range(len(input_grid[0])):
        if input_grid[i][x].isdigit() and input_grid[i][x + 1] == '#':
            list_of_nums.append(find_largest_number_at_index(input_grid[i], x))
        elif input_grid[i][x].isdigit() and input_grid[i][x - 1] == '#':
            print(i)
            print(x)
            list_of_nums.append(find_largest_number_at_index(input_grid[i], x))

print(list_of_nums)