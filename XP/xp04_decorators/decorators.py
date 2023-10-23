"""XP - decorators."""

import time
import inspect


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
    param_annotations = inspect.signature(func).parameters

    def wrapper(*args, **kwargs):
        # Check parameter types
        for arg_name, expected_type in param_annotations.items():
            if expected_type.annotation != inspect.Parameter.empty:
                if arg_name in kwargs:
                    actual_value = kwargs[arg_name]
                else:
                    arg_index = list(param_annotations).index(arg_name)
                    if arg_index < len(args):
                        actual_value = args[arg_index]
                    else:
                        # Argument not provided; skip type checking
                        continue
                if not isinstance(actual_value, expected_type.annotation) and expected_type is not inspect.Parameter.empty:
                    types = str(expected_type.annotation).split(' | ')
                    if len(types) == 1:
                        types_str = expected_type.annotation.__name__
                    elif len(types) > 1:
                        types_str = ', '.join(types[:-1]) + ' or ' + types[-1]
                    if len(types) > 0:
                        raise TypeError(
                            f"Argument '{arg_name}' must be of type {types_str}, but was {repr(actual_value)} of type {type(actual_value).__name__}"
                        )
        # Call the original function
        result = func(*args, **kwargs)
        # Check the return type
        return_annotation = inspect.signature(func).return_annotation
        if return_annotation != inspect.Parameter.empty:
            check_result(result, return_annotation)
        return result
    return wrapper


def check_result(result, return_annotation):
    if not isinstance(result, return_annotation):
        types = str(return_annotation).split(' | ')
        types_str = ', '.join(types[:-1]) + ' or ' + types[-1]
        raise TypeError(
            f"Returned value must be of type {types_str}, but was {repr(result)} of type {type(result).__name__}"
        )

@enforce_types
def foo(a: int, b: float | int) -> str | int:
    """Test for enforce_type."""
    if b:
        return str(a)
    return a
