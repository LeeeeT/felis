from collections.abc import Callable
from typing import TYPE_CHECKING

import felis.identity
from felis import applicative, monad
from felis.currying import curry
from felis.function.flip_ import flip
from felis.function.identity_ import identity

__all__ = [
    "Function",
    "flip",
    "neutral",
    "neutral2",
    "add",
    "add2",
    "map",
    "map2",
    "identity",
    "apply",
    "lift2",
    "take_after",
    "discard_after",
    "take_before",
    "discard_before",
    "when",
    "join",
    "bound",
    "bind",
    "compose",
]


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
@curry
def map[T, From, To](value: T, function_value: Function[T, From], function: Callable[[From], To]) -> To:
    return function(function_value(value))


map2 = felis.identity.compose(map)(map)


@curry
@curry
def apply[T, From, To](value: T, function_value: Function[T, From], function: Function[T, Callable[[From], To]]) -> To:
    return function(value)(function_value(value))


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[T, First, Second, Result](
        second: Function[T, Second],
        first: Function[T, First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> Function[T, Result]: ...

else:
    lift2 = applicative.lift2(map)(apply)


take_after = lift2(flip(identity))


discard_after = lift2(identity)


take_before = flip(discard_after)


discard_before = flip(take_after)


if TYPE_CHECKING:

    @curry
    def when[T](bool: bool, function_none: Function[T, None]) -> Function[T, None]: ...

else:
    when = applicative.when(identity)


@curry
def join[From, To](value: From, function_function_value: Function[From, Function[From, To]]) -> To:
    return function_function_value(value)(value)


if TYPE_CHECKING:

    @curry
    def bound[T, From, To](either_value: Function[T, From], function: Callable[[From], Function[T, To]]) -> Function[T, To]: ...

else:
    bound = monad.bound(map)(join)


bind = flip(bound)


if TYPE_CHECKING:

    @curry
    @curry
    def compose[T, From, Intermediate, To](
        value: From,
        first: Callable[[From], Function[T, Intermediate]],
        second: Callable[[Intermediate], Function[T, To]],
    ) -> Function[T, To]: ...

else:
    compose = monad.compose(bind)
