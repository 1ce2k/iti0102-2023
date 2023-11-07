"""Create beautiful fractal images."""
from PIL import Image


class Fractal:
    """Fractal class."""

    def __init__(self, size, scale, computation):
        """
        Initialize fractal.

        Arguments:
        size -- the size of the image as a tuple (x, y)
        scale -- the scale of x and y as a list of 2-tuple
                 [(minimum_x, minimum_y), (maximum_x, maximum_y)]
                 these are mathematical coordinates
        computation -- the function used for computing pixel values as a function
        """
        self.size = size
        self.scale = scale
        self.computation = computation
        self.image = Image.new("RGB", size)

    def compute(self):
        """Create the fractal by computing every pixel value."""
        pass

    def pixel_value(self, pixel):
        """
        Return the number of iterations it took for the pixel to go out of bounds.

        Arguments:
        pixel -- the pixel coordinate (x, y)

        Returns:
        the number of iterations of computation it took to go out of bounds as integer.
        """
        pass

    def save_image(self, filename):
        """
        Save the image to hard drive.

        Arguments:
        filename -- the file name to save the file to as a string.
        """
        self.image.save(filename)


def mandelbrot_computation(x: float, y: float, x_original: float, y_original: float) -> tuple:
    """
    Return single iteration result of computation as tuple[x, y].

    :param x - mathematical x coordinate (transformed)
    :param y - mathematical y coordinate (transformed)
    :param x_original - mathematical x coordinate of pixel
    :param y_original - mathematical y coordinate of pixel

    :return tuple[x, y] after single iteration
    """
    x_squared = x * x
    y_squared = y * y
    xy = x * y

    x_new = x_squared - y_squared + x_original
    y_new = 2 * xy + y_original

    return x_new, y_new


def julia_computation(x: float, y: float, x_original: float, y_original: float) -> tuple:
    """
    Return single iteration result of computation as tuple[x, y].

    For different c and n make new function rather than change these constants.
    Otherwise tester will not give you any points :p

    :param x - mathematical x coordinate (transformed)
    :param y - mathematical y coordinate (transformed)
    :param x_original - mathematical x coordinate of pixel
    :param y_original - mathematical y coordinate of pixel

    :return tuple[x, y] after single iteration
    """
    c = -0.7869 + 0.1889j  # DO NOT CHANGE
    n = 3  # DO NOT CHANGE

    pass


def ship_computation(x: float, y: float, x_original: float, y_original: float) -> tuple:
    """
    Return single iteration result of computation as tuple[x, y].

    You should invert y axis for correct results and picture

    :param x - mathematical x coordinate (transformed)
    :param y - mathematical y coordinate (transformed)
    :param x_original - mathematical x coordinate of pixel
    :param y_original - mathematical y coordinate of pixel

    :return tuple[x, y] after single iteration
    """
    pass


if __name__ == "__main__":
    mandelbrot = Fractal((1000, 1000), [(-2, -2), (2, 2)], mandelbrot_computation)
    mandelbrot.compute()
    mandelbrot.save_image("mandelbrot.png")
    mandelbrot2 = Fractal((1000, 1000), [(-0.74877, 0.065053), (-0.74872, 0.065103)], mandelbrot_computation)
    mandelbrot2.compute()
    mandelbrot2.save_image("mandelbrot2.png")
