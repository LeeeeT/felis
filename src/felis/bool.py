from felis import function
from felis.currying import curry

__all__ = ["Bool", "both_and", "different_from", "either_or", "negate", "same_as"]


Bool = bool


@curry
def both_and(first: bool, second: bool) -> bool:
    return first and second


@curry
def either_or(first: bool, second: bool) -> bool:
    return first or second


def negate(value: bool) -> bool:
    return not value


@curry
def same_as(first: bool, second: bool) -> bool:
    return first is second


different_from = function.map_by2(negate)(same_as)
