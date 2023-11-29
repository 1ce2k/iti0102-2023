"""."""

from default_operator import DefaultOperator
from operators.operator import Operator
from tree_node import TreeNode


class Mul(Operator):
    """Custom operation."""

    def __init__(self, left: TreeNode, right: TreeNode):
        """Create default constructor."""
        super().__init__((left, right))

    @property
    def priority(self):
        """:priority of the operation."""
        return -1

    @property
    def default_operator(self):
        """Make use of the 'operator' library or use a lambda function."""
        return DefaultOperator(lambda x, y: x * y, "*")

    @property
    def actions(self):
        """:return a dictionary of custom operations. Make use of frozensets."""
        return {
            (set, set): lambda set1, set2: {frozenset((x, y)) for x in set1 for y in set2},  # cartesian product
            (set, int): lambda set1, integer: {frozenset((x, integer)) for x in set1},  # {1, 3} * 2 == {{1, 2}, {3, 2}}
            (int, set): lambda integer, set1: {frozenset((integer, x)) for x in set1}  # 2 * {1, 3} == {{2, 1}, {2, 3}}
        }
