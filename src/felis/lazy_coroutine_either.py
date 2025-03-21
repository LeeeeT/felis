from collections.abc import Callable
from typing import TYPE_CHECKING

import felis.identity
from felis import applicative, either, either_t, function, lazy_coroutine, monad
from felis.currying import curry
from felis.either import Either
from felis.lazy_coroutine import LazyCoroutine

__all__ = [
    "LazyCoroutineEither",
    "apply",
    "bind",
    "bind_to",
    "compose",
    "default_to",
    "discard_after",
    "discard_before",
    "join",
    "lift2",
    "map_by",
    "pure",
    "take_after",
    "take_before",
    "to_add",
    "when",
]


type LazyCoroutineEither[L, R] = LazyCoroutine[Either[L, R]]


if TYPE_CHECKING:

    @curry
    def to_add[L, R](
        lazy_coroutine_either_augend: LazyCoroutineEither[L, R],
        lazy_coroutine_either_addend: LazyCoroutineEither[L, R],
    ) -> LazyCoroutineEither[L, R]: ...

else:
    to_add = either_t.to_add(lazy_coroutine.pure)(lazy_coroutine.bind)


if TYPE_CHECKING:

    @curry
    def map_by[L, From, To](lazy_coroutine_either_value: LazyCoroutineEither[L, From], function: Callable[[From], To]) -> LazyCoroutineEither[L, To]: ...

else:
    map_by = felis.identity.compose(lazy_coroutine.map_by)(either.map_by)


pure = felis.identity.compose(lazy_coroutine.pure)(either.pure)


apply = lazy_coroutine.lift2(either.apply)


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[L, First, Second, Result](
        second: LazyCoroutineEither[L, Second],
        first: LazyCoroutineEither[L, First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> LazyCoroutineEither[L, Result]: ...

else:
    lift2 = applicative.lift2(map_by)(apply)


take_after = lift2(function.flip(function.pure))


discard_after = lift2(function.pure)


take_before = function.flip(discard_after)


discard_before = function.flip(take_after)


if TYPE_CHECKING:

    @curry
    def when[L](lazy_coroutine_either_none: LazyCoroutineEither[L, None], bool: bool) -> LazyCoroutineEither[L, None]: ...

else:
    when = applicative.when(pure)


if TYPE_CHECKING:

    def join[L, R](lazy_coroutine_either_lazy_coroutine_either_value: LazyCoroutineEither[L, LazyCoroutineEither[L, R]]) -> LazyCoroutineEither[L, R]: ...

else:
    join = either_t.join(lazy_coroutine.pure)(lazy_coroutine.bind)


if TYPE_CHECKING:

    @curry
    def bind_to[L, From, To](
        lazy_coroutine_either_value: LazyCoroutineEither[L, From],
        function: Callable[[From], LazyCoroutineEither[L, To]],
    ) -> LazyCoroutineEither[L, To]: ...

else:
    bind_to = monad.bind_to(map_by)(join)


bind = function.flip(bind_to)


if TYPE_CHECKING:

    @curry
    @curry
    def compose[L, From, Intermediate, To](
        value: From,
        first: Callable[[From], LazyCoroutineEither[L, Intermediate]],
        second: Callable[[Intermediate], LazyCoroutineEither[L, To]],
    ) -> LazyCoroutineEither[L, To]: ...

else:
    compose = monad.compose(bind)


if TYPE_CHECKING:

    @curry
    def default_to[L, R](lazy_coroutine_either_value: LazyCoroutineEither[L, R], default_value: LazyCoroutine[R]) -> LazyCoroutine[R]: ...

else:
    default_to = either_t.default_to(lazy_coroutine.pure)(lazy_coroutine.bind)
