from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import felis.identity
from felis import applicative, monad
from felis.currying import curry

__all__ = [
    "Either",
    "Left",
    "Right",
    "add",
    "map",
    "identity",
    "apply",
    "lift2",
    "when",
    "fold",
    "traverse",
    "inject",
    "join",
    "bind",
    "compose",
    "then",
    "catch",
]


type Either[L, R] = Left[L] | Right[R]


@dataclass(frozen=True)
class Left[T]:
    value: T


@dataclass(frozen=True)
class Right[T]:
    value: T


@curry
def add[L, R](augend: Either[L, R], addend: Either[L, R]) -> Either[L, R]:
    match augend:
        case Left(value):
            return addend
        case Right(value):
            return Right(value)


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


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[L, First, Second, Result](
        second: Either[L, Second],
        first: Either[L, First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> Either[L, Result]: ...

else:
    lift2 = applicative.lift2(map)(apply)


if TYPE_CHECKING:

    @curry
    def when[L](bool: bool, either_none: Either[L, None]) -> Either[L, None]: ...

else:
    when = applicative.when(identity)


@curry
@curry
def fold[A, L, R](either_value: Either[L, R], function: Callable[[R], Callable[[A], A]], accumulator: A) -> A:
    match either_value:
        case Left(value):
            return accumulator
        case Right(value):
            return function(value)(accumulator)


# [L : Type] -> [A : Type -> Type] ->
# ([From : Type] -> [To : Type] -> (From -> To) -> A From -> A To) ->
# ([T : Type] -> T -> A T) ->
# [From : Type] -> [To : Type] -> (From -> A To) -> Either L From -> A (Either L To)
@curry
@curry
@curry
def traverse[L, From](
    either_value: Either[L, From],
    function: Callable[[From], Any],
    a_identity: Callable[[Any], Any],
    a_map: Callable[[Callable[[Any], Any]], Callable[[Any], Any]],
) -> Any:
    match either_value:
        case Left(value):
            return a_identity(Left(value))
        case Right(value):
            return a_map(identity)(function(value))


# [L : Type] -> [M : Type -> Type] -> ([T : Type] -> T -> M T) -> [R : Type] -> Either L (M (Either L R)) -> M (Either L R)
@curry
def inject[L](either_m_either_value: Either[L, Any], m_identity: Callable[[Any], Any]) -> Any:
    match either_m_either_value:
        case Left(value):
            return m_identity(Left(value))
        case Right(m_either_value):
            return m_either_value


if TYPE_CHECKING:

    def join[L, R](either_either_value: Either[L, Either[L, R]], /) -> Either[L, R]: ...

else:
    join = inject(felis.identity.identity)


if TYPE_CHECKING:

    @curry
    def bind[L, From, To](either_value: Either[L, From], function: Callable[[From], Either[L, To]]) -> Either[L, To]: ...

else:
    bind = monad.bind(map)(join)


if TYPE_CHECKING:

    @curry
    @curry
    def compose[L, From, Intermediate, To](
        value: From,
        first: Callable[[From], Either[L, Intermediate]],
        second: Callable[[Intermediate], Either[L, To]],
    ) -> Either[L, To]: ...

else:
    compose = monad.compose(bind)


if TYPE_CHECKING:

    @curry
    def then[L, First, Second](first: Either[L, First], second: Either[L, Second]) -> Either[L, Second]: ...

else:
    then = monad.then(bind)


@curry
@curry
def catch[E: BaseException, From, To](value: From, function: Callable[[From], To], exception_type: type[E]) -> Either[E, To]:
    try:
        return Right(function(value))
    except exception_type as exception:
        return Left(exception)
