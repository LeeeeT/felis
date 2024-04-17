from collections.abc import Callable
from typing import Protocol

import felis.identity
from felis import Coroutine, Option, coroutine, monad, option
from felis.currying import curry

__all__ = ["identity", "map", "join", "bind", "compose"]


class Identity(Protocol):
    @staticmethod
    def __call__[T](value: T, /) -> Coroutine[Option[T]]: ...


identity: Identity = felis.identity.compose(coroutine.identity)(option.identity)


class Map(Protocol):
    @staticmethod
    @curry
    def __call__[From, To](coroutine_option_value: Coroutine[Option[From]], function: Callable[[From], To], /) -> Coroutine[Option[To]]: ...


map: Map = felis.identity.compose(coroutine.map)(option.map)


class Join(Protocol):
    @staticmethod
    def __call__[T](coroutine_option_coroutine_option_value: Coroutine[Option[Coroutine[Option[T]]]], /) -> Coroutine[Option[T]]: ...


join: Join = coroutine.bind(option.inject(coroutine.identity))


class Bind(Protocol):
    @staticmethod
    @curry
    def __call__[From, To](coroutine_option_value: Coroutine[Option[From]], function: Callable[[From], Coroutine[Option[To]]], /) -> Coroutine[Option[To]]: ...


bind: Bind = monad.bind(map)(join)


class Compose(Protocol):
    @staticmethod
    @curry
    @curry
    def __call__[From, Intermediate, To](
        value: From,
        first: Callable[[From], Coroutine[Option[Intermediate]]],
        second: Callable[[Intermediate], Coroutine[Option[To]]],
        /,
    ) -> Coroutine[Option[To]]: ...


compose: Compose = monad.compose(bind)
