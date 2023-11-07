"""Password validation tests."""
import password


# ---------- Tests if password is correct length ----------

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


# ---------- Tests if password includes uppercase ----------

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


# ---------- Tests if password includes lowercase ----------

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


# ---------- Tests if password includes specials ----------

def test__includes_special_empty():
    """Test empty."""
    assert password.includes_special('') is False


def test__includes_special_fails():
    """Test if password has any specials."""
    assert password.includes_special('fegfvbbhefb') is False


def test__includes_special_passes():
    """Test if password has specials."""
    assert password.includes_special('ksmqwd p24DS') is True
    assert password.includes_special('!"№;;()*:_-') is True


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

def test__is_different__old_pass_case_sensitive():
    """Test 1."""
    assert password.is_different_from_old_password('PASS', 'pass') is False
    assert password.is_different_from_old_password('pasS', 'pass') is False


def test__is_different__new_pass_case_sensitive():
    """Test 2."""
    assert password.is_different_from_old_password('pass', 'PASS') is False
    assert password.is_different_from_old_password('pass', 'Pass') is False


def test__is_different__new_pass_even_length__barely_different():
    """Test 3."""
    assert password.is_different_from_old_password('new_pas', 'password') is True


def test__is_different__new_pass_even_length__barely_not_different():
    """Test 4."""
    assert password.is_different_from_old_password('123bbb', '123aaa') is False


def test__is_different__new_pass_even_length__barely_different_reverse():
    """Test 5."""
    assert password.is_different_from_old_password('aaab', 'baaa564712') is True


def test__is_different__new_pass_even_length__barely_not_different_reverse():
    """Test 6."""
    assert password.is_different_from_old_password('aaab', 'aaa562') is False


def test__is_different__new_pass_even_length__barely_not_different__not_in_beginning():
    """Test 8."""
    assert password.is_different_from_old_password('pass', '123pass4') is False




# def test__is_different__new_pass_odd_length__barely_not_different__not_in_beginning():
#     """Test 5."""
#     assert password.is_different_from_old_password('pas3', '12pas34') is False


# def test__is_different__new_pass_odd_length__barely_different():
#     """Test 6."""
#     assert password.is_different_from_old_password('pas', 'password') is True


# def test__is_different__new_pass_odd_length__barely_not_different():
#     """Test 7."""
#     assert password.is_different_from_old_password('123bb', '123aa') is False


# def test__is_different__new_pass_odd_length__barely_different__reverse():
#     """Test 9."""
#     assert password.is_different_from_old_password('aaba', 'abaa12341') is True


# def test__is_different__new_pass_odd_length__barely_not_different__reverse():
#     """Test 10."""
#     assert password.is_different_from_old_password('eva19701', '10791jfjf') is False

# def test__is_different__new_pass_even_length__barely_not_different__reverse():
#     """Test 11."""
#     assert password.is_different_from_old_password('eva1970', '0791jfjf') is False


# def test__is_different__new_pass_even_length__barely_not_different_reverse():
#     """Test 12."""
#     assert password.is_different_from_old_password('45678', '87654fgf') is False





#     """Tests if old and new passwords are different."""
#     assert password.is_different_from_old_password("1234ty", "iu4321") is False
#     assert password.is_different_from_old_password('aba', 'aba12341') is True
