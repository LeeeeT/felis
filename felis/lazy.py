from collections.abc import Callable

from felis import monad
from felis.currying import curry

__all__ = ["Lazy", "identity", "map", "join", "bind", "compose"]


type Lazy[T] = Callable[[], T]


def identity[T](value: T) -> Lazy[T]:
    return lambda: value


@curry
def map[From, To](lazy_value: Lazy[From], function: Callable[[From], To]) -> Lazy[To]:
    return lambda: function(lazy_value())


def join[T](lazy_lazy_value: Lazy[Lazy[T]]) -> Lazy[T]:
    return lambda: lazy_lazy_value()()


bind = monad.bind(map)(join)


compose = monad.compose(bind)
