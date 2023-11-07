"""Testing solution."""


from solution import students_study
from solution import lottery
from solution import fruit_order


def test_students_study():
    assert students_study(12, True) is True
    assert students_study(5, True) is True
    assert students_study(17, True) is True
    assert students_study(18, True) is True
    assert students_study(1, True) is False

