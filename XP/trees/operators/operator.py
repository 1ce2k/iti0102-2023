"""."""

from abc import abstractmethod
from tree_node import TreeNode


class Operator(TreeNode):
    """Custom operation wrapper."""

    def __init__(self, *args):
        """Store the given arguments somehow."""
        super().__init__(*args[0])
        self.__value = args[0]

    def apply(self):
        """Make use of the *args to compute the value of the given subtree. Recursion is your friend."""
        params = [x.apply() for x in self.__value]
        types = tuple(type(x) for x in params)
        if self.actions.get(types):
            return self.actions[types](*params)
        else:
            return self.default_operator(*params)

    def class_str(self):
        """:return class string representation of the object."""
        return f"{self.__class__.__name__}({', '.join([x.class_str() for x in self.__value])})"

    def __str__(self):
        """:return the mathematical string representation of the tree with least amount of parenthesis."""
        return f" {self.default_operator} ".join([self.__encase(x) for x in self.__value])

    def __encase(self, node):
        """Help func."""
        if type(node).__name__ == "Leaf":
            return f"{node}"
        elif type(self).__name__ != "Leaf" and type(self) is type(node) and node.associativity:
            return f"{node.__str__()}"
        elif type(self).__name__ != "Leaf" and type(self) is type(node) and not node.associativity:
            return f"({node.__str__()})"
        elif type(self).__name__ != "Leaf" and self.priority >= node.priority:
            return f"{node.__str__()}"
        return str(f"({node.__str__()})")

    @property
    @abstractmethod
    def default_operator(self):
        """:abstract method which should be overridden to return the default_operator object."""
        return self.default_operator
