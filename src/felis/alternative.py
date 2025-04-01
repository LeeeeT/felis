from collections.abc import Callable
from typing import Any, Final

import felis.applicative
import felis.monoid
from felis.applicative import Applicative
from felis.currying import curry
from felis.functor import Functor
from felis.monoid import Monoid
from felis.semigroup import Semigroup

__all__ = [
    "Alternative",
    "add_to",
    "applicative",
    "apply_to",
    "by_map",
    "discard_after",
    "discard_before",
    "functor",
    "guard",
    "lift",
    "map_by",
    "monoid",
    "neutral",
    "pure",
    "semigroup",
    "take_after",
    "take_before",
    "to_add",
    "to_apply",
    "when",
]


# [A : * -> *] ->
# ([T : *] -> Monoid (A T)) ->
# Applicative A ->
# Alternative A
class Alternative:
    def __init__(self, monoid: Monoid[Any], applicative: Applicative):
        self.monoid: Final = monoid
        self.applicative: Final = applicative


# [A : * -> *] -> Alternative A -> [T : *] -> Monoid (A T)
def monoid(instance: Alternative) -> Monoid[Any]:
    return instance.monoid


# [A : * -> *] -> Alternative A -> [T : *] -> Semigroup (A T)
def semigroup(instance: Alternative) -> Semigroup[Any]:
    return felis.monoid.semigroup(monoid(instance))


# [A : * -> *] -> Alternative A -> [T : *] -> A T -> A T -> A T
def to_add(instance: Alternative) -> Callable[[Any], Callable[[Any], Any]]:
    return felis.monoid.to_add(monoid(instance))


# [A : * -> *] -> Alternative A -> [T : *] -> A T -> A T -> A T
def add_to(instance: Alternative) -> Callable[[Any], Callable[[Any], Any]]:
    return felis.monoid.add_to(monoid(instance))


# [A : * -> *] -> Alternative A -> [T : *] -> A T
def neutral(instance: Alternative) -> Any:
    return felis.monoid.neutral(monoid(instance))


# [A : * -> *] -> Alternative A -> Applicative A
def applicative(instance: Alternative) -> Applicative:
    return instance.applicative


# [A : * -> *] -> Alternative A -> Functor A
def functor(instance: Alternative) -> Functor:
    return felis.applicative.functor(applicative(instance))


# [A : * -> *] -> Alternative A -> [From : *] -> [To : *] -> (From -> To) -> A From -> A To
def map_by(instance: Alternative) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
    return felis.applicative.map_by(applicative(instance))


# [A : * -> *] -> Alternative A -> [From : *] -> A From -> [To : *] -> (From -> To) -> A To
def by_map(instance: Alternative) -> Callable[[Any], Callable[[Callable[[Any], Any]], Any]]:
    return felis.applicative.by_map(applicative(instance))


# [A : * -> *] -> Alternative A -> [T : *] -> T -> A T
def pure(instance: Alternative) -> Callable[[Any], Any]:
    return felis.applicative.pure(applicative(instance))


# [A : * -> *] -> Alternative A -> [From : *] -> [To : *] -> A (From -> To) -> A From -> A To
def to_apply(instance: Alternative) -> Callable[[Any], Callable[[Any], Any]]:
    return felis.applicative.to_apply(applicative(instance))


# [A : * -> *] -> Alternative A -> [From : *] -> A From -> [To : *] -> A (From -> To) -> A To
def apply_to(instance: Alternative) -> Callable[[Any], Callable[[Any], Any]]:
    return felis.applicative.apply_to(applicative(instance))


# [A : * -> *] -> Alternative A -> [First : *] -> [Second : *] -> [Result : *] -> (First -> Second -> Result) -> A First -> A Second -> A Result
def lift(instance: Alternative) -> Callable[[Callable[[Any], Callable[[Any], Any]]], Callable[[Any], Callable[[Any], Any]]]:
    return felis.applicative.lift(applicative(instance))


# [A : * -> *] -> Alternative A -> [First : *] -> A First -> [Second : *] -> A Second -> A Second
def take_after(instance: Alternative) -> Callable[[Any], Callable[[Any], Any]]:
    return felis.applicative.take_after(applicative(instance))


# [A : * -> *] -> Alternative A -> [Second : *] -> A Second -> [First : *] -> A First -> A Second
def discard_before(instance: Alternative) -> Callable[[Any], Callable[[Any], Any]]:
    return felis.applicative.discard_before(applicative(instance))


# [A : * -> *] -> Alternative A -> [First : *] -> A First -> [Second : *] -> A Second -> A First
def discard_after(instance: Alternative) -> Callable[[Any], Callable[[Any], Any]]:
    return felis.applicative.discard_after(applicative(instance))


# [A : * -> *] -> Alternative A -> [Second : *] -> A Second -> [First : *] -> A First -> A First
def take_before(instance: Alternative) -> Callable[[Any], Callable[[Any], Any]]:
    return felis.applicative.take_before(applicative(instance))


# [A : * -> *] -> Alternative A -> bool -> A None -> A None
def when(instance: Alternative) -> Callable[[bool], Callable[[Any], Any]]:
    return felis.applicative.when(applicative(instance))


# [A : * -> *] -> Alternative A -> bool -> A None
@curry
def guard(bool: bool, instance: Alternative) -> Any:
    return pure(instance)(None) if bool else neutral(instance)
