import builtins
from collections.abc import Callable, Iterable
from typing import TYPE_CHECKING, Any

import felis.identity
import felis.order
from felis import applicative, function, monad
from felis.currying import curry
from felis.predicate import Predicate

__all__ = [
    "Iterable",
    "neutral",
    "append",
    "add",
    "map",
    "identity",
    "apply",
    "lift2",
    "take_after",
    "discard_after",
    "take_before",
    "discard_before",
    "when",
    "fold",
    "traverse",
    "join",
    "bound",
    "bind",
    "compose",
    "guard",
    "filter",
    "range",
]


# [T : Type] -> Iterable T
neutral: Iterable[Any] = ()


@curry
def append[T](iterable: Iterable[T], value: T) -> Iterable[T]:
    yield from iterable
    yield value


@curry
def add[T](augend: Iterable[T], addend: Iterable[T]) -> Iterable[T]:
    yield from augend
    yield from addend


@curry
def map[From, To](iterable_value: Iterable[From], function: Callable[[From], To]) -> Iterable[To]:
    for value in iterable_value:
        yield function(value)


def identity[T](value: T) -> Iterable[T]:
    yield value


@curry
def apply[From, To](iterable_value: Iterable[From], iterable_function: Iterable[Callable[[From], To]]) -> Iterable[To]:
    for function in iterable_function:
        for value in iterable_value:
            yield function(value)


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[First, Second, Result](
        second: Iterable[Second],
        first: Iterable[First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> Iterable[Result]: ...

else:
    lift2 = applicative.lift2(map)(apply)


take_after = lift2(function.flip(function.identity))


discard_after = lift2(function.identity)


take_before = function.flip(discard_after)


discard_before = function.flip(take_after)


if TYPE_CHECKING:

    @curry
    def when(bool: bool, iterable_none: Iterable[None]) -> Iterable[None]: ...

else:
    when = applicative.when(identity)


@curry
@curry
def fold[A, T](iterable_value: Iterable[T], function: Callable[[T], Callable[[A], A]], accumulator: A) -> A:
    for value in iterable_value:
        accumulator = function(value)(accumulator)
    return accumulator


# [A : Type -> Type] ->
# ([From : Type] -> [To : Type] -> (From -> To) -> A From -> A To) ->
# ([T : Type] -> T -> A T) ->
# [From : Type] -> [To : Type] -> (From -> A To) -> Iterable From -> A (Iterable To)
@curry
@curry
def traverse[From](
    function: Callable[[From], Any],
    a_lift2: Callable[[Callable[[Any], Callable[[Any], Any]]], Callable[[Any], Callable[[Any], Any]]],
    a_identity: Callable[[Any], Any],
) -> Callable[[Iterable[From]], Any]:
    return fold(a_identity(neutral))(felis.identity.compose(a_lift2(append))(function))


if TYPE_CHECKING:

    def join[T](iterable_iterable_value: Iterable[Iterable[T]]) -> Iterable[T]: ...

else:
    join = fold(neutral)(add)


if TYPE_CHECKING:

    @curry
    def bound[From, To](iterable_value: Iterable[From], function: Callable[[From], Iterable[To]]) -> Iterable[To]: ...

else:
    bound = monad.bound(map)(join)


bind = function.flip(bound)


if TYPE_CHECKING:

    @curry
    @curry
    def compose[From, Intermediate, To](
        value: From,
        first: Callable[[From], Iterable[Intermediate]],
        second: Callable[[Intermediate], Iterable[To]],
    ) -> Iterable[To]: ...

else:
    compose = monad.compose(bind)


if TYPE_CHECKING:

    def guard(bool: bool) -> Iterable[None]: ...

else:
    guard = monad.guard(neutral)(identity)


@curry
def filter[T](iterable: Iterable[T], predicate: Predicate[T]) -> Iterable[T]:
    for value in iterable:
        if predicate(value):
            yield value


@curry
def range(stop: int, start: int) -> Iterable[int]:
    return builtins.range(start, stop)
