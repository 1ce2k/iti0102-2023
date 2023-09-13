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

    # Calculate position
    honey_hopper_hex_positions = calculate_position_honey_hopper(honey_hopper_positions, honey_hopper_pattern,
                                                                 honeycomb_width)
    pollen_paddle_hex_positions = calculate_position_pollen_paddle(pollen_paddle_positions, pollen_paddle_pattern,
                                                                   honeycomb_width)

    # Check gor intersection
    for honey_hopper_pos in honey_hopper_hex_positions:
        if honey_hopper_pos in pollen_paddle_hex_positions:
            return True
    return False


def analyze_movement_pattern(positions):
    """Return movement pattern."""
    constant_gap = all(positions[i] - positions[i - 1] == positions[1] - positions[0] for i in range(1, len(positions)))
    if constant_gap:
        return 'constant_gap'

    increasing_gap = all(
        positions[i] / positions[i - 1] == positions[1] / positions[0] for i in range(1, len(positions)))
    if increasing_gap:
        return "increasing_gap"

    geometric_sequence = all(
        positions[i] / positions[i - 1] == positions[1] / positions[0] for i in range(1, len(positions)))
    if geometric_sequence:
        return "geometric_sequence"

    increasing_geometric_gap = all(
        positions[i] / positions[i - 1] > positions[1] - positions[0] for i in range(1, len(positions)))
    if increasing_geometric_gap:
        return

    if all(position == positions[0] for position in positions):
        return 'is_not_moving'

    raise ValueError("Insufficient data for sequence identification")


def calculate_position_honey_hopper(positions, pattern, honeycomb_width) -> list:
    """Return position for honey hopper."""
    # comb_size = calculate_honeycomb_size(honeycomb_width)
    calculated_positions = []
    if pattern == "constant_gap":
        gap = positions[1] - positions[0]
        for i in range(len(positions)):
            calculated_positions.append(positions[i] + gap * i)
    elif pattern == "increasing_gap":
        for i in range(len(positions)):
            calculated_positions.append(positions[i] + (i * (i + 1) // 2))
    elif pattern == "geometric_sequence":
        ratio = positions[1] // positions[0]
        for i in range(len(positions)):
            calculated_positions.append(positions[i] * (ratio ** i))
    elif pattern == "increasing_geometric_gap":
        for i in range(len(positions)):
            calculated_positions.append(positions[i] * (2 ** i))
    elif pattern == "is_not_moving":
        calculated_positions.append(positions[0])
    return calculated_positions


def calculate_position_pollen_paddle(positions, pattern, honeycomb_width) -> list:
    """Return position for pollen paddle."""
    calculated_positions = []
    comb_size = calculate_honeycomb_size(honeycomb_width)
    position = comb_size

    if pattern == "constant_gap":
        gap = positions[1] - positions[0]
        for i in range(len(positions)):
            if position >= 0:
                position = positions[i] - gap * i
                calculated_positions.append(position)
            else:
                position = comb_size - abs(position[i] - gap * 1) % comb_size
                calculated_positions.append(position)
    elif pattern == "increasing_gap":
        for i in range(len(positions)):
            if position >= 0:
                position = positions[i] - (i * (i + 1) // 2)
                calculated_positions.append(position)
            else:
                position = comb_size - (position[i] - (i * (i + 1))) % comb_size
    elif pattern == "geometric_sequence":
        ratio = positions[1] // positions[0]
        for i in range(len(positions)):
            calculated_positions.append(positions[i] * (ratio ** i))
    elif pattern == "increasing_geometric_gap":
        for i in range(len(positions)):
            calculated_positions.append(positions[i] * (2 ** i))
    elif pattern == "is_not_moving":
        calculated_positions.append(positions[0])
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


print(do_bees_meet(3, '1,2,3,4', '1,2,3,4'))  # =>7, 0, 1, True
print(do_bees_meet(3, '1,2,4,8', '1,2,4,8'))  # =>7, 0, 1, True
