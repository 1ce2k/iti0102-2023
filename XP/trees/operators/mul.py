"""."""

from default_operator import DefaultOperator
from operators.operator import Operator
from tree_node import TreeNode


class Mul(Operator):
    """Custom operation."""

    def __init__(self, left: TreeNode, right: TreeNode):
        """default constructor."""
        super().__init__((left, right))

    @property
    def priority(self):
        """priority of the operation."""
        return -1

    @property
    def default_operator(self):
        """Make use of the 'operator' library or use a lambda function."""
        return DefaultOperator(lambda x, y: x * y, "*")

    @property
    def actions(self):
        """:return a dictionary of custom operations. Make use of frozensets."""
        return {
            (set, set): {},  # cartesian product
            (set, int): {},  # {1, 3} * 2 == {{1, 2}, {3, 2}}
            (int, set): {}  # 2 * {1, 3} == {{2, 1}, {2, 3}}
        }
