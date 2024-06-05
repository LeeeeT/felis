from collections.abc import Callable

from felis import list, option
from felis.currying import curry
from felis.equal import Equal
from felis.list import List
from felis.option import Option
from felis.pair import Pair

__all__ = ["Dict", "Empty", "Constructor", "construct", "lookup", "insert", "remove", "neutral", "add", "map"]


type Dict[K, V] = List[Pair[K, V]]


Empty = list.Empty


Constructor = list.Constructor


@curry
def construct[K, V](items: List[Pair[K, V]], equal: Equal[K]) -> Dict[K, V]:
    match items:
        case list.Empty():
            return neutral
        case list.Constructor(Pair(key, value), tail):
            return insert(equal)(key)(value)(construct(equal)(tail))


@curry
@curry
def lookup[K, V](dict: Dict[K, V], key: K, equal: Equal[K]) -> Option[V]:
    match dict:
        case Empty():
            return option.Nothing()
        case Constructor(Pair(current_key, current_value), tail):
            if equal(key)(current_key):
                return option.Some(current_value)
            return lookup(equal)(key)(tail)


@curry
@curry
@curry
def insert[K, V](dict: Dict[K, V], value: V, key: K, equal: Equal[K]) -> Dict[K, V]:
    return Constructor(Pair(key, value), remove(equal)(key)(dict))


@curry
@curry
def remove[K, V](dict: Dict[K, V], key: K, equal: Equal[K]) -> Dict[K, V]:
    match dict:
        case Empty():
            return Empty()
        case Constructor(Pair(current_key, current_value), tail):
            if equal(key)(current_key):
                return tail
            return Constructor(Pair(current_key, current_value), remove(equal)(key)(tail))


neutral = list.neutral


@curry
@curry
def add[K, V](augend: Dict[K, V], addend: Dict[K, V], equal: Equal[K]) -> Dict[K, V]:
    return construct(equal)(list.add(augend)(addend))


@curry
def map[K, From, To](dict_value: Dict[K, From], function: Callable[[From], To]) -> Dict[K, To]:
    match dict_value:
        case Empty():
            return Empty()
        case Constructor(Pair(key, value), tail):
            return Constructor(Pair(key, function(value)), map(function)(tail))
