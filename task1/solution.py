import inspect
from functools import wraps
from typing import Callable


def strict(func) -> Callable:
    sig = inspect.signature(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound_args = sig.bind(*args, **kwargs)
        parameters = sig.parameters

        for name, value in bound_args.arguments.items():
            expected_type = parameters[name].annotation

            if expected_type is not inspect.Parameter.empty and not isinstance(value, expected_type):
                raise TypeError(f"Argument '{name}' = {value!r} is not of type {expected_type.__name__}")

        result = func(*args, **kwargs)

        return_type = sig.return_annotation
        if return_type is not inspect.Signature.empty and not isinstance(result, return_type):
            raise TypeError(f"Return value {result} is not of type {return_type.__name__}")

        return result

    return wrapper


if __name__ == '__main__':

    @strict
    def sum_two(a: int, b: int) -> int:
        return a + b


    print(sum_two(1, b=2))  # >>> 3
    print(sum_two(1, 2.4))  # >>> TypeError
