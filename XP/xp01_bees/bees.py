"""Whether bees meet"""


def do_bees_meet(honeycomb_width: int, honeyhopper_data: str, pollenpadle_data: str) -> bool:
    """Return whether bees meet."""
    if honeycomb_width < 0 or len(honeyhopper_data.split(',')) < 4 or len(pollenpadle_data.split(',')) < 4:
        raise ValueError("Insufficient data for sequence identification")

    hex_size = cells_count(honeycomb_width)
    h_steps = list(map(int, honeyhopper_data.split(',')))
    p_steps = list(map(int, pollenpadle_data.split(',')))
    h_pattern = bee_pattern(h_steps)
    p_pattern = bee_pattern(p_steps)
    h_start_pos = honey_start_pos(h_steps, hex_size)
    p_start_pos = pollen_start_pos(p_steps, hex_size)
    h_pos = h_start_pos
    p_pos = p_start_pos
    count = 0
    while count < hex_size:
        if h_pos == p_pos:
            return True
        else:
            h_pos = honey_next_pos(h_pos, h_pattern, hex_size, h_steps)
            p_pos = pollen_next_pos(p_pos, p_pattern, hex_size, p_steps, count)
        print(h_pos, p_pos)
        count += 1
    return False


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
    else:
        raise ValueError("Insufficient data for sequence identification")


def is_arithmetic(steps: list) -> bool:
    """Return True if sequence is arithmetic."""
    common_difference = steps[1] - steps[0]
    for i in range(2, len(steps)):
        if steps[i] - steps[i - 1] != common_difference:
            return False
    return True


def is_growing_arithmetic(steps: list) -> bool:
    """Return True if sequence is growing arithmetic."""
    differences = []
    for i in range(2, len(steps)):
        differences.append(steps[i] - steps[i - 1])
    return is_arithmetic(differences)


def is_geometric(steps: list) -> bool:
    """Return True if sequence is geometric."""
    common_ratio = steps[1] / steps[0]
    for i in range(2, len(steps)):
        if steps[i] / steps[i - 1] != common_ratio:
            return False
    return True


def is_growing_geometric(steps: list) -> bool:
    """Return True if sequence is growing arithmetic."""
    differences = []
    for i in range(2, len(steps)):
        differences.append(steps[i] / steps[i - 1])
    return is_geometric(differences)


def is_not_moving(steps: list) -> bool:
    """Return True if bee does not move."""
    if steps[0] == steps[1] == steps[2] == steps[3]:
        return True
    return False


def honey_start_pos(steps: list, hex_size: int) -> int:
    """Find honey bee first pos."""
    pos = steps[0] % hex_size
    if pos == 0:
        pos = hex_size
    return pos


def pollen_start_pos(steps: list, hex_size: int) -> int:
    """Find pollen bee first pos."""
    if steps[0] == 1:
        return hex_size
    if steps[0] % hex_size == 0:
        return 1
    return hex_size - steps[0] % hex_size + 1


def honey_next_pos(position: int, h_pattern: str, hex_size: int, h_steps: list) -> int:
    """Return next pos for honey bee."""
    pos = position
    if h_pattern == 'standing':
        pos = h_steps[0]
    elif h_pattern == 'arithmetic':
        pos = (pos + (h_steps[1] - h_steps[0])) % hex_size
        if pos == 0:
            pos = 1
    elif h_pattern == 'geometric':
        pos = (pos * int(h_steps[1] / h_steps[0])) % hex_size
    elif h_pattern == 'growing-arithmetic':
        step = h_steps[1] - h_steps[0]
        step_increment = h_steps[h_steps.index(pos)] - h_steps[h_steps.index(pos) - 1]
        if h_steps.index(pos) == 0:
            pos += step
        else:
            pos = (pos + step + step_increment) % hex_size
    elif h_pattern == 'growing-geometric':
        step_ratio = int((h_steps[2] - h_steps[1]) / (h_steps[1] - h_steps[0]))
        step = int(h_steps[h_steps.index(pos)] - h_steps[h_steps.index(pos) - 1])
        step1 = h_steps[1] - h_steps[0]
        if h_steps.index(pos) == 0:
            pos += step1
        else:
            pos = (pos + step * step_ratio) % hex_size
    return pos


def pollen_next_pos(position: int, p_pattern: str, hex_size: int, p_steps: list, grade: int) -> int:
    """Find pollen bee next position."""
    pos = position
    if p_pattern == 'standing':
        pos = position
    if p_pattern == 'arithmetic':
        pos = (pos - (p_steps[1] - p_steps[0])) % hex_size
    if p_pattern == 'geometric':
        step = p_steps[1] / p_steps[0]
        pos = int(pos - step ** grade) % hex_size
    if pos == 0:
        pos %= hex_size
    return pos


# if __name__ == '__main__':
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
    # print(bee_pattern([1, 3, 7, 15]))
    # print(bee_pattern([5, 9, 17, 33]))

    # print('\nFind honey bee start pos:')
    # print(honey_start_pos([1, 2, 3, 4], 61))  # => 1
    # print(honey_start_pos([61, 62, 63, 64], 61))  # => 2
    # print(honey_start_pos([63, 64, 65, 66], 61))  # => 1

    # print('\nFind pollen bee start pos:')
    # print(pollen_start_pos([1, 2, 3, 4], 61))  # => 61
    # print(pollen_start_pos([61, 62, 63, 64], 61))  # => 1
    # print(pollen_start_pos([63, 64, 65, 66], 61))  # => 60
    # print(pollen_start_pos([4, 5, 6, 7], 61))  # => 58
    # print(pollen_start_pos([60, 61, 62, 63], 61))  # => 2

    # print('\nFind next honey bee position:')
    # print(honey_next_pos(1, 'standing', 61, [1, 1, 1, 1]))  # => 1
    # print(honey_next_pos(1, 'arithmetic', 61, [1, 4, 7, 11]))  # => 4
    # print(honey_next_pos(2, 'arithmetic', 61, [2, 4, 6, 8]))  # => 4
    # print(honey_next_pos(8, 'arithmetic', 61, [2, 4, 6, 8]))  # => 10
    # print(honey_next_pos(7, 'growing-arithmetic', 61, [1, 2, 4, 7]))  # => 11
    # print(honey_next_pos(11, 'growing-arithmetic', 61, [1, 2, 4, 7, 11]))  # => 16
    # print(honey_next_pos(45, 'growing-arithmetic', 61, [5, 9, 17, 29, 45]))  # => 4
    # print(honey_next_pos(2, 'geometric', 61, [1, 2, 4, 8]))  # => 4
    # print(honey_next_pos(8, 'geometric', 61, [1, 2, 4, 8]))  # => 16
    # print(honey_next_pos(1, 'growing-geometric', 61, [1, 3, 7, 15]))  # => 3
    # print(honey_next_pos(15, 'growing-geometric', 61, [1, 3, 7, 15]))  # => 31
    # print(honey_next_pos(5, 'growing-geometric', 61, [5, 9, 17, 33]))  # => 9
    # print(honey_next_pos(33, 'growing-geometric', 61, [5, 9, 17, 33]))  # => 4

    # print('\nFind next pollen bee position:')
    # print(pollen_next_pos(61, 'standing', 61, [1, 1, 1, 1]))
    # print(pollen_next_pos(61, 'arithmetic', 61, [1, 2, 3, 4]))  # => [60]
    # print(pollen_next_pos(58, 'arithmetic', 61, [1, 2, 3, 4]))  # => [57]

    # print(do_bees_meet(5, '1,2,3,4', '1,2,3,4'))
    # print(do_bees_meet(5, '1,2,4,8', '1,2,4,8'))
