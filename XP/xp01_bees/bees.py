"""Whether bees meet."""


def do_bees_meet(honeycomb_width: int, honeyhopper_data: str, pollenpadle_data: str) -> bool:
    """Return whether bees meet."""
    if not honeycomb_width > 0 or len(honeyhopper_data.split(',')) < 4 or len(pollenpadle_data.split(',')) < 4:
        raise ValueError("Insufficient data for sequence identification")

    honey_moves = list(map(int, honeyhopper_data.split(',')))
    pollen_moves = list(map(int, pollenpadle_data.split(',')))
    end_honey = len(honey_moves)
    end_pollen = len(pollen_moves)
    for i in range(2, end_honey):
        for x in range(2, end_pollen):
            if honey_moves[end_honey - 1] - honey_moves[end_honey - 2] == honey_moves[i] - honey_moves[i - 1] == \
                    honey_moves[1] - honey_moves[0]:
                if pollen_moves[end_pollen - 1] - pollen_moves[end_honey - 2] == honey_moves[x] - honey_moves[x - 1] == \
                        pollen_moves[1] - pollen_moves[0]:
                    return True

    return False


print(do_bees_meet(3, '1,2,3,4', '1,2,3,4'))  # =>7, 0, 1, False
print(do_bees_meet(3, '1,2,3,4', '5,9,17,33'))  # =>7, 0, 2, False
print(do_bees_meet(3, '1,2,3,4', '1,2,4,7'))  # =>7, 0, 3, False
