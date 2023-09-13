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
    #         if sequence[end - 1] - sequence[end - 2] == sequence[i] - sequence[i - 1] == sequence[1] - sequence[0] != 0:
    #             print(0)
    #             return 0
    #         # if one is not moving
    #         elif sequence[i] - sequence[i - 1] == sequence[1] - sequence[0] == sequence[end - 1] - sequence[end - 2] == 0:
    #             print(1)
    #             return 1
    #         # geometric sequence
    #         elif sequence[end - 1] / sequence[end - 2] == sequence[i] / sequence[i - 1] == sequence[1] / sequence[0]:
    #             print(2)
    #             return 2
    #         # sequence where different is in geometrical sequence 1,3,7,15
    #         elif int(sequence[end - 1] - sequence[end - 2]) == int(sequence[i] - sequence[i - 1]) * i == \
    #                 int(sequence[1] - sequence[0]) * i * i:
    #             print(3)
    #             return 3
    #             # sequence where different is in arithmetic sequence 1,2,4,7 or 5,9,17,29
    #         elif sequence[1] - sequence[0] == (sequence[i] - sequence[i - 1]) / i == \
    #                 (sequence[end - 1] - sequence[end - 2]) / (end - 1):
    #             print(4)
    #             return 4
    #
    #         else:
    #             raise ValueError("Insufficient data for sequence identification")
    #
    # honey_moves = list(map(int, honeyhopper_data.split(',')))
    # pollen_moves = list(map(int, pollenpadle_data.split(',')))
    # honey_pattern = movement_pattern(honey_moves)
    # pollen_pattern = movement_pattern(pollen_moves)
    #
    # comb_length = int(honeycomb_width / 2) + 1
    # count = comb_length
    # while comb_length < honeycomb_width:
    #     count = count + comb_length + 1
    #     comb_length += 1
    # count = count * 2 - honeycomb_width
    # honey_pos = 0
    # pollen_pos = count
    #
    # if honey_pattern == 0:
    #     if pollen_pattern == 0:
    #         if honey_pos == pollen_pos:
    #             return True
    # if honey_pattern == 4 or pollen_pattern == 4:
    #     return True

    # Parse movement data strings into lists of integers
    honeyhopper_moves = [int(x) for x in honeyhopper_data.split(',')]
    pollenpaddle_moves = [int(x) for x in pollenpadle_data.split(',')]

    # Initialize starting positions of both bees
    honeyhopper_position = (0, 0)
    pollenpaddle_position = (0, 0)

    # Iterate through movement data for both bees
    for h_move, p_move in zip(honeyhopper_moves, pollenpaddle_moves):
        # Update positions based on movement data
        honeyhopper_position = (honeyhopper_position[0] + h_move, honeyhopper_position[1] + h_move)
        pollenpaddle_position = (pollenpaddle_position[0] + p_move, pollenpaddle_position[1] + p_move)

        # Check if they land on the same hex
        if honeyhopper_position == pollenpaddle_position:
            return True

    # If they never land on the same hex, return False
    return False

    return False


print(do_bees_meet(3, '1,2,3,4', '1,2,3,4'))  # =>7, 0, 1, False
print(do_bees_meet(3, '1,2,3,4', '5,9,17,33'))  # =>7, 0, 2, False
print(do_bees_meet(3, '1,2,3,4', '1,2,4,7'))  # =>7, 0, 3, False
print(do_bees_meet(3, '0,0,0,0', '1,2,4,7'))  # =>7, 0, 3, False
