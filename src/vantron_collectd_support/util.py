from typing import TypeVar, cast

T = TypeVar("T")


def _nn_(t: T | None) -> T:
    if t is None:
        raise ValueError("t asserted as non-null")
    return cast(T, t)
