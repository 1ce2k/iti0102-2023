"""."""

import pytest

from operators.div import Div
from operators.leaf import Leaf
from operators.add import Add
from operators.sub import Sub


@pytest.mark.timeout(1.0)
def test_leaf_to_class_string():
    """."""
    assert eval(Leaf(6).class_str()).apply() == 6


@pytest.mark.timeout(1.0)
def test_addition_with_leaves_to_class_string():
    """."""
    assert eval(Add(Leaf(5), Leaf(6)).class_str()).apply() == 11


@pytest.mark.timeout(1.0)
def test_subtraction_with_leaves_to_class_string():
    """."""
    assert eval(Sub(Leaf(5), Leaf(6)).class_str()).apply() == -1


@pytest.mark.timeout(1.0)
def test_leaf_to_string():
    """."""
    assert Leaf(6).__str__() == "6"


@pytest.mark.timeout(1.0)
def test_addition_with_leaves_to_string():
    """."""
    tree = Add(Leaf(5), Leaf(6))
    assert tree.apply() == 11
    assert tree.__str__() == "5 + 6"


@pytest.mark.timeout(1.0)
def test_subtraction_with_leaves_to_string():
    """."""
    tree = Sub(Leaf(5), Leaf(6))
    assert tree.apply() == -1
    assert tree.__str__() == "5 - 6"


@pytest.mark.timeout(1.0)
def test_division_given_addition_to_string():
    """."""
    tree = Div(Add(Leaf(12), Leaf(6)), Leaf(6))
    assert tree.apply() == 3
    assert tree.__str__() == "(12 + 6) / 6"


def test_set_add_adds_when_given_leaves_with_sets():
    """."""
    assert Add(Leaf({5}), Leaf({6})).apply() == {5, 6}
