from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from felis.currying import curry

__all__ = ["Option", "Some", "neutral", "add", "inject"]


type Option[T] = None | Some[T]


@dataclass(frozen=True)
class Some[T]:
    value: T


# [M : Type -> Type] -> ([T : Type] -> T -> M T) -> [T : Type] -> M (Option T)
def neutral(m_identity: Callable[[Any], Any]) -> Any:
    return m_identity(None)


# [M : Type -> Type] ->
# ([From : Type] -> [To : Type] -> (From -> M To) -> M From -> M To) ->
# [T : Type] -> M (Option T) -> M (Option T) -> M (Option T)
@curry
@curry
def add(m_augend: Any, m_addend: Any, m_bind: Callable[[Callable[[Any], Any]], Callable[[Any], Any]]) -> Any:
    def augend_binder(augend: Option[Any]) -> Any:
        match augend:
            case None:
                return m_addend
            case Some(_):
                return m_augend

    return m_bind(m_augend)(augend_binder)


# [M : Type -> Type] -> ([T : Type] -> T -> M T) -> [T : Type] -> Option (M (Option T)) -> M (Option T)
@curry
def inject(option_m_option_value: Option[Any], m_identity: Callable[[Any], Any]) -> Any:
    match option_m_option_value:
        case None:
            return m_identity(None)
        case Some(m_option_value):
            return m_option_value
