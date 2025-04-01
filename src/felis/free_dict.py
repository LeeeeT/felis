from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Final

import felis.applicative
import felis.monad
from felis import dict, free
from felis.applicative import Applicative
from felis.currying import curry
from felis.functor import Functor
from felis.monad import Monad

__all__ = [
    "Applicative",
    "Bind",
    "FreeDict",
    "Functor",
    "Monad",
    "Pure",
    "applicative",
    "bind_to",
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


type FreeDict[K, T] = Pure[T] | Bind[K, T]


Pure = free.PureT


if TYPE_CHECKING:

    class Bind[K, T]:
        __match_args__ = ("f_free_value",)

        def __init__(self, f_free_value: dict.Dict[K, FreeDict[K, T]]):
            self.f_free_value: Final = f_free_value

else:

    class Bind[K, T](free.BindT[T]):
        pass


if TYPE_CHECKING:

    @curry
    def map_by[K, From, To](free_dict_value: FreeDict[K, From], function: Callable[[From], To]) -> FreeDict[K, To]: ...

else:
    map_by = free.map_by_t(dict.functor)


# [K : *] -> Functor (FreeDict K)
functor = Functor(map_by)


if TYPE_CHECKING:
    # [K : *] -> [T : *] -> T -> FreeDict K T
    def pure[K, T](value: T, /) -> FreeDict[K, T]: ...

else:
    pure = free.pure


if TYPE_CHECKING:

    @curry
    def to_apply[K, From, To](free_dict_value: FreeDict[K, From], free_dict_function: FreeDict[K, Callable[[From], To]]) -> FreeDict[K, To]: ...

else:
    to_apply = free.to_apply_t(dict.functor)


# [K : *] -> Applicative (FreeDict K)
applicative = Applicative(functor, pure, to_apply)


if TYPE_CHECKING:

    @curry
    @curry
    def lift[K, First, Second, Result](
        second: FreeDict[K, Second],
        first: FreeDict[K, First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> FreeDict[K, Result]: ...

else:
    lift = felis.applicative.lift(applicative)


if TYPE_CHECKING:

    @curry
    def take_after[K, First, Second](second: FreeDict[K, Second], first: FreeDict[K, First]) -> FreeDict[K, Second]: ...

else:
    take_after = felis.applicative.take_after(applicative)


if TYPE_CHECKING:

    @curry
    def discard_before[K, First, Second](first: FreeDict[K, First], second: FreeDict[K, Second]) -> FreeDict[K, Second]: ...

else:
    discard_before = felis.applicative.discard_before(applicative)


if TYPE_CHECKING:

    @curry
    def discard_after[K, First, Second](second: FreeDict[K, Second], first: FreeDict[K, First]) -> FreeDict[K, First]: ...

else:
    discard_after = felis.applicative.discard_after(applicative)


if TYPE_CHECKING:

    @curry
    def take_before[K, First, Second](first: FreeDict[K, First], second: FreeDict[K, Second]) -> FreeDict[K, First]: ...

else:
    take_before = felis.applicative.take_before(applicative)


if TYPE_CHECKING:

    @curry
    def when[K](free_dict_none: FreeDict[K, None], bool: bool) -> FreeDict[K, None]: ...

else:
    when = felis.applicative.when(applicative)


if TYPE_CHECKING:

    def join[K, T](free_dict_free_dict_value: FreeDict[K, FreeDict[K, T]], /) -> FreeDict[K, T]: ...

else:
    join = free.join_t(dict.functor)


# [K : *] -> Monad (FreeDict K)
monad = Monad(applicative, join)


if TYPE_CHECKING:

    @curry
    def bind_to[K, From, To](free_dict_value: FreeDict[K, From], function: Callable[[From], FreeDict[K, To]]) -> FreeDict[K, To]: ...

else:
    bind_to = felis.monad.bind_to(monad)


if TYPE_CHECKING:

    @curry
    def to_bind[K, From, To](function: Callable[[From], FreeDict[K, To]], free_dict_value: FreeDict[K, From]) -> FreeDict[K, To]: ...

else:
    to_bind = felis.monad.to_bind(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_after[K, From, Intermediate, To](
        value: From,
        second: Callable[[Intermediate], FreeDict[K, To]],
        first: Callable[[From], FreeDict[K, Intermediate]],
    ) -> FreeDict[K, To]: ...

else:
    compose_after = felis.monad.compose_after(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_before[K, From, Intermediate, To](
        value: From,
        first: Callable[[From], FreeDict[K, Intermediate]],
        second: Callable[[Intermediate], FreeDict[K, To]],
    ) -> FreeDict[K, To]: ...

else:
    compose_before = felis.monad.compose_before(monad)
