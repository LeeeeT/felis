from typing import Any

from felis.currying import curry

__all__ = ["pure"]


@curry
def pure[T](_: Any, value: T) -> T:
    return value
