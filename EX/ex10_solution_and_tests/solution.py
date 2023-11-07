"""Solution to be tested."""


def students_study(time: int, coffee_needed: bool) -> bool:
    """
    Return True if students study in given circumstances.

    (19, False) -> True
    (1, True) -> False.
    """
    if 18 <= time <= 24:
        return True
    if 1 <= time <= 4:
        return False if coffee_needed else True
    if 5 <= time <= 17:
        return True if coffee_needed else False


def lottery(a: int, b: int, c: int) -> int:
    """
    Return Lottery victory result 10, 5, 1, or 0 according to input values.

    (5, 5, 5) -> 10
    (2, 2, 1) -> 0
    (2, 3, 1) -> 1
    """
    if a == b == c == 5:
        return 10
    if a == b == c != 5:
        return 5
    if b != a and c != a:
        return 1
    return 0


def fruit_order(small_baskets: int, big_baskets: int, ordered_amount: int) -> int:
    """
    Return number of small fruit baskets if it's possible to finish the order, otherwise return -1.

    (4, 1, 9) -> 4
    (3, 1, 10) -> -1
    """
    total = small_baskets + big_baskets * 5
    if total < ordered_amount:
        return -1
    big_baskets_needed = ordered_amount // 5
    big_baskets_used = min(big_baskets_needed, big_baskets)
    remaining_weight = ordered_amount - big_baskets_used * 5
    small_baskets_needed = max(0, remaining_weight)
    return small_baskets_needed
