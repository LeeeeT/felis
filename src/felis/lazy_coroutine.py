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
    "bound",
    "compose",
    "discard_after",
    "discard_before",
    "identity",
    "join",
    "lift",
    "lift2",
    "map",
    "take_after",
    "take_before",
    "when",
]


type LazyCoroutine[T] = Lazy[Coroutine[T]]


if TYPE_CHECKING:

    @curry
    def map[From, To](lazy_coroutine_value: LazyCoroutine[From], function: Callable[[From], To]) -> LazyCoroutine[To]: ...

else:
    map = felis.identity.compose(lazy.map)(coroutine.map)


identity = felis.identity.compose(lazy.identity)(coroutine.identity)


lift = lazy.map(coroutine.identity)


if TYPE_CHECKING:

    @curry
    @curry
    def apply[From, To](lazy_coroutine_value: LazyCoroutine[From], lazy_coroutine_function: LazyCoroutine[Callable[[From], To]]) -> LazyCoroutine[To]: ...

else:
    apply = lazy_t.apply(coroutine.identity)(coroutine.bind)


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[First, Second, Result](
        second: LazyCoroutine[Second],
        first: LazyCoroutine[First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> LazyCoroutine[Result]: ...

else:
    lift2 = applicative.lift2(map)(apply)


take_after = lift2(function.flip(function.identity))


discard_after = lift2(function.identity)


take_before = function.flip(discard_after)


discard_before = function.flip(take_after)


if TYPE_CHECKING:

    @curry
    def when(bool: bool, lazy_coroutine_none: LazyCoroutine[None]) -> LazyCoroutine[None]: ...

else:
    when = applicative.when(identity)


if TYPE_CHECKING:

    def join[T](lazy_coroutine_lazy_coroutine_value: LazyCoroutine[LazyCoroutine[T]]) -> LazyCoroutine[T]: ...

else:
    join = lazy_t.join(coroutine.identity)(coroutine.bind)


if TYPE_CHECKING:

    @curry
    def bound[From, To](lazy_coroutine_value: LazyCoroutine[From], function: Callable[[From], LazyCoroutine[To]]) -> LazyCoroutine[To]: ...

else:
    bound = monad.bound(map)(join)


bind = function.flip(bound)


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
