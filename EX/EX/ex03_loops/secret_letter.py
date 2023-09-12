"""Secret letter."""


def secret_letter(letter: str) -> bool:
    """
    Check if the given secret letter follows all the necessary rules. Return True if it does, else False.

    Rules:
    1. The letter has more uppercase letters than lowercase letters.
    2. The sum of digits in the letter has to be equal to or less than the amount of uppercase letters.
    3. The sum of digits in the letter has to be equal to or more than the amount of lowercase letters.

    :param letter: secret letter
    :return: validation
    """
    upper_count = 0
    lower_count = 0
    sum_of_digits = 0
    for char in letter:
        if char.isalpha():
            if char == char.lower():
                lower_count += 1
            if char == char.upper():
                upper_count += 1
        if char.isdigit():
            sum_of_digits += int(char)
    if lower_count > upper_count:
        return False
    if sum_of_digits > upper_count:
        return False
    if sum_of_digits < lower_count:
        return False

    return True


if __name__ == '__main__':
    print(secret_letter("sOMEteSTLETTer8"))  # True
    print(secret_letter("thisisNOTvaliD4"))  # False
    print(secret_letter("TOOMANYnumbers99"))  # False
    print(secret_letter("anotherVALIDLETTER17"))  # True
    print(secret_letter("CANBENOLOWERCASENODIGITS"))  # True
