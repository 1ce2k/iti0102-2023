"""Password validation tests."""
# import password
import EX.ex04_validation.password as password

# ---------- Tests if password is correct length ----------

def test__is_correct_length_empty():
    """Test empty password."""
    assert password.is_correct_length('') is False


def test__is_correct_length_too_low():
    """Test password length < 8."""
    assert password.is_correct_length("passwor") is False


def test__is_correct_length_too_high():
    """Test password length > 64."""
    assert password.is_correct_length("a" * 65) is False


def test__is_correct_length_min():
    """Test password min length."""
    assert password.is_correct_length('password') is True


def test__is_correct_length_max():
    """Test password max length."""
    assert password.is_correct_length('a' * 64) is True


# ---------- Tests if password includes uppercase ----------

def test__includes_uppercase_empty():
    """Test passwords length that passes."""
    assert password.includes_uppercase('') is False


def test__includes_uppercase_every_letter():
    """Test all uppercase letters."""
    assert password.includes_uppercase('QWERTYUIOPASDFGHJKLZXCVBNM') is True


def test__includes_uppercase_only():
    """Test if there are only uppercase in password."""
    assert password.includes_uppercase('DGPEJNF') is True


def test__includes_uppercase_true_but_not_first():
    """Test if there are some uppercase in password."""
    assert password.includes_uppercase('fDGPEJNF') is True


def test__includes_uppercase_includes_number():
    """Test if there are some uppercase in password."""
    assert password.includes_uppercase('fDGPE3994JNF') is True


# ---------- Tests if password includes lowercase ----------

def test__includes_lowercase_empty():
    """Test empty password."""
    assert password.includes_lowercase('') is False


def test__includes_lowercase_all_letters():
    """Test all lowercase letters."""
    assert password.includes_lowercase('qwertyuiopasdfghjklzxcvbnm') is True


def test__includes_lowercase_only_lower():
    """Test if there are no lowercase in password."""
    assert password.includes_lowercase('fjghrghj') is True


def test__includes_lowercase_includes_number():
    """Test if there are some lowercase in password."""
    assert password.includes_lowercase('f3f35s1') is True


def test__includes_lowercase_not_first_lower():
    """Test if there are lowercase but not first one."""
    assert password.includes_lowercase('Fjfjfhh') is True


# ---------- Tests if password includes specials ----------

def test__includes_special_empty():
    """Test empty."""
    assert password.includes_special('') is False


def test__includes_special_fails():
    """Test if password has any specials."""
    assert password.includes_special('fegfvbbhefb') is False


def test__includes_special_includes_whitespace():
    """Test if there is a whitespace in password."""
    assert password.includes_special('ksmqwd p24DS') is True


def test__includes_special_no_several_specials():
    """Test if password has specials."""
    assert password.includes_special('!"№;;()*:_-') is True


def test__includes_special_no_special():
    """Test if password has no specials."""
    assert password.includes_special('jfjhrygfry') is False


# ---------- Tests if password includes numbers ----------

def test__include_number():
    """Test empty."""
    assert password.includes_number('') is False


def test__include_number_all_digits():
    """Test all digits."""
    assert password.includes_number('1234567890') is True


def test__include_number_fails():
    """Test if there are no digits."""
    assert password.includes_number('dfjehfuhFEDFeuhs') is False


def test__include_number_passes():
    """Test if there are digits in."""
    assert password.includes_number('dfjrfhrj34kfk') is True


# ---------- Tests if passwords are different enough ----------

def test__is_different__old_pass_case_sensitive_all_letters():
    """Test 1."""
    assert password.is_different_from_old_password('PASS', 'pass') is False


def test__is_different__old_pass_case_sensitive_one_letter():
    """Test 2."""
    assert password.is_different_from_old_password('pasS', 'pass') is False


def test__is_different__new_pass_case_sensitive_all_letters():
    """Test 3."""
    assert password.is_different_from_old_password('pass', 'PASS') is False


def test__is_different__new_pass_case_sensitive_one_letter():
    """Test 4."""
    assert password.is_different_from_old_password('pass', 'Pass') is False


def test__is_different__new_pass_even_length__barely_different():
    """Test 5."""
    assert password.is_different_from_old_password('new_pas', 'password') is True


def test__is_different__new_pass_even_length__barely_not_different():
    """Test 6."""
    assert password.is_different_from_old_password('123bbb', '123aaa') is False


def test__is_different__new_pass_even_length__barely_different_reverse():
    """Test 7."""
    assert password.is_different_from_old_password('aaab', 'baaa564712') is True


def test__is_different__new_pass_even_length__barely_not_different_reverse():
    """Test 8."""
    assert password.is_different_from_old_password('aaab', 'baaa5621') is False


def test__is_different__new_pass_even_length__barely_not_different__not_in_beginning():
    """Test 9."""
    assert password.is_different_from_old_password('pass', '123pass4') is False


def test__is_different__new_pass_odd_length__barely_different():
    """Test 10."""
    assert password.is_different_from_old_password('new_pas', 'passwor') is True


def test__is_different__new_pass_odd_length__barely_not_different():
    """Test 11."""
    assert password.is_different_from_old_password('123bbb', '123aa') is False


def test__is_different__new_pass_odd_length__barely_different_reverse():
    """Test 12."""
    assert password.is_different_from_old_password('aaab', 'baaa56471') is True


def test__is_different__new_pass_odd_length__barely_not_different_reverse():
    """Test 13."""
    assert password.is_different_from_old_password('aaab', 'baaa561') is False


def test__is_different__new_pass_odd_length__barely_not_different__not_in_beginning():
    """Test 14."""
    assert password.is_different_from_old_password('pass', '123pass') is False
