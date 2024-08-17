import builtins
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import felis.identity
import felis.order
from felis import applicative, function, monad
from felis.currying import curry
from felis.order import Order
from felis.predicate import Predicate

__all__ = [
    "neutral",
    "append",
    "add",
    "map",
    "identity",
    "apply",
    "lift2",
    "take_after",
    "discard_after",
    "take_before",
    "discard_before",
    "when",
    "fold",
    "traverse",
    "join",
    "bound",
    "bind",
    "compose",
    "guard",
    "filter",
    "sort",
    "range",
]


# [T : Type] -> list T
neutral: list[Any] = []


@curry
def append[T](list: list[T], value: T) -> list[T]:
    return [*list, value]


@curry
def add[T](augend: list[T], addend: list[T]) -> list[T]:
    return augend + addend


@curry
def map[From, To](list_value: list[From], function: Callable[[From], To]) -> list[To]:
    return [function(value) for value in list_value]


def identity[T](value: T) -> list[T]:
    return [value]


@curry
def apply[From, To](list_value: list[From], list_function: list[Callable[[From], To]]) -> list[To]:
    return [function(value) for function in list_function for value in list_value]


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[First, Second, Result](second: list[Second], first: list[First], function: Callable[[First], Callable[[Second], Result]]) -> list[Result]: ...

else:
    lift2 = applicative.lift2(map)(apply)


take_after = lift2(function.flip(function.identity))


discard_after = lift2(function.identity)


take_before = function.flip(discard_after)


discard_before = function.flip(take_after)


if TYPE_CHECKING:

    @curry
    def when(bool: bool, list_none: list[None]) -> list[None]: ...

else:
    when = applicative.when(identity)


@curry
@curry
def fold[A, T](list_value: list[T], function: Callable[[T], Callable[[A], A]], accumulator: A) -> A:
    for value in list_value:
        accumulator = function(value)(accumulator)
    return accumulator


# [A : Type -> Type] ->
# ([From : Type] -> [To : Type] -> (From -> To) -> A From -> A To) ->
# ([T : Type] -> T -> A T) ->
# [From : Type] -> [To : Type] -> (From -> A To) -> list From -> A (list To)
@curry
@curry
def traverse[From](
    function: Callable[[From], Any],
    a_lift2: Callable[[Callable[[Any], Callable[[Any], Any]]], Callable[[Any], Callable[[Any], Any]]],
    a_identity: Callable[[Any], Any],
) -> Callable[[list[From]], Any]:
    return fold(a_identity(neutral))(felis.identity.compose(a_lift2(append))(function))


if TYPE_CHECKING:

    def join[T](list_list_value: list[list[T]]) -> list[T]: ...

else:
    join = fold(neutral)(add)


if TYPE_CHECKING:

    @curry
    def bound[From, To](list_value: list[From], function: Callable[[From], list[To]]) -> list[To]: ...

else:
    bound = monad.bound(map)(join)


bind = function.flip(bound)


if TYPE_CHECKING:

    @curry
    @curry
    def compose[From, Intermediate, To](value: From, first: Callable[[From], list[Intermediate]], second: Callable[[Intermediate], list[To]]) -> list[To]: ...

else:
    compose = monad.compose(bind)


if TYPE_CHECKING:

    def guard(bool: bool) -> list[None]: ...

else:
    guard = monad.guard(neutral)(identity)


@curry
def filter[T](list: list[T], predicate: Predicate[T]) -> list[T]:
    return [value for value in list if predicate(value)]


@curry
def sort[T](list: list[T], order: Order[T]) -> list[T]:
    return sorted(list, key=felis.order.rich_comparison(order))


@curry
def range(stop: int, start: int) -> list[int]:
    return list(builtins.range(start, stop))
