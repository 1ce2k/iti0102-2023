"""Control number."""


def control_number(encrypted_string: str) -> bool:
    """
    Given encrypted string that has a control number in the end of it, return True if correct, else False.

    Calculating the correct control number:
    1. Start the calculation from 0.
    2. Add 1 for every lowercase occurrence.
    3. Add 2 for every uppercase occurrence.
    4. Add 5 for any of the following symbol occurrences: "?!@#".
    Other symbols/letters/digits don't affect the result.

    NB! If for example the number you come up with is 25, you only have to check the last two digits of the string.
    e.g. control_number("?!?!#4525") -> True, because it ends with 25.

    :param encrypted_string: encrypted string
    :return: validation
    """
    res = 0
    symbols_for_5 = ['?', '!', '@', '#']
    num_from_str = ''
    nums = []
    for char in encrypted_string:
        if char in symbols_for_5:
            res += 5
            num_from_str = ''
        if char.isalpha():
            num_from_str = ''
            if char == char.lower():
                res += 1
            else:
                res += 2
        if char.isdigit():
            num_from_str = num_from_str + char
    if num_from_str != '':
        nums.append(int(num_from_str))
    if len(nums) == 1:
        if int(encrypted_string[-1]) == 0:
            return True
    else:
        if res == nums[-1]:
            return True
    return False


if __name__ == '__main__':
    print(control_number("mE0W5"))  # True
    print(control_number("SomeControlNR?20"))  # False
    print(control_number("False?Nr9"))  # False
    print(control_number("#Hello?!?26"))  # True
    print(control_number("3423982340000000.....///....0"))  # True
    print(control_number("#Shift6"))  # False
