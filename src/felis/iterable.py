import builtins
from collections.abc import Callable, Iterable
from typing import Never

import felis.identity
import felis.order
from felis import applicative, monad
from felis.currying import curry, uncurry
from felis.predicate import Predicate

__all__ = [
    "neutral",
    "append",
    "add",
    "map",
    "identity",
    "apply",
    "lift2",
    "when",
    "fold",
    "traverse",
    "join",
    "bind",
    "compose",
    "then",
    "guard",
    "filter",
    "range",
]


neutral: Iterable[Never] = ()


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


lift2 = applicative.lift2(map)(apply)


when = applicative.when(identity)


@curry
@curry
def fold[A, T](iterable: Iterable[T], function: Callable[[T], Callable[[A], A]], accumulator: A) -> A:
    for value in iterable:
        accumulator = function(value)(accumulator)
    return accumulator


@curry
@curry
def traverse[From, To, ATo, AIterableTo](
    function: Callable[[From], ATo],
    a_lift2: Callable[[Callable[[To], Callable[[Iterable[To]], Iterable[To]]]], Callable[[ATo], Callable[[AIterableTo], AIterableTo]]],
    a_identity: Callable[[Iterable[To]], AIterableTo],
) -> Callable[[Iterable[From]], AIterableTo]:
    return fold(a_identity(neutral))(felis.identity.compose(a_lift2(append))(function))


join = uncurry(fold)(add, neutral)


bind = monad.bind(map)(join)


compose = monad.compose(bind)


then = monad.then(bind)


guard = uncurry(monad.guard)(identity, neutral)


@curry
def filter[T](iterable: Iterable[T], predicate: Predicate[T]) -> Iterable[T]:
    for value in iterable:
        if predicate(value):
            yield value


@curry
def range(stop: int, start: int) -> Iterable[int]:
    return builtins.range(start, stop)
