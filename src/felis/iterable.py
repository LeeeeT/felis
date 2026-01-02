import builtins
from collections.abc import Callable, Iterable
from typing import TYPE_CHECKING, Any

import felis.alternative
import felis.applicative
import felis.functor
import felis.identity
import felis.monad
import felis.semigroup
from felis.alternative import Alternative
from felis.applicative import Applicative
from felis.currying import curry
from felis.functor import Functor
from felis.monad import Monad
from felis.monoid import Monoid
from felis.predicate import Predicate
from felis.semigroup import Semigroup

__all__ = [
    "Iterable",
    "add_to",
    "alternative",
    "applicative",
    "apply_to",
    "bind_to",
    "by_map",
    "compose_after",
    "compose_before",
    "discard_after",
    "discard_before",
    "filter_by",
    "fold",
    "functor",
    "guard",
    "join",
    "lift",
    "map_by",
    "monad",
    "monoid",
    "neutral",
    "pure",
    "range_to_from",
    "semigroup",
    "take_after",
    "take_before",
    "to_add",
    "to_append",
    "to_apply",
    "to_bind",
    "traverse",
    "when",
]


@curry
def to_append[T](iterable: Iterable[T], value: T) -> Iterable[T]:
    yield from iterable
    yield value


@curry
def to_add[T](augend: Iterable[T], addend: Iterable[T]) -> Iterable[T]:
    yield from augend
    yield from addend


# [T : *] -> Semigroup (Iterable T)
semigroup: Semigroup[Iterable[Any]] = Semigroup(to_add)


if TYPE_CHECKING:

    @curry
    def add_to[T](addend: Iterable[T], augend: Iterable[T]) -> Iterable[T]: ...

else:
    add_to = felis.semigroup.add_to(semigroup)


# [T : *] -> Iterable T
neutral: Iterable[Any] = ()


monoid = Monoid(semigroup, neutral)


@curry
def map_by[From, To](iterable_value: Iterable[From], function: Callable[[From], To]) -> Iterable[To]:
    for value in iterable_value:
        yield function(value)


# Functor Iterable
functor = Functor(map_by)


if TYPE_CHECKING:

    @curry
    def by_map[From, To](function: Callable[[From], To], iterable_value: Iterable[From]) -> Iterable[To]: ...

else:
    by_map = felis.functor.by_map(functor)


def pure[T](value: T) -> Iterable[T]:
    yield value


@curry
def to_apply[From, To](iterable_value: Iterable[From], iterable_function: Iterable[Callable[[From], To]]) -> Iterable[To]:
    for function in iterable_function:
        for value in iterable_value:
            yield function(value)


# Applicative Iterable
applicative = Applicative(functor, pure, to_apply)


if TYPE_CHECKING:

    @curry
    def apply_to[From, To](iterable_function: Iterable[Callable[[From], To]], iterable_value: Iterable[From]) -> Iterable[To]: ...

else:
    apply_to = felis.applicative.apply_to(applicative)


if TYPE_CHECKING:

    @curry
    @curry
    def lift[First, Second, Result](
        second: Iterable[Second],
        first: Iterable[First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> Iterable[Result]: ...

else:
    lift = felis.applicative.lift(applicative)


if TYPE_CHECKING:

    @curry
    def take_after[First, Second](second: Iterable[Second], first: Iterable[First]) -> Iterable[Second]: ...

else:
    take_after = felis.applicative.take_after(applicative)


if TYPE_CHECKING:

    @curry
    def discard_before[First, Second](first: Iterable[First], second: Iterable[Second]) -> Iterable[Second]: ...

else:
    discard_before = felis.applicative.discard_before(applicative)


if TYPE_CHECKING:

    @curry
    def discard_after[First, Second](second: Iterable[Second], first: Iterable[First]) -> Iterable[First]: ...

else:
    discard_after = felis.applicative.discard_after(applicative)


if TYPE_CHECKING:

    @curry
    def take_before[First, Second](first: Iterable[First], second: Iterable[Second]) -> Iterable[First]: ...

else:
    take_before = felis.applicative.take_before(applicative)


if TYPE_CHECKING:

    @curry
    def when(iterable_none: Iterable[None], bool: bool) -> Iterable[None]: ...

else:
    when = felis.applicative.when(applicative)


# Alternative Iterable
alternative = Alternative(monoid, applicative)


if TYPE_CHECKING:

    def guard(bool: bool, /) -> Iterable[None]: ...

else:
    guard = felis.alternative.guard(alternative)


@curry
@curry
def fold[A, T](iterable_value: Iterable[T], function: Callable[[T], Callable[[A], A]], accumulator: A) -> A:
    for value in iterable_value:
        accumulator = function(value)(accumulator)
    return accumulator


# [A : * -> *] -> Applicative A -> [From : *] -> [To : *] -> (From -> A To) -> Iterable From -> A (Iterable To)
@curry
@curry
def traverse[From](function: Callable[[From], Any], a: Applicative) -> Callable[[Iterable[From]], Any]:
    return fold(felis.applicative.pure(a)(neutral))(felis.identity.compose_before(felis.applicative.lift(a)(to_append))(function))


if TYPE_CHECKING:

    def join[T](iterable_iterable_value: Iterable[Iterable[T]], /) -> Iterable[T]: ...

else:
    join = fold(neutral)(to_add)


# Monad Iterable
monad = Monad(applicative, join)


if TYPE_CHECKING:

    @curry
    def bind_to[From, To](iterable_value: Iterable[From], function: Callable[[From], Iterable[To]]) -> Iterable[To]: ...

else:
    bind_to = felis.monad.bind_to(monad)


if TYPE_CHECKING:

    @curry
    def to_bind[From, To](function: Callable[[From], Iterable[To]], iterable_value: Iterable[From]) -> Iterable[To]: ...

else:
    to_bind = felis.monad.to_bind(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_after[From, Intermediate, To](
        value: From,
        second: Callable[[Intermediate], Iterable[To]],
        first: Callable[[From], Iterable[Intermediate]],
    ) -> Iterable[To]: ...

else:
    compose_after = felis.monad.compose_after(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_before[From, Intermediate, To](
        value: From,
        first: Callable[[From], Iterable[Intermediate]],
        second: Callable[[Intermediate], Iterable[To]],
    ) -> Iterable[To]: ...

else:
    compose_before = felis.monad.compose_before(monad)


@curry
def filter_by[T](iterable: Iterable[T], predicate: Predicate[T]) -> Iterable[T]:
    for value in iterable:
        if predicate(value):
            yield value


@curry
def range_to_from(stop: int, start: int) -> Iterable[int]:
    return builtins.range(start, stop)

