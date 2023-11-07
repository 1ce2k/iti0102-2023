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
    assert password.includes_lowercase('qwertyuiopasdfghjklzxcvbnm') is True


def test_includes_special():
    """Test if password has any specials or not."""
    assert password.includes_special('') is False
    assert password.includes_special('ksmqwd p24DS') is True
    assert password.includes_special('fegfvbbhefb') is False
    assert password.includes_special('!"№;;()*:_-') is True


def test_include_number():
    """Test if there is a digit in password."""
    assert password.includes_number('') is False
    assert password.includes_number('1234567890') is True
    assert password.includes_number('dfjrfhrj34kfk') is True
    assert password.includes_number('dfjehfuhFEDFeuhs') is False


def test_is_different_enough():
    """Tests if old and new passwords are different."""
    assert password.is_different_from_old_password('pass', 'PASS') is False
    assert password.is_different_from_old_password('pass', 'Pass') is False
    assert password.is_different_from_old_password('pasS', 'pass') is False
    assert password.is_different_from_old_password('PASS', 'pass') is False
    assert password.is_different_from_old_password('pass', 'new_pas') is True
    assert password.is_different_from_old_password('pass', 'ssap') is False
    assert password.is_different_from_old_password('aaaab', 'baaaa') is False
