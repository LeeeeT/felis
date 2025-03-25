from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from felis import applicative, dict, free_t, monad
from felis.currying import curry, flip
from felis.free_t import Pure

__all__ = [
    "Bind",
    "FreeDict",
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
    def map_by[K, From, To](free_dict_value: FreeDict[K, From], function: Callable[[From], To]) -> FreeDict[K, To]: ...

else:
    map_by = free_t.map_by(dict.map_by)


if TYPE_CHECKING:
    # [K : *] -> [T : *] -> T -> FreeDict K T
    pure: FreeDict[Any, Any]
else:
    from felis.free_t import pure


if TYPE_CHECKING:

    @curry
    def apply[K, From, To](free_dict_value: FreeDict[K, From], free_dict_function: FreeDict[K, Callable[[From], To]]) -> FreeDict[K, To]: ...

else:
    apply = free_t.apply(dict.map_by)


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[K, First, Second, Result](
        second: FreeDict[K, Second],
        first: FreeDict[K, First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> FreeDict[K, Result]: ...

else:
    lift2 = applicative.lift2(map_by)(apply)


if TYPE_CHECKING:

    @curry
    def take_after[K, First, Second](second: FreeDict[K, Second], first: FreeDict[K, First]) -> FreeDict[K, Second]: ...

else:
    take_after = applicative.take_after(lift2)


if TYPE_CHECKING:

    @curry
    def discard_before[K, First, Second](first: FreeDict[K, First], second: FreeDict[K, Second]) -> FreeDict[K, Second]: ...

else:
    discard_before = applicative.discard_before(lift2)


if TYPE_CHECKING:

    @curry
    def discard_after[K, First, Second](second: FreeDict[K, Second], first: FreeDict[K, First]) -> FreeDict[K, First]: ...

else:
    discard_after = applicative.discard_after(lift2)


if TYPE_CHECKING:

    @curry
    def take_before[K, First, Second](first: FreeDict[K, First], second: FreeDict[K, Second]) -> FreeDict[K, First]: ...

else:
    take_before = applicative.take_before(lift2)


if TYPE_CHECKING:

    @curry
    def when[K](free_dict_none: FreeDict[K, None], bool: bool) -> FreeDict[K, None]: ...

else:
    when = applicative.when(pure)


if TYPE_CHECKING:

    def join[K, T](free_dict_free_dict_value: FreeDict[K, FreeDict[K, T]], /) -> FreeDict[K, T]: ...

else:
    join = free_t.join(dict.map_by)


if TYPE_CHECKING:

    @curry
    def bind_to[K, From, To](free_dict_value: FreeDict[K, From], function: Callable[[From], FreeDict[K, To]]) -> FreeDict[K, To]: ...

else:
    bind_to = monad.bind_to(map_by)(join)


bind = flip(bind_to)


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
