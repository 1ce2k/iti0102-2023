"""Whether bees meet."""


def do_bees_meet(honeycomb_width: int, honeyhopper_data: str, pollenpadle_data: str) -> bool:
    """Return whether bees meet."""
    if not honeycomb_width > 0 or len(honeyhopper_data.split(',')) < 4 or len(pollenpadle_data.split(',')) < 4:
        raise ValueError("Insufficient data for sequence identification")
    #
    # def movement_pattern(sequence):
    #     end = len(sequence)
    #     for i in range(2, end):
    #         # arithmetic sequence
    #         if sequence[end - 1] - sequence[end - 2] == sequence[i] - sequence[i - 1] == sequence[1] - sequence[0]:
    #             return sequence[1] - sequence[0]
    #         # geometric sequence
    #         elif sequence[end - 1] / sequence[end - 2] == sequence[i] / sequence[i - 1] == sequence[1] / sequence[0]:
    #             return sequence[1] / sequence[0]
    #         # sequence where different is in geometrical sequence 1,3,7,15
    #         elif int(sequence[end - 1] - sequence[end - 2]) == int(sequence[i] - sequence[i - 1]) * i ==\
    #                 int(sequence[1] - sequence[0]) * i * i:
    #             return
    #         # sequence where different is in arithmetic sequence 1,2,4,7 or 5,9,17,29
    #         elif sequence[1] - sequence[0] == (sequence[i] - sequence[i - 1]) / i ==\
    #                 (sequence[end - 1] - sequence[end - 2]) / (end - 1):
    #             return sequence[1] - sequence[0]
    #         else:
    #             raise ValueError("Insufficient data for sequence identification")
    #
    # comb_length = int(honeycomb_width / 2) + 1
    # count = comb_length
    # while comb_length < honeycomb_width:
    #     count = count + comb_length + 1
    #     comb_length += 1
    # count = count * 2 - honeycomb_width
    # print(count)
    #
    # honey_moves = list(map(int, honeyhopper_data.split(',')))
    # pollen_moves = list(map(int, pollenpadle_data.split(',')))
    # honey_pattern = movement_pattern(honey_moves)
    # pollen_pattern = movement_pattern(pollen_moves)
    # print(honey_pattern, pollen_pattern)
    #
    # honey_step = 0
    # pollen_step = 0
    #
    #
    # return False
    return False


print(do_bees_meet(3, '1,2,3,4', '1,2,4,8'))  # =>7, 0, 1, False
print(do_bees_meet(3, '1,2,3,4', '5,9,17,33'))  # =>7, 0, 2, False
print(do_bees_meet(3, '1,2,3,4', '1,2,4,7'))  # =>7, 0, 3, False
