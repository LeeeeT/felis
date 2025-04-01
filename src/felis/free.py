from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Final

import felis.applicative
import felis.functor
import felis.identity
import felis.monad
from felis.applicative import Applicative
from felis.currying import curry, flip
from felis.functor import Functor
from felis.monad import Monad

__all__ = [
    "Applicative",
    "Bind",
    "BindT",
    "Free",
    "FreeT",
    "Functor",
    "Monad",
    "Pure",
    "PureT",
    "applicative",
    "bind_to",
    "by_map",
    "compose_after",
    "compose_before",
    "discard_after",
    "discard_before",
    "functor",
    "join",
    "join_t",
    "lift",
    "map_by",
    "map_by_t",
    "monad",
    "pure",
    "pure_t",
    "take_after",
    "take_before",
    "to_apply",
    "to_apply_t",
    "to_bind",
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


# [F : * -> *] -> Functor F -> [From : *] -> [To : *] -> (From -> To) -> FreeT F From -> FreeT F To
@curry
@curry
def map_by_t[From, To](free_value: FreeT[From], function: Callable[[From], To], f: Functor) -> FreeT[To]:
    match free_value:
        case PureT(value):
            return PureT(function(value))
        case BindT(f_free_value):
            return BindT(felis.functor.map_by(f)(map_by_t(f)(function))(f_free_value))


if TYPE_CHECKING:

    @curry
    def map_by[From, To](free_value: Free[From], function: Callable[[From], To]) -> Free[To]: ...

else:
    map_by = map_by_t(felis.identity.functor)


# Functor Free
functor = Functor(map_by)


if TYPE_CHECKING:

    @curry
    def by_map[From, To](function: Callable[[From], To], free_value: Free[From]) -> Free[To]: ...

else:
    by_map = felis.functor.by_map(functor)


if TYPE_CHECKING:
    # [F : * -> *] -> [T : *] -> T -> FreeT F T
    def pure_t(value: Any, /) -> FreeT[Any]: ...

else:
    pure_t = PureT


if TYPE_CHECKING:
    # [T : *] -> T -> Free T
    def pure(value: Any, /) -> Free[Any]: ...

else:
    pure = PureT


# [F : * -> *] -> Functor F -> [From : *] -> [To : *] -> FreeT F (From -> To) -> FreeT F From -> FreeT F To
@curry
@curry
def to_apply_t[From, To](free_value: FreeT[From], free_function: FreeT[Callable[[From], To]], f: Functor) -> FreeT[To]:
    match free_function:
        case PureT(function):
            return map_by_t(f)(function)(free_value)
        case BindT(f_free_function):
            return BindT(felis.functor.map_by(f)(flip(to_apply_t(f))(free_value))(f_free_function))


if TYPE_CHECKING:

    @curry
    def to_apply[From, To](free_value: Free[From], free_function: Free[Callable[[From], To]]) -> Free[To]: ...

else:
    to_apply = to_apply_t(felis.identity.functor)


# Applicative Free
applicative = Applicative(functor, pure, to_apply)


if TYPE_CHECKING:

    @curry
    @curry
    def lift[First, Second, Result](
        second: Free[Second],
        first: Free[First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> Free[Result]: ...

else:
    lift = felis.applicative.lift(applicative)


if TYPE_CHECKING:

    @curry
    def take_after[First, Second](second: Free[Second], first: Free[First]) -> Free[Second]: ...

else:
    take_after = felis.applicative.take_after(applicative)


if TYPE_CHECKING:

    @curry
    def discard_before[First, Second](first: Free[First], second: Free[Second]) -> Free[Second]: ...

else:
    discard_before = felis.applicative.discard_before(applicative)


if TYPE_CHECKING:

    @curry
    def discard_after[First, Second](second: Free[Second], first: Free[First]) -> Free[First]: ...

else:
    discard_after = felis.applicative.discard_after(applicative)


if TYPE_CHECKING:

    @curry
    def take_before[First, Second](first: Free[First], second: Free[Second]) -> Free[First]: ...

else:
    take_before = felis.applicative.take_before(applicative)


if TYPE_CHECKING:

    @curry
    def when(free_none: Free[None], bool: bool) -> Free[None]: ...

else:
    when = felis.applicative.when(applicative)


# [F : * -> *] -> Functor F -> [T : *] -> FreeT F (FreeT F T) -> FreeT F T
@curry
def join_t[T](free_free_value: FreeT[FreeT[T]], f: Functor) -> FreeT[T]:
    match free_free_value:
        case PureT(free_value):
            return free_value
        case BindT(f_free_free_value):
            return BindT(felis.functor.map_by(f)(join_t(f))(f_free_free_value))


if TYPE_CHECKING:

    def join[T](free_free_value: Free[Free[T]], /) -> Free[T]: ...

else:
    join = join_t(felis.identity.functor)


# Monad Free
monad = Monad(applicative, join)


if TYPE_CHECKING:

    @curry
    def bind_to[From, To](free_value: Free[From], function: Callable[[From], Free[To]]) -> Free[To]: ...

else:
    bind_to = felis.monad.bind_to(monad)


if TYPE_CHECKING:

    @curry
    def to_bind[From, To](function: Callable[[From], Free[To]], free_value: Free[From]) -> Free[To]: ...

else:
    to_bind = felis.monad.to_bind(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_after[From, Intermediate, To](
        value: From,
        second: Callable[[Intermediate], Free[To]],
        first: Callable[[From], Free[Intermediate]],
    ) -> Free[To]: ...

else:
    compose_after = felis.monad.compose_after(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_before[From, Intermediate, To](
        value: From,
        first: Callable[[From], Free[Intermediate]],
        second: Callable[[Intermediate], Free[To]],
    ) -> Free[To]: ...

else:
    compose_before = felis.monad.compose_before(monad)
