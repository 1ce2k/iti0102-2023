def calculate_position(positions, start_pos, pattern, comb_size, who):
    calculated_positions = []
    d = positions[1] - positions[0]
    d2 = positions[2] - positions[1]
    q = positions[1] / positions[0]
    q2 = positions[2] // positions[1]
    if who == 'h':
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
        elif pattern == 4:
            calculated_positions.append(start_pos)
            for n in range(1, comb_size):
                position = calculated_positions[n - 1] + d * n
                if 1 <= position <= comb_size:
                    calculated_positions.append(position)
                else:
                    position = abs(position % comb_size)
                    if 1 <= position <= comb_size:
                        calculated_positions.append(position)
                    elif position == 0:
                        position = start_pos
                        calculated_positions.append(position)
    if who == 'p':
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
            for i in range(1, comb_size + 1):
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
            for n in range(1, comb_size):
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


def do_they_meet():
    array_a = calculate_position([1, 2, 3, 4], 1, 0, 7, 'h')
    array_b = calculate_position([1, 2, 3, 4], 7, 3, 7, 'p')

    for i in range(len(array_a)):
        if array_a[i] == array_b[i]:
            return True
    return False


# print(calculate_position([1, 2, 3, 4], 1, 0, 7, 'h'))
# print(calculate_position([1, 2, 3, 4], 7, 0, 7, 'p'))
#
# print(calculate_position([1, 2, 2, 2], 1, 1, 7, 'p'))
# print(calculate_position([1, 1, 1, 1], 7, 1, 7, 'p'))
#
# print(calculate_position([1, 2, 4, 8], 1, 2, 7, 'h'))
# print(calculate_position([1, 2, 4, 8], 7, 2, 7, 'p'))

print(calculate_position([1, 3, 7, 15], 1, 3, 7, 'h'))
print(calculate_position([1, 3, 7, 15], 7, 3, 7, 'p'))

print(calculate_position([1, 2, 4, 7], 1, 4, 7, 'h'))
print(calculate_position([1, 2, 4, 7], 7, 4, 7, 'p'))

print(do_they_meet())
