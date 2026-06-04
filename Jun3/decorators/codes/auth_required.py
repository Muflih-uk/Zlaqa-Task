import functools
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class User:
    name: str
    role: str


current_user: ContextVar[User | None] = ContextVar("current_user", default=None)


def auth_required(role: str = "admin"):
    """Decorator factory — guards a view/action behind a role check."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            user = current_user.get()
            if user is None:
                raise PermissionError("Not authenticated.")
            if user.role != role:
                raise PermissionError(
                    f"'{user.role}' cannot access '{func.__name__}' (needs '{role}')."
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator
