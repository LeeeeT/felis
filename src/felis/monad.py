from collections.abc import Callable
from typing import Any

from felis.currying import curry

__all__ = ["bound", "compose", "guard"]


# [M : Type -> Type] ->
# ([From : Type] -> [To : Type] -> (From -> To) -> M From -> M To) ->
# ([T : Type] -> M (M T) -> M T) ->
# [From : Type] -> [To : Type] -> (From -> M To) -> M From -> M To
@curry
@curry
@curry
def bound(
    m_value: Any,
    function: Callable[[Any], Any],
    join: Callable[[Any], Any],
    map: Callable[[Callable[[Any], Any]], Callable[[Any], Any]],
) -> Any:
    return join(map(function)(m_value))


# [M : Type -> Type] ->
# ([From : Type] -> [To : Type] -> M From -> (From -> M To) -> M To) ->
# [Intermediate : Type] -> [To : Type] -> (Intermediate -> M To) -> [From : Type] -> (From -> M Intermediate) -> From -> M To
@curry
@curry
@curry
def compose[From](
    value: From,
    first: Callable[[From], Any],
    second: Callable[[Any], Any],
    bind: Callable[[Callable[[Any], Any]], Callable[[Any], Any]],
) -> Any:
    return bind(first(value))(second)


# [A : Type -> Type] -> ([T : Type] -> A T) -> ([T : Type] -> T -> A T) -> bool -> A None
@curry
@curry
def guard(bool: bool, identity: Callable[[Any], Any], neutral: Any) -> Any:
    return identity(None) if bool else neutral
