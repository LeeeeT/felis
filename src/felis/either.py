from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING

import felis.identity
from felis import applicative, monad
from felis.currying import curry

__all__ = ["Either", "Left", "Right", "map", "identity", "apply", "lift2", "when", "inject", "join", "bind", "compose", "then", "catch"]


type Either[L, R] = Left[L] | Right[R]


@dataclass(frozen=True)
class Left[T]:
    value: T


@dataclass(frozen=True)
class Right[T]:
    value: T


@curry
def map[L, From, To](either_value: Either[L, From], function: Callable[[From], To]) -> Either[L, To]:
    match either_value:
        case Left(value):
            return Left(value)
        case Right(value):
            return Right(function(value))


if TYPE_CHECKING:

    def identity[L, R](value: R) -> Either[L, R]: ...

else:
    identity = Right


@curry
def apply[L, From, To](either_value: Either[L, From], either_function: Either[L, Callable[[From], To]]) -> Either[L, To]:
    match either_function:
        case Left(value):
            return Left(value)
        case Right(function):
            return map(function)(either_value)


lift2 = applicative.lift2(map)(apply)


when = applicative.when(identity)


@curry
def inject[L, R, MEitherR](either_m_either_value: Either[L, MEitherR], m_identity: Callable[[Either[L, R]], MEitherR]) -> MEitherR:
    match either_m_either_value:
        case Left(value):
            return m_identity(Left(value))
        case Right(m_either_value):
            return m_either_value


if TYPE_CHECKING:

    def join[L, R](either_either_value: Either[L, Either[L, R]], /) -> Either[L, R]: ...

else:
    join = inject(felis.identity.identity)


bind = monad.bind(map)(join)


compose = monad.compose(bind)


then = monad.then(bind)


@curry
@curry
def catch[E: BaseException, From, To](value: From, function: Callable[[From], To], exception_type: type[E]) -> Either[E, To]:
    try:
        return Right(function(value))
    except exception_type as exception:
        return Left(exception)
