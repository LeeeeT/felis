from typing import Any

from felis.currying import curry

__all__ = ["identity"]


@curry
def identity[T](_: Any, value: T) -> T:
    return value
