from felis.currying import curry
from felis.predicate import Predicate, both_and, comparison
from felis.typing import SupportsRichComparison

__all__ = ["to_exclusively_from_exclusively", "to_exclusively_from_inclusively", "to_inclusively_from_exclusively", "to_inclusively_from_inclusively"]


@curry
def to_inclusively_from_inclusively[T: SupportsRichComparison](maximum: T, minimum: T) -> Predicate[T]:
    return both_and(comparison.less_than_or_equal_to(maximum))(comparison.greater_than_or_equal_to(minimum))


@curry
def to_exclusively_from_inclusively[T: SupportsRichComparison](maximum: T, minimum: T) -> Predicate[T]:
    return both_and(comparison.less_than(maximum))(comparison.greater_than_or_equal_to(minimum))


@curry
def to_inclusively_from_exclusively[T: SupportsRichComparison](maximum: T, minimum: T) -> Predicate[T]:
    return both_and(comparison.less_than_or_equal_to(maximum))(comparison.greater_than(minimum))


@curry
def to_exclusively_from_exclusively[T: SupportsRichComparison](maximum: T, minimum: T) -> Predicate[T]:
    return both_and(comparison.less_than(maximum))(comparison.greater_than(minimum))
