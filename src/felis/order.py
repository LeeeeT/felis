from collections.abc import Callable
from dataclasses import dataclass
from typing import Self

from felis import ordering
from felis.currying import curry
from felis.ordering import Ordering
from felis.typing import SupportsRichComparison

__all__ = ["Order", "worse", "not_worse", "same", "different", "better", "not_better", "reverse", "neutral", "add", "map", "dunder", "rich_comparison"]


type Order[T] = Callable[[T], Callable[[T], Ordering]]


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
def same[T](first: T, second: T, order: Order[T]) -> bool:
    return ordering.same(order(second)(first))


@curry
@curry
def different[T](first: T, second: T, order: Order[T]) -> bool:
    return ordering.different(order(second)(first))


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
def reverse[T](first: T, second: T, order: Order[T]) -> Ordering:
    return ordering.reverse(order(second)(first))


@curry
def neutral[T](first: T, second: T) -> Ordering:
    return ordering.neutral


@curry
@curry
@curry
def add[T](first: T, second: T, order_first: Order[T], order_second: Order[T]) -> Ordering:
    return ordering.add(order_second(second)(first))(order_first(second)(first))


@curry
@curry
@curry
def map[From, To](first: To, second: To, order: Order[From], function: Callable[[To], From]) -> Ordering:
    return order(function(second))(function(first))


@curry
def dunder[T: SupportsRichComparison](first: T, second: T) -> Ordering:
    if first > second:
        return ordering.Better()
    if first < second:
        return ordering.Worse()
    return ordering.Same()


def rich_comparison[T](order: Order[T]) -> Callable[[T], SupportsRichComparison]:
    @dataclass(frozen=True)
    class RichComparison:
        value: T

        def __lt__(self, other: Self, /) -> bool:
            if isinstance(other, RichComparison):
                return worse(order)(other.value)(self.value)
            return NotImplemented

        def __gt__(self, other: Self, /) -> bool:
            if isinstance(other, RichComparison):
                return better(order)(other.value)(self.value)
            return NotImplemented

        def __le__(self, other: Self, /) -> bool:
            if isinstance(other, RichComparison):
                return not_better(order)(other.value)(self.value)
            return NotImplemented

        def __ge__(self, other: Self, /) -> bool:
            if isinstance(other, RichComparison):
                return not_worse(order)(other.value)(self.value)
            return NotImplemented

    return RichComparison
