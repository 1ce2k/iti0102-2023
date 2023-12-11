"""Some cool pyramids."""


def create_simple_pyramid_left(height: int) -> str:
    """
    Create simple pyramid on the left side.

    Use recursion!

    create_simple_pyramid_left(4) => *
                                     **
                                     ***
                                     ****

    :param height: Pyramid height.
    :return: Pyramid.
    """
    if height == 0:
        return ''
    else:
        stars = '*' * height
        return create_simple_pyramid_left(height - 1) + f'{stars}\n'


def create_simple_pyramid_right(height: int, current=1) -> str:
    """
    Create simple pyramid on the right side.

    Use recursion!

    create_simple_pyramid_right(4) =>   *
                                       **
                                      ***
                                     ****

    :param height: Pyramid height.
    :param current: Keeping track of current layer.
    :return: Pyramid.
    """
    if current > height:
        return ""

    spaces = " " * (height - current)
    stars = "*" * current
    layer = spaces + stars + "\n"
    return layer + create_simple_pyramid_right(height, current + 1)


def create_number_pyramid_left(height: int, current=1) -> str:
    """
    Create left-aligned number pyramid.

    Use recursion!

    create_number_pyramid_left(4) => 1
                                     12
                                     123
                                     1234

    :param height: Pyramid height.
    :param current: Keeping track of current layer.
    :return: Pyramid.
    """
    if current > height:
        return ""

    current_line = ''.join(str(i) for i in range(1, current + 1))
    next_lines = create_number_pyramid_left(height, current + 1)
    pyramid = f"{current_line}\n{next_lines}" if next_lines else current_line
    return pyramid


def create_number_pyramid_right(height: int, current=1) -> str:
    """
    Create right-aligned number pyramid.

    Use recursion!

    create_number_pyramid_right(4) =>    1
                                        21
                                       321
                                      4321

    :param height: Pyramid height.
    :param current: Keeping track of current layer.
    :return: Pyramid.
    """
    if current > height:
        return ''

    spaces = ' ' * (height - current)
    numbers = ''.join(str(i) for i in range(current, 0, -1))
    pyramid_layer = spaces + numbers + '\n'

    return pyramid_layer + create_number_pyramid_right(height, current + 1)


def create_number_pyramid_left_down(height: int, current=1) -> str:
    """
    Create left-aligned number pyramid upside-down.

    Use recursion!

    create_number_pyramid_left(4) => 4321
                                     321
                                     21
                                     1

    :param height: Pyramid height.
    :param current: Keeping track of current layer.
    :return: Pyramid.
    """
    if current > height:  # Base case: when current layer exceeds the height
        return ''

    layer = ''.join(str(i) for i in range(height, current - 1, -1))  # Generate the current layer
    pyramid_rest = create_number_pyramid_left_down(height, current + 1)  # Recursively generate the rest of the pyramid

    return layer + '\n' + pyramid_rest if pyramid_rest else layer  # Combine current layer with the rest of the pyramid


print(create_number_pyramid_left_down(4))



def create_number_pyramid_right_down(height: int, current=1) -> str:
    """
    Create right-aligned number pyramid upside-down.

    Use recursion!

    create_number_pyramid_right(4) => 1234
                                       123
                                        12
                                         1

    :param height: Pyramid height.
    :param current: Keeping track of current layer.
    :return: Pyramid.
    """
    pass


def create_regular_pyramid(height: int, current=1) -> str:
    """
    Create regular pyramid.

    Use recursion!

    create_regular_pyramid(4) =>    *
                                   ***
                                  *****
                                 *******

    :param height: Pyramid height.
    :param current: Keeping track of current layer.
    :return: Pyramid.
    """
    if current > height:
        return ""

    spaces = " " * (height - current)
    stars = "*" * (2 * current - 1)

    pyramid_layer = spaces + stars + "\n"

    return pyramid_layer + create_regular_pyramid(height, current + 1)


def create_regular_pyramid_upside_down(height: int, current=1) -> str:
    """
    Create regular pyramid upside down.

    Use recursion!

    create_regular_pyramid_upside_down(4) => *******
                                              *****
                                               ***
                                                *

    :param height: Pyramid height.
    :param current: Keeping track of current layer.
    :return: Pyramid.
    """
    pass


def create_diamond(height: int, current=1) -> str:
    """
    Create diamond.

    Use recursion!

    create_diamond(4) =>    *
                           ***
                          *****
                         *******
                         *******
                          *****
                           ***
                            *

    :param height: Height of half of the diamond.
    :param current: Keeping track of current layer.
    :return: Diamond.
    """
    pass


def create_empty_pyramid(height: int, current=1) -> str:
    """
    Create empty pyramid.

    Use recursion!

    create_empty_pyramid(4) =>    *
                                 * *
                                *   *
                               *******

    :param height: Pyramid height.
    :param current: Keeping track of current layer.
    :return: Pyramid.
    """
    pass

