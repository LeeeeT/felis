from collections.abc import Callable
from typing import TYPE_CHECKING

import felis.identity
from felis import applicative, coroutine, function, lazy, lazy_t, monad
from felis.coroutine import Coroutine
from felis.currying import curry
from felis.lazy import Lazy

__all__ = [
    "LazyCoroutine",
    "apply",
    "bind",
    "bind_to",
    "compose",
    "discard_after",
    "discard_before",
    "join",
    "lift",
    "lift2",
    "map_by",
    "pure",
    "take_after",
    "take_before",
    "when",
]


type LazyCoroutine[T] = Lazy[Coroutine[T]]


if TYPE_CHECKING:

    @curry
    def map_by[From, To](lazy_coroutine_value: LazyCoroutine[From], function: Callable[[From], To]) -> LazyCoroutine[To]: ...

else:
    map_by = felis.identity.compose(lazy.map_by)(coroutine.map_by)


pure = felis.identity.compose(lazy.pure)(coroutine.pure)


lift = lazy.map_by(coroutine.pure)  # TODO


if TYPE_CHECKING:

    @curry
    @curry
    def apply[From, To](lazy_coroutine_value: LazyCoroutine[From], lazy_coroutine_function: LazyCoroutine[Callable[[From], To]]) -> LazyCoroutine[To]: ...

else:
    apply = lazy_t.apply(coroutine.pure)(coroutine.bind)


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[First, Second, Result](
        second: LazyCoroutine[Second],
        first: LazyCoroutine[First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> LazyCoroutine[Result]: ...

else:
    lift2 = applicative.lift2(map_by)(apply)


take_after = lift2(function.flip(function.pure))


discard_after = lift2(function.pure)


take_before = function.flip(discard_after)


discard_before = function.flip(take_after)


if TYPE_CHECKING:

    @curry
    def when(lazy_coroutine_none: LazyCoroutine[None], bool: bool) -> LazyCoroutine[None]: ...

else:
    when = applicative.when(pure)


if TYPE_CHECKING:

    def join[T](lazy_coroutine_lazy_coroutine_value: LazyCoroutine[LazyCoroutine[T]]) -> LazyCoroutine[T]: ...

else:
    join = lazy_t.join(coroutine.pure)(coroutine.bind)


if TYPE_CHECKING:

    @curry
    def bind_to[From, To](lazy_coroutine_value: LazyCoroutine[From], function: Callable[[From], LazyCoroutine[To]]) -> LazyCoroutine[To]: ...

else:
    bind_to = monad.bind_to(map_by)(join)


bind = function.flip(bind_to)


if TYPE_CHECKING:

    @curry
    @curry
    def compose[From, Intermediate, To](
        value: From,
        first: Callable[[From], LazyCoroutine[Intermediate]],
        second: Callable[[Intermediate], LazyCoroutine[To]],
    ) -> LazyCoroutine[To]: ...

else:
    compose = monad.compose(bind)
