from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol, cast

import felis.order
from felis import monad
from felis.currying import curry
from felis.order import Order
from felis.predicate import Predicate

__all__ = ["List", "Empty", "Constructor", "identity", "map", "join", "bind", "compose", "then", "fold", "filter", "sort"]


type List[T] = Empty | Constructor[T]


@dataclass(frozen=True)
class Empty:
    pass


@dataclass(frozen=True)
class Constructor[T]:
    head: T
    tail: List[T]


neutral = Empty()


@curry
def add[T](augend: List[T], addend: List[T]) -> List[T]:
    match augend:
        case Empty():
            return addend
        case Constructor(head, tail):
            return Constructor(head, add(addend)(tail))


def identity[T](value: T) -> List[T]:
    return Constructor(value, Empty())


@curry
@curry
def fold[M](list: List[M], add: Callable[[M], Callable[[M], M]], neutral: M) -> M:
    match list:
        case Empty():
            return neutral
        case Constructor(head, tail):
            return add(fold(neutral)(add)(tail))(head)


@curry
def map[From, To](list_value: List[From], function: Callable[[From], To]) -> List[To]:
    match list_value:
        case Empty():
            return Empty()
        case Constructor(head, tail):
            return Constructor(function(head), map(function)(tail))


# TODO: remove this
class Join(Protocol):
    def __call__[T](self, list_list_value: List[List[T]], /) -> List[T]: ...


# TODO: remove the cast
join = cast(Join, fold(neutral)(add))  # type: ignore


bind = monad.bind(map)(join)


compose = monad.compose(bind)


then = monad.then(bind)


@curry
def filter[T](list: List[T], predicate: Predicate[T]) -> List[T]:
    match list:
        case Empty():
            return Empty()
        case Constructor(head, tail):
            return Constructor(head, filter(predicate)(tail)) if predicate(head) else filter(predicate)(tail)


@curry
def sort[T](list: List[T], order: Order[T]) -> List[T]:
    match list:
        case Empty():
            return Empty()
        case Constructor(head, tail):
            worse = filter(felis.order.worse(order)(head))(tail)
            not_worse = filter(felis.order.not_worse(order)(head))(tail)
            return add(sort(order)(not_worse))(add(identity(head))(sort(order)(worse)))
