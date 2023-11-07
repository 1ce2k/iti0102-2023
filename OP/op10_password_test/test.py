"""Password validation tests."""
import password


def test__is_correct_length__too_short():
    """Test whether password of length 7 is not correct."""
    assert password.is_correct_length("passwor") is False
    assert password.is_correct_length('') is False


def test__is_correct_length__too_long():
    """Test whether password of length > 64 is incorrect."""
    assert password.is_correct_length("a" * 65) is False


def test_is_correct_length_true():
    assert password.is_correct_length('password') is True
    assert password.is_correct_length('a' * 64) is True
