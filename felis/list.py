from collections.abc import Callable
from typing import Protocol

from felis import monad
from felis.currying import curry

__all__ = ["List", "identity", "map", "join", "bind", "compose"]


type List[T] = list[T]


def identity[T](value: T) -> List[T]:
    return [value]


@curry
def map[From, To](list_value: List[From], function: Callable[[From], To]) -> List[To]:
    return [function(value) for value in list_value]


def join[T](list_list_value: List[List[T]]) -> List[T]:
    return [value for list_value in list_list_value for value in list_value]


class Bind(Protocol):
    @staticmethod
    @curry
    def __call__[From, To](list_value: List[From], function: Callable[[From], List[To]], /) -> List[To]: ...


bind: Bind = monad.bind(map)(join)


class Compose(Protocol):
    @staticmethod
    @curry
    @curry
    def __call__[From, Intermediate, To](
        value: From,
        first: Callable[[From], List[Intermediate]],
        second: Callable[[Intermediate], List[To]],
        /,
    ) -> List[To]: ...


compose: Compose = monad.compose(bind)
