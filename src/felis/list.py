from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

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
def fold[T](list: List[T], neutral: T, add: Callable[[T], Callable[[T], T]]) -> T:
    match list:
        case Empty():
            return neutral
        case Constructor(head, tail):
            return add(fold(add)(neutral)(tail))(head)


@curry
def map[From, To](list_value: List[From], function: Callable[[From], To]) -> List[To]:
    match list_value:
        case Empty():
            return Empty()
        case Constructor(head, tail):
            return Constructor(function(head), map(function)(tail))


join = fold(add)(neutral)


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
