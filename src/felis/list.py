from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import felis.order
from felis import monad
from felis.currying import curry
from felis.order import Order
from felis.predicate import Predicate

__all__ = ["neutral", "add", "identity", "fold", "map", "join", "bind", "compose", "then", "filter", "sort"]


neutral: list[Any] = []


@curry
def add[T](augend: list[T], addend: list[T]) -> list[T]:
    return augend + addend


def identity[T](value: T) -> list[T]:
    return [value]


@curry
@curry
def fold[T](list: list[T], add: Callable[[T], Callable[[T], T]], neutral: T) -> T:
    match list:
        case [head, *tail]:
            return add(fold(neutral)(add)(tail))(head)
        case _:
            return neutral


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
