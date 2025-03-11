from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import felis.identity
from felis import applicative, either_t, function, monad
from felis.currying import curry
from felis.either_t import Either, Left, Right

__all__ = [
    "Either",
    "Left",
    "Right",
    "add",
    "apply",
    "bind",
    "bound",
    "catch",
    "compose",
    "discard_after",
    "discard_before",
    "fold",
    "identity",
    "join",
    "lift2",
    "map",
    "take_after",
    "take_before",
    "traverse",
    "when",
]


if TYPE_CHECKING:

    @curry
    def add[L, R](augend: Either[L, R], addend: Either[L, R]) -> Either[L, R]: ...

else:
    add = either_t.add(felis.identity.identity)(felis.identity.bind)


@curry
def map[L, From, To](either_value: Either[L, From], function: Callable[[From], To]) -> Either[L, To]:
    match either_value:
        case Left(value):
            return Left(value)
        case Right(value):
            return Right(function(value))


if TYPE_CHECKING:
    # [L : *] -> [R : *] -> R -> Either L R
    def identity[R](value: R) -> Either[Any, R]: ...

else:
    identity = Right


if TYPE_CHECKING:

    @curry
    def apply[L, From, To](either_value: Either[L, From], either_function: Either[L, Callable[[From], To]]) -> Either[L, To]: ...

else:
    apply = either_t.apply(felis.identity.identity)(felis.identity.bind)


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


take_after = lift2(function.flip(function.identity))


discard_after = lift2(function.identity)


take_before = function.flip(discard_after)


discard_before = function.flip(take_after)


if TYPE_CHECKING:

    @curry
    def when[L](bool: bool, either_none: Either[L, None]) -> Either[L, None]: ...

else:
    when = applicative.when(identity)


# [L : *] -> [A : *] -> A -> [R : *] -> (R -> A -> A) -> Either L R -> A
@curry
@curry
def fold[A, R](either_value: Either[Any, R], function: Callable[[R], Callable[[A], A]], accumulator: A) -> A:
    match either_value:
        case Left(value):
            return accumulator
        case Right(value):
            return function(value)(accumulator)


# [L : *] -> [A : * -> *] ->
# ([From : *] -> [To : *] -> (From -> To) -> A From -> A To) ->
# ([T : *] -> T -> A T) ->
# [From : *] -> [To : *] -> (From -> A To) -> Either L From -> A (Either L To)
@curry
@curry
@curry
def traverse[From](
    either_value: Either[Any, From],
    function: Callable[[From], Any],
    a_identity: Callable[[Any], Any],
    a_map: Callable[[Callable[[Any], Any]], Callable[[Any], Any]],
) -> Any:
    match either_value:
        case Left(value):
            return a_identity(Left(value))
        case Right(value):
            return a_map(identity)(function(value))


if TYPE_CHECKING:

    def join[L, R](either_either_value: Either[L, Either[L, R]], /) -> Either[L, R]: ...

else:
    join = either_t.join(felis.identity.identity)(felis.identity.bind)


if TYPE_CHECKING:

    @curry
    def bound[L, From, To](either_value: Either[L, From], function: Callable[[From], Either[L, To]]) -> Either[L, To]: ...

else:
    bound = monad.bound(map)(join)


bind = function.flip(bound)


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


@curry
@curry
def catch[E: BaseException, From, To](value: From, function: Callable[[From], To], exception_type: type[E]) -> Either[E, To]:
    try:
        return Right(function(value))
    except exception_type as exception:
        return Left(exception)
