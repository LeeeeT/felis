from collections.abc import Callable

from felis import monad
from felis.currying import curry

__all__ = ["neutral", "add", "identity", "map", "inject", "join", "bind", "compose", "then"]


@curry
def neutral[M](value: object, m_neutral: M) -> M:
    return m_neutral


def add[M, T](value: T, first: Callable[[T], M], second: Callable[[T], M], m_add: Callable[[M], Callable[[M], M]]) -> M:
    return m_add(second(value))(first(value))


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


then = monad.then(bind)
