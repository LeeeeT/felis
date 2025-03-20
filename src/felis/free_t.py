from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import felis.function
from felis.currying import curry

__all__ = ["Bind", "Free", "Pure", "apply", "join", "map_by", "pure"]


@dataclass(frozen=True)
class Pure[T]:
    value: T


# [F : * -> *] -> [T : *] -> F (Free F T) -> Free F T
@dataclass(frozen=True)
class Bind:
    f_free_value: Any


type Free[T] = Pure[T] | Bind


# [F : * -> *] ->
# ([From : *] -> [To : *] -> (From -> To) -> F From -> F To) ->
# [From : *] -> [To : *] -> (From -> To) -> Free F From -> Free F To
@curry
@curry
def map_by[From, To](free_value: Free[From], function: Callable[[From], To], f_map_by: Callable[[Callable[[Any], Any]], Callable[[Any], Any]]) -> Free[To]:
    match free_value:
        case Pure(value):
            return Pure(function(value))
        case Bind(f_free_value):
            return Bind(f_map_by(map_by(f_map_by)(function))(f_free_value))


if TYPE_CHECKING:
    # [F : * -> *] -> [T : *] -> T -> Free F T
    pure: Free[Any]
else:
    pure = Pure


# [F : * -> *] ->
# ([From : *] -> [To : *] -> (From -> To) -> F From -> F To) ->
# [From : *] -> [To : *] -> Free F (From -> To) -> Free F From -> Free F To
@curry
@curry
def apply[From, To](
    free_value: Free[From],
    free_function: Free[Callable[[From], To]],
    f_map_by: Callable[[Callable[[Any], Any]], Callable[[Any], Any]],
) -> Free[To]:
    match free_function:
        case Pure(function):
            return map_by(f_map_by)(function)(free_value)
        case Bind(f_free_function):
            return Bind(f_map_by(felis.function.flip(apply(f_map_by))(free_value))(f_free_function))


# [F : * -> *] -> ([From : *] -> [To : *] -> (From -> To) -> F From -> F To) -> [T : *] -> Free F (Free F T) -> Free F T
@curry
def join[T](free_free_value: Free[Free[T]], f_map_by: Callable[[Callable[[Any], Any]], Callable[[Any], Any]]) -> Free[T]:
    match free_free_value:
        case Pure(free_value):
            return free_value
        case Bind(f_free_free_value):
            return Bind(f_map_by(join(f_map_by))(f_free_free_value))
