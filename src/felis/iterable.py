import builtins
from collections.abc import Callable, Iterable
from typing import TYPE_CHECKING, Any

import felis.identity
from felis import applicative, monad
from felis.currying import curry, flip
from felis.predicate import Predicate

__all__ = [
    "Iterable",
    "add_to",
    "apply",
    "bind",
    "bind_to",
    "compose_after",
    "compose_before",
    "discard_after",
    "discard_before",
    "filter_by",
    "fold",
    "guard",
    "join",
    "lift2",
    "map_by",
    "neutral",
    "pure",
    "range_to_from",
    "take_after",
    "take_before",
    "to_add",
    "to_append",
    "traverse",
    "when",
]


# [T : *] -> Iterable T
neutral: Iterable[Any] = ()


@curry
def to_append[T](iterable: Iterable[T], value: T) -> Iterable[T]:
    yield from iterable
    yield value


@curry
def to_add[T](augend: Iterable[T], addend: Iterable[T]) -> Iterable[T]:
    yield from augend
    yield from addend


add_to = flip(to_add)


@curry
def map_by[From, To](iterable_value: Iterable[From], function: Callable[[From], To]) -> Iterable[To]:
    for value in iterable_value:
        yield function(value)


def pure[T](value: T) -> Iterable[T]:
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
    lift2 = applicative.lift2(map_by)(apply)


if TYPE_CHECKING:

    @curry
    def take_after[First, Second](second: Iterable[Second], first: Iterable[First]) -> Iterable[Second]: ...

else:
    take_after = applicative.take_after(lift2)


if TYPE_CHECKING:

    @curry
    def discard_before[First, Second](first: Iterable[First], second: Iterable[Second]) -> Iterable[Second]: ...

else:
    discard_before = applicative.discard_before(lift2)


if TYPE_CHECKING:

    @curry
    def discard_after[First, Second](second: Iterable[Second], first: Iterable[First]) -> Iterable[First]: ...

else:
    discard_after = applicative.discard_after(lift2)


if TYPE_CHECKING:

    @curry
    def take_before[First, Second](first: Iterable[First], second: Iterable[Second]) -> Iterable[First]: ...

else:
    take_before = applicative.take_before(lift2)


if TYPE_CHECKING:

    @curry
    def when(iterable_none: Iterable[None], bool: bool) -> Iterable[None]: ...

else:
    when = applicative.when(pure)


@curry
@curry
def fold[A, T](iterable_value: Iterable[T], function: Callable[[T], Callable[[A], A]], accumulator: A) -> A:
    for value in iterable_value:
        accumulator = function(value)(accumulator)
    return accumulator


# [A : * -> *] ->
# ([From : *] -> [To : *] -> (From -> To) -> A From -> A To) ->
# ([T : *] -> T -> A T) ->
# [From : *] -> [To : *] -> (From -> A To) -> Iterable From -> A (Iterable To)
@curry
@curry
def traverse[From](
    function: Callable[[From], Any],
    a_lift2: Callable[[Callable[[Any], Callable[[Any], Any]]], Callable[[Any], Callable[[Any], Any]]],
    a_identity: Callable[[Any], Any],
) -> Callable[[Iterable[From]], Any]:
    return fold(a_identity(neutral))(felis.identity.compose_before(a_lift2(to_append))(function))


if TYPE_CHECKING:

    def join[T](iterable_iterable_value: Iterable[Iterable[T]]) -> Iterable[T]: ...

else:
    join = fold(neutral)(to_add)


if TYPE_CHECKING:

    @curry
    def bind_to[From, To](iterable_value: Iterable[From], function: Callable[[From], Iterable[To]]) -> Iterable[To]: ...

else:
    bind_to = monad.bind_to(map_by)(join)


bind = flip(bind_to)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_after[From, Intermediate, To](
        value: From,
        second: Callable[[Intermediate], Iterable[To]],
        first: Callable[[From], Iterable[Intermediate]],
    ) -> Iterable[To]: ...

else:
    compose_after = monad.compose_after(bind)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_before[From, Intermediate, To](
        value: From,
        first: Callable[[From], Iterable[Intermediate]],
        second: Callable[[Intermediate], Iterable[To]],
    ) -> Iterable[To]: ...

else:
    compose_before = monad.compose_before(bind)


if TYPE_CHECKING:

    def guard(bool: bool) -> Iterable[None]: ...

else:
    guard = monad.guard(neutral)(pure)


@curry
def filter_by[T](iterable: Iterable[T], predicate: Predicate[T]) -> Iterable[T]:
    for value in iterable:
        if predicate(value):
            yield value


@curry
def range_to_from(stop: int, start: int) -> Iterable[int]:
    return builtins.range(start, stop)
