"""."""

from default_operator import DefaultOperator
from operators.operator import Operator
from tree_node import TreeNode


class Sub(Operator):
    """Custom operation."""

    def __init__(self, left: TreeNode, right: TreeNode):
        """default constructor."""
        super().__init__((left, right))
        self.left = left
        self.right = right

    @property
    def priority(self):
        """priority of the operation."""
        return -1

    @property
    def default_operator(self):
        """Make use of the 'operator' library or use a lambda function."""
        return DefaultOperator(lambda x, y: x - y, "-")

    def remove(self, set_a, int_a):
        """Remove int from set."""
        if int_a in set_a:
            set_a.remove(int_a)
        return set_a

    @property
    def actions(self):
        """:return a dictionary of custom operations."""
        return {
            (set, int): self.remove  # set without the element
        }
