from collections.abc import Callable
from typing import Protocol

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


class Bind(Protocol):
    @staticmethod
    @curry
    def __call__[From, To](lazy_value: Lazy[From], function: Callable[[From], Lazy[To]], /) -> Lazy[To]: ...


bind: Bind = monad.bind(map)(join)


class Compose(Protocol):
    @staticmethod
    @curry
    @curry
    def __call__[From, Intermediate, To](
        value: From,
        first: Callable[[From], Lazy[Intermediate]],
        second: Callable[[Intermediate], Lazy[To]],
        /,
    ) -> Lazy[To]: ...


compose: Compose = monad.compose(bind)
