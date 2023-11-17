"""."""

from abc import ABCMeta, abstractmethod


class TreeNode(metaclass=ABCMeta):
    """The main node class."""

    def __init__(self, *args):
        """:param make use of *args and store them in a way that it is easy to use them."""
        self.__value = args

    @abstractmethod
    def apply(self):
        """abstract method which should be overridden to compute the value of the given abstract tree."""
        print(self.__value)

    @abstractmethod
    def class_str(self):
        """:return class string representation of the object."""
        return f"{self.__class__.__name__}({', '.join([x.class_str() for x in self.__value])})"

    @abstractmethod
    def __str__(self):
        """:return string representation of the object."""
        return f" {self.default_operator} ".join([self.__encase(x, i == 0) for i, x in enumerate(self.__value)])

    def __eq__(self, other):
        """:return True when 2 object trees have the same shape and values."""
        if type(other) is str:
            return self.__str__() == other
        return self.__str__() == other.__str__()

    def __ne__(self, other):
        """:return True when 2 object trees have a different shape and/or values."""
        for item in self.__value:
            if type(item) is type(other):
                return False
            else:
                return True
