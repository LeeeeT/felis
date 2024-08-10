from collections.abc import Callable
from typing import Any

from felis.currying import curry

__all__ = ["bind", "compose", "then", "guard"]


# [M : Type -> Type] ->
# ([From : Type] -> [To : Type] -> (From -> To) -> M From -> M To) ->
# ([T : Type] -> M (M T) -> M T) ->
# [From : Type] -> [To : Type] -> (From -> M To) -> M From -> M To
@curry
@curry
@curry
def bind[From](
    m_value: Any,
    function: Callable[[From], Any],
    join: Callable[[Any], Any],
    map: Callable[[Callable[[Any], Any]], Callable[[Any], Any]],
) -> Any:
    return join(map(function)(m_value))


# [M : Type -> Type] ->
# ([From : Type] -> [To : Type] -> (From -> M To) -> M From -> M To) ->
# [Intermediate : Type] -> [To : Type] -> (Intermediate -> M To) -> [From : Type] -> (From -> M Intermediate) -> From -> M To
@curry
@curry
@curry
def compose[From, Intermediate](
    value: From,
    first: Callable[[From], Any],
    second: Callable[[Intermediate], Any],
    bind: Callable[[Callable[[Any], Any]], Callable[[Any], Any]],
) -> Any:
    return bind(second)(first(value))


# [M : Type -> Type] ->
# ([From : Type] -> [To : Type] -> (From -> M To) -> M From -> M To) ->
# [Second : Type] -> M Second -> [First : Type] -> M First -> M Second
@curry
@curry
def then(first: Any, second: Any, bind: Callable[[Callable[[Any], Any]], Callable[[Any], Any]]) -> Any:
    return bind(lambda _: second)(first)


# [A : Type -> Type] -> ([T : Type] -> A T) -> ([T : Type] -> T -> A T) -> bool -> A None
@curry
@curry
def guard(bool: bool, identity: Callable[[Any], Any], neutral: Any) -> Any:
    return identity(None) if bool else neutral
