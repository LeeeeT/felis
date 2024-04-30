from collections.abc import Callable

from felis import ordering
from felis.currying import curry
from felis.typing import SupportsRichComparison

__all__ = ["Order", "worse", "not_worse", "better", "not_better", "reverse", "neutral", "add", "map", "dunder"]


type Order[T] = Callable[[T], Callable[[T], ordering.Ordering]]


@curry
@curry
def worse[T](first: T, second: T, order: Order[T]) -> bool:
    return ordering.worse(order(second)(first))


@curry
@curry
def not_worse[T](first: T, second: T, order: Order[T]) -> bool:
    return ordering.not_worse(order(second)(first))


@curry
@curry
def better[T](first: T, second: T, order: Order[T]) -> bool:
    return ordering.better(order(second)(first))


@curry
@curry
def not_better[T](first: T, second: T, order: Order[T]) -> bool:
    return ordering.not_better(order(second)(first))


@curry
@curry
def reverse[T](first: T, second: T, order: Order[T]) -> ordering.Ordering:
    return ordering.reverse(order(second)(first))


@curry
def neutral[T](first: T, second: T) -> ordering.Ordering:
    return ordering.neutral


@curry
@curry
@curry
def add[T](first: T, second: T, order_first: Order[T], order_second: Order[T]) -> ordering.Ordering:
    return ordering.add(order_second(second)(first))(order_first(second)(first))


@curry
@curry
@curry
def map[From, To](first: To, second: To, order: Order[From], function: Callable[[To], From]) -> ordering.Ordering:
    return order(function(second))(function(first))


@curry
def dunder[T: SupportsRichComparison](first: T, second: T) -> ordering.Ordering:
    if first > second:
        return ordering.Better()
    if first < second:
        return ordering.Worse()
    return ordering.Equal()
