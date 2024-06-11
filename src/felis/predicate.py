from collections.abc import Callable

import felis.bool
from felis import function, identity
from felis.currying import curry
from felis.typing import SupportsRichComparison

__all__ = [
    "Predicate",
    "both",
    "either",
    "negate",
    "same",
    "different",
    "truthy",
    "falsey",
    "less",
    "less_or_equal",
    "equal",
    "not_equal",
    "greater_or_equal",
    "greater",
]


type Predicate[T] = Callable[[T], bool]


both = function.add(felis.bool.both)


either = function.add(felis.bool.either)


negate = identity.compose(felis.bool.negate)


same = function.add(felis.bool.same)


different = function.add(felis.bool.different)


def truthy(value: object) -> bool:
    return bool(value)


falsey = negate(truthy)


@curry
def less[T: SupportsRichComparison](first: T, second: T) -> bool:
    return first < second


@curry
def less_or_equal[T: SupportsRichComparison](first: T, second: T) -> bool:
    return first <= second


@curry
def equal[T: SupportsRichComparison](first: T, second: T) -> bool:
    return first == second


@curry
def not_equal[T: SupportsRichComparison](first: T, second: T) -> bool:
    return first != second


@curry
def greater_or_equal[T: SupportsRichComparison](first: T, second: T) -> bool:
    return first >= second


@curry
def greater[T: SupportsRichComparison](first: T, second: T) -> bool:
    return first > second
