from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import felis.identity
from felis import applicative, free_t, function, monad
from felis.currying import curry
from felis.free_t import Pure

__all__ = [
    "Bind",
    "Free",
    "Pure",
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


take_after = lift2(function.flip(function.pure))


discard_after = lift2(function.pure)


take_before = function.flip(discard_after)


discard_before = function.flip(take_after)


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


bind = function.flip(bind_to)


if TYPE_CHECKING:

    @curry
    @curry
    def compose[From, Intermediate, To](
        value: From,
        first: Callable[[From], Free[Intermediate]],
        second: Callable[[Intermediate], Free[To]],
    ) -> Free[To]: ...

else:
    compose = monad.compose(bind)
