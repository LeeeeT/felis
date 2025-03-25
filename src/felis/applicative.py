from collections.abc import Callable
from typing import Any

from felis.currying import curry, flip

__all__ = ["discard_after", "discard_before", "lift2", "take_after", "take_before", "when"]


# [A : * -> *] ->
# ([From : *] -> [To : *] -> (From -> To) -> A From -> A To) ->
# ([From : *] -> [To : *] -> A (From -> To) -> A From -> A To) ->
# [First : *] -> [Second : *] -> [Result : *] -> (First -> Second -> Result) -> A First -> A Second -> A Result
@curry
@curry
@curry
def lift2(
    first: Any,
    function: Callable[[Any], Callable[[Any], Any]],
    apply: Callable[[Callable[[Any], Any]], Callable[[Any], Any]],
    map_by: Callable[[Callable[[Any], Any]], Callable[[Any], Any]],
) -> Callable[[Any], Any]:
    return apply(map_by(function)(first))


# [A : * -> *] ->
# ([First : *] -> [Second : *] -> [Result : *] -> (First -> Second -> Result) -> A First -> A Second -> A Result) ->
# [First : *] -> A First -> [Second : *] -> A Second -> A Second
def take_after(lift2: Callable[[Callable[[Any], Callable[[Any], Any]]], Callable[[Any], Callable[[Any], Any]]]) -> Callable[[Any], Callable[[Any], Any]]:
    return lift2(lambda first: lambda second: second)


# [A : * -> *] ->
# ([First : *] -> [Second : *] -> [Result : *] -> (First -> Second -> Result) -> A First -> A Second -> A Result) ->
# [Second : *] -> A Second -> [First : *] -> A First -> A Second
def discard_before(lift2: Callable[[Callable[[Any], Callable[[Any], Any]]], Callable[[Any], Callable[[Any], Any]]]) -> Callable[[Any], Callable[[Any], Any]]:
    return flip(take_after(lift2))


# [A : * -> *] ->
# ([First : *] -> [Second : *] -> [Result : *] -> (First -> Second -> Result) -> A First -> A Second -> A Result) ->
# [First : *] -> A First -> [Second : *] -> A Second -> A First
def discard_after(lift2: Callable[[Callable[[Any], Callable[[Any], Any]]], Callable[[Any], Callable[[Any], Any]]]) -> Callable[[Any], Callable[[Any], Any]]:
    return lift2(lambda first: lambda second: first)


# [A : * -> *] ->
# ([First : *] -> [Second : *] -> [Result : *] -> (First -> Second -> Result) -> A First -> A Second -> A Result) ->
# [Second : *] -> A Second -> [First : *] -> A First -> A First
def take_before(lift2: Callable[[Callable[[Any], Callable[[Any], Any]]], Callable[[Any], Callable[[Any], Any]]]) -> Callable[[Any], Callable[[Any], Any]]:
    return flip(discard_after(lift2))


# [A : * -> *] -> ([T : *] -> T -> A T) -> bool -> A None -> A None
@curry
@curry
def when(a_none: Any, bool: bool, pure: Callable[[Any], Any]) -> Any:
    return a_none if bool else pure(None)
