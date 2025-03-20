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
    "bind_to",
    "compose",
    "discard_after",
    "discard_before",
    "join",
    "lift2",
    "map_by",
    "pure",
    "take_after",
    "take_before",
    "when",
]


type LazyCoroutineEitherList[L, R] = LazyCoroutineEither[L, List[R]]


if TYPE_CHECKING:

    @curry
    def map_by[L, From, To](
        lazy_coroutine_either_list_value: LazyCoroutineEitherList[L, From],
        function: Callable[[From], To],
    ) -> LazyCoroutineEitherList[L, To]: ...

else:
    map_by = felis.identity.compose(lazy_coroutine_either.map_by)(list.map_by)


pure = felis.identity.compose(lazy_coroutine_either.pure)(list.pure)


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
    lift2 = applicative.lift2(map_by)(apply)


take_after = lift2(function.flip(function.pure))


discard_after = lift2(function.pure)


take_before = function.flip(discard_after)


discard_before = function.flip(take_after)


if TYPE_CHECKING:

    @curry
    def when[L](lazy_coroutine_either_list_none: LazyCoroutineEitherList[L, None], bool: bool) -> LazyCoroutineEitherList[L, None]: ...

else:
    when = applicative.when(pure)


if TYPE_CHECKING:

    def join[L, R](
        lazy_coroutine_either_list_lazy_coroutine_either_list_value: LazyCoroutineEitherList[L, LazyCoroutineEitherList[L, R]],
    ) -> LazyCoroutineEitherList[L, R]: ...

else:
    join = list_t.join(lazy_coroutine_either.pure)(lazy_coroutine_either.bind)


if TYPE_CHECKING:

    @curry
    def bind_to[L, From, To](
        lazy_coroutine_either_list_value: LazyCoroutineEitherList[L, From],
        function: Callable[[From], LazyCoroutineEitherList[L, To]],
    ) -> LazyCoroutineEitherList[L, To]: ...

else:
    bind_to = monad.bind_to(map_by)(join)


bind = function.flip(bind_to)


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
