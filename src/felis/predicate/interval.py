from felis.currying import curry
from felis.predicate import Predicate, both, comparison
from felis.typing import SupportsRichComparison

__all__ = ["inclusive", "inclusive_exclusive", "exclusive_inclusive", "exclusive"]


@curry
def inclusive[T: SupportsRichComparison](maximum: T, minimum: T) -> Predicate[T]:
    return both(comparison.greater_or_equal(minimum))(comparison.less_or_equal(maximum))


@curry
def inclusive_exclusive[T: SupportsRichComparison](maximum: T, minimum: T) -> Predicate[T]:
    return both(comparison.greater_or_equal(minimum))(comparison.less(maximum))


@curry
def exclusive_inclusive[T: SupportsRichComparison](maximum: T, minimum: T) -> Predicate[T]:
    return both(comparison.greater(minimum))(comparison.less_or_equal(maximum))


@curry
def exclusive[T: SupportsRichComparison](maximum: T, minimum: T) -> Predicate[T]:
    return both(comparison.greater(minimum))(comparison.less(maximum))
