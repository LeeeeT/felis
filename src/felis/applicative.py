from collections.abc import Callable
from typing import Any, Final

import felis.functor
from felis.currying import curry, flip
from felis.functor import Functor

__all__ = [
    "Applicative",
    "apply_to",
    "by_map",
    "discard_after",
    "discard_before",
    "functor",
    "lift",
    "map_by",
    "pure",
    "take_after",
    "take_before",
    "to_apply",
    "when",
]


# [A : * -> *] ->
# Functor A ->
# ([T : *] -> T -> A T) ->
# ([From : *] -> [To : *] -> A (From -> To) -> A From -> A To) ->
# Applicative A
class Applicative:
    def __init__(self, functor: Functor, pure: Callable[[Any], Any], to_apply: Callable[[Any], Callable[[Any], Any]]):
        self.functor: Final = functor
        self.pure: Final = pure
        self.to_apply: Final = to_apply


# [A : * -> *] -> Applicative A -> Functor A
def functor(instance: Applicative) -> Functor:
    return instance.functor


# [A : * -> *] -> Applicative A -> [From : *] -> [To : *] -> (From -> To) -> A From -> A To
def map_by(instance: Applicative) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
    return felis.functor.map_by(functor(instance))


# [A : * -> *] -> Applicative A -> [From : *] -> A From -> [To : *] -> (From -> To) -> A To
def by_map(instance: Applicative) -> Callable[[Any], Callable[[Callable[[Any], Any]], Any]]:
    return felis.functor.by_map(functor(instance))


# [A : * -> *] -> Applicative A -> [T : *] -> T -> A T
def pure(instance: Applicative) -> Callable[[Any], Any]:
    return instance.pure


# [A : * -> *] -> Applicative A -> [From : *] -> [To : *] -> A (From -> To) -> A From -> A To
def to_apply(instance: Applicative) -> Callable[[Any], Callable[[Any], Any]]:
    return instance.to_apply


# [A : * -> *] -> Applicative A -> [From : *] -> A From -> [To : *] -> A (From -> To) -> A To
def apply_to(instance: Applicative) -> Callable[[Any], Callable[[Any], Any]]:
    return flip(to_apply(instance))


# [A : * -> *] -> Applicative A -> [First : *] -> [Second : *] -> [Result : *] -> (First -> Second -> Result) -> A First -> A Second -> A Result
@curry
@curry
@curry
def lift(second: Any, first: Any, function: Callable[[Any], Callable[[Any], Any]], instance: Applicative) -> Any:
    return to_apply(instance)(map_by(instance)(function)(first))(second)


# [A : * -> *] -> Applicative A -> [First : *] -> A First -> [Second : *] -> A Second -> A Second
def take_after(instance: Applicative) -> Callable[[Any], Callable[[Any], Any]]:
    return lift(instance)(lambda first: lambda second: second)


# [A : * -> *] -> Applicative A -> [Second : *] -> A Second -> [First : *] -> A First -> A Second
def discard_before(instance: Applicative) -> Callable[[Any], Callable[[Any], Any]]:
    return flip(take_after(instance))


# [A : * -> *] -> Applicative A -> [First : *] -> A First -> [Second : *] -> A Second -> A First
def discard_after(instance: Applicative) -> Callable[[Any], Callable[[Any], Any]]:
    return lift(instance)(lambda first: lambda second: first)


# [A : * -> *] -> Applicative A -> [Second : *] -> A Second -> [First : *] -> A First -> A First
def take_before(instance: Applicative) -> Callable[[Any], Callable[[Any], Any]]:
    return flip(discard_after(instance))


# [A : * -> *] -> Applicative A -> bool -> A None -> A None
@curry
@curry
def when(a_none: Any, bool: bool, instance: Applicative) -> Any:
    return a_none if bool else pure(instance)(None)
