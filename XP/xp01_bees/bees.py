"""Whether bees meet."""


def do_bees_meet(honeycomb_width: int, honey_hopper_data: str, pollen_paddle_data: str) -> bool:
    """Return whether bees meet."""
    # Validate the input
    if not honeycomb_width > 0 or len(honey_hopper_data.split(',')) < 4 or len(pollen_paddle_data.split(',')) < 4:
        raise ValueError("Insufficient data for sequence identification")

    # Parse input
    honey_hopper_positions = list(map(int, honey_hopper_data.split(',')))
    pollen_paddle_positions = list(map(int, pollen_paddle_data.split(',')))

    # Analyze movement pattern
    honey_hopper_pattern = analyze_movement_pattern(honey_hopper_positions)
    pollen_paddle_pattern = analyze_movement_pattern(pollen_paddle_positions)

    honey_comb_size = calculate_honeycomb_size(honeycomb_width)
    h_start_pos = honey_hopper_positions[0]
    p_start_pos = honey_comb_size - pollen_paddle_positions[0]
    # Calculate position
    honey_hopper_hex_positions = calculate_position(honey_hopper_positions, h_start_pos, honey_hopper_pattern,
                                                    honey_comb_size, 'h')
    pollen_paddle_hex_positions = calculate_position(pollen_paddle_positions, p_start_pos, pollen_paddle_pattern,
                                                     honey_comb_size, 'p')

    for i in range(len(honey_hopper_hex_positions)):
        if honey_hopper_hex_positions[i] == pollen_paddle_hex_positions[i]:
            return True
    return False

    # Check gor intersection
    for x in range(len(honey_hopper_hex_positions)):
        for i in range(len(pollen_paddle_hex_positions)):
            if honey_hopper_hex_positions[x] == pollen_paddle_hex_positions[i]:
                return True
    return False


def analyze_movement_pattern(sequence):
    """Return position pattern."""
    end = len(sequence)
    for i in range(2, end):
        # arithmetic sequence
        if sequence[end - 1] - sequence[end - 2] == sequence[i] - sequence[i - 1] == sequence[1] - sequence[0] != 0:
            print(0)
            return 0
        # if one is not moving
        elif all(sequence[i] == sequence[0] for i in range(1, len(sequence))):
            print(1)
            return 1
        # geometric sequence
        elif sequence[end - 1] / sequence[end - 2] == sequence[i] / sequence[i - 1] == sequence[1] / sequence[0]:
            print(2)
            return 2
        # sequence where different is in geometrical sequence 1,3,7,15
        elif int(sequence[end - 1] - sequence[end - 2]) == int(sequence[i] - sequence[i - 1]) * i == \
                int(sequence[1] - sequence[0]) * i * i:
            print(3)
            return 3
        # sequence where different is in arithmetic sequence 1,2,4,7 or 5,9,17,29
        elif sequence[1] - sequence[0] == (sequence[i] - sequence[i - 1]) / i == (
                sequence[end - 1] - sequence[end - 2]) / (end - 1):
            print(4)
            return 4
        else:
            raise ValueError("Insufficient data for sequence identification")


def calculate_position(positions, start_pos, pattern, comb_size, who_is_moving):
    calculated_positions = []
    d = positions[1] - positions[0]
    d2 = positions[2] - positions[1]
    q = positions[1] / positions[0]
    q2 = positions[2] / positions[1]
    if who_is_moving == 'h':
        if pattern == 0:
            for n in range(1, comb_size + 1):
                position = start_pos + d * (n - 1)
                if 1 <= position <= comb_size:
                    calculated_positions.append(position)
                else:
                    position = position % comb_size
                    if 1 <= position <= comb_size:
                        calculated_positions.append(position)
                    elif position == 0:
                        position = position + d * (n - 1)
                        calculated_positions.append(position)
        elif pattern == 1:
            for i in range(1, comb_size + 1):
                position = start_pos
                calculated_positions.append(position)
        elif pattern == 2:
            calculated_positions.append(start_pos)
            for n in range(1, comb_size):
                position = int(positions[1] * q ** (n - 1))
                if 1 <= position <= comb_size:
                    calculated_positions.append(position)
                else:
                    position = int(position % comb_size)
                    if 1 <= position <= comb_size:
                        calculated_positions.append(position)
                    elif position == 0:
                        position = start_pos
                        calculated_positions.append(position)
        elif pattern == 3:
            calculated_positions.append(start_pos)
            for n in range(1, comb_size):
                step = d * q2 ** (n - 1)
                position = int(calculated_positions[n - 1] + step)
                if 1 <= position <= comb_size and step <= comb_size:
                    calculated_positions.append(position)
                else:
                    position = position % comb_size
                    if 1 <= position <= comb_size:
                        calculated_positions.append(position)
                    elif position == 0:
                        position = start_pos
                        calculated_positions.append(position)
    if who_is_moving == 'p':
        if pattern == 0:
            for n in range(1, comb_size + 1):
                position = start_pos - d * (n - 1)
                if 1 <= position <= comb_size:
                    calculated_positions.append(position)
                else:
                    position = position % comb_size
                    if 1 <= position <= comb_size:
                        calculated_positions.append(position)
                    elif position == 0:
                        position = abs(d * (n - 1))
                        calculated_positions.append(position)
        elif pattern == 1:
            position = start_pos
            for n in range(1, comb_size + 1):
                position = start_pos
                calculated_positions.append(position)
        elif pattern == 2:
            calculated_positions.append(start_pos)
            for n in range(1, comb_size + 1):
                position = int(calculated_positions[n - 1] - (positions[0] * q ** (n - 1)))
                if 1 <= position <= comb_size:
                    calculated_positions.append(position)
                else:
                    position = int(position % comb_size)
                    if 1 <= position <= comb_size:
                        calculated_positions.append(position)
                    elif position == 0:
                        position = start_pos
                        calculated_positions.append(position)
        elif pattern == 3:
            calculated_positions.append(start_pos)
            for n in range(1, comb_size):
                step = d * q2 ** (n - 1)
                position = int(calculated_positions[n - 1] - step)
                if 1 <= position <= comb_size and step <= comb_size:
                    calculated_positions.append(position)
                else:
                    position = position % comb_size
                    if 1 <= position <= comb_size:
                        calculated_positions.append(position)
                    elif position == 0:
                        position = start_pos
                        calculated_positions.append(position)
        elif pattern == 4:
            calculated_positions.append(start_pos)
            for n in range(1 , comb_size):
                position = calculated_positions[n - 1] - d * n
                if 1 <= position <= comb_size:
                    calculated_positions.append(position)
                else:
                    position = position % comb_size
                    if 1 <= position <= comb_size:
                        calculated_positions.append(position)
                    elif position == 0:
                        position = start_pos
                        calculated_positions.append(position)

    return calculated_positions


def calculate_honeycomb_size(honeycomb_width) -> int:
    """Return size of honey comb."""
    comb_length = int(honeycomb_width / 2) + 1
    comb_size = comb_length
    while comb_length < honeycomb_width:
        comb_size = comb_size + comb_length + 1
        comb_length += 1
    comb_size = comb_size * 2 - honeycomb_width
    return comb_size


print(do_bees_meet(3, '1,2,3,4', '5,9,13,17'))  # => 0, 0, True
print(do_bees_meet(3, '1,1,1,1', '2,2,2,2'))  # =>7, 1, 1, False
print(do_bees_meet(3, '1,2,4,8', '2,6,18,54'))  # =>7, 2, 2, True
print(do_bees_meet(3, '1,3,7,15', '5,9,17,33'))  # =>7, 3, 3, True
print(do_bees_meet(3, '1,2,4,7', '5,9,17,29'))  # =>7, 4, 4, True
