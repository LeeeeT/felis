from collections.abc import Callable
from typing import TYPE_CHECKING

import felis.identity
from felis import applicative, function, lazy_coroutine, monad, option, option_t
from felis.currying import curry
from felis.lazy_coroutine import LazyCoroutine
from felis.option import Option

__all__ = [
    "LazyCoroutineOption",
    "apply",
    "bind",
    "bind_to",
    "compose",
    "default_to",
    "discard_after",
    "discard_before",
    "guard",
    "join",
    "lift2",
    "map_by",
    "pure",
    "take_after",
    "take_before",
    "to_add",
    "when",
]


type LazyCoroutineOption[T] = LazyCoroutine[Option[T]]


if TYPE_CHECKING:

    @curry
    def to_add[T](lazy_coroutine_option_augend: LazyCoroutineOption[T], lazy_coroutine_option_addend: LazyCoroutineOption[T]) -> LazyCoroutineOption[T]: ...

else:
    to_add = option_t.to_add(lazy_coroutine.pure)(lazy_coroutine.bind)


if TYPE_CHECKING:

    @curry
    def map_by[From, To](lazy_coroutine_option_value: LazyCoroutineOption[From], function: Callable[[From], To]) -> LazyCoroutineOption[To]: ...

else:
    map_by = felis.identity.compose(lazy_coroutine.map_by)(option.map_by)


pure = felis.identity.compose(lazy_coroutine.pure)(option.pure)


apply = lazy_coroutine.lift2(option.apply)


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[First, Second, Result](
        second: LazyCoroutineOption[Second],
        first: LazyCoroutineOption[First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> LazyCoroutineOption[Result]: ...

else:
    lift2 = applicative.lift2(map_by)(apply)


take_after = lift2(function.flip(function.pure))


discard_after = lift2(function.pure)


take_before = function.flip(discard_after)


discard_before = function.flip(take_after)


if TYPE_CHECKING:

    @curry
    def when(lazy_coroutine_option_none: LazyCoroutineOption[None], bool: bool) -> LazyCoroutineOption[None]: ...

else:
    when = applicative.when(pure)


if TYPE_CHECKING:

    def join[T](lazy_coroutine_option_lazy_coroutine_option_value: LazyCoroutineOption[LazyCoroutineOption[T]]) -> LazyCoroutineOption[T]: ...

else:
    join = option_t.join(lazy_coroutine.pure)(lazy_coroutine.bind)


if TYPE_CHECKING:

    @curry
    def bind_to[From, To](
        lazy_coroutine_option_value: LazyCoroutineOption[From],
        function: Callable[[From], LazyCoroutineOption[To]],
    ) -> LazyCoroutineOption[To]: ...

else:
    bind_to = monad.bind_to(map_by)(join)


bind = function.flip(bind_to)


if TYPE_CHECKING:

    @curry
    @curry
    def compose[From, Intermediate, To](
        value: From,
        first: Callable[[From], LazyCoroutineOption[Intermediate]],
        second: Callable[[Intermediate], LazyCoroutineOption[To]],
    ) -> LazyCoroutineOption[To]: ...

else:
    compose = monad.compose(bind)


guard = felis.identity.compose(lazy_coroutine.pure)(option.guard)


if TYPE_CHECKING:

    @curry
    def default_to[T](lazy_coroutine_option_value: LazyCoroutineOption[T], default_value: LazyCoroutine[T]) -> LazyCoroutine[T]: ...

else:
    default_to = option_t.default_to(lazy_coroutine.pure)(lazy_coroutine.bind)
