from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Final

import felis.identity
from felis import applicative, monad
from felis.currying import curry, flip

__all__ = [
    "Bind",
    "BindT",
    "Free",
    "FreeT",
    "Pure",
    "PureT",
    "apply",
    "apply_t",
    "bind",
    "bind_to",
    "compose_after",
    "compose_before",
    "discard_after",
    "discard_before",
    "join",
    "join_t",
    "lift2",
    "map_by",
    "map_by_t",
    "pure",
    "take_after",
    "take_before",
    "when",
]


type FreeT[T] = PureT[T] | BindT[T]


class PureT[T]:
    __match_args__ = ("value",)

    def __init__(self, value: T):
        self.value: Final = value


# [F : * -> *] -> [T : *] -> F (Free F T) -> Free F T
class BindT[T]:
    __match_args__ = ("f_free_value",)

    def __init__(self, f_free_value: Any):
        self.f_free_value: Final = f_free_value


type Free[T] = Pure[T] | Bind[T]


Pure = PureT


if TYPE_CHECKING:

    class Bind[T]:
        __match_args__ = ("f_free_value",)

        def __init__(self, f_free_value: Free[T]):
            self.f_free_value: Final = f_free_value

else:
    Bind = BindT


# [F : * -> *] ->
# ([From : *] -> [To : *] -> (From -> To) -> F From -> F To) ->
# [From : *] -> [To : *] -> (From -> To) -> Free F From -> Free F To
@curry
@curry
def map_by_t[From, To](free_value: FreeT[From], function: Callable[[From], To], f_map_by: Callable[[Callable[[Any], Any]], Callable[[Any], Any]]) -> FreeT[To]:
    match free_value:
        case PureT(value):
            return PureT(function(value))
        case BindT(f_free_value):
            return BindT(f_map_by(map_by_t(f_map_by)(function))(f_free_value))


if TYPE_CHECKING:
    # [F : * -> *] -> [T : *] -> T -> Free F T
    pure: FreeT[Any]
else:
    pure = PureT


if TYPE_CHECKING:

    @curry
    def map_by[From, To](free_value: Free[From], function: Callable[[From], To]) -> Free[To]: ...

else:
    map_by = map_by_t(felis.identity.map_by)


# [F : * -> *] ->
# ([From : *] -> [To : *] -> (From -> To) -> F From -> F To) ->
# [From : *] -> [To : *] -> Free F (From -> To) -> Free F From -> Free F To
@curry
@curry
def apply_t[From, To](
    free_value: FreeT[From],
    free_function: FreeT[Callable[[From], To]],
    f_map_by: Callable[[Callable[[Any], Any]], Callable[[Any], Any]],
) -> FreeT[To]:
    match free_function:
        case PureT(function):
            return map_by_t(f_map_by)(function)(free_value)
        case BindT(f_free_function):
            return BindT(f_map_by(flip(apply_t(f_map_by))(free_value))(f_free_function))


if TYPE_CHECKING:

    @curry
    def apply[From, To](free_value: Free[From], free_function: Free[Callable[[From], To]]) -> Free[To]: ...

else:
    apply = apply_t(felis.identity.map_by)


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[First, Second, Result](
        second: Free[Second],
        first: Free[First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> Free[Result]: ...

else:
    lift2 = applicative.lift2(map_by)(apply)


if TYPE_CHECKING:

    @curry
    def take_after[First, Second](second: Free[Second], first: Free[First]) -> Free[Second]: ...

else:
    take_after = applicative.take_after(lift2)


if TYPE_CHECKING:

    @curry
    def discard_before[First, Second](first: Free[First], second: Free[Second]) -> Free[Second]: ...

else:
    discard_before = applicative.discard_before(lift2)


if TYPE_CHECKING:

    @curry
    def discard_after[First, Second](second: Free[Second], first: Free[First]) -> Free[First]: ...

else:
    discard_after = applicative.discard_after(lift2)


if TYPE_CHECKING:

    @curry
    def take_before[First, Second](first: Free[First], second: Free[Second]) -> Free[First]: ...

else:
    take_before = applicative.take_before(lift2)


if TYPE_CHECKING:

    @curry
    def when(free_none: Free[None], bool: bool) -> Free[None]: ...

else:
    when = applicative.when(pure)


# [F : * -> *] -> ([From : *] -> [To : *] -> (From -> To) -> F From -> F To) -> [T : *] -> Free F (Free F T) -> Free F T
@curry
def join_t[T](free_free_value: FreeT[FreeT[T]], f_map_by: Callable[[Callable[[Any], Any]], Callable[[Any], Any]]) -> FreeT[T]:
    match free_free_value:
        case PureT(free_value):
            return free_value
        case BindT(f_free_free_value):
            return BindT(f_map_by(join_t(f_map_by))(f_free_free_value))


if TYPE_CHECKING:

    def join[T](free_free_value: Free[Free[T]], /) -> Free[T]: ...

else:
    join = join_t(felis.identity.map_by)


if TYPE_CHECKING:

    @curry
    def bind_to[From, To](free_value: Free[From], function: Callable[[From], Free[To]]) -> Free[To]: ...

else:
    bind_to = monad.bind_to(map_by)(join)


bind = flip(bind_to)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_after[From, Intermediate, To](
        value: From,
        second: Callable[[Intermediate], Free[To]],
        first: Callable[[From], Free[Intermediate]],
    ) -> Free[To]: ...

else:
    compose_after = monad.compose_after(bind)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_before[From, Intermediate, To](
        value: From,
        first: Callable[[From], Free[Intermediate]],
        second: Callable[[Intermediate], Free[To]],
    ) -> Free[To]: ...

else:
    compose_before = monad.compose_before(bind)
