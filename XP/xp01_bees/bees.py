"""Whether bees meet."""


def do_bees_meet(honeycomb_width: int, honeyhopper_data: str, pollenpadle_data: str) -> bool:
    """Return whether bees meet."""
    if honeycomb_width < 0 or len(honeyhopper_data.split(',')) < 4 or len(pollenpadle_data.split(',')) < 4:
        raise ValueError("Insufficient data for sequence identification")

    hex_size = cells_count(honeycomb_width)
    h_steps = [int(x) for x in honeyhopper_data.split(',')]
    p_steps = [int(x) for x in pollenpadle_data.split(',')]
    h_pattern = bee_pattern(h_steps)
    p_pattern = bee_pattern(p_steps)
    h_moves = honey_first_steps(h_steps, hex_size)
    p_moves = pollen_first_steps(p_steps, hex_size)
    if h_pattern == p_pattern == 'standing':
        # 'standing' and
        if h_moves[0] != p_moves[0]:
            return False

    h_pos = honey_start_pos(h_steps[0], hex_size)
    p_pos = pollen_start_pos(p_steps[0], hex_size)
    if h_pos == p_pos:
        return True
    else:
        for i in range(1, hex_size):
            h_pos = honey_next_pos(h_pos, h_pattern, hex_size, h_steps, i)
            print(h_pos)
            # p_pos = pollen_next_pos(p_pos, p_pattern, hex_size, p_steps)
    # print(h_moves, p_moves)
    return False


def honey_next_pos(position: int, h_pattern: str, hex_size: int, h_steps: list, i: int):
    """Return next pos for honey bee."""
    pos = position
    if h_pattern == 'standing':
        pos = position
    elif h_pattern == 'arithmetic':
        pos = (position + (h_steps[1] - h_steps[0])) % hex_size
        if pos == 0:
            pos = 1
    elif h_pattern == 'geometric':
        pos = (position * int(h_steps[1] / h_steps[0])) % hex_size
        if pos == 0:
            pos = 1
    elif h_pattern == 'growing-arithmetic':
        step = h_steps[1] - h_steps[0]
        step_increment = h_steps[-1] - h_steps[-2]
        if h_steps.index(position) == 0:
            pos = (position + step) % hex_size
        else:
            pos = (position + step + step_increment) % hex_size
    elif h_pattern == 'growing-geometric':
        step = h_steps[1] - h_steps[0]
        step_ratio = int((h_steps[2] - h_steps[1]) / (h_steps[1] - h_steps[0]))
        pos = (pos + step * step_ratio ** (i - 1)) % hex_size
        if pos == 0:
            pos = hex_size
    return pos


def cells_count(honeycomb_width: int) -> int:
    """Return cells count."""
    if honeycomb_width <= 0:
        return 0
    hex_size = 0
    for i in range(honeycomb_width):
        hex_size += honeycomb_width + i
    hex_size = hex_size * 2 - (2 * honeycomb_width - 1)
    return hex_size


def bee_pattern(steps: list) -> str:
    """Find what movement pattern has the bee."""
    if is_arithmetic(steps):
        return 'arithmetic'
    elif is_geometric(steps):
        return 'geometric'
    elif is_growing_arithmetic(steps):
        return 'growing-arithmetic'
    elif is_growing_geometric(steps):
        return 'growing-geometric'
    elif is_not_moving(steps):
        return 'standing'
    raise ValueError("Insufficient data for sequence identification")


def is_arithmetic(steps: list) -> bool:
    """Return True if sequence is arithmetic."""
    common_difference = steps[1] - steps[0]
    if common_difference == 0:
        return False
    for i in range(2, len(steps)):
        if steps[i] - steps[i - 1] != common_difference:
            return False
    return True


def is_growing_arithmetic(steps: list) -> bool:
    """Return True if sequence is growing arithmetic."""
    differences = []
    for i in range(1, len(steps)):
        differences.append(steps[i] - steps[i - 1])
    return is_arithmetic(differences)


def is_geometric(steps: list) -> bool:
    """Return True if sequence is geometric."""
    if steps[0] == 0 or steps[1] / steps[0] == 1:
        return False
    common_ratio = steps[1] / steps[0]
    for i in range(2, len(steps)):
        if steps[i] / steps[i - 1] != common_ratio:
            return False
    return True


def is_growing_geometric(steps: list) -> bool:
    """Return True if sequence is growing arithmetic."""
    differences = []
    for i in range(1, len(steps)):
        differences.append(steps[i] - steps[i - 1])
    return is_geometric(differences)


def is_not_moving(steps: list) -> bool:
    """Return True if bee does not move."""
    if steps[0] == steps[1] == steps[2] == steps[3]:
        return True
    return False


def honey_start_pos(step: int, hex_size: int) -> int:
    """Find honey bee first pos."""
    pos = step % hex_size
    if pos == 0:
        pos = hex_size
    return pos


def pollen_start_pos(step: int, hex_size: int) -> int:
    """Find pollen bee first pos."""
    if step == 1:
        return hex_size
    if step % hex_size == 0:
        return 1
    return hex_size - step % hex_size + 1


def pollen_next_pos(position: int, p_pattern: str, hex_size: int, p_moves: list, p_steps: list) -> list:
    """Find pollen bee next position."""
    pos = position
    if p_pattern == 'standing':
        pos = position
    if p_pattern == 'arithmetic':
        pos = (pos - (p_steps[1] - p_steps[0]))
    if p_pattern == 'geometric':
        multiplier = int(p_steps[1] / p_steps[0])
        step = p_moves[p_moves.index(pos)] - p_moves[p_moves.index(pos) - 1]
        if position == p_moves[0]:
            pos = p_moves[1]
        else:
            pos = (pos + step * multiplier)
    if p_pattern == 'growing-arithmetic':
        step = p_moves[p_moves.index(pos)] - p_moves[p_moves.index(pos) - 1]
        step_difference = p_moves[1] - p_moves[0]
        pos = (pos + (step - step_difference))
    if p_pattern == 'growing-geometric':
        step_ratio = int((p_moves[2] - p_moves[1]) / (p_moves[1] - p_moves[0]))
        step = int(p_moves[p_moves.index(pos)] - p_moves[p_moves.index(pos) - 1])
        pos = (pos + step * step_ratio)
    pos %= hex_size
    if pos == 0:
        pos = 1
    if pos not in p_moves:
        p_moves.append(pos)
    return p_moves


def honey_first_steps(steps: list, cells: int) -> list:
    """Return the honey start positions."""
    moves = []
    for i in steps:
        moves.append(honey_start_pos(i, cells))
    return moves


def pollen_first_steps(steps: list, cells: int) -> list:
    """Return the pollen start positions."""
    moves = []
    for i in steps:
        moves.append(pollen_start_pos(i, cells))
    return moves


if __name__ == '__main__':
    # print('Calculate hex_size:')
    # print(cells_count(5))  # => 61
    # print(cells_count(4))  # => 37
    # print(cells_count(3))  # => 19

    # print('\nFind bee pattern:')
    # print(bee_pattern([1, 2, 3, 4]))
    # print(bee_pattern([5, 11, 17, 23]))
    # print(bee_pattern([1, 2, 4, 7]))
    # print(bee_pattern([5, 9, 17, 29]))
    # print(bee_pattern([1, 2, 4, 8]))
    # print(bee_pattern([2, 6, 18, 54]))
    # print(bee_pattern([1, 3, 7, 15, 31]))
    # print(bee_pattern([5, 9, 17, 33]))
    # print(bee_pattern([5, 9, 19, 33]))

    # print('\nFind honey bee start pos:')
    # print(honey_start_pos(1, 61))  # => 1
    # print(honey_start_pos(2, 61))  # => 2
    # print(honey_start_pos(63, 61))  # => 2

    # print('\nFind pollen bee start pos:')
    # print(pollen_start_pos(1, 61))  # => 61
    # print(pollen_start_pos(61, 61))  # => 1
    # print(pollen_start_pos(63, 61))  # => 60
    # print(pollen_start_pos(4, 61))  # => 58
    # print(pollen_start_pos(60, 61))  # => 2

    # print(honey_first_steps([69, 70, 71, 72], 61))  # => [8, 9, 10, 11]
    # print(pollen_first_steps([1, 2, 3, 4], 61))  # => [61, 60, 59, 58]

    # print('\nFind next honey bee position:')
    print(honey_next_pos(1, 'standing', 61, [1, 1, 1, 1], 1))  # => 1
    print(honey_next_pos(1, 'arithmetic', 61, [1, 4, 7, 11], 1))  # => 4
    print(honey_next_pos(2, 'arithmetic', 61, [2, 4, 6, 8], 1))  # => 4
    print(honey_next_pos(8, 'arithmetic', 61, [2, 4, 6, 8], 1))  # => 10
    print(honey_next_pos(7, 'growing-arithmetic', 61, [1, 2, 4, 7], 1))  # => 11
    print(honey_next_pos(11, 'growing-arithmetic', 61, [1, 2, 4, 7, 11], 1))  # => 16
    print(honey_next_pos(45, 'growing-arithmetic', 61, [5, 9, 17, 29, 45], 1))  # => 4
    print(honey_next_pos(2, 'geometric', 61, [1, 2, 4, 8], 1))  # => 4
    print(honey_next_pos(8, 'geometric', 61, [1, 2, 4, 8], 1))  # => 16
    print(honey_next_pos(1, 'growing-geometric', 61, [1, 3, 7, 15], 1))  # => 3
    print(honey_next_pos(15, 'growing-geometric', 61, [1, 3, 7, 15], 4))  # => 31
    print(honey_next_pos(5, 'growing-geometric', 61, [5, 9, 17, 33], 1))  # => 9
    print(honey_next_pos(33, 'growing-geometric', 61, [5, 9, 17, 33], 4))  # => 4

    # print('\nFind next pollen bee position:')
    # print(pollen_next_pos(61, 'standing', 61, [1, 1, 1, 1]))
    # print(pollen_next_pos(61, 'arithmetic', 61, [1, 2, 3, 4]))  # => [60]
    # print(pollen_next_pos(58, 'arithmetic', 61, [1, 2, 3, 4]))  # => [57]
    # print(pollen_next_pos(30, 'geometric', 61, [61, 60, 58, 54, 46, 30], [1, 2, 4, 8]))

    # print(do_bees_meet(3, '1,3,7,15', '1,1,1,1'))
    # assert do_bees_meet(50, '1,1,1,1', '1,1,1,1') is False
    # assert do_bees_meet(20, '1,1,1,1', '7,7,7,7') is False
    # assert do_bees_meet(50, '1,1,1,1', '1,2,3,4') is True
    # assert do_bees_meet(500, '1,2,4,8', '1,2,4,8') is True
    # assert do_bees_meet(5, '1,3,7,15', '1,3,7,15') is True
    # assert do_bees_meet(2, "1,2,4,7", "2,4,8,14") is True
    # sequence_1 = ",".join(str(x) for x in range(50000, 200001, 10000))  # Arithmetic sequence with a large difference
    # assert do_bees_meet(2, sequence_1, sequence_1) is True
    # sequence_2 = ",".join(
    #     str(2 ** x) for x in range(30, 45))  # Geometric sequence with a ratio of 2, but starting from a larger power
    # assert do_bees_meet(300, sequence_1, sequence_2) is True
