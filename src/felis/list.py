from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import felis.alternative
import felis.applicative
import felis.functor
import felis.identity
import felis.monad
import felis.order
import felis.semigroup
from felis.alternative import Alternative
from felis.applicative import Applicative
from felis.currying import curry
from felis.functor import Functor
from felis.monad import Monad
from felis.monoid import Monoid
from felis.order import Order
from felis.predicate import Predicate
from felis.semigroup import Semigroup

__all__ = [
    "List",
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
    "fold_left",
    "fold_right",
    "functor",
    "guard",
    "join",
    "join_t",
    "lift",
    "map_by",
    "monad",
    "monoid",
    "neutral",
    "pure",
    "range_to_from",
    "semigroup",
    "sort_by",
    "take_after",
    "take_before",
    "to_add",
    "to_append",
    "to_apply",
    "to_apply_t",
    "to_bind",
    "traverse",
    "traverse_t",
    "when",
]


List = list


@curry
def to_append[T](list: List[T], value: T) -> List[T]:
    return [*list, value]


@curry
def to_add[T](augend: List[T], addend: List[T]) -> List[T]:
    return augend + addend


# [T : *] -> Semigroup (List T)
semigroup: Semigroup[List[Any]] = Semigroup(to_add)


if TYPE_CHECKING:

    @curry
    def add_to[T](addend: List[T], augend: List[T]) -> List[T]: ...

else:
    add_to = felis.semigroup.add_to(semigroup)


# [T : *] -> List T
neutral: list[Any] = []


# [T : *] -> Monoid (List T)
monoid = Monoid(semigroup, neutral)


@curry
def map_by[From, To](list_value: List[From], function: Callable[[From], To]) -> List[To]:
    return [function(value) for value in list_value]


# Functor List
functor = Functor(map_by)


if TYPE_CHECKING:

    @curry
    def by_map[From, To](function: Callable[[From], To], list_value: List[From]) -> List[To]: ...

else:
    by_map = felis.functor.by_map(functor)


def pure[T](value: T) -> List[T]:
    return [value]


# [M : * -> *] -> Monad M -> [From : *] -> [To : *] -> M (List (From -> To)) -> M (List From) -> M (List To)
@curry
@curry
def to_apply_t(m_list_value: Any, m_list_function: Any, m: Monad) -> Any:
    return felis.monad.to_bind(m)(m_list_function)(
        lambda list_function: felis.monad.to_bind(m)(m_list_value)(
            lambda list_value: felis.monad.pure(m)([function(value) for function in list_function for value in list_value]),
        ),
    )


if TYPE_CHECKING:

    @curry
    def to_apply[From, To](list_value: List[From], list_function: List[Callable[[From], To]]) -> List[To]: ...

else:
    to_apply = to_apply_t(felis.identity.monad)


# Applicative List
applicative = Applicative(functor, pure, to_apply)


if TYPE_CHECKING:

    @curry
    def apply_to[From, To](list_function: List[Callable[[From], To]], list_value: List[From]) -> List[To]: ...

else:
    apply_to = felis.applicative.apply_to(applicative)


if TYPE_CHECKING:

    @curry
    @curry
    def lift[First, Second, Result](second: List[Second], first: List[First], function: Callable[[First], Callable[[Second], Result]]) -> List[Result]: ...

else:
    lift = felis.applicative.lift(applicative)


if TYPE_CHECKING:

    @curry
    def take_after[First, Second](second: List[Second], first: List[First]) -> List[Second]: ...

else:
    take_after = felis.applicative.take_after(applicative)


if TYPE_CHECKING:

    @curry
    def discard_before[First, Second](first: List[First], second: List[Second]) -> List[Second]: ...

else:
    discard_before = felis.applicative.discard_before(applicative)


if TYPE_CHECKING:

    @curry
    def discard_after[First, Second](second: List[Second], first: List[First]) -> List[First]: ...

else:
    discard_after = felis.applicative.discard_after(applicative)


if TYPE_CHECKING:

    @curry
    def take_before[First, Second](first: List[First], second: List[Second]) -> List[First]: ...

else:
    take_before = felis.applicative.take_before(applicative)


if TYPE_CHECKING:

    @curry
    def when(list_none: List[None], bool: bool) -> List[None]: ...

else:
    when = felis.applicative.when(applicative)


# Alternative List
alternative = Alternative(monoid, applicative)


if TYPE_CHECKING:

    def guard(bool: bool, /) -> List[None]: ...

else:
    guard = felis.alternative.guard(alternative)


# [M : * -> *] -> Monad M -> [T : *] -> M (List (M (List T))) -> M (List T)
@curry
def join_t(m_list_m_list_value: Any, m: Monad) -> Any:
    def list_m_list_binder(list_m_list_value: List[Any]) -> Any:
        m_list = felis.monad.pure(m)([])
        for m_list_value in list_m_list_value:
            m_list = felis.monad.to_bind(m)(m_list_value)(
                lambda addend, current_m_list=m_list: felis.monad.to_bind(m)(current_m_list)(lambda augend: felis.monad.pure(m)(augend + addend)),
            )
        return m_list

    return felis.monad.to_bind(m)(m_list_m_list_value)(list_m_list_binder)


if TYPE_CHECKING:

    def join[T](list_list_value: List[List[T]], /) -> List[T]: ...

else:
    join = join_t(felis.identity.monad)


# Monad List
monad = Monad(applicative, join)


if TYPE_CHECKING:

    @curry
    def bind_to[From, To](list_value: List[From], function: Callable[[From], List[To]]) -> List[To]: ...

else:
    bind_to = felis.monad.bind_to(monad)


if TYPE_CHECKING:

    @curry
    def to_bind[From, To](function: Callable[[From], List[To]], list_value: List[From]) -> List[To]: ...

else:
    to_bind = felis.monad.to_bind(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_after[From, Intermediate, To](
        value: From,
        second: Callable[[Intermediate], List[To]],
        first: Callable[[From], List[Intermediate]],
    ) -> List[To]: ...

else:
    compose_after = felis.monad.compose_after(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_before[From, Intermediate, To](
        value: From,
        first: Callable[[From], List[Intermediate]],
        second: Callable[[Intermediate], List[To]],
    ) -> List[To]: ...

else:
    compose_before = felis.monad.compose_before(monad)


@curry
@curry
def fold[A, T](list_value: List[T], function: Callable[[T], Callable[[A], A]], accumulator: A) -> A:
    for value in list_value:
        accumulator = function(value)(accumulator)
    return accumulator


@curry
@curry
def fold_right[A, T](list_value: List[T], function: Callable[[T], Callable[[A], A]], accumulator: A) -> A:
    if list_value:
        return function(list_value[0])(fold_right(accumulator)(function)(list_value[1:]))
    return accumulator


@curry
@curry
def fold_left[A, T](list_value: List[T], function: Callable[[A], Callable[[T], A]], accumulator: A) -> A:
    if list_value:
        return fold_left(function(accumulator)(list_value[0]))(function)(list_value[1:])
    return accumulator


# [A : * -> *] -> Applicative A -> [From : *] -> [To : *] -> (From -> A To) -> List From -> A (List To)
@curry
def traverse_t[From](function: Callable[[From], Any], a: Applicative) -> Callable[[List[From]], Any]:
    return fold(felis.applicative.pure(a)(neutral))(felis.identity.compose_before(felis.applicative.lift(a)(to_append))(function))


if TYPE_CHECKING:

    @curry
    def traverse[From, To](list_value: List[From], function: Callable[[From], List[To]]) -> List[To]: ...

else:
    traverse = traverse_t(felis.identity.applicative)


@curry
def filter_by[T](list: List[T], predicate: Predicate[T]) -> List[T]:
    return [value for value in list if predicate(value)]


@curry
def sort_by[T](list: List[T], order: Order[T]) -> List[T]:
    return sorted(list, key=felis.order.rich_comparison(order))


@curry
def range_to_from(stop: int, start: int) -> List[int]:
    return list(range(start, stop))
