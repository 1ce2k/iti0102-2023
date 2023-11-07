"""Testing solution."""


from solution import students_study
from solution import lottery
from solution import fruit_order


def test_students_study_evening():
    """Tests students_study evening time."""
    assert students_study(20, True) is True
    assert students_study(20, False) is True
    assert students_study(18, False) is True
    assert students_study(18, True) is True
    assert students_study(24, True) is True
    assert students_study(24, False) is True


def test_students_study_night():
    """Tests students_study night time."""
    assert students_study(1, True) is False
    assert students_study(1, False) is False
    assert students_study(4, True) is False
    assert students_study(4, False) is False


def test_students_study_day():
    """Tests students_study day time."""
    assert students_study(5, True) is True
    assert students_study(5, False) is False
    assert students_study(7, True) is True
    assert students_study(8, False) is False
    assert students_study(17, True) is True
    assert students_study(17, False) is False


def test_lottery_all_fives():
    """Test if all are 5."""
    assert lottery(5, 5, 5) == 10


def test_lottery_all_same_but_not_five():
    """Test if all are same but not 5."""
    assert lottery(1, 1, 1) == 5
    assert lottery(-2, -2, -2) == 5
    assert lottery(0, 0, 0) == 5


def test_lottery_b_c_different_than_a():
    """Test if b and are different from a."""
    assert lottery(4, 3, 2) == 1
    assert lottery(1, 2, 3) == 1
    assert lottery(3, 4, 4) == 1


def test_lottery_b_or_c_same_as_a():
    """Test if b or c is same as a."""
    assert lottery(1, 2, 1) == 0
    assert lottery(2, 2, 1) == 0
    assert lottery(3, 3, 1) == 0


def test_fruit_order_zeros():
    assert fruit_order(0, 0, 0) == 0
    assert fruit_order(1, 0, 0) == 0
    assert fruit_order(0, 1, 0) == 0
    assert fruit_order(1, 1, 0) == 0
    assert fruit_order(5, 5, 25) == 0
    assert fruit_order(0, 5, 25) == 0
    assert fruit_order(0, 1200, 6000) == 0
    assert fruit_order(0, 120, 600) == 0
    assert fruit_order(0, 5, 20) == 0
