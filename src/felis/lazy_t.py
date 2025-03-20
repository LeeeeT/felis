from collections.abc import Callable
from typing import Any

from felis.currying import curry

__all__ = ["Lazy", "apply", "join"]


type Lazy[T] = Callable[[], T]


# [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [From : *] -> [To : *] -> Lazy (M (From -> To)) -> Lazy (M From) -> Lazy (M To)
@curry
@curry
@curry
@curry
def apply(
    lazy_m_value: Lazy[Any],
    lazy_m_function: Lazy[Any],
    m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]],
    m_pure: Callable[[Any], Any],
) -> Lazy[Any]:
    return lambda: m_bind(lazy_m_function())(lambda function: m_bind(lazy_m_value())(lambda value: m_pure(function(value))))


# [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [T : *] -> Lazy (M (Lazy (M T))) -> Lazy (M T)
@curry
@curry
def join(lazy_m_lazy_m_value: Lazy[Any], m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]], m_pure: Callable[[Any], Any]) -> Lazy[Any]:
    return lambda: m_bind(lazy_m_lazy_m_value())(lambda m_lazy_value: m_lazy_value())
