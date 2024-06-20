import builtins
from collections.abc import Callable
from typing import Any

import felis.identity
import felis.order
from felis import applicative, monad
from felis.currying import curry, uncurry
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
    "when",
    "fold",
    "traverse",
    "join",
    "bind",
    "compose",
    "then",
    "guard",
    "filter",
    "sort",
    "range",
]


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


lift2 = applicative.lift2(map)(apply)


when = applicative.when(identity)


@curry
@curry
def fold[A, T](list_value: list[T], function: Callable[[T], Callable[[A], A]], accumulator: A) -> A:
    for value in list_value:
        accumulator = function(value)(accumulator)
    return accumulator


@curry
@curry
def traverse[From, To, ATo, AListTo](
    function: Callable[[From], ATo],
    a_lift2: Callable[[Callable[[To], Callable[[list[To]], list[To]]]], Callable[[ATo], Callable[[AListTo], AListTo]]],
    a_identity: Callable[[list[To]], AListTo],
) -> Callable[[list[From]], AListTo]:
    return fold(a_identity(neutral))(felis.identity.compose(a_lift2(append))(function))


join = uncurry(fold)(add, neutral)


bind = monad.bind(map)(join)


compose = monad.compose(bind)


then = monad.then(bind)


guard = uncurry(monad.guard)(identity, neutral)


@curry
def filter[T](list: list[T], predicate: Predicate[T]) -> list[T]:
    return [value for value in list if predicate(value)]


@curry
def sort[T](list: list[T], order: Order[T]) -> list[T]:
    return sorted(list, key=felis.order.rich_comparison(order))


@curry
def range(stop: int, start: int) -> list[int]:
    return list(builtins.range(start, stop))
