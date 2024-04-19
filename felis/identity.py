from collections.abc import Callable

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


join = inject(identity)


bind = monad.bind(map)(join)


compose = monad.compose(bind)
