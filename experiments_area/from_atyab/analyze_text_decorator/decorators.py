"""Reusable decorators for text-producing functions."""

from collections.abc import Callable
from functools import wraps
from typing import ParamSpec

P = ParamSpec("P")

VOWELS = frozenset("aeiouAEIOU")


def analyze_text(
    *,
    words: bool = False,
    vowels: bool = False,
    spaces: bool = False,
) -> Callable[[Callable[P, str]], Callable[P, str]]:
    """Print requested text statistics without changing the function's result."""

    def decorator(func: Callable[P, str]) -> Callable[P, str]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> str:
            result = func(*args, **kwargs)

            if not any((words, vowels, spaces)):
                return result

            if words:
                print(f"Words: {len(result.split())}")

            if vowels:
                print(f"Vowels: {sum(char in VOWELS for char in result)}")

            if spaces:
                print(f"Spaces: {result.count(' ')}")

            return result

        return wrapper

    return decorator
