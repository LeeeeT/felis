from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from felis.currying import curry

__all__ = ["Option", "Some", "add", "apply", "default", "join", "neutral"]


type Option[T] = None | Some[T]


@dataclass(frozen=True)
class Some[T]:
    value: T


# [M : * -> *] -> ([T : *] -> T -> M T) -> [T : *] -> M (Option T)
def neutral(m_identity: Callable[[Any], Any]) -> Any:
    return m_identity(None)


# [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [T : *] -> M (Option T) -> M (Option T) -> M (Option T)
@curry
@curry
@curry
def add(m_augend: Any, m_addend: Any, m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]], m_identity: Callable[[Any], Any]) -> Any:
    def augend_binder(augend: Option[Any]) -> Any:
        match augend:
            case None:
                return m_addend
            case Some(value):
                return m_identity(Some(value))

    return m_bind(m_augend)(augend_binder)


# [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [From : *] -> [To : *] -> M (Option (From -> To)) -> M (Option From) -> M (Option To)
@curry
@curry
@curry
def apply(
    m_either_value: Any,
    m_either_function: Any,
    m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]],
    m_identity: Callable[[Any], Any],
) -> Any:
    def option_function_binder(option_function: Option[Callable[[Any], Any]]) -> Any:
        match option_function:
            case None:
                return m_identity(None)
            case Some(function):

                def option_value_binder(option_value: Option[Any]) -> Any:
                    match option_value:
                        case None:
                            return m_identity(None)
                        case Some(value):
                            return m_identity(Some(function(value)))

                return m_bind(m_either_value)(option_value_binder)

    return m_bind(m_either_function)(option_function_binder)


# [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [T : *] -> M (Option (M (Option T))) -> M (Option T)
@curry
@curry
def join(m_option_m_option_value: Any, m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]], m_identity: Callable[[Any], Any]) -> Any:
    def binder(option_m_option_value: Option[Any]) -> Any:
        match option_m_option_value:
            case None:
                return m_identity(None)
            case Some(m_option_value):
                return m_option_value

    return m_bind(m_option_m_option_value)(binder)


# [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [T : *] -> M T -> M (Option T) -> M T
@curry
@curry
@curry
def default(
    m_option_value: Any,
    default_value: Any,
    m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]],
    m_identity: Callable[[Any], Any],
) -> Any:
    def binder(option_value: Option[Any]) -> Any:
        match option_value:
            case None:
                return default_value
            case Some(value):
                return m_identity(value)

    return m_bind(m_option_value)(binder)
