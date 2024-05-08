from collections.abc import Callable

from felis import monad
from felis.currying import curry

__all__ = ["Function", "identity", "map", "join", "bind", "compose", "then"]


type Function[From, To] = Callable[[From], To]


@curry
def identity[T](_: object, value: T) -> T:
    return value


@curry
@curry
def map[T, From, To](value: T, function_value: Function[T, From], function: Callable[[From], To]) -> To:
    return function(function_value(value))


@curry
def join[From, To](value: From, function_function_value: Function[From, Function[From, To]]) -> To:
    return function_function_value(value)(value)


bind = monad.bind(map)(join)


compose = monad.compose(bind)


then = monad.then(bind)
