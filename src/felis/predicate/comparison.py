from felis.currying import curry
from felis.typing import SupportsRichComparison

__all__ = ["equal_to", "greater_than", "greater_than_or_equal_to", "less_than", "less_than_or_equal_to", "not_equal_to"]


@curry
def less_than[T: SupportsRichComparison](first: T, second: T) -> bool:
    return first < second


@curry
def less_than_or_equal_to[T: SupportsRichComparison](first: T, second: T) -> bool:
    return first <= second


@curry
def equal_to[T: SupportsRichComparison](first: T, second: T) -> bool:
    return first == second


@curry
def not_equal_to[T: SupportsRichComparison](first: T, second: T) -> bool:
    return first != second


@curry
def greater_than_or_equal_to[T: SupportsRichComparison](first: T, second: T) -> bool:
    return first >= second


@curry
def greater_than[T: SupportsRichComparison](first: T, second: T) -> bool:
    return first > second
