from collections.abc import Callable

from felis import applicative, monad
from felis.currying import curry

__all__ = ["map", "identity", "when", "inject", "join", "bind", "compose", "then"]


@curry
def map[From, To](value: From, function: Callable[[From], To]) -> To:
    return function(value)


def identity[T](value: T) -> T:
    return value


when = applicative.when(identity)


@curry
def inject[T, MT](m_value: MT, m_identity: Callable[[T], MT]) -> MT:
    return m_value


join = inject(identity)


bind = monad.bind(map)(join)


compose = monad.compose(bind)


then = monad.then(bind)
