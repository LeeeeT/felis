from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from felis import applicative, monad
from felis.currying import curry
from felis.function import flip_, pure_

__all__ = [
    "Identity",
    "apply",
    "bind",
    "bind_to",
    "compose",
    "discard_after",
    "discard_before",
    "inject",
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


take_after = lift2(flip_.flip(pure_.pure))


discard_after = lift2(pure_.pure)


take_before = flip_.flip(discard_after)


discard_before = flip_.flip(take_after)


if TYPE_CHECKING:

    @curry
    def when(identity_none: Identity[None], bool: bool) -> Identity[None]: ...

else:
    when = applicative.when(pure)


# TODO
# [M : * -> *] -> [T : *] -> Identity (M T) -> M T
def inject(identity_m_identity_value: Identity[Any]) -> Any:
    return identity_m_identity_value


join = inject


if TYPE_CHECKING:

    @curry
    def bind_to[From, To](identity_value: Identity[From], function: Callable[[From], Identity[To]]) -> Identity[To]: ...

else:
    bind_to = monad.bind_to(map_by)(join)


bind = flip_.flip(bind_to)


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
