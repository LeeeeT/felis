from collections.abc import Callable
from typing import Any

from felis.currying import curry

__all__ = ["lift2", "when"]


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


# [A : * -> *] -> ([T : *] -> T -> A T) -> bool -> A None -> A None
@curry
@curry
def when(a_none: Any, bool: bool, pure: Callable[[Any], Any]) -> Any:
    return a_none if bool else pure(None)
