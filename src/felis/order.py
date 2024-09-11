from collections.abc import Callable
from dataclasses import dataclass
from typing import Self

from felis import function, ordering
from felis.currying import curry
from felis.ordering import Ordering
from felis.typing import SupportsRichComparison

__all__ = [
    "Order",
    "worse",
    "same_or_better",
    "not_worse",
    "same",
    "different",
    "better",
    "same_or_worse",
    "not_better",
    "reverse",
    "neutral",
    "add",
    "map",
    "dunder",
    "rich_comparison",
]


type Order[T] = Callable[[T], Callable[[T], Ordering]]


worse = function.map2(ordering.worse)


same_or_better = not_worse = function.map2(ordering.not_worse)


same = function.map2(ordering.same)


different = function.map2(ordering.different)


better = function.map2(ordering.better)


same_or_worse = not_better = function.map2(ordering.not_better)


reverse = function.map2(ordering.reverse)


neutral = function.neutral2(ordering.neutral)


add = function.add2(ordering.add)


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
            if isinstance(other, RichComparison):  # pyright: ignore[reportUnnecessaryIsInstance]
                return worse(order)(other.value)(self.value)
            return NotImplemented

        def __gt__(self, other: Self, /) -> bool:
            if isinstance(other, RichComparison):  # pyright: ignore[reportUnnecessaryIsInstance]
                return better(order)(other.value)(self.value)
            return NotImplemented

        def __le__(self, other: Self, /) -> bool:
            if isinstance(other, RichComparison):  # pyright: ignore[reportUnnecessaryIsInstance]
                return same_or_worse(order)(other.value)(self.value)
            return NotImplemented

        def __ge__(self, other: Self, /) -> bool:
            if isinstance(other, RichComparison):  # pyright: ignore[reportUnnecessaryIsInstance]
                return same_or_better(order)(other.value)(self.value)
            return NotImplemented

    return RichComparison
