from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import felis.applicative
import felis.functor
import felis.identity
import felis.monad
from felis.applicative import Applicative
from felis.currying import curry
from felis.functor import Functor
from felis.monad import Monad

__all__ = [
    "Function",
    "Function2",
    "applicative",
    "apply_to",
    "bind_to",
    "by_map",
    "by_map2",
    "compose_after",
    "compose_before",
    "discard_after",
    "discard_before",
    "functor",
    "functor2",
    "join",
    "lift",
    "map_by",
    "map_by2",
    "monad",
    "neutral2_t",
    "neutral_t",
    "pure",
    "take_after",
    "take_before",
    "to_add2_t",
    "to_add_t",
    "to_apply",
    "to_bind",
    "when",
]


type Function[From, To] = Callable[[From], To]


@curry
@curry
@curry
def to_add_t[M, T](value: T, augend: Function[T, M], addend: Function[T, M], m_add: Callable[[M], Callable[[M], M]]) -> M:
    return m_add(addend(value))(augend(value))


@curry
def neutral_t[M](_: object, m_neutral: M) -> M:
    return m_neutral


@curry
@curry
def map_by[T, From, To](value: T, function_value: Function[T, From], function: Callable[[From], To]) -> To:
    return function(function_value(value))


# [T : *] -> Functor (Function T)
functor = Functor(map_by)


if TYPE_CHECKING:

    @curry
    def by_map[T, From, To](function: Callable[[From], To], function_value: Function[T, From]) -> Function[T, To]: ...

else:
    by_map = felis.functor.by_map(functor)


@curry
def pure[T](_: Any, value: T) -> T:
    return value


@curry
@curry
def to_apply[T, From, To](value: T, function_value: Function[T, From], function: Function[T, Callable[[From], To]]) -> To:
    return function(value)(function_value(value))


# [T :*] -> Applicative (Function T)
applicative = Applicative(functor, pure, to_apply)


if TYPE_CHECKING:

    @curry
    def apply_to[T, From, To](function: Function[T, Callable[[From], To]], function_value: Function[T, From]) -> Function[T, To]: ...

else:
    apply_to = felis.applicative.apply_to(applicative)


if TYPE_CHECKING:

    @curry
    @curry
    def lift[T, First, Second, Result](
        second: Function[T, Second],
        first: Function[T, First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> Function[T, Result]: ...

else:
    lift = felis.applicative.lift(applicative)


if TYPE_CHECKING:

    @curry
    def take_after[T, First, Second](second: Function[T, Second], first: Function[T, First]) -> Function[T, Second]: ...

else:
    take_after = felis.applicative.take_after(applicative)


if TYPE_CHECKING:

    @curry
    def discard_before[T, First, Second](first: Function[T, First], second: Function[T, Second]) -> Function[T, Second]: ...

else:
    discard_before = felis.applicative.discard_before(applicative)


if TYPE_CHECKING:

    @curry
    def discard_after[T, First, Second](second: Function[T, Second], first: Function[T, First]) -> Function[T, First]: ...

else:
    discard_after = felis.applicative.discard_after(applicative)


if TYPE_CHECKING:

    @curry
    def take_before[T, First, Second](first: Function[T, First], second: Function[T, Second]) -> Function[T, First]: ...

else:
    take_before = felis.applicative.take_before(applicative)


if TYPE_CHECKING:

    @curry
    def when[T](function_none: Function[T, None], bool: bool) -> Function[T, None]: ...

else:
    when = felis.applicative.when(applicative)


@curry
def join[From, To](value: From, function_function_value: Function[From, Function[From, To]]) -> To:
    return function_function_value(value)(value)


# [T : *] -> Monad (Function T)
monad = Monad(applicative, join)


if TYPE_CHECKING:

    @curry
    def bind_to[T, From, To](function_value: Function[T, From], function: Callable[[From], Function[T, To]]) -> Function[T, To]: ...

else:
    bind_to = felis.monad.bind_to(monad)


if TYPE_CHECKING:

    @curry
    def to_bind[T, From, To](function: Callable[[From], Function[T, To]], function_value: Function[T, From]) -> Function[T, To]: ...

else:
    to_bind = felis.monad.to_bind(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_after[T, From, Intermediate, To](
        value: From,
        second: Callable[[Intermediate], Function[T, To]],
        first: Callable[[From], Function[T, Intermediate]],
    ) -> Function[T, To]: ...

else:
    compose_after = felis.monad.compose_after(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_before[T, From, Intermediate, To](
        value: From,
        first: Callable[[From], Function[T, Intermediate]],
        second: Callable[[Intermediate], Function[T, To]],
    ) -> Function[T, To]: ...

else:
    compose_before = felis.monad.compose_before(monad)


type Function2[First, Second, Result] = Function[First, Function[Second, Result]]


to_add2_t = felis.identity.compose_before(to_add_t)(to_add_t)


neutral2_t = felis.identity.compose_before(neutral_t)(neutral_t)


map_by2 = felis.identity.compose_before(map_by)(map_by)


# [First : *] -> [Second : *] -> Functor (Function2 First Second)
functor2 = Functor(map_by2)


if TYPE_CHECKING:

    @curry
    def by_map2[First, Second, From, To](function: Callable[[From], To], function2_value: Function2[First, Second, From]) -> Function2[First, Second, To]: ...

else:
    by_map2 = felis.functor.by_map(functor2)
