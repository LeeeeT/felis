from collections.abc import Callable
from typing import Any

from felis.currying import curry

__all__ = ["bind_to", "compose", "guard"]


# [M : * -> *] ->
# ([From : *] -> [To : *] -> (From -> To) -> M From -> M To) ->
# ([T : *] -> M (M T) -> M T) ->
# [From : *] -> [To : *] -> (From -> M To) -> M From -> M To
@curry
@curry
@curry
def bind_to(
    m_value: Any,
    function: Callable[[Any], Any],
    join: Callable[[Any], Any],
    map_by: Callable[[Callable[[Any], Any]], Callable[[Any], Any]],
) -> Any:
    return join(map_by(function)(m_value))


# [M : * -> *] ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [Intermediate : *] -> [To : *] -> (Intermediate -> M To) -> [From : *] -> (From -> M Intermediate) -> From -> M To
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


# [A : * -> *] -> ([T : *] -> A T) -> ([T : *] -> T -> A T) -> bool -> A None
@curry
@curry
def guard(bool: bool, identity: Callable[[Any], Any], neutral: Any) -> Any:
    return identity(None) if bool else neutral
