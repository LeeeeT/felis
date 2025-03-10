from collections.abc import Callable
from typing import Any

from felis.currying import curry

__all__ = ["Lazy", "join"]


type Lazy[T] = Callable[[], T]


# [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [T : *] -> Lazy (M (Lazy (M T))) -> Lazy (M T)
@curry
@curry
def join(lazy_m_lazy_m_value: Lazy[Any], m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]], m_identity: Callable[[Any], Any]) -> Lazy[Any]:
    return lambda: m_bind(lazy_m_lazy_m_value())(lambda m_lazy_value: m_lazy_value())
