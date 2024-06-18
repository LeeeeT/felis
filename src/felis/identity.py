from collections.abc import Callable

from felis import applicative, monad
from felis.currying import curry

__all__ = ["identity", "when", "map", "inject", "join", "bind", "compose", "then"]


def identity[T](value: T) -> T:
    return value


when = applicative.when(identity)


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
