"""Custom wrapper for function with a string representation."""


class DefaultOperator:
    """Default operator is a wrapper to a mathematical function with a string form."""

    def __init__(self, function_to_apply, string_repr_of_func):
        self.function = function_to_apply
        self.representation = string_repr_of_func

    def __call__(self, *args):
        return self.function(*args)

    def __repr__(self):
        return self.representation

if __name__ == '__main__':
    operator = DefaultOperator(lambda x, y: x + y, "+")
    assert operator.__call__(1, 2) == 3
    assert operator(1, 2) == 3
    assert operator.__str__() == "+"
    assert str(operator) == "+"
