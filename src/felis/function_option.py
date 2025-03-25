from collections.abc import Callable
from typing import TYPE_CHECKING

import felis.identity
from felis import applicative, function, monad, option, option_t
from felis.currying import curry, flip
from felis.function import Function
from felis.option import Option

__all__ = [
    "FunctionOption",
    "apply",
    "bind",
    "bind_to",
    "compose_after",
    "compose_before",
    "discard_after",
    "discard_before",
    "guard",
    "join",
    "lift2",
    "map_by",
    "pure",
    "take_after",
    "take_before",
    "when",
]


type FunctionOption[From, To] = Function[From, Option[To]]


if TYPE_CHECKING:

    @curry
    def map_by[T, From, To](function_option_value: FunctionOption[T, From], function: Callable[[From], To]) -> FunctionOption[T, To]: ...

else:
    map_by = felis.identity.compose_before(function.map_by)(option.map_by)


pure = felis.identity.compose_before(function.pure)(option.pure)


apply = function.lift2(option.apply)


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[T, First, Second, Result](
        second: FunctionOption[T, Second],
        first: FunctionOption[T, First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> FunctionOption[T, Result]: ...

else:
    lift2 = applicative.lift2(map_by)(apply)


if TYPE_CHECKING:

    @curry
    def take_after[T, First, Second](second: FunctionOption[T, Second], first: FunctionOption[T, First]) -> FunctionOption[T, Second]: ...

else:
    take_after = applicative.take_after(lift2)


if TYPE_CHECKING:

    @curry
    def discard_before[T, First, Second](first: FunctionOption[T, First], second: FunctionOption[T, Second]) -> FunctionOption[T, Second]: ...

else:
    discard_before = applicative.discard_before(lift2)


if TYPE_CHECKING:

    @curry
    def discard_after[T, First, Second](second: FunctionOption[T, Second], first: FunctionOption[T, First]) -> FunctionOption[T, First]: ...

else:
    discard_after = applicative.discard_after(lift2)


if TYPE_CHECKING:

    @curry
    def take_before[T, First, Second](first: FunctionOption[T, First], second: FunctionOption[T, Second]) -> FunctionOption[T, First]: ...

else:
    take_before = applicative.take_before(lift2)


if TYPE_CHECKING:

    @curry
    def when[T](function_option_none: FunctionOption[T, None], bool: bool) -> FunctionOption[T, None]: ...

else:
    when = applicative.when(pure)


if TYPE_CHECKING:

    def join[T, From, To](function_option_function_option_value: FunctionOption[T, FunctionOption[T, From]]) -> FunctionOption[T, To]: ...

else:
    join = option_t.join(function.pure)(function.bind)


if TYPE_CHECKING:

    @curry
    def bind_to[T, From, To](
        function_option_value: FunctionOption[T, From],
        function: Callable[[From], FunctionOption[T, To]],
    ) -> FunctionOption[T, To]: ...

else:
    bind_to = monad.bind_to(map_by)(join)


bind = flip(bind_to)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_after[T, From, Intermediate, To](
        value: From,
        second: Callable[[Intermediate], FunctionOption[T, To]],
        first: Callable[[From], FunctionOption[T, Intermediate]],
    ) -> FunctionOption[T, To]: ...

else:
    compose_after = monad.compose_after(bind)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_before[T, From, Intermediate, To](
        value: From,
        first: Callable[[From], FunctionOption[T, Intermediate]],
        second: Callable[[Intermediate], FunctionOption[T, To]],
    ) -> FunctionOption[T, To]: ...

else:
    compose_before = monad.compose_before(bind)


guard = felis.identity.compose_before(function.pure)(option.guard)
