from collections.abc import Callable

__all__ = ["Equal"]


type Equal[T] = Callable[[T], Callable[[T], bool]]
