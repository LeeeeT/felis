from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Final, Self

import felis.functor
import felis.semigroup
from felis import function, ordering
from felis.currying import curry
from felis.functor import Functor
from felis.monoid import Monoid
from felis.ordering import Ordering
from felis.semigroup import Semigroup
from felis.typing import SupportsRichComparison

__all__ = [
    "Order",
    "add_to",
    "add_to",
    "better_than",
    "by_map",
    "different_from",
    "dunder",
    "functor",
    "map_by",
    "monoid",
    "neutral",
    "not_better_than",
    "not_worse_than",
    "reverse",
    "rich_comparison",
    "same_as",
    "same_as_or_better_than",
    "same_as_or_worse_than",
    "semigroup",
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


if TYPE_CHECKING:

    @curry
    def to_add[T](augend: Order[T], addend: Order[T]) -> Order[T]: ...

else:
    to_add = function.lift(ordering.to_add)


# [T : *] -> Semigroup (Order T)
semigroup: Semigroup[Order[Any]] = Semigroup(to_add)


if TYPE_CHECKING:

    @curry
    def add_to[T](addend: Order[T], augend: Order[T]) -> Order[T]: ...

else:
    add_to = felis.semigroup.add_to(semigroup)


neutral = function.pure(function.pure(ordering.neutral))


# [T : *] -> Monoid (Order T)
monoid = Monoid(semigroup, neutral)


@curry
@curry
@curry
def map_by[From, To](first: To, second: To, order: Order[From], function: Callable[[To], From]) -> Ordering:
    return order(function(second))(function(first))


# Functor Order
functor = Functor(map_by)


if TYPE_CHECKING:

    @curry
    def by_map[From, To](function: Callable[[To], From], order: Order[From]) -> Order[To]: ...

else:
    by_map = felis.functor.by_map(functor)


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

        def __hash__(self) -> int:
            return hash(self.value)

    return RichComparison
