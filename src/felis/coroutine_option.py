from collections.abc import Callable
from typing import TYPE_CHECKING

import felis.identity
from felis import applicative, coroutine, function, monad, option, option_t
from felis.coroutine import Coroutine
from felis.currying import curry
from felis.option import Option

__all__ = [
    "CoroutineOption",
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


type CoroutineOption[T] = Coroutine[Option[T]]


if TYPE_CHECKING:

    @curry
    def add[T](coroutine_option_augend: CoroutineOption[T], coroutine_option_addend: CoroutineOption[T]) -> CoroutineOption[T]: ...

else:
    add = option_t.add(coroutine.identity)(coroutine.bind)


if TYPE_CHECKING:

    @curry
    def map[From, To](coroutine_option_value: CoroutineOption[From], function: Callable[[From], To]) -> CoroutineOption[To]: ...

else:
    map = felis.identity.compose(coroutine.map)(option.map)


identity = felis.identity.compose(coroutine.identity)(option.identity)


apply = coroutine.lift2(option.apply)


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[First, Second, Result](
        second: CoroutineOption[Second],
        first: CoroutineOption[First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> CoroutineOption[Result]: ...

else:
    lift2 = applicative.lift2(map)(apply)


take_after = lift2(function.flip(function.identity))


discard_after = lift2(function.identity)


take_before = function.flip(discard_after)


discard_before = function.flip(take_after)


if TYPE_CHECKING:

    @curry
    def when(bool: bool, coroutine_option_none: CoroutineOption[None]) -> CoroutineOption[None]: ...

else:
    when = applicative.when(identity)


if TYPE_CHECKING:

    def join[T](coroutine_option_coroutine_option_value: CoroutineOption[CoroutineOption[T]]) -> CoroutineOption[T]: ...

else:
    join = option_t.join(coroutine.identity)(coroutine.bind)


if TYPE_CHECKING:

    @curry
    def bound[From, To](coroutine_option_value: CoroutineOption[From], function: Callable[[From], CoroutineOption[To]]) -> CoroutineOption[To]: ...

else:
    bound = monad.bound(map)(join)


bind = function.flip(bound)


if TYPE_CHECKING:

    @curry
    @curry
    def compose[From, Intermediate, To](
        value: From,
        first: Callable[[From], CoroutineOption[Intermediate]],
        second: Callable[[Intermediate], CoroutineOption[To]],
    ) -> CoroutineOption[To]: ...

else:
    compose = monad.compose(bind)


guard = felis.identity.compose(coroutine.identity)(option.guard)


if TYPE_CHECKING:

    @curry
    def default[T](coroutine_option_value: CoroutineOption[T], default_value: Coroutine[T]) -> Coroutine[T]: ...

else:
    default = option_t.default(coroutine.identity)(coroutine.bind)
