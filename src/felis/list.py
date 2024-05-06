from collections.abc import Callable

import felis.order
from felis import monad
from felis.currying import curry
from felis.order import Order

__all__ = ["identity", "map", "join", "bind", "compose", "then", "fold_left"]


def identity[T](value: T) -> list[T]:
    return [value]


@curry
def map[From, To](list_value: list[From], function: Callable[[From], To]) -> list[To]:
    return [function(value) for value in list_value]


def join[T](list_list_value: list[list[T]]) -> list[T]:
    return [value for list_value in list_list_value for value in list_value]


bind = monad.bind(map)(join)


compose = monad.compose(bind)


then = monad.then(bind)


@curry
@curry
def fold_left[T](list: list[T], empty: T, add: Callable[[T], Callable[[T], T]]) -> T:
    result = empty
    for value in list:
        result = add(value)(result)
    return result


@curry
def filter[T](list: list[T], condition: Callable[[T], bool]) -> list[T]:
    return [value for value in list if condition(value)]


@curry
def sort[T](list: list[T], order: Order[T]) -> list[T]:
    return sorted(list, key=felis.order.rich_comparison(order))
