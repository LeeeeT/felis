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
    "List",
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


List = list


# [T : Type] -> List T
neutral: list[Any] = []


@curry
def append[T](list: List[T], value: T) -> List[T]:
    return [*list, value]


@curry
def add[T](augend: List[T], addend: List[T]) -> List[T]:
    return augend + addend


@curry
def map[From, To](list_value: List[From], function: Callable[[From], To]) -> List[To]:
    return [function(value) for value in list_value]


def identity[T](value: T) -> List[T]:
    return [value]


@curry
def apply[From, To](list_value: List[From], list_function: List[Callable[[From], To]]) -> List[To]:
    return [function(value) for function in list_function for value in list_value]


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[First, Second, Result](second: List[Second], first: List[First], function: Callable[[First], Callable[[Second], Result]]) -> List[Result]: ...

else:
    lift2 = applicative.lift2(map)(apply)


take_after = lift2(function.flip(function.identity))


discard_after = lift2(function.identity)


take_before = function.flip(discard_after)


discard_before = function.flip(take_after)


if TYPE_CHECKING:

    @curry
    def when(bool: bool, list_none: List[None]) -> List[None]: ...

else:
    when = applicative.when(identity)


@curry
@curry
def fold[A, T](list_value: List[T], function: Callable[[T], Callable[[A], A]], accumulator: A) -> A:
    for value in list_value:
        accumulator = function(value)(accumulator)
    return accumulator


# [A : Type -> Type] ->
# ([From : Type] -> [To : Type] -> (From -> To) -> A From -> A To) ->
# ([T : Type] -> T -> A T) ->
# [From : Type] -> [To : Type] -> (From -> A To) -> List From -> A (List To)
@curry
@curry
def traverse[From](
    function: Callable[[From], Any],
    a_lift2: Callable[[Callable[[Any], Callable[[Any], Any]]], Callable[[Any], Callable[[Any], Any]]],
    a_identity: Callable[[Any], Any],
) -> Callable[[List[From]], Any]:
    return fold(a_identity(neutral))(felis.identity.compose(a_lift2(append))(function))


if TYPE_CHECKING:

    def join[T](list_list_value: List[List[T]]) -> List[T]: ...

else:
    join = fold(neutral)(add)


if TYPE_CHECKING:

    @curry
    def bound[From, To](list_value: List[From], function: Callable[[From], List[To]]) -> List[To]: ...

else:
    bound = monad.bound(map)(join)


bind = function.flip(bound)


if TYPE_CHECKING:

    @curry
    @curry
    def compose[From, Intermediate, To](value: From, first: Callable[[From], List[Intermediate]], second: Callable[[Intermediate], List[To]]) -> List[To]: ...

else:
    compose = monad.compose(bind)


if TYPE_CHECKING:

    def guard(bool: bool) -> List[None]: ...

else:
    guard = monad.guard(neutral)(identity)


@curry
def filter[T](list: List[T], predicate: Predicate[T]) -> List[T]:
    return [value for value in list if predicate(value)]


@curry
def sort[T](list: List[T], order: Order[T]) -> List[T]:
    return sorted(list, key=felis.order.rich_comparison(order))


@curry
def range(stop: int, start: int) -> List[int]:
    return list(builtins.range(start, stop))
