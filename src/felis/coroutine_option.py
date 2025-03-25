from collections.abc import Callable
from typing import TYPE_CHECKING

import felis.identity
from felis import applicative, coroutine, monad, option, option_t
from felis.coroutine import Coroutine
from felis.currying import curry, flip
from felis.option import Option

__all__ = [
    "CoroutineOption",
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
    map_by = felis.identity.compose_before(coroutine.map_by)(option.map_by)


pure = felis.identity.compose_before(coroutine.pure)(option.pure)


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


if TYPE_CHECKING:

    @curry
    def take_after[First, Second](second: CoroutineOption[Second], first: CoroutineOption[First]) -> CoroutineOption[Second]: ...

else:
    take_after = applicative.take_after(lift2)


if TYPE_CHECKING:

    @curry
    def discard_before[First, Second](first: CoroutineOption[First], second: CoroutineOption[Second]) -> CoroutineOption[Second]: ...

else:
    discard_before = applicative.discard_before(lift2)


if TYPE_CHECKING:

    @curry
    def discard_after[First, Second](second: CoroutineOption[Second], first: CoroutineOption[First]) -> CoroutineOption[First]: ...

else:
    discard_after = applicative.discard_after(lift2)


if TYPE_CHECKING:

    @curry
    def take_before[First, Second](first: CoroutineOption[First], second: CoroutineOption[Second]) -> CoroutineOption[First]: ...

else:
    take_before = applicative.take_before(lift2)


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


bind = flip(bind_to)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_after[From, Intermediate, To](
        value: From,
        second: Callable[[Intermediate], CoroutineOption[To]],
        first: Callable[[From], CoroutineOption[Intermediate]],
    ) -> CoroutineOption[To]: ...

else:
    compose_after = monad.compose_after(bind)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_before[From, Intermediate, To](
        value: From,
        first: Callable[[From], CoroutineOption[Intermediate]],
        second: Callable[[Intermediate], CoroutineOption[To]],
    ) -> CoroutineOption[To]: ...

else:
    compose_before = monad.compose_before(bind)


guard = felis.identity.compose_before(coroutine.pure)(option.guard)


if TYPE_CHECKING:

    @curry
    def default_to[T](coroutine_option_value: CoroutineOption[T], default_value: Coroutine[T]) -> Coroutine[T]: ...

else:
    default_to = option_t.default_to(coroutine.pure)(coroutine.bind)
