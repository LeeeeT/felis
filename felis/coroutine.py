import collections.abc
from collections.abc import Callable
from typing import Any

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


bind = monad.bind(map)(join)


compose = monad.compose(bind)
