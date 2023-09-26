def number_of_phones(all_phones: str) -> list:
    """
    Create a list of tuples with brand quantities.

    The result is a list of tuples.
    Each tuple is in the form: (brand_name: str, quantity: int).
    The order of the tuples (brands) is the same as the first appearance in the list.
    """
    if all_phones == '':
        return []
    phones = all_phones.split(',')
    brands = []
    ret = []
    for phone in phones:
        brand = phone.split(' ')[0]
        brands.append(brand)
    for i in brands:
        new_tuple = (i, brands.count(i))
        if new_tuple not in ret:
            ret.append((i, brands.count(i)))
    return ret


def phone_list_as_string(phone_list: list) -> str:
    """
    Create a list of phones.

    The input list is in the same format as the result of phone_brand_and_models function.
    The order of the elements in the string is the same as in the list.
    [['IPhone', ['11']], ['Google', ['Pixel']]] =>
    "IPhone 11,Google Pixel"
    """


if __name__ == "__main__":
    print(number_of_phones('Iphone 12,samsung 9,huawei honor,Iphone 13'))