from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import felis.identity
from felis import applicative, monad
from felis.currying import curry, flip

__all__ = [
    "Function",
    "apply",
    "bind",
    "bind_to",
    "compose",
    "discard_after",
    "discard_before",
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
def pure[T](_: Any, value: T) -> T:
    return value


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


if TYPE_CHECKING:

    @curry
    def take_after[T, First, Second](second: Function[T, Second], first: Function[T, First]) -> Function[T, Second]: ...

else:
    take_after = applicative.take_after(lift2)


if TYPE_CHECKING:

    @curry
    def discard_before[T, First, Second](first: Function[T, First], second: Function[T, Second]) -> Function[T, Second]: ...

else:
    discard_before = applicative.discard_before(lift2)


if TYPE_CHECKING:

    @curry
    def discard_after[T, First, Second](second: Function[T, Second], first: Function[T, First]) -> Function[T, First]: ...

else:
    discard_after = applicative.discard_after(lift2)


if TYPE_CHECKING:

    @curry
    def take_before[T, First, Second](first: Function[T, First], second: Function[T, Second]) -> Function[T, First]: ...

else:
    take_before = applicative.take_before(lift2)


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
