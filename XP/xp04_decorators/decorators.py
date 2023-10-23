"""XP - decorators."""

import time
import inspect
import types


def double(func):
    """
    Double the return value of a function.

    :param func: The decorated function.
    :return: Inner function.
    """

    def wrapper(*args, **kwargs):
        # return value from func()
        result = func(*args, **kwargs)
        # return value * 2
        return result * 2

    return wrapper


def stopwatch(func):
    """
    Print the runtime of a function.

    It should be printed out like: "It took [time] seconds for [function_name] to run",
    where [time] is the number of seconds (with the precision of at least 5 decimal places)
    it took for the function to run and [function_name] is the name of the function.
    The function's return value should not be affected.
    :param func: The decorated function.
    :return: Inner function.
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        function_name = func.__name__
        print(f"It took {elapsed_time} seconds for {function_name} to run")
        return result

    return wrapper


def memoize(func):
    """
    Cache the return value of a function.

    Memoization is an optimisation technique used primarily to speed up computer programs
    by storing the results of expensive function calls and returning the cached result
    when the same inputs occur again.
    For efficiency purposes, you can assume, that the function only takes one argument,
    and that the argument is an integer.
    :param func: The decorated function.
    :return: Inner function.
    """
    cache = {}

    def inner(arg):
        if arg not in cache:
            result = func(arg)
            cache[arg] = result
            return result
        else:
            return cache[arg]

    return inner


def read_data(func):
    """
    Read the data from the file "data.txt" and pass it to the function.

    The data must be passed as a list of strings, where each string is a line from the file.
    It also must be passed as the first argument to the function, followed by any other given arguments.
    :param func: The decorated function.
    :return: Inner function.
    """

    def inner(*args, **kwargs):
        with open('data.txt', 'r') as file:
            data = [line.strip() for line in file.readlines()]
        return func(data, *args, **kwargs)

    return inner


def catch(*error_classes):
    """
    Catch the specified exceptions.

    If the function raises one of the specified exceptions, return a tuple of (1, exception_class),
    where exception_class is the type of the exception that was raised. Otherwise, return a tuple of (0, result),
    where result is the result of the function.

    This decorator must be able to handle the following cases:
    1. The decorator is used with no arguments, e.g. @catch. Such usage should catch all exceptions.
    2. The decorator is used with one argument, e.g. @catch(ValueError).
    3. The decorator is used with multiple arguments, e.g. @catch(KeyError, TypeError).
    :param error_classes: The exceptions to catch.
    :return: Inner function.
    """

    def inner(*args, **kwargs):
        possible_func = args[0]
        is_func_callable = callable(possible_func)

        def wrapper(*iargs, **ikwargs):
            error_length = 0 if not (error_classes and is_func_callable) else len(error_classes)
            if error_length > 0:
                errors = error_classes
            else:
                errors = Exception
            func_used = possible_func if is_func_callable else error_classes[0]
            try:
                res = func_used(*iargs, **ikwargs)
                return 0, res
            except errors as e:
                return 1, type(e)

        if is_func_callable:
            return wrapper
        return wrapper(*args, **kwargs)

    return inner


def enforce_types(func):
    """
    Enforce the types of the function's parameters and return value.

    If the function is called with an argument of the wrong type, raise a TypeError with the message:
    "Argument '[argument_name]' must be of type [expected_type], but was [value] of type [actual_type]".
    If the function returns a value of the wrong type, raise a TypeError with the message:
    "Returned value must be of type [expected_type], but was [value] of type [actual_type]".

    If an argument or the return value can be of multiple types, then the [expected_type]
    in the error message should be "[type_1], [type_2], ..., [type_(n-1)] or [type_n]".
    For example if the type annotation for an argument is int | float | str | bool, then the error message should be
    "Argument '[argument_name]' must be of type int, float, str or bool, but was [value] of type [actual_type]".

    If there's no type annotation for a parameter or the return value, then it can be of any type.

    Using the inspect module to get the function's signature and annotations is recommended.

    Exceptions, that happen during the execution of the function, should still occur normally,
    if the argument types are correct.
    :param func: The decorated function.
    :return: Inner function.
    """
    sig = inspect.signature(func)
    parameters = sig.parameters
    return_annotation = sig.return_annotation

    def is_instance_of_union(value, union_type):
        for t in union_type.__args__:
            if isinstance(value, t):
                return True
        return False

    def inner(*args, **kwargs):
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        for name, value in bound_args.arguments.items():
            if name in parameters:
                expected_type = parameters[name].annotation

                if expected_type is not inspect.Parameter.empty:
                    if isinstance(expected_type, types.UnionType):
                        if not is_instance_of_union(value, expected_type):
                            actual_type = type(value).__name__
                            expected = ', '.join(t.__name__ for t in expected_type.__args__[:-1]) + ' or ' + \
                                       expected_type.__args__[-1].__name__
                            raise TypeError(
                                f"Argument '{name}' must be of type {expected}, but was {value} of type {actual_type}")
                    elif not isinstance(expected_type, types.UnionType) and (
                            value is not None or expected_type is not None):
                        actual_type = type(value)
                        if type(value) is not expected_type:
                            raise TypeError(
                                f"Argument '{name}' must be of type {expected_type.__name__}, but was '{value}' of type {actual_type.__name__}")
        result = func(*args, **kwargs)
        if return_annotation is not inspect.Signature.empty:
            expected_type = return_annotation
            check_result(result, expected_type)
        return result

    def check_result(result, expected_type):
        if isinstance(expected_type, types.UnionType) and not is_instance_of_union(result, expected_type):
            actual_type = type(result).__name__
            expected_types = ', '.join(t.__name__ for t in expected_type.__args__[:-1]) + ' or ' + expected_type.__args__[-1].__name__
            raise TypeError(f"Returned value must be of type {expected_types}, but was {result} of type {actual_type}")
        else:
            actual_type = type(result).__name__
            if actual_type != expected_type.__name__:
                raise TypeError(f"Returned value must be of type {expected_type.__name__}, but was {result} of type {actual_type}")

    return inner


#  Everything below is just for testing purposes, tester does not care what you do with them.
#    |           |           |           |           |           |           |           |
#    V           V           V           V           V           V           V           V


@double
def double_me(element):
    """Test function for @double."""
    return element


@stopwatch
def measure_me():
    """Test function for @stopwatch."""
    time.sleep(0.21)
    return 5


@memoize
def fibonacci(n: int):
    """Test function for @memoize."""
    if n in (0, 1):
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)


@catch
def error_func(iterable):
    """Test function for @catch."""
    return iterable[2]


@read_data
def process_file_contents(data: list, prefix: str = ""):
    """Test function for @read_data."""
    return [prefix + line for line in data]


@enforce_types
def no_more_duck_typing(a, b) -> int:
    """Test function for @enforce_types."""
    return 1 + 2


print(no_more_duck_typing(1, 2))
