from collections.abc import Callable
from typing import Any

from felis import option
from felis.currying import curry
from felis.option import Option

__all__ = ["Dict", "neutral", "set", "get", "add", "map"]


Dict = dict


# [K : Type] -> [V : Type] -> dict K V
neutral: dict[Any, Any] = {}


@curry
@curry
def set[K, V](dict: Dict[K, V], value: V, key: K) -> Dict[K, V]:
    return {**dict, key: value}


@curry
def get[K, V](dict: Dict[K, V], key: K) -> Option[V]:
    return option.Some(dict[key]) if key in dict else None


@curry
def add[K, V](augend: Dict[K, V], addend: Dict[K, V]) -> Dict[K, V]:
    return {**augend, **addend}


@curry
def map[K, From, To](dict_value: Dict[K, From], function: Callable[[From], To]) -> Dict[K, To]:
    return {key: function(value) for key, value in dict_value.items()}
