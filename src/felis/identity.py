from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from felis import applicative, monad
from felis.currying import curry
from felis.function import flip_, identity_

__all__ = [
    "Identity",
    "map",
    "identity",
    "apply",
    "lift2",
    "take_after",
    "discard_after",
    "take_before",
    "discard_before",
    "when",
    "inject",
    "join",
    "bound",
    "bind",
    "compose",
]


type Identity[T] = T


@curry
def map[From, To](identity_value: Identity[From], function: Callable[[From], To]) -> Identity[To]:
    return function(identity_value)


def identity[T](value: T) -> Identity[T]:
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
    lift2 = applicative.lift2(map)(apply)


take_after = lift2(flip_.flip(identity_.identity))


discard_after = lift2(identity_.identity)


take_before = flip_.flip(discard_after)


discard_before = flip_.flip(take_after)


if TYPE_CHECKING:

    @curry
    def when(bool: bool, identity_none: Identity[None]) -> Identity[None]: ...

else:
    when = applicative.when(identity)


# [M : Type -> Type] -> [T : Type] -> Identity (M T) -> M T
def inject(identity_m_identity_value: Identity[Any]) -> Any:
    return identity_m_identity_value


join = inject


if TYPE_CHECKING:

    @curry
    def bound[From, To](identity_value: Identity[From], function: Callable[[From], Identity[To]]) -> Identity[To]: ...

else:
    bound = monad.bound(map)(join)


bind = flip_.flip(bound)


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
