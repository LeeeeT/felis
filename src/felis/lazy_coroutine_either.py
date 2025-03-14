from collections.abc import Callable
from typing import TYPE_CHECKING

import felis.identity
from felis import applicative, either, either_t, function, lazy_coroutine, monad
from felis.currying import curry
from felis.either import Either
from felis.lazy_coroutine import LazyCoroutine

__all__ = [
    "LazyCoroutineEither",
    "add",
    "apply",
    "bind",
    "bound",
    "compose",
    "default",
    "discard_after",
    "discard_before",
    "identity",
    "join",
    "lift2",
    "map",
    "take_after",
    "take_before",
    "when",
]


type LazyCoroutineEither[L, R] = LazyCoroutine[Either[L, R]]


if TYPE_CHECKING:

    @curry
    def add[L, R](
        lazy_coroutine_either_augend: LazyCoroutineEither[L, R],
        lazy_coroutine_either_addend: LazyCoroutineEither[L, R],
    ) -> LazyCoroutineEither[L, R]: ...

else:
    add = either_t.add(lazy_coroutine.identity)(lazy_coroutine.bind)


if TYPE_CHECKING:

    @curry
    def map[L, From, To](lazy_coroutine_either_value: LazyCoroutineEither[L, From], function: Callable[[From], To]) -> LazyCoroutineEither[L, To]: ...

else:
    map = felis.identity.compose(lazy_coroutine.map)(either.map)


identity = felis.identity.compose(lazy_coroutine.identity)(either.identity)


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
    lift2 = applicative.lift2(map)(apply)


take_after = lift2(function.flip(function.identity))


discard_after = lift2(function.identity)


take_before = function.flip(discard_after)


discard_before = function.flip(take_after)


if TYPE_CHECKING:

    @curry
    def when[L](bool: bool, lazy_coroutine_either_none: LazyCoroutineEither[L, None]) -> LazyCoroutineEither[L, None]: ...

else:
    when = applicative.when(identity)


if TYPE_CHECKING:

    def join[L, R](lazy_coroutine_either_lazy_coroutine_either_value: LazyCoroutineEither[L, LazyCoroutineEither[L, R]]) -> LazyCoroutineEither[L, R]: ...

else:
    join = either_t.join(lazy_coroutine.identity)(lazy_coroutine.bind)


if TYPE_CHECKING:

    @curry
    def bound[L, From, To](
        lazy_coroutine_either_value: LazyCoroutineEither[L, From],
        function: Callable[[From], LazyCoroutineEither[L, To]],
    ) -> LazyCoroutineEither[L, To]: ...

else:
    bound = monad.bound(map)(join)


bind = function.flip(bound)


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
    def default[L, R](lazy_coroutine_either_value: LazyCoroutineEither[L, R], default_value: LazyCoroutine[R]) -> LazyCoroutine[R]: ...

else:
    default = either_t.default(lazy_coroutine.identity)(lazy_coroutine.bind)
