from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import felis.identity
from felis import applicative, free_t, monad
from felis.currying import curry, flip
from felis.free_t import Pure

__all__ = [
    "Bind",
    "Free",
    "Pure",
    "apply",
    "bind",
    "bind_to",
    "compose_after",
    "compose_before",
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


if TYPE_CHECKING:

    @dataclass(frozen=True)
    class Bind[T]:
        f_free_value: felis.identity.Identity[Free[T]]

else:
    from felis.free_t import Bind


if TYPE_CHECKING:
    type Free[T] = Pure[T] | Bind[T]
else:
    from felis.free_t import Free


if TYPE_CHECKING:

    @curry
    def map_by[From, To](free_value: Free[From], function: Callable[[From], To]) -> Free[To]: ...

else:
    map_by = free_t.map_by(felis.identity.map_by)


if TYPE_CHECKING:
    # [T : *] -> T -> Free T
    pure: Free[Any]
else:
    from felis.free_t import pure


if TYPE_CHECKING:

    @curry
    def apply[From, To](free_value: Free[From], free_function: Free[Callable[[From], To]]) -> Free[To]: ...

else:
    apply = free_t.apply(felis.identity.map_by)


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


if TYPE_CHECKING:

    def join[T](free_free_value: Free[Free[T]], /) -> Free[T]: ...

else:
    join = free_t.join(felis.identity.map_by)


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
