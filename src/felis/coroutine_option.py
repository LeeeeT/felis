from collections.abc import Callable
from typing import TYPE_CHECKING

import felis.identity
from felis import applicative, coroutine, function, monad, option, option_t
from felis.coroutine import Coroutine
from felis.currying import curry
from felis.option import Option

__all__ = [
    "CoroutineOption",
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


type CoroutineOption[T] = Coroutine[Option[T]]


if TYPE_CHECKING:

    @curry
    def to_add[T](coroutine_option_augend: CoroutineOption[T], coroutine_option_addend: CoroutineOption[T]) -> CoroutineOption[T]: ...

else:
    to_add = option_t.to_add(coroutine.pure)(coroutine.bind)


if TYPE_CHECKING:

    @curry
    def map_by[From, To](coroutine_option_value: CoroutineOption[From], function: Callable[[From], To]) -> CoroutineOption[To]: ...

else:
    map_by = felis.identity.compose(coroutine.map_by)(option.map_by)


pure = felis.identity.compose(coroutine.pure)(option.pure)


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
    lift2 = applicative.lift2(map_by)(apply)


take_after = lift2(function.flip(function.pure))


discard_after = lift2(function.pure)


take_before = function.flip(discard_after)


discard_before = function.flip(take_after)


if TYPE_CHECKING:

    @curry
    def when(coroutine_option_none: CoroutineOption[None], bool: bool) -> CoroutineOption[None]: ...

else:
    when = applicative.when(pure)


if TYPE_CHECKING:

    def join[T](coroutine_option_coroutine_option_value: CoroutineOption[CoroutineOption[T]]) -> CoroutineOption[T]: ...

else:
    join = option_t.join(coroutine.pure)(coroutine.bind)


if TYPE_CHECKING:

    @curry
    def bind_to[From, To](coroutine_option_value: CoroutineOption[From], function: Callable[[From], CoroutineOption[To]]) -> CoroutineOption[To]: ...

else:
    bind_to = monad.bind_to(map_by)(join)


bind = function.flip(bind_to)


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


guard = felis.identity.compose(coroutine.pure)(option.guard)


if TYPE_CHECKING:

    @curry
    def default_to[T](coroutine_option_value: CoroutineOption[T], default_value: Coroutine[T]) -> Coroutine[T]: ...

else:
    default_to = option_t.default_to(coroutine.pure)(coroutine.bind)
