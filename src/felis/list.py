from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import felis.identity
import felis.order
from felis import monad
from felis.currying import curry
from felis.order import Order
from felis.predicate import Predicate

__all__ = ["neutral", "add", "identity", "fold", "map", "join", "bind", "compose", "then", "filter", "sort"]


neutral: list[Any] = []


@curry
def append[T](list: list[T], value: T) -> list[T]:
    return [*list, value]


@curry
def add[T](augend: list[T], addend: list[T]) -> list[T]:
    return augend + addend


def identity[T](value: T) -> list[T]:
    return [value]


@curry
@curry
def fold[A, T](list: list[T], function: Callable[[T], Callable[[A], A]], accumulator: A) -> A:
    for value in list:
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


@curry
def map[From, To](list_value: list[From], function: Callable[[From], To]) -> list[To]:
    return [function(value) for value in list_value]


if TYPE_CHECKING:

    def join[T](list_list_value: list[list[T]], /) -> list[T]: ...


join = fold(neutral)(add)


bind = monad.bind(map)(join)


compose = monad.compose(bind)


then = monad.then(bind)


@curry
def filter[T](list: list[T], predicate: Predicate[T]) -> list[T]:
    return [value for value in list if predicate(value)]


@curry
def sort[T](list: list[T], order: Order[T]) -> list[T]:
    return sorted(list, key=felis.order.rich_comparison(order))
