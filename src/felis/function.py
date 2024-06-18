from collections.abc import Callable

import felis.identity
from felis import applicative, monad
from felis.currying import curry

__all__ = ["Function", "neutral", "neutral2", "add", "add2", "identity", "when", "map", "map2", "apply", "join", "bind", "compose", "then"]


type Function[From, To] = Callable[[From], To]


@curry
def neutral[M](_: object, m_neutral: M) -> M:
    return m_neutral


neutral2 = felis.identity.compose(neutral)(neutral)


@curry
@curry
@curry
def add[M, T](value: T, augend: Function[T, M], addend: Function[T, M], m_add: Callable[[M], Callable[[M], M]]) -> M:
    return m_add(addend(value))(augend(value))


add2 = felis.identity.compose(add)(add)


@curry
def identity[T](_: object, value: T) -> T:
    return value


when = applicative.when(identity)


@curry
@curry
def map[T, From, To](value: T, function_value: Function[T, From], function: Callable[[From], To]) -> To:
    return function(function_value(value))


map2 = felis.identity.compose(map)(map)


@curry
@curry
def apply[T, From, To](value: T, function_value: Function[T, From], function: Function[T, Callable[[From], To]]) -> To:
    return function(value)(function_value(value))


@curry
def join[From, To](value: From, function_function_value: Function[From, Function[From, To]]) -> To:
    return function_function_value(value)(value)


bind = monad.bind(map)(join)


compose = monad.compose(bind)


then = monad.then(bind)
