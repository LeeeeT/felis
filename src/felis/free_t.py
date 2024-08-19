from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import felis.function
from felis.currying import curry

__all__ = ["Pure", "Bind", "Free", "map", "identity", "apply", "join"]


@dataclass(frozen=True)
class Pure[T]:
    value: T


# [F : Type -> Type] -> [T : Type] -> F (Free F T) -> Free F T
@dataclass(frozen=True)
class Bind:
    f_free_value: Any


type Free[T] = Pure[T] | Bind


# [F : Type -> Type] ->
# ([From : Type] -> [To : Type] -> (From -> To) -> F From -> F To) ->
# [From : Type] -> [To : Type] -> (From -> To) -> Free F From -> Free F To
@curry
@curry
def map[From, To](free_value: Free[From], function: Callable[[From], To], f_map: Callable[[Any], Callable[[Any], Any]]) -> Free[To]:
    match free_value:
        case Pure(value):
            return Pure(function(value))
        case Bind(f_free_value):
            return Bind(f_map(map(f_map)(function))(f_free_value))


identity = Pure


# [F : Type -> Type] ->
# ([From : Type] -> [To : Type] -> (From -> To) -> F From -> F To) ->
# [From : Type] -> [To : Type] -> Free F (From -> To) -> Free F From -> Free F To
@curry
@curry
def apply[From, To](free_value: Free[From], free_function: Free[Callable[[From], To]], f_map: Callable[[Any], Callable[[Any], Any]]) -> Free[To]:
    match free_function:
        case Pure(function):
            return map(f_map)(function)(free_value)
        case Bind(f_free_function):
            return Bind(f_map(felis.function.flip(apply(f_map))(free_value))(f_free_function))


# [F : Type -> Type] -> ([From : Type] -> [To : Type] -> (From -> To) -> F From -> F To) -> [T : Type] -> Free F (Free F T) -> Free F T
@curry
def join[T](free_free_value: Free[Free[T]], f_map: Callable[[Any], Callable[[Any], Any]]) -> Free[T]:
    match free_free_value:
        case Pure(free_value):
            return free_value
        case Bind(f_free_free_value):
            return Bind(f_map(join(f_map))(f_free_free_value))
