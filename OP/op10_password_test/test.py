"""Password validation tests."""
import password


def test__is_correct_length__too_short():
    """Test whether password of length 7 is not correct."""
    assert password.is_correct_length("passwor") is False
    # pass_1 = 'a' * 64
    # pass_2 = 'a' * 65
    # assert password.is_correct_length(pass_1) is True
    # assert password.is_correct_length(pass_2) is False


def test__is_correct_length__too_long():
    """Test whether password of length > 64 is incorrect."""
    assert password.is_correct_length("pass" * 18) is False
