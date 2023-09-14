def calculate_position(positions, start_pos, pattern, comb_size):
    calculated_positions = []
    d = positions[1] - positions[0]
    d2 = positions[2] - positions[1]
    q = positions[1] / positions[0]
    if start_pos == 1:
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
    if 1 < start_pos <= comb_size:
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
    return calculated_positions


def do_they_meet():
    array_a = calculate_position([1,2,3,4], 1, 0, 15)
    array_b = calculate_position([1,3,5,7], 13, 0, 15)

    for i in range(len(array_a)):
        if array_a[i] == array_b[i]:
            return True
    return False

print(calculate_position([1, 5, 9, 12], 1, 0, 15))
print(calculate_position([1,3,5,7], 13, 0, 15))

print(do_they_meet())
