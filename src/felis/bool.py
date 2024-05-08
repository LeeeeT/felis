from felis import identity
from felis.currying import curry

__all__ = ["both", "either", "negate", "same", "different"]


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


different = identity.compose2(negate)(same)
