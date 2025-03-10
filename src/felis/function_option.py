from collections.abc import Callable
from typing import TYPE_CHECKING

import felis.identity
from felis import applicative, function, monad, option, option_t
from felis.currying import curry
from felis.function import Function
from felis.option import Option

__all__ = [
    "FunctionOption",
    "apply",
    "bind",
    "bound",
    "compose",
    "discard_after",
    "discard_before",
    "guard",
    "identity",
    "join",
    "lift2",
    "map",
    "take_after",
    "take_before",
    "when",
]


type FunctionOption[From, To] = Function[From, Option[To]]


if TYPE_CHECKING:

    @curry
    def map[T, From, To](function_option_value: FunctionOption[T, From], function: Callable[[From], To]) -> FunctionOption[T, To]: ...

else:
    map = felis.identity.compose(function.map)(option.map)


identity = felis.identity.compose(function.identity)(option.identity)


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
    lift2 = applicative.lift2(map)(apply)


take_after = lift2(function.flip(function.identity))


discard_after = lift2(function.identity)


take_before = function.flip(discard_after)


discard_before = function.flip(take_after)


if TYPE_CHECKING:

    @curry
    def when[T](bool: bool, function_option_none: FunctionOption[T, None]) -> FunctionOption[T, None]: ...

else:
    when = applicative.when(identity)


if TYPE_CHECKING:

    def join[T, From, To](function_option_function_option_value: FunctionOption[T, FunctionOption[T, From]]) -> FunctionOption[T, To]: ...

else:
    join = option_t.join(function.identity)(function.bind)


if TYPE_CHECKING:

    @curry
    def bound[T, From, To](
        function_option_value: FunctionOption[T, From],
        function: Callable[[From], FunctionOption[T, To]],
    ) -> FunctionOption[T, To]: ...

else:
    bound = monad.bound(map)(join)


bind = function.flip(bound)


if TYPE_CHECKING:

    @curry
    @curry
    def compose[T, From, Intermediate, To](
        value: From,
        first: Callable[[From], FunctionOption[T, Intermediate]],
        second: Callable[[Intermediate], FunctionOption[T, To]],
    ) -> FunctionOption[T, To]: ...

else:
    compose = monad.compose(bind)


guard = felis.identity.compose(function.identity)(option.guard)
