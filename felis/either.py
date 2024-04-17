from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol

import felis.identity
from felis import monad
from felis.currying import curry

__all__ = ["Either", "Left", "Right", "identity", "map", "inject", "join", "bind", "compose"]


type Either[L, R] = Left[L] | Right[R]


@dataclass(frozen=True)
class Left[T]:
    value: T


@dataclass(frozen=True)
class Right[T]:
    value: T


def identity[L, R](value: R) -> Either[L, R]:
    return Right(value)


@curry
def map[L, From, To](either_value: Either[L, From], function: Callable[[From], To]) -> Either[L, To]:
    match either_value:
        case Left(value):
            return Left(value)
        case Right(value):
            return Right(function(value))


@curry
def inject[L, R, MEitherR](either_m_either_value: Either[L, MEitherR], m_identity: Callable[[Either[L, R]], MEitherR]) -> MEitherR:
    match either_m_either_value:
        case Left(value):
            return m_identity(Left(value))
        case Right(m_either_value):
            return m_either_value


class Join(Protocol):
    @staticmethod
    def __call__[L, R](either_either_value: Either[L, Either[L, R]], /) -> Either[L, R]: ...


join: Join = inject(felis.identity.identity)


class Bind(Protocol):
    @staticmethod
    @curry
    def __call__[L, From, To](either_value: Either[L, From], function: Callable[[From], Either[L, To]], /) -> Either[L, To]: ...


bind: Bind = monad.bind(map)(join)


class Compose(Protocol):
    @staticmethod
    @curry
    @curry
    def __call__[L, From, Intermediate, To](
        value: Either[L, From],
        first: Callable[[From], Either[L, Intermediate]],
        second: Callable[[Intermediate], Either[L, To]],
        /,
    ) -> Either[L, To]: ...


compose: Compose = monad.compose(bind)
