import builtins
from dataclasses import dataclass

from felis import function
from felis.currying import curry

__all__ = ["Bool", "No", "Yes", "from_builtin", "to_builtin", "both", "either", "negate", "same", "different"]


type Bool = No | Yes


@dataclass(frozen=True)
class No:
    pass


@dataclass(frozen=True)
class Yes:
    pass


def from_builtin(bool: builtins.bool) -> Bool:
    return Yes() if bool else No()


def to_builtin(bool: Bool) -> builtins.bool:
    match bool:
        case No():
            return False
        case Yes():
            return True


@curry
def both(first: Bool, second: Bool) -> Bool:
    match first:
        case No():
            return No()
        case Yes():
            return second


@curry
def either(first: Bool, second: Bool) -> Bool:
    match first:
        case No():
            return second
        case Yes():
            return Yes()


def negate(value: Bool) -> Bool:
    match value:
        case No():
            return Yes()
        case Yes():
            return No()


@curry
def same(first: Bool, second: Bool) -> Bool:
    match first, second:
        case No(), No():
            return Yes()
        case Yes(), Yes():
            return Yes()
        case _, _:
            return No()


different = function.map2(negate)(same)
