from collections.abc import Callable
from typing import Any

from felis import option
from felis.currying import curry
from felis.option import Option

__all__ = ["neutral", "set", "get", "add", "map"]


# [K : Type] -> [V : Type] -> dict K V
neutral: dict[Any, Any] = {}


@curry
@curry
def set[K, V](dict: dict[K, V], value: V, key: K) -> dict[K, V]:
    return {**dict, key: value}


@curry
def get[K, V](dict: dict[K, V], key: K) -> Option[V]:
    return option.Some(dict[key]) if key in dict else None


@curry
def add[K, V](augend: dict[K, V], addend: dict[K, V]) -> dict[K, V]:
    return {**augend, **addend}


@curry
def map[K, From, To](dict_value: dict[K, From], function: Callable[[From], To]) -> dict[K, To]:
    return {key: function(value) for key, value in dict_value.items()}
