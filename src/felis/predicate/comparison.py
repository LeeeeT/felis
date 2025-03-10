from felis.currying import curry
from felis.typing import SupportsRichComparison

__all__ = ["different", "greater_than", "greater_than_or_same_as", "less_than", "less_than_or_same_as", "same"]


@curry
def less_than[T: SupportsRichComparison](first: T, second: T) -> bool:
    return first < second


@curry
def less_than_or_same_as[T: SupportsRichComparison](first: T, second: T) -> bool:
    return first <= second


@curry
def same[T: SupportsRichComparison](first: T, second: T) -> bool:
    return first == second


@curry
def different[T: SupportsRichComparison](first: T, second: T) -> bool:
    return first != second


@curry
def greater_than_or_same_as[T: SupportsRichComparison](first: T, second: T) -> bool:
    return first >= second


@curry
def greater_than[T: SupportsRichComparison](first: T, second: T) -> bool:
    return first > second
