from collections.abc import Callable
from typing import TYPE_CHECKING

import felis.identity
from felis import applicative, function, monad, option
from felis.currying import curry
from felis.function import Function
from felis.option import Option

__all__ = ["map", "identity", "apply", "lift2", "take_after", "discard_after", "take_before", "discard_before", "when", "join", "bound", "bind", "compose", "guard"]


if TYPE_CHECKING:

    @curry
    def map[T, From, To](function_option_value: Function[T, Option[From]], function: Callable[[From], To]) -> Function[T, Option[To]]: ...

else:
    map = felis.identity.compose(function.map)(option.map)


identity = felis.identity.compose(function.identity)(option.identity)


apply = function.lift2(option.apply)


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[T, First, Second, Result](
        second: Function[T, Option[Second]],
        first: Function[T, Option[First]],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> Function[T, Option[Result]]: ...

else:
    lift2 = applicative.lift2(map)(apply)


take_after = lift2(function.flip(function.identity))


discard_after = lift2(function.identity)


take_before = function.flip(discard_after)


discard_before = function.flip(take_after)


if TYPE_CHECKING:

    @curry
    def when[T](bool: bool, function_option_none: Function[T, Option[None]]) -> Function[T, Option[None]]: ...

else:
    when = applicative.when(identity)


join = function.bound(option.inject(function.identity))


if TYPE_CHECKING:

    @curry
    def bound[T, From, To](
        function_option_value: Function[T, Option[From]], function: Callable[[From], Function[T, Option[To]]]
    ) -> Function[T, Option[To]]: ...

else:
    bound = monad.bound(map)(join)


bind = function.flip(bound)


if TYPE_CHECKING:

    @curry
    @curry
    def compose[T, From, Intermediate, To](
        value: From,
        first: Callable[[From], Function[T, Option[Intermediate]]],
        second: Callable[[Intermediate], Function[T, Option[To]]],
    ) -> Function[T, Option[To]]: ...

else:
    compose = monad.compose(bound)


guard = felis.identity.compose(function.identity)(option.guard)
