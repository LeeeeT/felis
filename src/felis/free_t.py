from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Final

from felis.currying import curry, flip

__all__ = ["Bind", "Free", "Pure", "apply", "join", "map_by", "pure"]


class Pure[T]:
    __match_args__ = ("value",)

    def __init__(self, value: T):
        self.value: Final = value


# [F : * -> *] -> [T : *] -> F (Free F T) -> Free F T
class Bind:
    __match_args__ = ("f_free_value",)

    def __init__(self, f_free_value: Any):
        self.f_free_value: Final = f_free_value


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
            return Bind(f_map_by(flip(apply(f_map_by))(free_value))(f_free_function))


# [F : * -> *] -> ([From : *] -> [To : *] -> (From -> To) -> F From -> F To) -> [T : *] -> Free F (Free F T) -> Free F T
@curry
def join[T](free_free_value: Free[Free[T]], f_map_by: Callable[[Callable[[Any], Any]], Callable[[Any], Any]]) -> Free[T]:
    match free_free_value:
        case Pure(free_value):
            return free_value
        case Bind(f_free_free_value):
            return Bind(f_map_by(join(f_map_by))(f_free_free_value))
