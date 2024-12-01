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
    "bound",
    "compose",
    "discard_after",
    "discard_before",
    "identity",
    "join",
    "lift2",
    "map",
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
    def map[From, To](free_value: Free[From], function: Callable[[From], To]) -> Free[To]: ...

else:
    map = free_t.map(felis.identity.map)


if TYPE_CHECKING:
    # [T : Type] -> T -> Free T
    identity: Free[Any]
else:
    from felis.free_t import identity


if TYPE_CHECKING:

    @curry
    def apply[From, To](free_value: Free[From], free_function: Free[Callable[[From], To]]) -> Free[To]: ...

else:
    apply = free_t.apply(felis.identity.map)


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[First, Second, Result](
        second: Free[Second],
        first: Free[First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> Free[Result]: ...

else:
    lift2 = applicative.lift2(map)(apply)


take_after = lift2(function.flip(function.identity))


discard_after = lift2(function.identity)


take_before = function.flip(discard_after)


discard_before = function.flip(take_after)


if TYPE_CHECKING:

    @curry
    def when(bool: bool, free_none: Free[None]) -> Free[None]: ...

else:
    when = applicative.when(identity)


if TYPE_CHECKING:

    def join[T](free_free_value: Free[Free[T]], /) -> Free[T]: ...

else:
    join = free_t.join(felis.identity.map)


if TYPE_CHECKING:

    @curry
    def bound[From, To](free_value: Free[From], function: Callable[[From], Free[To]]) -> Free[To]: ...

else:
    bound = monad.bound(map)(join)


bind = function.flip(bound)


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
