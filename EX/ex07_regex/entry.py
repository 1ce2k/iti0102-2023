"""Entry."""
import re


def parse(row: str) -> tuple:
    """
    Parse string row into a tuple.

    The row has a first name, last name, ID code, phone number, date of birth and address.
    'name,lastname,id,phone,date,address
    Only ID code is mandatory, other values may not be included.

    They can be found by the following rules:
    - Both the first name and last name begin with a capital letter and are followed by a lowercase letter
    - ID code is an 11-digit number
    - Phone number has the same rules applied as in the previous task
    - Date of birth is in the form of dd-MM-YYYY
    - Address is everything else that's left

    :param row: given string to find values from
    :return: tuple of values found in given string
    """
    first_name, last_name, id_code, phone_num, date_of_birth, address = None, None, None, None, None, None

    name_match = re.search(r'(^[A-Z][a-z]+)([A-Z][a-z]+)', row)
    id_match = re.search(r'\d{11}', row)
    phone_match = re.search(r'(?<=\d{11})\s?(\+?\d{3}\s?\d{8}|\d{8})', row)
    dob_match = re.search(r'\d{2}-\d{2}-\d{4}', row)

    if name_match:
        first_name, last_name = name_match.group(1), name_match.group(2)

    if id_match:
        id_code = id_match.group(0)

    if phone_match:
        phone_num = "+" + phone_match.group(0) if phone_match.group(0).startswith('372') else phone_match.group(0)
    # "+" + phone_match.group(0) if not phone_match.group(0).startswith('+') else
    if dob_match:
        date_of_birth = dob_match.group(0)

    if dob_match:
        address = row[dob_match.end():]
    elif phone_match:
        address = row[phone_match.end():]
    elif id_match:
        address = row[id_match.end():]
    else:
        address = None
    if not address:
        address = None
    return first_name, last_name, id_code, phone_num, date_of_birth, address


if __name__ == '__main__':
    print(1)
    print(parse('PriitPann397120476235688736402-12-1998Oja 18-2,Pärnumaa,Are'))
    # ('Priit', 'Pann', '39712047623', '+372 56887364', '02-12-1998', 'Oja 18-2,Pärnumaa,Are')
    print(2)
    print(parse('39712047623+372 5688736402-12-1998Oja 18-2,Pärnumaa,Are'))
    # (None, None, '39712047623', None, None, None)
    print(3)
    print(parse('PriitPann3971204762302-12-1998Oja 18-2,Pärnumaa,Are'))
    # ('Priit', 'Pann', '39712047623', None, '02-12-1998', 'Oja 18-2,Pärnumaa,Are')
    print(4)
    print(parse('PriitPann39712047623372 56887364Oja 18-2,Pärnumaa,Are'))
    # ('Priit', 'Pann', '39712047623', '+372 56887364', None, 'Oja 18-2,Pärnumaa,Are')
    print(5)
    print(parse('39712047623'))
    # (None, None, '39712047623', None, None, None)
