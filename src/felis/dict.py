from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import felis.functor
import felis.semigroup
from felis import option
from felis.currying import curry
from felis.functor import Functor
from felis.monoid import Monoid
from felis.option import Option
from felis.semigroup import Semigroup

__all__ = [
    "Dict",
    "add_to",
    "by_map",
    "functor",
    "in_get",
    "in_to_set",
    "map_by",
    "monoid",
    "neutral",
    "semigroup",
    "to_add",
]


Dict = dict


@curry
def to_add[K, V](augend: Dict[K, V], addend: Dict[K, V]) -> Dict[K, V]:
    return {**augend, **addend}


# [K : *] -> [V : *] -> Semigroup (Dict K V)
semigroup: Semigroup[Dict[Any, Any]] = Semigroup(to_add)


if TYPE_CHECKING:

    @curry
    def add_to[K, V](addend: Dict[K, V], augend: Dict[K, V]) -> Dict[K, V]: ...

else:
    add_to = felis.semigroup.add_to(semigroup)


# [K : *] -> [V : *] -> Dict K V
neutral: Dict[Any, Any] = {}


# [K : *] -> [V : *] -> Monoid (Dict K V)
monoid = Monoid(semigroup, neutral)


@curry
def map_by[K, From, To](dict_value: Dict[K, From], function: Callable[[From], To]) -> Dict[K, To]:
    return {key: function(value) for key, value in dict_value.items()}


# [K : *] -> Functor (Dict K)
functor = Functor(map_by)


if TYPE_CHECKING:

    @curry
    def by_map[K, From, To](function: Callable[[From], To], dict_value: Dict[K, From]) -> Dict[K, To]: ...

else:
    by_map = felis.functor.by_map(functor)


@curry
@curry
def in_to_set[K, V](dict: Dict[K, V], value: V, key: K) -> Dict[K, V]:
    return {**dict, key: value}


@curry
def in_get[K, V](dict: Dict[K, V], key: K) -> Option[V]:
    return option.Some(dict[key]) if key in dict else None
