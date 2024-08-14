from collections.abc import Callable
from typing import TYPE_CHECKING

from felis import applicative, function, monad
from felis.currying import curry

__all__ = ["Lazy", "map", "identity", "apply", "lift2", "take_after", "discard_after", "take_before", "discard_before", "when", "join", "bind", "compose"]


type Lazy[T] = Callable[[], T]


@curry
def map[From, To](lazy_value: Lazy[From], function: Callable[[From], To]) -> Lazy[To]:
    return lambda: function(lazy_value())


def identity[T](value: T) -> Lazy[T]:
    return lambda: value


@curry
def apply[From, To](lazy_value: Lazy[From], lazy_function: Lazy[Callable[[From], To]]) -> Lazy[To]:
    return lambda: lazy_function()(lazy_value())


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[First, Second, Result](second: Lazy[Second], first: Lazy[First], function: Callable[[First], Callable[[Second], Result]]) -> Lazy[Result]: ...

else:
    lift2 = applicative.lift2(map)(apply)


take_after = lift2(function.flip(function.identity))


discard_after = lift2(function.identity)


take_before = function.flip(discard_after)


discard_before = function.flip(take_after)


if TYPE_CHECKING:

    @curry
    def when(bool: bool, lazy_none: Lazy[None]) -> Lazy[None]: ...

else:
    when = applicative.when(identity)


def join[T](lazy_lazy_value: Lazy[Lazy[T]]) -> Lazy[T]:
    return lambda: lazy_lazy_value()()


if TYPE_CHECKING:

    @curry
    def bind[From, To](lazy_value: Lazy[From], function: Callable[[From], Lazy[To]]) -> Lazy[To]: ...

else:
    bind = monad.bind(map)(join)


if TYPE_CHECKING:

    @curry
    @curry
    def compose[From, Intermediate, To](value: From, first: Callable[[From], Lazy[Intermediate]], second: Callable[[Intermediate], Lazy[To]]) -> Lazy[To]: ...

else:
    compose = monad.compose(bind)
