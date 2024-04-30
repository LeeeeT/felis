from collections.abc import Callable

import felis.order
from felis import Order, monad
from felis.currying import curry

__all__ = ["List", "identity", "map", "join", "bind", "compose", "then", "fold_left"]


type List[T] = list[T]


def identity[T](value: T) -> List[T]:
    return [value]


@curry
def map[From, To](list_value: List[From], function: Callable[[From], To]) -> List[To]:
    return [function(value) for value in list_value]


def join[T](list_list_value: List[List[T]]) -> List[T]:
    return [value for list_value in list_list_value for value in list_value]


bind = monad.bind(map)(join)


compose = monad.compose(bind)


then = monad.then(bind)


@curry
@curry
def fold_left[T](list: List[T], empty: T, add: Callable[[T], Callable[[T], T]]) -> T:
    result = empty
    for value in list:
        result = add(value)(result)
    return result


@curry
def filter[T](list: list[T], condition: Callable[[T], bool]) -> list[T]:
    return [value for value in list if condition(value)]


@curry
def sort[T](list: list[T], order: Order[T]) -> list[T]:
    match list:
        case [head, *tail]:
            bad = filter(felis.order.worse(order)(head))(tail)
            good = filter(felis.order.not_worse(order)(head))(tail)
            return [*sort(order)(bad), head, *sort(order)(good)]
        case _:
            return []
