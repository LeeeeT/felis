from felis.currying import curry
from felis.typing import SupportsRichComparison

__all__ = ["equal", "greater", "greater_or_equal", "less", "less_or_equal", "not_equal"]


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
