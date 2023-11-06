"""WAT."""


def function_a(x: int) -> int:
    """Return 1."""
    return 1


def function_b(x: int) -> int:
    """Return x + 11."""
    return x + 11


def function_c(x: int) -> int:
    """Return x in power 8."""
    return x ** 8


def function_d(x: int) -> int:
    """Return x in power 2 multiplied by 36."""
    return x ** 2 * 36


def function_e(x: int) -> int:
    """Return x multiplied by 32."""
    return x * 32


def function_f(x: int) -> int:
    """Return sum - 2 of digits of x."""
    return sum([int(y) for y in str(x)]) - 2


def function_g(x: int) -> int:
    """Return -x."""
    return -x


def function_h(x: int) -> int:
    """Do func h."""
    return x * 1431


def function_i(x: int) -> int:
    """Return 0."""
    return 0


def function_j(x: int) -> int:
    """Return smth."""
    return x
