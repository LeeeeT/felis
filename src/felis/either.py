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
    "apply",
    "bind",
    "bind_to",
    "catch",
    "compose",
    "default_to",
    "discard_after",
    "discard_before",
    "fold",
    "join",
    "lift2",
    "map_by",
    "pure",
    "take_after",
    "take_before",
    "to_add",
    "traverse",
    "when",
]


if TYPE_CHECKING:

    @curry
    def to_add[L, R](augend: Either[L, R], addend: Either[L, R]) -> Either[L, R]: ...

else:
    to_add = either_t.to_add(felis.identity.pure)(felis.identity.bind)


@curry
def map_by[L, From, To](either_value: Either[L, From], function: Callable[[From], To]) -> Either[L, To]:
    match either_value:
        case Left(value):
            return Left(value)
        case Right(value):
            return Right(function(value))


if TYPE_CHECKING:
    # [L : *] -> [R : *] -> R -> Either L R
    def pure[R](value: R) -> Either[Any, R]: ...

else:
    pure = Right


if TYPE_CHECKING:

    @curry
    def apply[L, From, To](either_value: Either[L, From], either_function: Either[L, Callable[[From], To]]) -> Either[L, To]: ...

else:
    apply = either_t.apply(felis.identity.pure)(felis.identity.bind)


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[L, First, Second, Result](
        second: Either[L, Second],
        first: Either[L, First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> Either[L, Result]: ...

else:
    lift2 = applicative.lift2(map_by)(apply)


take_after = lift2(function.flip(function.pure))


discard_after = lift2(function.pure)


take_before = function.flip(discard_after)


discard_before = function.flip(take_after)


if TYPE_CHECKING:

    @curry
    def when[L](either_none: Either[L, None], bool: bool) -> Either[L, None]: ...

else:
    when = applicative.when(pure)


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
            return a_map(pure)(function(value))


if TYPE_CHECKING:

    def join[L, R](either_either_value: Either[L, Either[L, R]], /) -> Either[L, R]: ...

else:
    join = either_t.join(felis.identity.pure)(felis.identity.bind)


if TYPE_CHECKING:

    @curry
    def bind_to[L, From, To](either_value: Either[L, From], function: Callable[[From], Either[L, To]]) -> Either[L, To]: ...

else:
    bind_to = monad.bind_to(map_by)(join)


bind = function.flip(bind_to)


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
    def default_to[L, R](either_value: Either[L, R], default_value: R) -> R: ...

else:
    default_to = either_t.default_to(felis.identity.pure)(felis.identity.bind)


@curry
@curry
def catch[E: BaseException, From, To](value: From, function: Callable[[From], To], exception_type: type[E]) -> Either[E, To]:
    try:
        return Right(function(value))
    except exception_type as exception:
        return Left(exception)
