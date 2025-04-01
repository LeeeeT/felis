from collections.abc import Callable
from typing import Any, Final

import felis.applicative
from felis.applicative import Applicative
from felis.currying import curry, flip
from felis.functor import Functor

__all__ = [
    "Monad",
    "applicative",
    "apply_to",
    "bind_to",
    "by_map",
    "compose_after",
    "compose_before",
    "discard_after",
    "discard_before",
    "functor",
    "join",
    "lift",
    "map_by",
    "pure",
    "take_after",
    "take_before",
    "to_apply",
    "to_bind",
    "when",
]


# [M : * -> *] ->
# Applicative M ->
# ([T : *] -> M (M T) -> M T) ->
# Monad A
class Monad:
    def __init__(self, applicative: Applicative, join: Callable[[Any], Any]):
        self.applicative: Final = applicative
        self.join: Final = join


# [M : * -> *] -> Monad M -> Applicative M
def applicative(instance: Monad) -> Applicative:
    return instance.applicative


# [M : * -> *] -> Monad M -> Functor M
def functor(instance: Monad) -> Functor:
    return felis.applicative.functor(applicative(instance))


# [M : * -> *] -> Monad M -> [From : *] -> [To : *] -> (From -> To) -> M From -> M To
def map_by(instance: Monad) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
    return felis.applicative.map_by(applicative(instance))


# [M : * -> *] -> Monad M -> [From : *] -> M From -> [To : *] -> (From -> To) -> M To
def by_map(instance: Monad) -> Callable[[Any], Callable[[Callable[[Any], Any]], Any]]:
    return felis.applicative.by_map(applicative(instance))


# [M : * -> *] -> Monad M -> [T : *] -> T -> M T
def pure(instance: Monad) -> Callable[[Any], Any]:
    return felis.applicative.pure(applicative(instance))


# [M : * -> *] -> Monad M -> [From : *] -> [To : *] -> M (From -> To) -> M From -> M To
def to_apply(instance: Monad) -> Callable[[Any], Callable[[Any], Any]]:
    return felis.applicative.to_apply(applicative(instance))


# [M : * -> *] -> Monad M -> [From : *] -> M From -> [To : *] -> M (From -> To) -> M To
def apply_to(instance: Monad) -> Callable[[Any], Callable[[Any], Any]]:
    return felis.applicative.apply_to(applicative(instance))


# [M : * -> *] -> Monad M -> [First : *] -> [Second : *] -> [Result : *] -> (First -> Second -> Result) -> M First -> M Second -> M Result
def lift(instance: Monad) -> Callable[[Callable[[Any], Callable[[Any], Any]]], Callable[[Any], Callable[[Any], Any]]]:
    return felis.applicative.lift(applicative(instance))


# [M : * -> *] -> Monad M -> [First : *] -> M First -> [Second : *] -> M Second -> M Second
def take_after(instance: Monad) -> Callable[[Any], Callable[[Any], Any]]:
    return felis.applicative.take_after(applicative(instance))


# [M : * -> *] -> Monad M -> [Second : *] -> M Second -> [First : *] -> M First -> M Second
def discard_before(instance: Monad) -> Callable[[Any], Callable[[Any], Any]]:
    return felis.applicative.discard_before(applicative(instance))


# [M : * -> *] -> Monad M -> [First : *] -> M First -> [Second : *] -> M Second -> M First
def discard_after(instance: Monad) -> Callable[[Any], Callable[[Any], Any]]:
    return felis.applicative.discard_after(applicative(instance))


# [M : * -> *] -> Monad M -> [Second : *] -> M Second -> [First : *] -> M First -> M First
def take_before(instance: Monad) -> Callable[[Any], Callable[[Any], Any]]:
    return felis.applicative.take_before(applicative(instance))


# [M : * -> *] -> Monad M -> bool -> M None -> M None
def when(instance: Monad) -> Callable[[bool], Callable[[Any], Any]]:
    return felis.applicative.when(applicative(instance))


# [M : * -> *] -> Monad M -> [T : *] -> M (M T) -> M T
def join(instance: Monad) -> Callable[[Any], Any]:
    return instance.join


# [M : * -> *] -> Monad M -> [From : *] -> [To : *] -> (From -> M To) -> M From -> M To
@curry
@curry
def bind_to(m_value: Any, function: Callable[[Any], Any], instance: Monad) -> Any:
    return join(instance)(map_by(instance)(function)(m_value))


# [M : * -> *] -> Monad M -> [From : *] -> M From -> [To : *] -> (From -> M To) -> M To
def to_bind(instance: Monad) -> Callable[[Any], Callable[[Callable[[Any], Any]], Any]]:
    return flip(bind_to(instance))


# [M : * -> *] -> Monad M -> [From : *] -> [Intermediate : *] -> (From -> M Intermediate) -> [To : *] -> (Intermediate -> M To) -> From -> M To
@curry
@curry
@curry
def compose_after[From](value: From, second: Callable[[Any], Any], first: Callable[[From], Any], instance: Monad) -> Any:
    return to_bind(instance)(first(value))(second)


# [M : * -> *] -> Monad M -> [Intermediate : *] -> [To : *] -> (Intermediate -> M To) -> [From : *] -> (From -> M Intermediate) -> From -> M To
def compose_before(instance: Monad) -> Callable[[Callable[[Any], Any]], Callable[[Callable[[Any], Any]], Callable[[Any], Any]]]:
    return flip(compose_after(instance))
