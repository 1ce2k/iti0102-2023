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
    assert password.includes_uppercase('QWERTYUIOPASDFGHJKLZXCVBNM') is True


def test_includes_lowercase():
    """Test if there are some lowercase in password."""
    assert password.includes_lowercase('') is False
    assert password.includes_lowercase('JfjrhfJ') is True
    assert password.includes_lowercase('FJHFHFHF') is False
    assert password.includes_lowercase('fdfdf') is True
    assert password.includes_lowercase('f3f35s1') is True


def test_includes_special():
    """Test if password has any specials or not."""
    assert password.includes_special('') is False
    assert password.includes_special('ksmqwd p24DS') is True
    assert password.includes_special('fegfvbbhefb') is False
    assert password.includes_special('!"№;;()*:_-') is True
