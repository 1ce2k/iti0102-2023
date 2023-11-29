"""."""

from default_operator import DefaultOperator
from operators.operator import Operator
from tree_node import TreeNode


class Div(Operator):
    """Custom operation."""

    def __init__(self, left: TreeNode, right: TreeNode):
        """Create default constructor."""
        super().__init__((left, right))

    @property
    def priority(self):
        """:priority of the operation."""
        return -2

    @property
    def default_operator(self):
        """Make use of the 'operator' library or use a lambda function."""
        return DefaultOperator(lambda x, y: x / y, "/")

    @property
    def actions(self):
        """:return a dictionary of custom operations."""
        return {
            (set, set): lambda x, y: x - y,  # set exclusion
            (set, int): lambda x, y: x - {y},  # remove from set
            (set, float): lambda x, y: x,
            (int, int): lambda x, y: x // y  # integer division
        }

    @property
    def associativity(self):
        """Return if operator is associative or not."""
        return False
