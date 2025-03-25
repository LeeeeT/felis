from collections.abc import Callable
from typing import TYPE_CHECKING

import felis.identity
from felis import applicative, coroutine, lazy, lazy_t, monad
from felis.coroutine import Coroutine
from felis.currying import curry, flip
from felis.lazy import Lazy

__all__ = [
    "LazyCoroutine",
    "apply",
    "bind",
    "bind_to",
    "compose_after",
    "compose_before",
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
    map_by = felis.identity.compose_before(lazy.map_by)(coroutine.map_by)


pure = felis.identity.compose_before(lazy.pure)(coroutine.pure)


lift = lazy.map_by(coroutine.pure)


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


if TYPE_CHECKING:

    @curry
    def take_after[First, Second](second: LazyCoroutine[Second], first: LazyCoroutine[First]) -> LazyCoroutine[Second]: ...

else:
    take_after = applicative.take_after(lift2)


if TYPE_CHECKING:

    @curry
    def discard_before[First, Second](first: LazyCoroutine[First], second: LazyCoroutine[Second]) -> LazyCoroutine[Second]: ...

else:
    discard_before = applicative.discard_before(lift2)


if TYPE_CHECKING:

    @curry
    def discard_after[First, Second](second: LazyCoroutine[Second], first: LazyCoroutine[First]) -> LazyCoroutine[First]: ...

else:
    discard_after = applicative.discard_after(lift2)


if TYPE_CHECKING:

    @curry
    def take_before[First, Second](first: LazyCoroutine[First], second: LazyCoroutine[Second]) -> LazyCoroutine[First]: ...

else:
    take_before = applicative.take_before(lift2)


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


bind = flip(bind_to)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_after[From, Intermediate, To](
        value: From,
        second: Callable[[Intermediate], LazyCoroutine[To]],
        first: Callable[[From], LazyCoroutine[Intermediate]],
    ) -> LazyCoroutine[To]: ...

else:
    compose_after = monad.compose_after(bind)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_before[From, Intermediate, To](
        value: From,
        first: Callable[[From], LazyCoroutine[Intermediate]],
        second: Callable[[Intermediate], LazyCoroutine[To]],
    ) -> LazyCoroutine[To]: ...

else:
    compose_before = monad.compose_before(bind)
