"""Password validation tests."""
# from EX.ex04_validation import password
import password


def test__is_correct_length_empty():
    """Test empty password."""
    assert password.is_correct_length('') is False


def test__is_correct_length_fails():
    """Test passwords length that fails."""
    assert password.is_correct_length("passwor") is False
    assert password.is_correct_length("a" * 65) is False


def test__is_correct_length_passed():
    """Test passwords length that passes."""
    assert password.is_correct_length('password') is True
    assert password.is_correct_length('a' * 64) is True


def test__includes_uppercase_empty():
    """Test passwords length that passes."""
    assert password.includes_uppercase('') is False


def test__includes_uppercase_every_letter():
    """Test all uppercase letters."""
    assert password.includes_uppercase('QWERTYUIOPASDFGHJKLZXCVBNM') is True


def test__includes_uppercase_fails():
    """Test if there are no uppercase in password."""
    assert password.includes_uppercase('e/¤!fwe64fwevw') is False


def test__includes_uppercase_passes():
    """Test if there are some uppercase in password."""
    assert password.includes_uppercase('Defwefwevwe') is True
    assert password.includes_uppercase('fDGPEJNF') is True
    assert password.includes_uppercase('DGPEJNF') is True


def test__includes_lowercase_empty():
    """Test empty password."""
    assert password.includes_lowercase('') is False


def test__includes_lowercase_all_letters():
    """Test all lowercase letters."""
    assert password.includes_lowercase('qwertyuiopasdfghjklzxcvbnm') is True


def test__includes_lowercase_fails():
    """Test if there are no lowercase in password."""
    assert password.includes_lowercase('FJHFHFHF') is False


def test__includes_lowercase_passes():
    """Test if there are some lowercase in password."""
    assert password.includes_lowercase('JfjrhfJ') is True
    assert password.includes_lowercase('fdfdf') is True
    assert password.includes_lowercase('f3f35s1') is True


def test__includes_special_fails():
    """Test if password has any specials."""
    assert password.includes_special('') is False
    assert password.includes_special('fegfvbbhefb') is False


def test__includes_special_passes():
    """Test if password has specials."""
    assert password.includes_special('ksmqwd p24DS') is True
    assert password.includes_special('!"№;;()*:_-') is True


def test__include_number():
    """Test if there is a digit in password."""
    assert password.includes_number('') is False
    assert password.includes_number('1234567890') is True
    assert password.includes_number('dfjrfhrj34kfk') is True
    assert password.includes_number('dfjehfuhFEDFeuhs') is False


def test__is_different_enough():
    """Tests if old and new passwords are different."""
    assert password.is_different_from_old_password('123bb', '123aa') is False
    assert password.is_different_from_old_password('123bbb', '123aaa') is False
    assert password.is_different_from_old_password('pass', 'PASS') is False
    assert password.is_different_from_old_password('pass', 'Pass') is False
    assert password.is_different_from_old_password('pasS', 'pass') is False
    assert password.is_different_from_old_password('PASS', 'pass') is False
    assert password.is_different_from_old_password("1234ty", "iu4321") is False
    assert password.is_different_from_old_password('pas3', '12pas34') is False
    assert password.is_different_from_old_password('pass', '123pass4') is False
    assert password.is_different_from_old_password('pass', 'new_pas') is True
    assert password.is_different_from_old_password('pas', 'password') is True
    assert password.is_different_from_old_password('aaba', 'abaa12341') is True
    assert password.is_different_from_old_password('aba', 'aba12341') is True
    assert password.is_different_from_old_password('eva1970', '0791jfjf') is True
    assert password.is_different_from_old_password('eva19701', '10791jfjf') is True
