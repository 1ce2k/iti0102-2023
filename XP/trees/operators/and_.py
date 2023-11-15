"""."""

from XP.trees.default_operator import DefaultOperator
from operator import Operator
from XP.trees.tree_node import TreeNode


class And(Operator):
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
        return DefaultOperator(lambda x, y: -1, "?")

    @property
    def actions(self):
        """No additional actions needs to be defined here."""
        return {}
