from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING

from felis import applicative, dict, free_t, function, monad
from felis.currying import curry
from felis.free_t import Pure, identity

__all__ = [
    "Pure",
    "Bind",
    "FreeDict",
    "map",
    "identity",
    "apply",
    "lift2",
    "take_after",
    "discard_after",
    "take_before",
    "discard_before",
    "when",
    "join",
    "bound",
    "bind",
    "compose",
]


if TYPE_CHECKING:

    @dataclass(frozen=True)
    class Bind[K, T]:
        f_free_dict_value: dict.Dict[K, FreeDict[K, T]]

else:
    from felis.free_t import Bind


if TYPE_CHECKING:
    type FreeDict[K, T] = Pure[T] | Bind[K, T]
else:
    from felis.free_t import Free as FreeDict


if TYPE_CHECKING:

    @curry
    def map[K, From, To](free_dict_value: FreeDict[K, From], function: Callable[[From], To]) -> FreeDict[K, To]: ...

else:
    map = free_t.map(dict.map)


if TYPE_CHECKING:

    @curry
    def apply[K, From, To](free_dict_value: FreeDict[K, From], free_dict_function: FreeDict[K, Callable[[From], To]]) -> FreeDict[K, To]: ...

else:
    apply = free_t.apply(dict.map)


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[K, First, Second, Result](
        second: FreeDict[K, Second],
        first: FreeDict[K, First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> FreeDict[K, Result]: ...

else:
    lift2 = applicative.lift2(map)(apply)


take_after = lift2(function.flip(function.identity))


discard_after = lift2(function.identity)


take_before = function.flip(discard_after)


discard_before = function.flip(take_after)


if TYPE_CHECKING:

    @curry
    def when[K](bool: bool, free_dict_none: FreeDict[K, None]) -> FreeDict[K, None]: ...

else:
    when = applicative.when(identity)


if TYPE_CHECKING:

    def join[K, T](free_dict_free_dict_value: FreeDict[K, FreeDict[K, T]], /) -> FreeDict[K, T]: ...

else:
    join = free_t.join(dict.map)


if TYPE_CHECKING:

    @curry
    def bound[K, From, To](free_dict_value: FreeDict[K, From], function: Callable[[From], FreeDict[K, To]]) -> FreeDict[K, To]: ...

else:
    bound = monad.bound(map)(join)


bind = function.flip(bound)


if TYPE_CHECKING:

    @curry
    @curry
    def compose[K, From, Intermediate, To](
        value: From,
        first: Callable[[From], FreeDict[K, Intermediate]],
        second: Callable[[Intermediate], FreeDict[K, To]],
    ) -> FreeDict[K, To]: ...

else:
    compose = monad.compose(bind)
