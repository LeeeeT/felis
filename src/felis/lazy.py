from collections.abc import Callable

from felis import applicative, monad
from felis.currying import curry

__all__ = ["Lazy", "map", "identity", "when", "join", "bind", "compose", "then"]


type Lazy[T] = Callable[[], T]


@curry
def map[From, To](lazy_value: Lazy[From], function: Callable[[From], To]) -> Lazy[To]:
    return lambda: function(lazy_value())


def identity[T](value: T) -> Lazy[T]:
    return lambda: value


when = applicative.when(identity)


def join[T](lazy_lazy_value: Lazy[Lazy[T]]) -> Lazy[T]:
    return lambda: lazy_lazy_value()()


bind = monad.bind(map)(join)


compose = monad.compose(bind)


then = monad.then(bind)
