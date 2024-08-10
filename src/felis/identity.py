from collections.abc import Callable
from typing import TYPE_CHECKING

from felis import applicative, monad
from felis.currying import curry

__all__ = ["Identity", "map", "identity", "apply", "lift2", "when", "inject", "join", "bind", "compose", "then"]


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


if TYPE_CHECKING:

    @curry
    def when(bool: bool, identity_none: Identity[None]) -> Identity[None]: ...

else:
    when = applicative.when(identity)


def inject[MT](m_value: MT) -> MT:
    return m_value


join = inject


if TYPE_CHECKING:

    @curry
    def bind[From, To](identity_value: Identity[From], function: Callable[[From], Identity[To]]) -> Identity[To]: ...

else:
    bind = monad.bind(map)(join)


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


if TYPE_CHECKING:

    @curry
    def then[First, Second](first: Identity[First], second: Identity[Second]) -> Identity[Second]: ...

else:
    then = monad.then(bind)
