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
    first_name = None
    last_name = None
    id_code = None
    phone_num = None
    date_of_birth = None
    address = None

    # name_pattern = r'^[A-Z][a-z]+[A-Z][a-z]+'
    name_pattern = r'(^[A-Z][a-z]+)([A-Z][a-z]+)'
    id_pattern = r'\d{11}'
    phone_pattern = r'(?<=\d{11})(\+?\d{3} \d{8})'
    dob_pattern = r'\d{2}-\d{2}-\d{4}'

    name_match = re.findall(name_pattern, row)
    id_match = re.search(id_pattern, row)
    phone_match = re.search(phone_pattern, row)
    dob_match = re.search(dob_pattern, row)

    if name_match:
        first_name, last_name = name_match[0][0], name_match[0][1]

    if id_match:
        id_code = id_match.group(0)

    if phone_match:
        phone_num = phone_match.group(0)
        if '+' not in phone_num:
            phone_num = '+' + phone_num
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
    if address == '':
        address = None
    return first_name, last_name, id_code, phone_num, date_of_birth, address




if __name__ == '__main__':
    print(1)
    print(parse('PriitPann39712047623+372 5688736402-12-1998Oja 18-2,Pärnumaa,Are'))
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
