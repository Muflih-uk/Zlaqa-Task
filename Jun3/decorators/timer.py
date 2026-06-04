import asyncio
import functools
import time
from typing import Any, Callable


def timer(func: Callable) -> Callable:
    """Log execution time for sync and async callables."""

    "Sync function wrapper"

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[timer] {func.__name__} -> {elapsed:.4f}s")
        return result

    "Async function wrapper"

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs) -> Any:
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[timer] {func.__name__} (async) → {elapsed:.4f}s")
        return result

    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
