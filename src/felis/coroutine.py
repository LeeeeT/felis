import collections.abc
from collections.abc import Callable
from typing import Any

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


lift2 = applicative.lift2(map)(apply)


when = applicative.when(identity)


async def join[T](coroutine_coroutine_value: Coroutine[Coroutine[T]]) -> T:
    return await (await coroutine_coroutine_value)


bind = monad.bind(map)(join)


compose = monad.compose(bind)


then = monad.then(bind)
