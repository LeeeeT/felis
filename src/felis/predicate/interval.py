from felis.currying import curry
from felis.predicate import Predicate, both, comparison
from felis.typing import SupportsRichComparison

__all__ = ["exclusive", "exclusive_inclusive", "inclusive", "inclusive_exclusive"]


@curry
def inclusive[T: SupportsRichComparison](maximum: T, minimum: T) -> Predicate[T]:
    return both(comparison.greater_than_or_same_as(minimum))(comparison.less_than_or_same_as(maximum))


@curry
def inclusive_exclusive[T: SupportsRichComparison](maximum: T, minimum: T) -> Predicate[T]:
    return both(comparison.greater_than_or_same_as(minimum))(comparison.less_than(maximum))


@curry
def exclusive_inclusive[T: SupportsRichComparison](maximum: T, minimum: T) -> Predicate[T]:
    return both(comparison.greater_than(minimum))(comparison.less_than_or_same_as(maximum))


@curry
def exclusive[T: SupportsRichComparison](maximum: T, minimum: T) -> Predicate[T]:
    return both(comparison.greater_than(minimum))(comparison.less_than(maximum))
