from collections.abc import Callable
from typing import Any, Final

from felis.currying import flip

__all__ = ["Functor", "by_map", "map_by"]


# [F : * -> *] -> ([From : *] -> [To : *] -> (From -> To) -> F From -> F To) -> Functor F
class Functor:
    def __init__(self, map_by: Callable[[Callable[[Any], Any]], Callable[[Any], Any]]):
        self.map_by: Final = map_by


# [F : * -> *] -> Functor F -> [From : *] -> [To : *] -> (From -> To) -> F From -> F To
def map_by(instance: Functor) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
    return instance.map_by


# [F : * -> *] -> Functor F -> [From : *] -> F From -> [To : *] -> (From -> To) -> F To
def by_map(instance: Functor) -> Callable[[Any], Callable[[Callable[[Any], Any]], Any]]:
    return flip(map_by(instance))
