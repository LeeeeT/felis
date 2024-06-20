from collections.abc import Callable

from felis import applicative, monad
from felis.currying import curry

__all__ = ["Identity", "map", "identity", "apply", "lift2", "when", "inject", "join", "bind", "compose", "then"]


type Identity[T] = T


@curry
def map[From, To](identity_value: Identity[From], function: Callable[[From], To]) -> Identity[To]:
    return function(identity_value)


def identity[T](value: T) -> Identity[T]:
    return value


@curry
def apply[From, To](identity_value: Identity[From], identity_function: Identity[Callable[[From], To]]) -> Identity[To]:
    return identity_function(identity_value)


lift2 = applicative.lift2(map)(apply)


when = applicative.when(identity)


def inject[MT](m_value: MT) -> MT:
    return m_value


join = inject


bind = monad.bind(map)(join)


compose = monad.compose(bind)


then = monad.then(bind)
