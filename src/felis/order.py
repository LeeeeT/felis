from collections.abc import Callable
from typing import Final, Self

from felis import function, ordering
from felis.currying import curry, flip
from felis.ordering import Ordering
from felis.typing import SupportsRichComparison

__all__ = [
    "Order",
    "add_to",
    "better_than",
    "different_from",
    "dunder",
    "map_by",
    "neutral",
    "not_better_than",
    "not_worse_than",
    "reverse",
    "rich_comparison",
    "same_as",
    "same_as_or_better_than",
    "same_as_or_worse_than",
    "to_add",
    "worse_than",
]


type Order[T] = Callable[[T], Callable[[T], Ordering]]


worse_than = function.map_by2(ordering.worse)


same_as_or_better_than = not_worse_than = function.map_by2(ordering.not_worse)


same_as = function.map_by2(ordering.same)


different_from = function.map_by2(ordering.different)


better_than = function.map_by2(ordering.better)


same_as_or_worse_than = not_better_than = function.map_by2(ordering.not_better)


reverse = function.map_by2(ordering.reverse)


neutral = function.pure(ordering.neutral)


to_add = function.lift(ordering.to_add)


add_to = flip(to_add)


def map_by[From, To](first: To, second: To, order: Order[From], function: Callable[[To], From]) -> Ordering:
    return order(function(second))(function(first))


@curry
def dunder[T: SupportsRichComparison](first: T, second: T) -> Ordering:
    if first > second:
        return ordering.Better()
    if first < second:
        return ordering.Worse()
    return ordering.Same()


def rich_comparison[T](order: Order[T]) -> Callable[[T], SupportsRichComparison]:
    class RichComparison:
        def __init__(self, value: T):
            self.value: Final = value

        def __eq__(self, other: object, /) -> bool:
            if isinstance(other, RichComparison):
                return same_as(order)(other.value)(self.value)
            return NotImplemented

        def __ne__(self, other: object, /) -> bool:
            if isinstance(other, RichComparison):
                return different_from(order)(other.value)(self.value)
            return NotImplemented

        def __lt__(self, other: Self, /) -> bool:
            if isinstance(other, RichComparison):  # pyright: ignore[reportUnnecessaryIsInstance]
                return worse_than(order)(other.value)(self.value)
            return NotImplemented

        def __gt__(self, other: Self, /) -> bool:
            if isinstance(other, RichComparison):  # pyright: ignore[reportUnnecessaryIsInstance]
                return better_than(order)(other.value)(self.value)
            return NotImplemented

        def __le__(self, other: Self, /) -> bool:
            if isinstance(other, RichComparison):  # pyright: ignore[reportUnnecessaryIsInstance]
                return same_as_or_worse_than(order)(other.value)(self.value)
            return NotImplemented

        def __ge__(self, other: Self, /) -> bool:
            if isinstance(other, RichComparison):  # pyright: ignore[reportUnnecessaryIsInstance]
                return same_as_or_better_than(order)(other.value)(self.value)
            return NotImplemented

    return RichComparison
