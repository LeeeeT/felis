from collections.abc import Callable
from typing import TYPE_CHECKING

from felis import applicative, monad
from felis.currying import curry, flip

__all__ = [
    "Identity",
    "apply",
    "bind",
    "bind_to",
    "compose",
    "discard_after",
    "discard_before",
    "join",
    "lift2",
    "map_by",
    "pure",
    "take_after",
    "take_before",
    "when",
]


type Identity[T] = T


@curry
def map_by[From, To](identity_value: Identity[From], function: Callable[[From], To]) -> Identity[To]:
    return function(identity_value)


def pure[T](value: T) -> Identity[T]:
    return value


@curry
def apply[From, To](identity_value: Identity[From], identity_function: Identity[Callable[[From], To]]) -> Identity[To]:
    return identity_function(identity_value)


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[First, Second, Result](
        second: Identity[Second],
        first: Identity[First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> Identity[Result]: ...

else:
    lift2 = applicative.lift2(map_by)(apply)


if TYPE_CHECKING:

    @curry
    def take_after[First, Second](second: Identity[Second], first: Identity[First]) -> Identity[Second]: ...

else:
    take_after = applicative.take_after(lift2)


if TYPE_CHECKING:

    @curry
    def discard_before[First, Second](first: Identity[First], second: Identity[Second]) -> Identity[Second]: ...

else:
    discard_before = applicative.discard_before(lift2)


if TYPE_CHECKING:

    @curry
    def discard_after[First, Second](second: Identity[Second], first: Identity[First]) -> Identity[First]: ...

else:
    discard_after = applicative.discard_after(lift2)


if TYPE_CHECKING:

    @curry
    def take_before[First, Second](first: Identity[First], second: Identity[Second]) -> Identity[First]: ...

else:
    take_before = applicative.take_before(lift2)


if TYPE_CHECKING:

    @curry
    def when(identity_none: Identity[None], bool: bool) -> Identity[None]: ...

else:
    when = applicative.when(pure)


def join[T](identity_identity_value: Identity[Identity[T]]) -> Identity[T]:
    return identity_identity_value


if TYPE_CHECKING:

    @curry
    def bind_to[From, To](identity_value: Identity[From], function: Callable[[From], Identity[To]]) -> Identity[To]: ...

else:
    bind_to = monad.bind_to(map_by)(join)


bind = flip(bind_to)


if TYPE_CHECKING:

    @curry
    @curry
    def compose[From, Intermediate, To](
        value: From,
        first: Callable[[From], Identity[Intermediate]],
        second: Callable[[Intermediate], Identity[To]],
    ) -> Identity[To]: ...

else:
    compose = monad.compose(bind)
