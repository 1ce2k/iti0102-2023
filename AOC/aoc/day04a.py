"""AOC DAY 4 part A."""


with open('data.txt', 'r') as file:
    input_data = [line.strip() for line in file]

total_points = 0
# print(input_data)
for line in input_data:
    card_poits = 0
    matching_num_count = 0
    card_num, nums = line.split(':')
    win_nums, all_nums = nums.split('|')
    winning_nums = win_nums.split()
    card_nums = all_nums.split()
    for num in winning_nums:
        if num in card_nums:
            if matching_num_count == 0:
                matching_num_count += 1
                card_poits += 1
            else:
                matching_num_count += 1
                card_poits *= 2
    total_points += card_poits
print(total_points)
