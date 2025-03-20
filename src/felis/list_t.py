from collections.abc import Callable
from typing import Any

from felis.currying import curry

__all__ = ["List", "apply", "join"]


List = list


# [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [From : *] -> [To : *] -> M (List (From -> To)) -> M (List From) -> M (List To)
@curry
@curry
@curry
def apply(
    m_list_value: Any,
    m_list_function: Any,
    m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]],
    m_pure: Callable[[Any], Any],
) -> Any:
    return m_bind(m_list_function)(
        lambda list_function: m_bind(m_list_value)(lambda list_value: m_pure([function(value) for function in list_function for value in list_value])),
    )


# [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [T : *] -> M (List (M (List T))) -> M (List T)
@curry
@curry
def join(m_list_m_list_value: Any, m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]], m_pure: Callable[[Any], Any]) -> Any:
    def list_m_list_binder(list_m_list_value: List[Any]) -> Any:
        m_list = m_pure([])
        for m_list_value in list_m_list_value:
            m_list = m_bind(m_list_value)(lambda addend, current_m_list=m_list: m_bind(current_m_list)(lambda augend: m_pure(augend + addend)))
        return m_list

    return m_bind(m_list_m_list_value)(list_m_list_binder)
