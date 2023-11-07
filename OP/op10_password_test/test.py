"""Password validation tests."""
import password


def test__is_correct_length():
    """Test whether password is correct length or not."""
    assert password.is_correct_length("passwor") is False
    assert password.is_correct_length('') is False
    assert password.is_correct_length("a" * 65) is False
    assert password.is_correct_length('password') is True
    assert password.is_correct_length('a' * 64) is True


def test_includes_uppercase():
    """Test if there are some uppercase in password."""
    assert password.includes_uppercase('') is False
    assert password.includes_uppercase('Defwefwevwe') is True
    assert password.includes_uppercase('e/¤!fwe64fwevw') is False
    assert password.includes_uppercase('fDGPEJNF') is True
    assert password.includes_uppercase('DGPEJNF') is True


def test_includes_lowercase():
    assert password.includes_lowercase('') is False
    assert password.includes_lowercase('JfjrhfJ') is True
    assert password.includes_lowercase('FJHFHFHF') is False
    assert password.includes_lowercase('fdfdf') is True
    assert password.includes_lowercase('f3f35s1') is True


