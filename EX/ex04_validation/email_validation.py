"""Email validation."""


# Write your functions here
def has_at_symbol(email: str) -> bool:
    """Return true if email has @ symbol."""
    if '@' in email:
        return True
    return False


def is_valid_username(email: str) -> bool:
    """
    Return true if username do not contain symbols.
    The only symbol that can be used is '.'.
    """
    username = email.split('@')
    if len(username) > 2:
        return False
    for i in range(len(username[0])):
        if username[0][i].isdigit() or username[0][i].isalpha() or username[0][i] == '.':
            return True
        elif username[0][i].isalnum() and not username[0][i] == '.' and username[0][i] == ' ':
            return False
    print(username[0])


def find_domain():

    pass


def is_valid_domain():
    pass


def is_valid_email_address():
    pass


def create_email_address():
    pass


if __name__ == '__main__':
    print("Email has the @ symbol:")
    print(has_at_symbol("joonas.kivi@gmail.com"))  # -> True
    print(has_at_symbol("joonas.kivigmail.com"))  # -> False

    print("\nUsername has no special symbols:")
    print(is_valid_username("martalumi@taltech.ee"))  # -> True
    print(is_valid_username("marta.lumi@taltech.ee"))  # -> True
    print(is_valid_username("marta lumi@taltech.ee"))  # -> False
    print(is_valid_username("marta&lumi@taltech.ee"))  # -> False
    print(is_valid_username("marta@lumi@taltech.ee"))  # -> False

    print("\nFind the email domain name:")
    print(find_domain("karla.karu@saku.ee"))  # -> saku.ee
    print(find_domain("karla.karu@taltech.ee"))  # -> taltech.ee
    print(find_domain("karla.karu@yahoo.com"))  # -> yahoo.com
    print(find_domain("karla@karu@yahoo.com"))  # -> yahoo.com

    print("\nCheck if the domain is correct:")
    print(is_valid_domain("pihkva.pihvid@ttu.ee"))  # -> True
    print(is_valid_domain("metsatoll@&gmail.com"))  # -> False
    print(is_valid_domain("ewewewew@i.u.i.u.ewww"))  # -> False
    print(is_valid_domain("pannkook@m.oos"))  # -> False

    print("\nIs the email valid:")
    print(is_valid_email_address("DARJA.darja@gmail.com"))  # -> True
    print(is_valid_email_address("DARJA=darjamail.com"))  # -> False

    print("\nCreate your own email address:")
    print(create_email_address("hot.ee", "vana.ema"))  # -> vana.ema@hot.ee
    print(create_email_address("jaani.org", "lennakuurma"))  # -> lennakuurma@jaani.org
    print(create_email_address("koobas.com", "karu&pojad"))  # -> Cannot create a valid email address using the given parameters!
