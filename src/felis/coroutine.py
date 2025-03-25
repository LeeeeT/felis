import collections.abc
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from felis import applicative, monad
from felis.currying import curry, flip

__all__ = [
    "Coroutine",
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


type Coroutine[T] = collections.abc.Coroutine[Any, Any, T]


@curry
async def map_by[From, To](coroutine_value: Coroutine[From], function: Callable[[From], To]) -> To:
    return function(await coroutine_value)


async def pure[T](value: T) -> T:
    return value


@curry
async def apply[From, To](coroutine_value: Coroutine[From], coroutine_function: Coroutine[Callable[[From], To]]) -> To:
    return await map_by(await coroutine_function)(coroutine_value)


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[First, Second, Result](
        second: Coroutine[Second],
        first: Coroutine[First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> Coroutine[Result]: ...

else:
    lift2 = applicative.lift2(map_by)(apply)


if TYPE_CHECKING:

    @curry
    def take_after[First, Second](second: Coroutine[Second], first: Coroutine[First]) -> Coroutine[Second]: ...

else:
    take_after = applicative.take_after(lift2)


if TYPE_CHECKING:

    @curry
    def discard_before[First, Second](first: Coroutine[First], second: Coroutine[Second]) -> Coroutine[Second]: ...

else:
    discard_before = applicative.discard_before(lift2)


if TYPE_CHECKING:

    @curry
    def discard_after[First, Second](second: Coroutine[Second], first: Coroutine[First]) -> Coroutine[First]: ...

else:
    discard_after = applicative.discard_after(lift2)


if TYPE_CHECKING:

    @curry
    def take_before[First, Second](first: Coroutine[First], second: Coroutine[Second]) -> Coroutine[First]: ...

else:
    take_before = applicative.take_before(lift2)


if TYPE_CHECKING:

    @curry
    def when(coroutine_none: Coroutine[None], bool: bool) -> Coroutine[None]: ...

else:
    when = applicative.when(pure)


async def join[T](coroutine_coroutine_value: Coroutine[Coroutine[T]]) -> T:
    return await (await coroutine_coroutine_value)


if TYPE_CHECKING:

    @curry
    def bind_to[From, To](coroutine_value: Coroutine[From], function: Callable[[From], Coroutine[To]]) -> Coroutine[To]: ...

else:
    bind_to = monad.bind_to(map_by)(join)


bind = flip(bind_to)


if TYPE_CHECKING:

    @curry
    @curry
    def compose[From, Intermediate, To](
        value: From,
        first: Callable[[From], Coroutine[Intermediate]],
        second: Callable[[Intermediate], Coroutine[To]],
    ) -> Coroutine[To]: ...

else:
    compose = monad.compose(bind)
