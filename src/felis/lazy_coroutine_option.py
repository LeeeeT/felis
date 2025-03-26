from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

import felis.identity
from felis import applicative, lazy_coroutine, monad, option, option_t
from felis.currying import curry, flip
from felis.lazy_coroutine import LazyCoroutine
from felis.option import Option

if TYPE_CHECKING:
    from felis import Either

__all__ = [
    "LazyCoroutineOption",
    "add_to",
    "apply",
    "bind",
    "bind_to",
    "compose_after",
    "compose_before",
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
    "to_either",
    "when",
]


type LazyCoroutineOption[T] = LazyCoroutine[Option[T]]


if TYPE_CHECKING:

    @curry
    def to_add[T](lazy_coroutine_option_augend: LazyCoroutineOption[T], lazy_coroutine_option_addend: LazyCoroutineOption[T]) -> LazyCoroutineOption[T]: ...

else:
    to_add = option_t.to_add(lazy_coroutine.pure)(lazy_coroutine.bind)


add_to = flip(to_add)


if TYPE_CHECKING:

    @curry
    def map_by[From, To](lazy_coroutine_option_value: LazyCoroutineOption[From], function: Callable[[From], To]) -> LazyCoroutineOption[To]: ...

else:
    map_by = felis.identity.compose_before(lazy_coroutine.map_by)(option.map_by)


pure = felis.identity.compose_before(lazy_coroutine.pure)(option.pure)


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


if TYPE_CHECKING:

    @curry
    def take_after[First, Second](second: LazyCoroutineOption[Second], first: LazyCoroutineOption[First]) -> LazyCoroutineOption[Second]: ...

else:
    take_after = applicative.take_after(lift2)


if TYPE_CHECKING:

    @curry
    def discard_before[First, Second](first: LazyCoroutineOption[First], second: LazyCoroutineOption[Second]) -> LazyCoroutineOption[Second]: ...

else:
    discard_before = applicative.discard_before(lift2)


if TYPE_CHECKING:

    @curry
    def discard_after[First, Second](second: LazyCoroutineOption[Second], first: LazyCoroutineOption[First]) -> LazyCoroutineOption[First]: ...

else:
    discard_after = applicative.discard_after(lift2)


if TYPE_CHECKING:

    @curry
    def take_before[First, Second](first: LazyCoroutineOption[First], second: LazyCoroutineOption[Second]) -> LazyCoroutineOption[First]: ...

else:
    take_before = applicative.take_before(lift2)


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


bind = flip(bind_to)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_after[From, Intermediate, To](
        value: From,
        second: Callable[[Intermediate], LazyCoroutineOption[To]],
        first: Callable[[From], LazyCoroutineOption[Intermediate]],
    ) -> LazyCoroutineOption[To]: ...

else:
    compose_after = monad.compose_after(bind)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_before[From, Intermediate, To](
        value: From,
        first: Callable[[From], LazyCoroutineOption[Intermediate]],
        second: Callable[[Intermediate], LazyCoroutineOption[To]],
    ) -> LazyCoroutineOption[To]: ...

else:
    compose_before = monad.compose_before(bind)


guard = felis.identity.compose_before(lazy_coroutine.pure)(option.guard)


if TYPE_CHECKING:

    @curry
    def default_to[T](lazy_coroutine_option_value: LazyCoroutineOption[T], default_value: LazyCoroutine[T]) -> LazyCoroutine[T]: ...

else:
    default_to = option_t.default_to(lazy_coroutine.pure)(lazy_coroutine.bind)


if TYPE_CHECKING:

    @curry
    def to_either[L, R](coroutine_option_value: LazyCoroutineOption[R], left: LazyCoroutine[L]) -> LazyCoroutine[Either[L, R]]: ...

else:
    to_either = option_t.to_either(lazy_coroutine.pure)(lazy_coroutine.bind)
