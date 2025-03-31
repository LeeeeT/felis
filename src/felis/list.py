from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import felis.identity
import felis.order
from felis import applicative, monad
from felis.currying import curry, flip
from felis.order import Order
from felis.predicate import Predicate

__all__ = [
    "List",
    "add_to",
    "apply",
    "apply_t",
    "bind",
    "bind_to",
    "compose_after",
    "compose_before",
    "discard_after",
    "discard_before",
    "filter_by",
    "fold",
    "fold_left",
    "fold_right",
    "guard",
    "join",
    "join_t",
    "lift2",
    "map_by",
    "neutral",
    "pure",
    "range_to_from",
    "sort_by",
    "take_after",
    "take_before",
    "to_add",
    "to_append",
    "traverse",
    "traverse_t",
    "when",
]


List = list


# [T : *] -> List T
neutral: list[Any] = []


@curry
def to_append[T](list: List[T], value: T) -> List[T]:
    return [*list, value]


@curry
def to_add[T](augend: List[T], addend: List[T]) -> List[T]:
    return augend + addend


add_to = flip(to_add)


@curry
def map_by[From, To](list_value: List[From], function: Callable[[From], To]) -> List[To]:
    return [function(value) for value in list_value]


def pure[T](value: T) -> List[T]:
    return [value]


# [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [From : *] -> [To : *] -> M (List (From -> To)) -> M (List From) -> M (List To)
@curry
@curry
@curry
def apply_t(
    m_list_value: Any,
    m_list_function: Any,
    m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]],
    m_pure: Callable[[Any], Any],
) -> Any:
    return m_bind(m_list_function)(
        lambda list_function: m_bind(m_list_value)(lambda list_value: m_pure([function(value) for function in list_function for value in list_value])),
    )


if TYPE_CHECKING:

    @curry
    def apply[From, To](list_value: List[From], list_function: List[Callable[[From], To]]) -> List[To]: ...

else:
    apply = apply_t(felis.identity.pure)(felis.identity.bind)


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[First, Second, Result](second: List[Second], first: List[First], function: Callable[[First], Callable[[Second], Result]]) -> List[Result]: ...

else:
    lift2 = applicative.lift2(map_by)(apply)


if TYPE_CHECKING:

    @curry
    def take_after[First, Second](second: List[Second], first: List[First]) -> List[Second]: ...

else:
    take_after = applicative.take_after(lift2)


if TYPE_CHECKING:

    @curry
    def discard_before[First, Second](first: List[First], second: List[Second]) -> List[Second]: ...

else:
    discard_before = applicative.discard_before(lift2)


if TYPE_CHECKING:

    @curry
    def discard_after[First, Second](second: List[Second], first: List[First]) -> List[First]: ...

else:
    discard_after = applicative.discard_after(lift2)


if TYPE_CHECKING:

    @curry
    def take_before[First, Second](first: List[First], second: List[Second]) -> List[First]: ...

else:
    take_before = applicative.take_before(lift2)


if TYPE_CHECKING:

    @curry
    def when(list_none: List[None], bool: bool) -> List[None]: ...

else:
    when = applicative.when(pure)


# [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [T : *] -> M (List (M (List T))) -> M (List T)
@curry
@curry
def join_t(m_list_m_list_value: Any, m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]], m_pure: Callable[[Any], Any]) -> Any:
    def list_m_list_binder(list_m_list_value: List[Any]) -> Any:
        m_list = m_pure([])
        for m_list_value in list_m_list_value:
            m_list = m_bind(m_list_value)(lambda addend, current_m_list=m_list: m_bind(current_m_list)(lambda augend: m_pure(augend + addend)))
        return m_list

    return m_bind(m_list_m_list_value)(list_m_list_binder)


if TYPE_CHECKING:

    def join[T](list_list_value: List[List[T]]) -> List[T]: ...

else:
    join = join_t(felis.identity.pure)(felis.identity.bind)


if TYPE_CHECKING:

    @curry
    def bind_to[From, To](list_value: List[From], function: Callable[[From], List[To]]) -> List[To]: ...

else:
    bind_to = monad.bind_to(map_by)(join)


bind = flip(bind_to)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_after[From, Intermediate, To](
        value: From,
        second: Callable[[Intermediate], List[To]],
        first: Callable[[From], List[Intermediate]],
    ) -> List[To]: ...

else:
    compose_after = monad.compose_after(bind)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_before[From, Intermediate, To](
        value: From,
        first: Callable[[From], List[Intermediate]],
        second: Callable[[Intermediate], List[To]],
    ) -> List[To]: ...

else:
    compose_before = monad.compose_before(bind)


if TYPE_CHECKING:

    def guard(bool: bool) -> List[None]: ...

else:
    guard = monad.guard(neutral)(pure)


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


# [A : * -> *] ->
# ([From : *] -> [To : *] -> (From -> To) -> A From -> A To) ->
# ([T : *] -> T -> A T) ->
# [From : *] -> [To : *] -> (From -> A To) -> List From -> A (List To)
@curry
@curry
def traverse_t[From](
    function: Callable[[From], Any],
    a_lift2: Callable[[Callable[[Any], Callable[[Any], Any]]], Callable[[Any], Callable[[Any], Any]]],
    a_pure: Callable[[Any], Any],
) -> Callable[[List[From]], Any]:
    return fold(a_pure(neutral))(felis.identity.compose_before(a_lift2(to_append))(function))


if TYPE_CHECKING:

    @curry
    def traverse[From, To](list_value: List[From], function: Callable[[From], List[To]]) -> List[To]: ...

else:
    traverse = traverse_t(felis.identity.pure)(felis.identity.bind)


@curry
def filter_by[T](list: List[T], predicate: Predicate[T]) -> List[T]:
    return [value for value in list if predicate(value)]


@curry
def sort_by[T](list: List[T], order: Order[T]) -> List[T]:
    return sorted(list, key=felis.order.rich_comparison(order))


@curry
def range_to_from(stop: int, start: int) -> List[int]:
    return list(range(start, stop))
