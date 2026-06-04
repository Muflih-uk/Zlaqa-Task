import functools
from typing import Any, Callable


def logger(func: Callable) -> Callable:
    """Log call signature and return value."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        arg_repr = ", ".join(
            [repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()]
        )

        print(f"[logger] CALL  {func.__name__}({arg_repr})")
        result = func(*args, **kwargs)
        print(f"[logger] RETURN {func.__name__} → {result!r}")
        return result

    return wrapper
