from collections.abc import Callable
from dataclasses import dataclass
from typing import Self

from felis import identity, ordering
from felis.currying import curry
from felis.ordering import Ordering
from felis.typing import SupportsRichComparison

__all__ = ["Order", "worse", "not_worse", "same", "different", "better", "not_better", "reverse", "neutral", "add", "map", "dunder", "rich_comparison"]


type Order[T] = Callable[[T], Callable[[T], Ordering]]


worse = identity.compose2(ordering.worse)


not_worse = identity.compose2(ordering.not_worse)


same = identity.compose2(ordering.same)


different = identity.compose2(ordering.different)


better = identity.compose2(ordering.better)


not_better = identity.compose2(ordering.not_better)


reverse = identity.compose2(ordering.reverse)


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

        def __eq__(self, other: object, /) -> bool:
            if isinstance(other, RichComparison):
                return same(order)(other.value)(self.value)
            return NotImplemented

        def __ne__(self, other: object, /) -> bool:
            if isinstance(other, RichComparison):
                return different(order)(other.value)(self.value)
            return NotImplemented

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
