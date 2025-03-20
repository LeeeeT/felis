import builtins
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import felis.identity
import felis.order
from felis import applicative, function, list_t, monad
from felis.currying import curry
from felis.list_t import List
from felis.order import Order
from felis.predicate import Predicate

__all__ = [
    "List",
    "apply",
    "bind",
    "bind_to",
    "compose",
    "discard_after",
    "discard_before",
    "filter_by",
    "fold",
    "guard",
    "join",
    "lift2",
    "map_by",
    "neutral",
    "pure",
    "range_to_from",
    "sort_by",
    "take_after",
    "take_before",
    "to_add",
    "to_append",
    "traverse",
    "when",
]


# [T : *] -> List T
neutral: list[Any] = []


@curry
def to_append[T](list: List[T], value: T) -> List[T]:
    return [*list, value]


@curry
def to_add[T](augend: List[T], addend: List[T]) -> List[T]:
    return augend + addend


@curry
def map_by[From, To](list_value: List[From], function: Callable[[From], To]) -> List[To]:
    return [function(value) for value in list_value]


def pure[T](value: T) -> List[T]:
    return [value]


if TYPE_CHECKING:

    @curry
    def apply[From, To](list_value: List[From], list_function: List[Callable[[From], To]]) -> List[To]: ...

else:
    apply = list_t.apply(felis.identity.pure)(felis.identity.bind)


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[First, Second, Result](second: List[Second], first: List[First], function: Callable[[First], Callable[[Second], Result]]) -> List[Result]: ...

else:
    lift2 = applicative.lift2(map_by)(apply)


take_after = lift2(function.flip(function.pure))


discard_after = lift2(function.pure)


take_before = function.flip(discard_after)


discard_before = function.flip(take_after)


if TYPE_CHECKING:

    @curry
    def when(list_none: List[None], bool: bool) -> List[None]: ...

else:
    when = applicative.when(pure)


@curry
@curry
def fold[A, T](list_value: List[T], function: Callable[[T], Callable[[A], A]], accumulator: A) -> A:
    for value in list_value:
        accumulator = function(value)(accumulator)
    return accumulator


@curry
@curry
def fold_right[A, T](list_value: List[T], function: Callable[[T], Callable[[A], A]], accumulator: A) -> A:
    if list_value:
        return function(list_value[0])(fold_right(accumulator)(function)(list_value[1:]))
    return accumulator


@curry
@curry
def fold_left[A, T](list_value: List[T], function: Callable[[A], Callable[[T], A]], accumulator: A) -> A:
    if list_value:
        return fold_left(function(accumulator)(list_value[0]))(function)(list_value[1:])
    return accumulator


# [A : * -> *] ->
# ([From : *] -> [To : *] -> (From -> To) -> A From -> A To) ->
# ([T : *] -> T -> A T) ->
# [From : *] -> [To : *] -> (From -> A To) -> List From -> A (List To)
@curry
@curry
def traverse[From](
    function: Callable[[From], Any],
    a_lift2: Callable[[Callable[[Any], Callable[[Any], Any]]], Callable[[Any], Callable[[Any], Any]]],
    a_identity: Callable[[Any], Any],
) -> Callable[[List[From]], Any]:
    return fold(a_identity(neutral))(felis.identity.compose(a_lift2(to_append))(function))


if TYPE_CHECKING:

    def join[T](list_list_value: List[List[T]]) -> List[T]: ...

else:
    join = list_t.join(felis.identity.pure)(felis.identity.bind)


if TYPE_CHECKING:

    @curry
    def bind_to[From, To](list_value: List[From], function: Callable[[From], List[To]]) -> List[To]: ...

else:
    bind_to = monad.bind_to(map_by)(join)


bind = function.flip(bind_to)


if TYPE_CHECKING:

    @curry
    @curry
    def compose[From, Intermediate, To](value: From, first: Callable[[From], List[Intermediate]], second: Callable[[Intermediate], List[To]]) -> List[To]: ...

else:
    compose = monad.compose(bind)


if TYPE_CHECKING:

    def guard(bool: bool) -> List[None]: ...

else:
    guard = monad.guard(neutral)(pure)


@curry
def filter_by[T](list: List[T], predicate: Predicate[T]) -> List[T]:
    return [value for value in list if predicate(value)]


@curry
def sort_by[T](list: List[T], order: Order[T]) -> List[T]:
    return sorted(list, key=felis.order.rich_comparison(order))


@curry
def range_to_from(stop: int, start: int) -> List[int]:
    return list(builtins.range(start, stop))
