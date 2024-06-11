from felis.currying import curry
from felis.typing import SupportsRichComparison

__all__ = ["less", "less_or_equal", "equal", "not_equal", "greater_or_equal", "greater"]


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
