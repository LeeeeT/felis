from collections.abc import Callable
from typing import TYPE_CHECKING

import felis.identity
from felis import applicative, function, lazy_coroutine_either, list, list_t, monad
from felis.currying import curry
from felis.lazy_coroutine_either import LazyCoroutineEither
from felis.list import List

__all__ = [
    "LazyCoroutineEitherList",
    "apply",
    "bind",
    "bound",
    "compose",
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


type LazyCoroutineEitherList[L, R] = LazyCoroutineEither[L, List[R]]


if TYPE_CHECKING:

    @curry
    def map[L, From, To](
        lazy_coroutine_either_list_value: LazyCoroutineEitherList[L, From], function: Callable[[From], To],
    ) -> LazyCoroutineEitherList[L, To]: ...

else:
    map = felis.identity.compose(lazy_coroutine_either.map)(list.map)


identity = felis.identity.compose(lazy_coroutine_either.identity)(list.identity)


apply = lazy_coroutine_either.lift2(list.apply)


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[L, First, Second, Result](
        second: LazyCoroutineEitherList[L, Second],
        first: LazyCoroutineEitherList[L, First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> LazyCoroutineEitherList[L, Result]: ...

else:
    lift2 = applicative.lift2(map)(apply)


take_after = lift2(function.flip(function.identity))


discard_after = lift2(function.identity)


take_before = function.flip(discard_after)


discard_before = function.flip(take_after)


if TYPE_CHECKING:

    @curry
    def when[L](bool: bool, lazy_coroutine_either_list_none: LazyCoroutineEitherList[L, None]) -> LazyCoroutineEitherList[L, None]: ...

else:
    when = applicative.when(identity)


if TYPE_CHECKING:

    def join[L, R](
        lazy_coroutine_either_list_lazy_coroutine_either_list_value: LazyCoroutineEitherList[L, LazyCoroutineEitherList[L, R]],
    ) -> LazyCoroutineEitherList[L, R]: ...

else:
    join = list_t.join(lazy_coroutine_either.identity)(lazy_coroutine_either.bind)


if TYPE_CHECKING:

    @curry
    def bound[L, From, To](
        lazy_coroutine_either_list_value: LazyCoroutineEitherList[L, From],
        function: Callable[[From], LazyCoroutineEitherList[L, To]],
    ) -> LazyCoroutineEitherList[L, To]: ...

else:
    bound = monad.bound(map)(join)


bind = function.flip(bound)


if TYPE_CHECKING:

    @curry
    @curry
    def compose[L, From, Intermediate, To](
        value: From,
        first: Callable[[From], LazyCoroutineEitherList[L, Intermediate]],
        second: Callable[[Intermediate], LazyCoroutineEitherList[L, To]],
    ) -> LazyCoroutineEitherList[L, To]: ...

else:
    compose = monad.compose(bind)
