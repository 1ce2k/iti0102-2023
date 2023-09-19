"""Test bees."""


def do_bees_meet(honeycomb_width: int, honey_hopper_data: str, pollen_paddle_data: str) -> bool:
    """Return whether bees meet."""
    # Validate the input
    if honeycomb_width < 0 or len(honey_hopper_data.split(',')) < 4 or len(pollen_paddle_data.split(',')) < 4:
        raise ValueError("Insufficient data for sequence identification")

    # Parse input
    honey_hopper_positions = list(map(int, honey_hopper_data.split(',')))
    pollen_paddle_positions = list(map(int, pollen_paddle_data.split(',')))

    # Analyze movement pattern
    h_pattern = analyze_movement_pattern(honey_hopper_positions)
    p_pattern = analyze_movement_pattern(pollen_paddle_positions)

    honey_comb_size = calculate_honeycomb_size(honeycomb_width)

    if pollen_paddle_positions[0] != 1:
        p_pos = honey_comb_size - pollen_paddle_positions[0]
    # Calculate position
    honey_step = calculate_step(honey_hopper_positions, h_pattern, 'h')
    pollen_step = calculate_step(pollen_paddle_positions, p_pattern, 'p')
    h_pos = 0
    if honey_hopper_positions[0] >= 1:
        h_pos = honey_hopper_positions[0]
    elif honey_hopper_positions[0] == -1:
        h_pos = honey_comb_size
    elif honey_hopper_positions[0] < -1:
        h_pos = honey_comb_size + honey_hopper_positions[0]

    p_pos = 0
    if pollen_paddle_positions[0] == 1:
        p_pos = honey_comb_size
    elif pollen_paddle_positions[0] == -1:
        p_pos = abs(pollen_paddle_positions[0])
    elif honey_comb_size - pollen_paddle_positions[0] == 0:
        p_pos = 1
    else:
        p_pos = (honey_comb_size - pollen_paddle_positions[0] - 1) % honey_comb_size
    print(h_pos, p_pos)
    # Check for intersection
    for i in range(1, honey_comb_size):
        if h_pos == p_pos:
            return True
        else:
            # calculate next pos for honey hopper
            if h_pattern == 0:
                if honey_step > 0:
                    h_pos = h_pos + honey_step
                    if h_pos > honey_comb_size:
                        h_pos = h_pos % honey_comb_size
                elif honey_step < 0:
                    h_pos = h_pos + honey_step
                    if h_pos <= 0:
                        h_pos = honey_comb_size + h_pos

            elif h_pattern == 2:
                h_pos = h_pos * honey_step
                if h_pos > honey_comb_size:
                    h_pos = h_pos % honey_comb_size
            elif h_pattern == 3:
                h_pos = h_pos + honey_step ** i
                if h_pos > honey_comb_size:
                    h_pos = h_pos % honey_comb_size
                    if h_pos == 0:
                        h_pos = honey_comb_size
            elif h_pattern == 4:
                h_pos = (h_pos + honey_step * i) % honey_comb_size

            # calculate next pos for pollen paddle
            if p_pattern == 0:
                p_pos = p_pos + pollen_step
                if p_pos < 0:
                    p_pos = honey_comb_size + p_pos
            elif p_pattern == 2:
                step = pollen_step ** (i - 1)
                p_pos = p_pos - step
                if p_pos < 0:
                    temp = abs(p_pos) // honey_comb_size
                    if temp == 0:
                        p_pos = honey_comb_size % abs(p_pos)
                    else:
                        p_pos = honey_comb_size - (abs(p_pos) % honey_comb_size)
            elif p_pattern == 3:
                p_pos = (p_pos - pollen_step ** i) % honey_comb_size
                if p_pos == 0:
                    p_pos = 1
            elif p_pattern == 4:
                p_pos = p_pos + pollen_step * i
                if p_pos < 0:
                    p_pos = p_pos % honey_comb_size

            # print(h_pos, p_pos)
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
        elif int(sequence[end - 1] - sequence[end - 2]) == int(sequence[i] - sequence[i - 1]) * i == int(
                sequence[1] - sequence[0]) * i * i:
            return 3
        # sequence where different is in arithmetic sequence 1,2,4,7 or 5,9,17,29
        elif sequence[1] - sequence[0] == (sequence[i] - sequence[i - 1]) / i == (
                sequence[end - 1] - sequence[end - 2]) / (end - 1):
            return 4
        else:
            raise ValueError("Insufficient data for sequence identification")


def calculate_step(positions, pattern, who) -> int:
    """Calculate bee positions."""
    step = 0
    # calculate for arithmetic
    if pattern == 0:
        step = (-1 if who == 'p' else 1) * (positions[1] - positions[0])
    # calculate for not moving
    elif pattern == 1:
        step = positions[1] - positions[0]
    # calculate for geometric sequence
    elif pattern == 2:
        step = round(positions[1] / positions[0])
    # sequence where different is in geometrical sequence
    elif pattern == 3:
        step = (positions[1] - positions[0])
    # sequence where different is in arithmetic sequence 1,2,4,7 or 5,9,17,29
    elif pattern == 4:
        step = (-1 if who == 'p' else 1) * (positions[1] - positions[0])
    print(f"pattern: {pattern} and step: {step}")
    return step


if __name__ == "__main__":
    # print(do_bees_meet(300, "1,2,3,4,5", "1,2,3,4,5"))      # True
    # print(do_bees_meet(3, '2,4,6,8', '1,2,3,4'))              #True
    print(do_bees_meet(3, '2,4,6,8', '19,21,23,25'))              #True
    print(do_bees_meet(3, '2,4,6,8', '2,4,6,8'))              #True
    # assert do_bees_meet(5, "1,2,4,7", "2,4,8,14") is True
    # print(do_bees_meet(300, '1,2,4,8', '1,2,4,8'))          # True
    # print(do_bees_meet(3, '-1,-2,-3,-4', '-1,-2,-3,-4'))    # True
    # print(do_bees_meet(400, '1,3,7,15', '1,3,7,15'))    # True
    # print(do_bees_meet(300, '1,2,4,7', '1,2,4,7'))          # True
    # print(do_bees_meet(3, '-1,-2,-3,-4', '1,2,3,4'))        # True
    # sequence_1 = ",".join(str(x) for x in range(50000, 200001, 10000))  # Arithmetic sequence with a large difference
    # sequence_2 = ",".join(
    # str(2 ** x) for x in range(30, 45))  # Geometric sequence with a ratio of 2, but starting from a larger power
    # print(do_bees_meet(300, sequence_1, sequence_2))