from collections.abc import Callable
from typing import TYPE_CHECKING

import felis.identity
from felis import applicative, lazy_t, monad
from felis.currying import curry, flip
from felis.lazy_t import Lazy

__all__ = [
    "Lazy",
    "apply",
    "bind",
    "bind_to",
    "compose",
    "discard_after",
    "discard_before",
    "join",
    "lift2",
    "map_by",
    "pure",
    "run",
    "take_after",
    "take_before",
    "to_add",
    "when",
]


def run[T](lazy_value: Lazy[T]) -> T:
    return lazy_value()


@curry
@curry
def to_add[M](first: Lazy[M], second: Lazy[M], m_add: Callable[[M], Callable[[M], M]]) -> Lazy[M]:
    return lambda: m_add(second())(first())


@curry
def map_by[From, To](lazy_value: Lazy[From], function: Callable[[From], To]) -> Lazy[To]:
    return lambda: function(lazy_value())


def pure[T](value: T) -> Lazy[T]:
    return lambda: value


if TYPE_CHECKING:

    @curry
    def apply[From, To](lazy_value: Lazy[From], lazy_function: Lazy[Callable[[From], To]]) -> Lazy[To]: ...

else:
    apply = lazy_t.apply(felis.identity.pure)(felis.identity.bind)


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[First, Second, Result](second: Lazy[Second], first: Lazy[First], function: Callable[[First], Callable[[Second], Result]]) -> Lazy[Result]: ...

else:
    lift2 = applicative.lift2(map_by)(apply)


if TYPE_CHECKING:

    @curry
    def take_after[First, Second](second: Lazy[Second], first: Lazy[First]) -> Lazy[Second]: ...

else:
    take_after = applicative.take_after(lift2)


if TYPE_CHECKING:

    @curry
    def discard_before[First, Second](first: Lazy[First], second: Lazy[Second]) -> Lazy[Second]: ...

else:
    discard_before = applicative.discard_before(lift2)


if TYPE_CHECKING:

    @curry
    def discard_after[First, Second](second: Lazy[Second], first: Lazy[First]) -> Lazy[First]: ...

else:
    discard_after = applicative.discard_after(lift2)


if TYPE_CHECKING:

    @curry
    def take_before[First, Second](first: Lazy[First], second: Lazy[Second]) -> Lazy[First]: ...

else:
    take_before = applicative.take_before(lift2)


if TYPE_CHECKING:

    @curry
    def when(lazy_none: Lazy[None], bool: bool) -> Lazy[None]: ...

else:
    when = applicative.when(pure)


if TYPE_CHECKING:

    def join[T](lazy_lazy_value: Lazy[Lazy[T]]) -> Lazy[T]: ...

else:
    join = lazy_t.join(felis.identity.pure)(felis.identity.bind)


if TYPE_CHECKING:

    @curry
    def bind_to[From, To](lazy_value: Lazy[From], function: Callable[[From], Lazy[To]]) -> Lazy[To]: ...

else:
    bind_to = monad.bind_to(map_by)(join)


bind = flip(bind_to)


if TYPE_CHECKING:

    @curry
    @curry
    def compose[From, Intermediate, To](value: From, first: Callable[[From], Lazy[Intermediate]], second: Callable[[Intermediate], Lazy[To]]) -> Lazy[To]: ...

else:
    compose = monad.compose(bind)
