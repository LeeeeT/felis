from collections.abc import Callable
from typing import Final

from felis.currying import flip

__all__ = ["Semigroup", "add_to", "to_add"]


class Semigroup[S]:
    def __init__(self, to_add: Callable[[S], Callable[[S], S]]):
        self.to_add: Final = to_add


def to_add[S](instance: Semigroup[S]) -> Callable[[S], Callable[[S], S]]:
    return instance.to_add


def add_to[S](instance: Semigroup[S]) -> Callable[[S], Callable[[S], S]]:
    return flip(to_add(instance))
