from collections.abc import Callable
from typing import Final

import felis.semigroup
from felis.semigroup import Semigroup

__all__ = ["Monoid", "add_to", "neutral", "semigroup", "to_add"]


class Monoid[M]:
    def __init__(self, semigroup: Semigroup[M], neutral: M):
        self.semigroup: Final = semigroup
        self.neutral: Final = neutral


def semigroup[M](instance: Monoid[M]) -> Semigroup[M]:
    return instance.semigroup


def to_add[M](instance: Monoid[M]) -> Callable[[M], Callable[[M], M]]:
    return felis.semigroup.to_add(semigroup(instance))


def add_to[M](instance: Monoid[M]) -> Callable[[M], Callable[[M], M]]:
    return felis.semigroup.add_to(semigroup(instance))


def neutral[M](instance: Monoid[M]) -> M:
    return instance.neutral
