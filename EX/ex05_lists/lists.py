"""Phone inventory."""


def list_of_phones(all_phones: str) -> list:
    """
    Return list of phones.

    The input string contains of phone brands and models, separated by comma.
    Both the brand and the model do not contain spaces (both are one word).

    "Google Pixel,Honor Magic5,Google Pixel" => ["Google Pixel', 'Honor Magic5', 'Google Pixel"]
    """
    if len(all_phones) == 0:
        return []
    return all_phones.split(',')


def phone_brands(all_phones: str) -> list:
    """
    Return list of unique phone brands.

    The order of the elements should be the same as in the input string (first appearance).

    "Google Pixel,Honor Magic5,Google Pixel" => ["Google", "Honor"]
    """
    if len(all_phones) == 0:
        return []
    phones = all_phones.split(',')
    brands = []
    for phone in phones:
        brand = phone.split(' ')
        if brand[0] not in brands:
            brands.append(brand[0])
    return brands


def phone_models(all_phones: str) -> list:
    """
    Return list of unique phone models.

    The order of the elements should be the same as in the input string (first appearance).

    "Honor Magic5,Google Pixel,Honor Magic4" => ['Magic5', 'Pixel', 'Magic4']
    """
    if len(all_phones) == 0:
        return []
    phones = all_phones.split(',')
    models = []
    for phone in phones:
        model = phone.replace(phone.split(' ')[0] + ' ', '')
        if model not in models:
            models.append(model)
    return models


def search_by_brand(all_phones: str, phone_brand: str) -> list:
    """Return list of phones from one brand."""
    phones = all_phones.split(',')
    ret = []
    for phone in phones:
        brand = phone.split(' ')
        if brand[0].lower() == phone_brand.lower():
            ret.append(phone)
    return ret


def search_by_model(all_phones: str, phone_model: str) -> list:
    """Return list of phones of same model."""
    phones = all_phones.split(',')
    ret = []
    for phone in phones:
        model = phone.replace(phone.split(' ')[0] + ' ', '')
        model_part = model.split(' ')
        print(model, model_part)
        for i in range(len(model_part)):
            if phone_model.lower() == model_part[i].lower():
                ret.append(phone)
    return ret


if __name__ == '__main__':
    print(list_of_phones("Google Pixel,Honor Magic5,Google Pixel"))  # ["Google Pixel', 'Honor Magic5', 'Google Pixel"]
    print(phone_brands(
        "Google Pixel,Honor Magic5,Google Pix,Honor Magic6,IPhone 12,Samsung S10,Honor Magic,IPhone 11"))  # ['Google', 'Honor', 'IPhone', 'Samsung']
    print(phone_brands("Google Pixel,Google Pixel,Google Pixel,Google Pixel"))  # ['Google']
    print(phone_brands(""))  # []
    print(phone_models("IPhone 14,Google Pixel,Google Pixel 2022, Honor Magic5,IPhone 14"))  # ['14', 'Pixel', 'Magic5']
    # print(search_by_model("IPhone X,IPhone 12 Pro,IPhone 14 pro Max", 'max'))
    # print(search_by_model("IPhone X,IPhone 12 Pro,IPhone 14 pro Max", '1'))
    # print(search_by_model("Google Pixel 2021,Google Pixel 2022", 'Pixel'))
