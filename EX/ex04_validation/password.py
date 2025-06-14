"""Password validation."""


def is_correct_length(password: str) -> bool:
    """
    Check if the password's length is within the valid range.

    The password should have a length between 8 and 64 symbols.
    :param password: Password to be checked
    :return: True if the password's length is within the valid range, False otherwise
    """
    if 8 <= len(password) <= 64:
        return True
    return False


def includes_uppercase(password: str) -> bool:
    """
    Check if the password contains at least one uppercase letter.

    :param password: Password to be checked
    :return: True if the password contains at least one uppercase letter, False otherwise
    """
    for i in password:
        if i.isupper():
            return True
    return False


def includes_lowercase(password: str) -> bool:
    """
    Check if the password contains at least one lowercase letter.

    :param password: Password to be checked
    :return: True if the password contains at least one lowercase letter, False otherwise
    """
    for i in password:
        if i.islower():
            return True
    return False


def includes_special(password: str) -> bool:
    """
    Check if the password contains at least one special character (whitespace is also considered a special character).

    :param password: Password to be checked
    :return: True if the password contains at least one special character, False otherwise
    """
    for i in password:
        if not i.isalnum():
            return True
    return False


def includes_number(password: str) -> bool:
    """
    Check if the password contains at least one numeric digit.

    :param password: Password to be checked
    :return: True if the password contains at least one numeric digit, False otherwise
    """
    for i in password:
        if i.isdigit():
            return True
    return False


def is_different_from_old_password(old_pass: str, new_pass: str) -> bool:
    """
    Check if the new password is different enough from the old password.

    The overlap between the new password and old password should be less than 50%.
    The check for overlap is case-insensitive.
    The overlap is also checked for the reversed version of the new password.

    :param old_pass: The old password
    :param new_pass: The new password
    :return: True if the new password is different enough, False otherwise
    """
    old = old_pass.lower()
    new = new_pass.lower()
    if old == new or new == old[::-1]:
        return False
    if old in new or old in new[::-1]:
        if len(old) / len(new) * 100 >= 50:
            return False

    if new in old or new in old[::-1]:
        if len(new) / len(old) * 100 >= 50:
            return False

    part1 = find_the_longest_overlap_for_normal(old_pass, new_pass)
    part2 = find_the_longest_overlap_for_reversed(old_pass, new_pass)
    parts = []
    if part1 != '':
        parts.append(part1)
    if part2 != '':
        parts.append(part2)
    if len(parts) == 0:
        return True
    ret = max(parts, key=len)
    if len(ret) / len(new) >= 0.5:
        return False
    return True


def find_the_longest_overlap_for_normal(old_pass: str, new_pass: str) -> str:
    """Return the longest overlap match for normal."""
    repeated_parts = []
    repeated_part = ''
    new = new_pass.lower()
    old = old_pass.lower()

    for i in range(len(old)):
        for j in range(i, len(old)):
            substring = old[i:j + 1]
            if substring in new and len(substring) > len(repeated_part):
                repeated_part = substring

            if repeated_part != '':
                repeated_parts.append(repeated_part)
                repeated_part = ''
    if len(repeated_parts) == 0:
        return ''
    ret = max(repeated_parts, key=len)
    if ret != '':
        return ret
    return ''


def find_the_longest_overlap_for_reversed(old_pass: str, new_pass: str) -> str:
    """Return the longest overlap match for reversed."""
    repeated_parts = []
    repeated_part = ''
    new = new_pass[::-1].lower()
    old = old_pass.lower()
    for i in range(len(old)):
        for j in range(i, len(old)):
            substring = old[i:j]
            if substring in new and len(substring) > len(repeated_part):
                repeated_part = substring
            if repeated_part != '':
                repeated_parts.append(repeated_part)
                repeated_part = ''
    if len(repeated_parts) == 0:
        return ''
    ret = max(repeated_parts, key=len)
    if ret != '':
        return ret
    return ''


def is_name_in_password(password: str, name: str) -> bool:
    """
    Check if the password contains the name of the account owner.

    The name received as input may contain whitespace to separate the first and last name, neither of which should be
    present in the password.
    If the name contains a hyphen (such as Mari-Liis), neither part of the name should be present in the password.
    The name should not be in the password even if the casing of it is different in the password.
    Reversed format of the name is also not allowed in the password

    :param password: The password to be validated
    :param name: The full name of the account owner
    :return: True if the name is present in the password, False otherwise
    """
    name_list = name.split(' ')
    name_part = []
    for i in name_list:
        line = i.split('-')
        for x in line:
            name_part.append(x)
    for i in range(len(name_part)):
        if name_part[i].lower() in password.lower() or name_part[i][::-1].lower() in password.lower():
            return True
    return False


def is_birthday_in_password(password: str, birthdate: str) -> bool:
    """
    Check if the password contains the birthday of the account owner.

    The day, month or year in the birthdate cannot be present in the password. For the birth year, the last two digits
    of the birth year separately is also not allowed.

    For the day, month or last 2 digits of the year, the reversed number is allowed but for the full 4-digit year is
    not allowed in the reverse format.

    The date is always in the format "dd.mm.yyyy", where
    dd is 2-digit day (01, 02, .. 31)
    mm is 2-digit month (01, 02, .. 12)
    yyyy is 4-digit year (0001, 0002, ..., 2022, 2023, ..., 3000, ...)

    You don't have to validate the date.

    :param password: The password to be validated
    :param birthdate: Birthday of the account owner, format is dd.mm.yyyy
    :return: True if the birthday is present in the password, False otherwise
    """
    date = birthdate.split('.')
    for i in range(3):
        if date[i] in password:
            return True
    if date[2][-2::] in password:
        return True
    return False


def is_password_valid(new_password: str, old_password: str, name: str, birthdate: str) -> bool:
    """
    Check whether the given password is valid.

    This function combines several checks to determine if the provided password is valid.
    It checks the length, presence of uppercase and lowercase letters, inclusion of at least one number,
    inclusion of at least one special character, absence of the user's name and birthdate in the password.
    Call the functions you wrote before within this one to complete the validation.

    :param new_password: The password to be checked
    :param old_password: the previous password of this account
    :param name: The user's full name
    :param birthdate: The user's birthdate
    :return: True if the password is valid, False otherwise.
    """
    if is_correct_length(new_password) and includes_number(new_password) and includes_lowercase(new_password) \
            and includes_uppercase(new_password) and includes_special(new_password) \
            and is_different_from_old_password(old_password, new_password) \
            and not is_name_in_password(new_password, name) and not is_birthday_in_password(new_password, birthdate):
        return True
    return False


if __name__ == '__main__':
    print("Password length validation:")
    print(is_correct_length("kascnewi3r34t"))  # -> True
    print(is_correct_length("%df#S1"))  # -> False
    print(is_correct_length("kascn¤e%wi3r34tkj*bö ihvlc&?¤kfxyzsr<eq 3454566FGHJOI*UYUF& %¤##&TTRq6"))  # -> False

    print("\nPassword has at least one uppercase letter validation:")
    print(includes_uppercase("Defwefwevwe"))  # -> True
    print(includes_uppercase("e/¤!fwe64fwevw"))  # -> False

    print("\nPassword has at least one lowercase letter validation:")
    print(includes_lowercase("dJOWE821%&/"))  # -> True
    print(includes_lowercase("ÖJOWE821%&/"))  # -> False

    print("\nPassword has at least one special character validation:")
    print(includes_special("&smqwdp24DS"))  # -> True
    print(includes_special("ksmqwd p24DS"))  # -> True
    print(includes_special("ksmqwdp24DS"))  # -> False
    print(includes_special(""))  # -> False

    print("\nPassword has at least one number validation:")
    print(includes_number("dJOWE8%&/"))  # -> True
    print(includes_number("ÖJOWE%&/"))  # -> False

    print("\nNew password is different from the old one validation:")
    print(is_different_from_old_password("õunamoos", "maasikamoos"))  # -> True
    print(is_different_from_old_password("olevsulev67", "ämblikmees18"))  # -> True
    print(is_different_from_old_password("seinav2rv", "seinakapp"))  # -> False
    print(is_different_from_old_password("merineitsi99", "mereneitsi11"))  # -> False
    print(is_different_from_old_password("eva1970", "0791ave"))  # -> False
    print(is_different_from_old_password("eva1970", "0791avyryryr"))  # -> True
    print(is_different_from_old_password("123456", "654321"))  # -> False
    print(is_different_from_old_password("1234ty", "iu4321"))  # -> False
    print(is_different_from_old_password("pass", "passaaa"))  # -> False
    print(is_different_from_old_password("pass", "aaapass"))  # -> False
    print(is_different_from_old_password("aaapass", "pass"))  # -> False
    print(is_different_from_old_password("aaapass", "pass"))  # -> False
    print(is_different_from_old_password('12345678', '87654321'))  # -> False
    print(is_different_from_old_password('Danil567123', 'xxx67123'))  # -> False
    print(is_different_from_old_password('aaa123', 'bb123'))

    print("\nPassword has your name:")
    print(is_name_in_password("ddccwemelani", "Melani Mets"))  # -> True
    print(is_name_in_password("ddccwinalemw", "Melani Mets"))  # -> True
    print(is_name_in_password("ddccwsSTEMq", "Melani Mets"))  # -> True
    print(is_name_in_password("ddccwinagregorq", "Karl-Gregor Mustikas"))  # -> True
    print(is_name_in_password("ddccwinamustikas", "Karl-Gregor Mustikas"))  # -> True

    print("\nPassword has your birthdate:")
    print(is_birthday_in_password("dd&&ccwe30", "30.04.2023"))  # -> True
    print(is_birthday_in_password("dd&&ccwe03", "30.04.2023"))  # -> False
    print(is_birthday_in_password("ddccw%2023", "30.04.2023"))  # -> True
    print(is_birthday_in_password("ddccw%3202", "30.04.2023"))  # -> True
    print(is_birthday_in_password("04ddccw%&1", "30.04.2023"))  # -> True
    print(is_birthday_in_password("40ddccw%&1", "30.04.2023"))  # -> False
    print(is_birthday_in_password("56ddccw%&1", "30.04.2023"))  # -> False
    print(is_birthday_in_password("23ddccw%&1", "30.04.2023"))  # -> True

    print("\nPassword is completely validated:")
    print(is_password_valid("k45aLK%1", "SunsetBeach2022!", "Marek Põõsas", "26.06.2003"))  # -> True
    print(is_password_valid("keramRTYUY2003RDSCF.", "PurpleDragon42*", "Marek Põõsas", "12.04.2003"))  # -> False
