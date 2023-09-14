"""Test bees."""


def do_bees_meet(honeycomb_width: int, honey_hopper_data: str, pollen_paddle_data: str) -> bool:
    """Return whether bees meet."""
    # Validate the input
    if not honeycomb_width >= 3 or len(honey_hopper_data.split(',')) < 4 or len(pollen_paddle_data.split(',')) < 4:
        raise ValueError("Insufficient data for sequence identification")

    # Parse input
    honey_hopper_positions = list(map(int, honey_hopper_data.split(',')))
    pollen_paddle_positions = list(map(int, pollen_paddle_data.split(',')))

    # Analyze movement pattern
    honey_hopper_pattern = analyze_movement_pattern(honey_hopper_positions)
    pollen_paddle_pattern = analyze_movement_pattern(pollen_paddle_positions)

    honey_comb_size = calculate_honeycomb_size(honeycomb_width)
    h_start_pos = honey_hopper_positions[0]
    p_start_pos = 0
    if pollen_paddle_positions[0] == 1:
        p_start_pos = honey_comb_size
    else:
        p_start_pos = honey_comb_size - pollen_paddle_positions[0]
    # Calculate position
    honey_hopper_hex_positions = calculate_position(honey_hopper_positions, h_start_pos, honey_hopper_pattern, honey_comb_size, 'h')
    pollen_paddle_hex_positions = calculate_position(pollen_paddle_positions, p_start_pos, pollen_paddle_pattern, honey_comb_size, 'p')

    # Check gor intersection
    for x in range(len(honey_hopper_hex_positions)):
        for i in range(len(pollen_paddle_hex_positions)):
            if honey_hopper_hex_positions[x] == pollen_paddle_hex_positions[i]:
                return True
    return False


def calculate_honeycomb_size(honeycomb_width) -> int:
    """Return size of honey comb."""
    if honeycomb_width <= 0:
        return 0
    cells_count = 0
    for i in range(honeycomb_width):
        cells_count = cells_count + honeycomb_width + i
    cells_count = cells_count * 2 - (2 * honeycomb_width - 1)
    return cells_count


def analyze_movement_pattern(sequence):
    """Return position pattern."""
    end = len(sequence)
    for i in range(2, end):
        # arithmetic sequence
        if sequence[end - 1] - sequence[end - 2] == sequence[i] - sequence[i - 1] == sequence[1] - sequence[0] != 0:
            return 0
        # if one is not moving
        elif all(sequence[i] == sequence[0] for i in range(1, len(sequence))):
            return 1
        # geometric sequence
        elif sequence[end - 1] / sequence[end - 2] == sequence[i] / sequence[i - 1] == sequence[1] / sequence[0]:
            return 2
        # sequence where different is in geometrical sequence 1,3,7,15
        elif int(sequence[end - 1] - sequence[end - 2]) == int(sequence[i] - sequence[i - 1]) * i == int(sequence[1] - sequence[0]) * i * i:
            return 3
        # sequence where different is in arithmetic sequence 1,2,4,7 or 5,9,17,29
        elif sequence[1] - sequence[0] == (sequence[i] - sequence[i - 1]) / i == (sequence[end - 1] - sequence[end - 2]) / (end - 1):
            return 4
        else:
            raise ValueError("Insufficient data for sequence identification")


def calculate_position(positions, start_pos, pattern, comb_size, who):
    """Calculate bee positions"""
    calculated_positions = []

    # calculate difference and ratio for sequence
    d = positions[1] - positions[0]
    q = positions[1] / positions[0]

    # calculate for arithmetic
    if pattern == 0:
        for n in range(1, comb_size + 1):
            position = start_pos + (-1 if who == 'p' else 1) * d * (n - 1)
            calculated_positions.append(position % comb_size or comb_size)

    # calculate for not moving
    elif pattern == 1:
        for n in range(1, comb_size + 1):
            position = start_pos
            calculated_positions.append(start_pos)

    # calculate for geometric sequence
    elif pattern == 2:
        for n in range(1, comb_size):
            position = start_pos + (-1 if who == 'p' else 1) * start_pos * q ** (n - 1)
            calculated_positions.append(position % comb_size or comb_size)

    # sequence where different is in geometrical sequence
    elif pattern == 3:
        q2 = positions[2] // positions[1]
        for n in range(1, comb_size):
            step = d * q2 ** (n - 1)
            position = int(calculated_positions[n - 1] + (-1 if who == 'p' else 1) * step)
            calculated_positions.append(position % comb_size or comb_size)

    # sequence where different is in arithmetic sequence 1,2,4,7 or 5,9,17,29
    elif pattern == 4:
        calculated_positions.append(start_pos)
        for n in range(1, comb_size):
            position = calculated_positions[n - 1] + (-1 if who == 'p' else 1) * d * n
            calculated_positions.append(position % comb_size or comb_size)
    print(calculated_positions)
    print(comb_size)
    print(pattern)
    return calculated_positions


if __name__ == "__main__":
     print(do_bees_meet(3, '1,2,4,7', '1,2,4,8'))
    # print(calculate_honeycomb_size(5))
    # print(calculate_honeycomb_size(23))
    # print(calculate_honeycomb_size(30))
    # print(calculate_honeycomb_size(50))
#    sequence_1 = ",".join(str(x) for x in range(50000, 200001, 10000))  # Arithmetic sequence with a large difference
#    sequence_2 = ",".join(
#        str(2 ** x) for x in range(30, 45))  # Geometric sequence with a ratio of 2, but starting from a larger power
#    assert do_bees_meet(300, sequence_1, sequence_2) is True
