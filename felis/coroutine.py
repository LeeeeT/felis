import collections.abc
from collections.abc import Callable
from typing import Any, Protocol

from felis import monad
from felis.currying import curry

__all__ = ["Coroutine", "identity", "map", "join", "bind", "compose"]


type Coroutine[T] = collections.abc.Coroutine[Any, Any, T]


async def identity[T](value: T) -> T:
    return value


@curry
async def map[From, To](coroutine_value: Coroutine[From], function: Callable[[From], To]) -> To:
    return function(await coroutine_value)


async def join[T](coroutine_coroutine__value: Coroutine[Coroutine[T]]) -> T:
    return await (await coroutine_coroutine__value)


class Bind(Protocol):
    @staticmethod
    @curry
    def __call__[From, To](coroutine_value: Coroutine[From], function: Callable[[From], Coroutine[To]], /) -> Coroutine[To]: ...


bind: Bind = monad.bind(map)(join)


class Compose(Protocol):
    @staticmethod
    @curry
    @curry
    def __call__[From, Intermediate, To](
        value: From,
        first: Callable[[From], Coroutine[Intermediate]],
        second: Callable[[Intermediate], Coroutine[To]],
        /,
    ) -> Coroutine[To]: ...


compose: Compose = monad.compose(bind)
