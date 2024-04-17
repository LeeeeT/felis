from collections.abc import Callable
from typing import Protocol

from felis import monad
from felis.currying import curry

__all__ = ["identity", "map", "inject", "join", "bind", "compose"]


def identity[T](value: T) -> T:
    return value


@curry
def map[From, To](value: From, function: Callable[[From], To]) -> To:
    return function(value)


@curry
def inject[T, MT](m_value: MT, m_identity: Callable[[T], MT]) -> MT:
    return m_value


class Join(Protocol):
    @staticmethod
    def __call__[T](value: T, /) -> T: ...


join: Join = inject(identity)


class Bind(Protocol):
    @staticmethod
    @curry
    def __call__[From, To](value: From, function: Callable[[From], To], /) -> To: ...


bind = monad.bind(map)(join)


class Compose(Protocol):
    @staticmethod
    @curry
    @curry
    def __call__[From, Intermediate, To](value: From, first: Callable[[From], Intermediate], second: Callable[[Intermediate], To], /) -> To: ...


compose: Compose = monad.compose(bind)
