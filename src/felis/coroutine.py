import collections.abc
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from felis import applicative, monad
from felis.currying import curry

__all__ = ["Coroutine", "map", "identity", "apply", "lift2", "when", "join", "bind", "compose", "then"]


type Coroutine[T] = collections.abc.Coroutine[Any, Any, T]


@curry
async def map[From, To](coroutine_value: Coroutine[From], function: Callable[[From], To]) -> To:
    return function(await coroutine_value)


async def identity[T](value: T) -> T:
    return value


@curry
async def apply[From, To](coroutine_value: Coroutine[From], coroutine_function: Coroutine[Callable[[From], To]]) -> To:
    return await map(await coroutine_function)(coroutine_value)


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[First, Second, Result](
        second: Coroutine[Second],
        first: Coroutine[First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> Coroutine[Result]: ...

else:
    lift2 = applicative.lift2(map)(apply)


if TYPE_CHECKING:

    @curry
    def when(bool: bool, coroutine_none: Coroutine[None]) -> Coroutine[None]: ...

else:
    when = applicative.when(identity)


async def join[T](coroutine_coroutine_value: Coroutine[Coroutine[T]]) -> T:
    return await (await coroutine_coroutine_value)


if TYPE_CHECKING:

    @curry
    def bind[From, To](coroutine_value: Coroutine[From], function: Callable[[From], Coroutine[To]]) -> Coroutine[To]: ...

else:
    bind = monad.bind(map)(join)


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


if TYPE_CHECKING:

    @curry
    def then[First, Second](first: Coroutine[First], second: Coroutine[Second]) -> Coroutine[Second]: ...

else:
    then = monad.then(bind)
