from collections.abc import Callable
from typing import Any

from felis.currying import curry

__all__ = ["lift2", "when"]


# [A : Type -> Type] ->
# ([From : Type] -> [To : Type] -> (From -> To) -> A From -> A To) ->
# ([From : Type] -> [To : Type] -> A (From -> To) -> A From -> A To) ->
# [First : Type] -> [Second : Type] -> [Result : Type] -> (First -> Second -> Result) -> A First -> A Second -> A Result
@curry
@curry
@curry
def lift2(
    first: Any,
    function: Callable[[Any], Callable[[Any], Any]],
    apply: Callable[[Callable[[Any], Any]], Callable[[Any], Any]],
    map: Callable[[Callable[[Any], Any]], Callable[[Any], Any]],
) -> Callable[[Any], Any]:
    return apply(map(function)(first))


# [A : Type -> Type] -> ([T : Type] -> T -> A T) -> bool -> A None -> A None
@curry
@curry
def when(a_none: Any, bool: bool, identity: Callable[[Any], Any]) -> Any:
    return a_none if bool else identity(None)
