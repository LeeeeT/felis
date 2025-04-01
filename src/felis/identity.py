from collections.abc import Callable
from typing import TYPE_CHECKING

import felis.applicative
import felis.functor
import felis.monad
from felis.applicative import Applicative
from felis.currying import curry
from felis.functor import Functor
from felis.monad import Monad

__all__ = [
    "Identity",
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
    "monad",
    "pure",
    "take_after",
    "take_before",
    "to_apply",
    "to_bind",
    "when",
]


type Identity[T] = T


@curry
def map_by[From, To](identity_value: Identity[From], function: Callable[[From], To]) -> Identity[To]:
    return function(identity_value)


# Functor Identity
functor = Functor(map_by)


if TYPE_CHECKING:

    @curry
    def by_map[From, To](function: Callable[[From], To], identity_value: Identity[From]) -> Identity[To]: ...

else:
    by_map = felis.functor.by_map(functor)


def pure[T](value: T) -> Identity[T]:
    return value


@curry
def to_apply[From, To](identity_value: Identity[From], identity_function: Identity[Callable[[From], To]]) -> Identity[To]:
    return identity_function(identity_value)


# Applicative Identity
applicative = Applicative(functor, pure, to_apply)


if TYPE_CHECKING:

    @curry
    def apply_to[From, To](identity_function: Identity[Callable[[From], To]], identity_value: Identity[From]) -> Identity[To]: ...

else:
    apply_to = felis.applicative.apply_to(applicative)


if TYPE_CHECKING:

    @curry
    @curry
    def lift[First, Second, Result](
        second: Identity[Second],
        first: Identity[First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> Identity[Result]: ...

else:
    lift = felis.applicative.lift(applicative)


if TYPE_CHECKING:

    @curry
    def take_after[First, Second](second: Identity[Second], first: Identity[First]) -> Identity[Second]: ...

else:
    take_after = felis.applicative.take_after(applicative)


if TYPE_CHECKING:

    @curry
    def discard_before[First, Second](first: Identity[First], second: Identity[Second]) -> Identity[Second]: ...

else:
    discard_before = felis.applicative.discard_before(applicative)


if TYPE_CHECKING:

    @curry
    def discard_after[First, Second](second: Identity[Second], first: Identity[First]) -> Identity[First]: ...

else:
    discard_after = felis.applicative.discard_after(applicative)


if TYPE_CHECKING:

    @curry
    def take_before[First, Second](first: Identity[First], second: Identity[Second]) -> Identity[First]: ...

else:
    take_before = felis.applicative.take_before(applicative)


if TYPE_CHECKING:

    @curry
    def when(identity_none: Identity[None], bool: bool) -> Identity[None]: ...

else:
    when = felis.applicative.when(applicative)


def join[T](identity_identity_value: Identity[Identity[T]]) -> Identity[T]:
    return identity_identity_value


# Monad Identity
monad = Monad(applicative, join)


if TYPE_CHECKING:

    @curry
    def bind_to[From, To](identity_value: Identity[From], function: Callable[[From], Identity[To]]) -> Identity[To]: ...

else:
    bind_to = felis.monad.bind_to(monad)


if TYPE_CHECKING:

    @curry
    def to_bind[From, To](function: Callable[[From], Identity[To]], identity_value: Identity[From]) -> Identity[To]: ...

else:
    to_bind = felis.monad.to_bind(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_after[From, Intermediate, To](
        value: From,
        second: Callable[[Intermediate], Identity[To]],
        first: Callable[[From], Identity[Intermediate]],
    ) -> Identity[To]: ...

else:
    compose_after = felis.monad.compose_after(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_before[From, Intermediate, To](
        value: From,
        first: Callable[[From], Identity[Intermediate]],
        second: Callable[[Intermediate], Identity[To]],
    ) -> Identity[To]: ...

else:
    compose_before = felis.monad.compose_before(monad)
