"""AOC DAY 4 part A."""
import re

"""Card 1: 4 matching => one copy of cards: 2, 3, 4, 5
Card 2: 2 matching => card 2 amount copies of cards: 3, 4
Card 3: 2 matching => card 3 amount copies of cards: 4, 5
Card 4: 1 matching => card 4 amount copies of cards: 5
Card 5: 0 matching => 0 copies
Card 6: 0 matching => 0 copies

Copys:
Card 1: 1
Card 2: 2
Card 3: 4
Card 4: 8
Card 5: 14
Card 6: 1

sum of copies = 1 + 2 + 4 + 8 + 14 + 1 = 30"""

with open('data.txt', 'r') as file:
    input_data = [line.strip() for line in file]


def create_dict_of_card_count():
    """Create dict with instance cards."""
    card_dict = {}
    for line in input_data:
        card_id = int(re.search(r'Card\s+(\d+):', line).group(1))
        if card_id not in card_dict:
            card_dict[card_id] = 1
    return card_dict


def count_cpoies():
    """Modify dict of cards, adding copies."""
    card_count_dict = create_dict_of_card_count()
    for line in input_data:
        card_id = int(re.search(r'Card\s+(\d+):', line).group(1))
        part1, nums = line.split(':')
        win_nums = nums.split('|')[0].split()
        all_nums = nums.split('|')[1].split()
        matching_cards = 0
        for num in win_nums:
            if num in all_nums:
                matching_cards += 1
        card_count = card_count_dict[card_id]
        for x in range(1, matching_cards + 1):
            card_count_dict[card_id + x] += 1 * card_count
    return card_count_dict


def sum_of_copies():
    """Find sum of copies."""
    count = 0
    card_dict = count_cpoies()
    for card, total in card_dict.items():
        count += total
    return count


print(sum_of_copies())
