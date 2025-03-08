from typing import TypeVar, cast

T = TypeVar("T")


def _nn_(t: T | None) -> T:
    """Assert that a value is non-null."""
    if t is None:
        raise ValueError("t asserted as non-null")
    return cast(T, t)
