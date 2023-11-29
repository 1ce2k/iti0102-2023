"""."""

from default_operator import DefaultOperator
from operators.operator import Operator
from tree_node import TreeNode


class Add(Operator):
    """Custom operation."""

    def __init__(self, left: TreeNode, right: TreeNode):
        """Create default constructor."""
        super().__init__((left, right))
        self.left = left
        self.right = right

    @property
    def priority(self):
        """Return the value of the operation."""
        return 11

    @property
    def default_operator(self):
        """Return the default operator of the operation."""
        return DefaultOperator(lambda x, y: x + y, "+")

    @property
    def associativity(self):
        """Return if operator is associative or not."""
        return True

    @property
    def actions(self):
        """Return a dictionary of custom operations."""
        return {
            (set, set): lambda x, y: x | y,  # set union
            (set, int): lambda x, y: {*x, y},  # add to set
        }
