"""Email validation."""


# Write your functions here
def has_at_symbol(email: str) -> bool:
    """Return True if there is @ in email and False if not."""
    return '@' in email


def is_valid_username(email: str) -> bool:
    """
    Return True if username is valid.

    Username cannot contain any special symbols except '.'.
    """
    allowed_chars = set('abcdefghijklmnopqrstuvwxyz0123456789.')
    username = email.split('@')
    if len(username) != 2:
        return False
    for i in username[0]:
        if i.lower() not in allowed_chars:
            return False
    return True


def find_domain(email: str) -> str:
    """Return emails domain."""
    domain = email.split('@')[-1]
    return domain


def is_valid_domain(email: str) -> bool:
    """
    Return True if domain is valid.

    Domain has to contain only letters.
    Domain has to contain only one '.'.
    From @ to . has to be from 3 up to 12 elements.
    From . to end has to be from 2 up to 5 elements.
    """
    domain = find_domain(email)
    allowed_symbols = set('abcdefghijklmnopqrstuvwxyz.')
    if domain.count('.') != 1:
        return False
    for i in domain:
        if i.lower() not in allowed_symbols:
            return False
    parts = domain.split('.')
    if len(parts[0]) < 3 or len(parts[0]) > 10:
        return False
    if len(parts[1]) < 2 or len(parts[1]) > 5:
        return False
    return True


def is_valid_email_address(email: str) -> bool:
    """
    Return True if all conditions are met.

    has_at_symbol(email) => True
    is_valid_username(email) => True
    is_valid_domain(email) => True
    """
    if has_at_symbol(email) and is_valid_username(email) and is_valid_domain(email):
        return True
    return False


def create_email_address(domain: str, username) -> str:
    """Return valid email if it is possible and raise an error if it is not."""
    email = username + "@" + domain
    if is_valid_email_address(email):
        return email
    return 'Cannot create a valid email address using the given parameters!'


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
