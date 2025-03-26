from collections.abc import Callable
from typing import Any, Final

from felis.currying import curry

__all__ = ["Option", "Some", "apply", "default_to", "join", "neutral", "to_add", "to_either"]


type Option[T] = None | Some[T]


class Some[T]:
    __match_args__ = ("value",)

    def __init__(self, value: T):
        self.value: Final = value


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
def to_add(m_augend: Any, m_addend: Any, m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]], m_pure: Callable[[Any], Any]) -> Any:
    def augend_binder(augend: Option[Any]) -> Any:
        match augend:
            case None:
                return m_addend
            case Some(value):
                return m_pure(Some(value))

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
    m_pure: Callable[[Any], Any],
) -> Any:
    def option_function_binder(option_function: Option[Callable[[Any], Any]]) -> Any:
        match option_function:
            case None:
                return m_pure(None)
            case Some(function):

                def option_value_binder(option_value: Option[Any]) -> Any:
                    match option_value:
                        case None:
                            return m_pure(None)
                        case Some(value):
                            return m_pure(Some(function(value)))

                return m_bind(m_either_value)(option_value_binder)

    return m_bind(m_either_function)(option_function_binder)


# [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [T : *] -> M (Option (M (Option T))) -> M (Option T)
@curry
@curry
def join(m_option_m_option_value: Any, m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]], m_pure: Callable[[Any], Any]) -> Any:
    def binder(option_m_option_value: Option[Any]) -> Any:
        match option_m_option_value:
            case None:
                return m_pure(None)
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
def default_to(
    m_option_value: Any,
    default_value: Any,
    m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]],
    m_pure: Callable[[Any], Any],
) -> Any:
    def binder(option_value: Option[Any]) -> Any:
        match option_value:
            case None:
                return default_value
            case Some(value):
                return m_pure(value)

    return m_bind(m_option_value)(binder)


# [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [L : *] -> M L -> [R : *] -> M (Option R) -> M (Either L R)
@curry
@curry
@curry
def to_either(m_option_value: Option[Any], m_left: Any, m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]], m_pure: Callable[[Any], Any]) -> Any:
    from felis import either

    def binder(option_value: Option[Any]) -> Any:
        match option_value:
            case None:
                return m_bind(m_left)(lambda left: m_pure(either.Left(left)))
            case Some(value):
                return m_pure(either.Right(value))

    return m_bind(m_option_value)(binder)
