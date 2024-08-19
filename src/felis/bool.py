from felis import function
from felis.currying import curry

__all__ = ["Bool", "both", "either", "negate", "same", "different"]


Bool = bool


@curry
def both(first: bool, second: bool) -> bool:
    return first and second


@curry
def either(first: bool, second: bool) -> bool:
    return first or second


def negate(value: bool) -> bool:
    return not value


@curry
def same(first: bool, second: bool) -> bool:
    return first is second


different = function.map2(negate)(same)
