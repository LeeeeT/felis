from collections.abc import Callable
from typing import TYPE_CHECKING

import felis.identity
from felis import applicative, monad
from felis.currying import curry
from felis.function.flip_ import flip
from felis.function.pure_ import pure

__all__ = [
    "Function",
    "apply",
    "bind",
    "bind_to",
    "compose",
    "discard_after",
    "discard_before",
    "flip",
    "join",
    "lift2",
    "map_by",
    "map_by2",
    "neutral",
    "neutral2",
    "pure",
    "take_after",
    "take_before",
    "to_add",
    "to_add2",
    "when",
]


type Function[From, To] = Callable[[From], To]


@curry
def neutral[M](_: object, m_neutral: M) -> M:
    return m_neutral


neutral2 = felis.identity.compose(neutral)(neutral)


@curry
@curry
@curry
def to_add[M, T](value: T, augend: Function[T, M], addend: Function[T, M], m_add: Callable[[M], Callable[[M], M]]) -> M:
    return m_add(addend(value))(augend(value))


to_add2 = felis.identity.compose(to_add)(to_add)


@curry
@curry
def map_by[T, From, To](value: T, function_value: Function[T, From], function: Callable[[From], To]) -> To:
    return function(function_value(value))


map_by2 = felis.identity.compose(map_by)(map_by)


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
    lift2 = applicative.lift2(map_by)(apply)


take_after = lift2(flip(pure))


discard_after = lift2(pure)


take_before = flip(discard_after)


discard_before = flip(take_after)


if TYPE_CHECKING:

    @curry
    def when[T](function_none: Function[T, None], bool: bool) -> Function[T, None]: ...

else:
    when = applicative.when(pure)


@curry
def join[From, To](value: From, function_function_value: Function[From, Function[From, To]]) -> To:
    return function_function_value(value)(value)


if TYPE_CHECKING:

    @curry
    def bind_to[T, From, To](either_value: Function[T, From], function: Callable[[From], Function[T, To]]) -> Function[T, To]: ...

else:
    bind_to = monad.bind_to(map_by)(join)


bind = flip(bind_to)


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
