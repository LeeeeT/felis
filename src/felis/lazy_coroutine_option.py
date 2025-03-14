from collections.abc import Callable
from typing import TYPE_CHECKING

import felis.identity
from felis import applicative, function, lazy_coroutine, monad, option, option_t
from felis.currying import curry
from felis.lazy_coroutine import LazyCoroutine
from felis.option import Option

__all__ = [
    "LazyCoroutineOption",
    "add",
    "apply",
    "bind",
    "bound",
    "compose",
    "default",
    "discard_after",
    "discard_before",
    "guard",
    "identity",
    "join",
    "lift2",
    "map",
    "take_after",
    "take_before",
    "when",
]


type LazyCoroutineOption[T] = LazyCoroutine[Option[T]]


if TYPE_CHECKING:

    @curry
    def add[T](lazy_coroutine_option_augend: LazyCoroutineOption[T], lazy_coroutine_option_addend: LazyCoroutineOption[T]) -> LazyCoroutineOption[T]: ...

else:
    add = option_t.add(lazy_coroutine.identity)(lazy_coroutine.bind)


if TYPE_CHECKING:

    @curry
    def map[From, To](lazy_coroutine_option_value: LazyCoroutineOption[From], function: Callable[[From], To]) -> LazyCoroutineOption[To]: ...

else:
    map = felis.identity.compose(lazy_coroutine.map)(option.map)


identity = felis.identity.compose(lazy_coroutine.identity)(option.identity)


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
    lift2 = applicative.lift2(map)(apply)


take_after = lift2(function.flip(function.identity))


discard_after = lift2(function.identity)


take_before = function.flip(discard_after)


discard_before = function.flip(take_after)


if TYPE_CHECKING:

    @curry
    def when(bool: bool, lazy_coroutine_option_none: LazyCoroutineOption[None]) -> LazyCoroutineOption[None]: ...

else:
    when = applicative.when(identity)


if TYPE_CHECKING:

    def join[T](lazy_coroutine_option_lazy_coroutine_option_value: LazyCoroutineOption[LazyCoroutineOption[T]]) -> LazyCoroutineOption[T]: ...

else:
    join = option_t.join(lazy_coroutine.identity)(lazy_coroutine.bind)


if TYPE_CHECKING:

    @curry
    def bound[From, To](
        lazy_coroutine_option_value: LazyCoroutineOption[From],
        function: Callable[[From], LazyCoroutineOption[To]],
    ) -> LazyCoroutineOption[To]: ...

else:
    bound = monad.bound(map)(join)


bind = function.flip(bound)


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


guard = felis.identity.compose(lazy_coroutine.identity)(option.guard)


if TYPE_CHECKING:

    @curry
    def default[T](lazy_coroutine_option_value: LazyCoroutineOption[T], default_value: LazyCoroutine[T]) -> LazyCoroutine[T]: ...

else:
    default = option_t.default(lazy_coroutine.identity)(lazy_coroutine.bind)
