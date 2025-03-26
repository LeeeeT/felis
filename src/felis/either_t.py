from collections.abc import Callable
from typing import Any, Final

from felis.currying import curry

__all__ = ["Either", "Left", "Right", "apply", "default_to", "join", "to_add"]


type Either[L, R] = Left[L] | Right[R]


class Left[T]:
    __match_args__ = ("value",)

    def __init__(self, value: T):
        self.value: Final = value


class Right[T]:
    __match_args__ = ("value",)

    def __init__(self, value: T):
        self.value: Final = value


# [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [L : *] -> [R : *] -> M (Either L R) -> M (Either L R) -> M (Either L R)
@curry
@curry
@curry
def to_add(m_augend: Any, m_addend: Any, m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]], m_pure: Callable[[Any], Any]) -> Any:
    def augend_binder(augend: Either[Any, Any]) -> Any:
        match augend:
            case Left(_):
                return m_addend
            case Right(right):
                return m_pure(Right(right))

    return m_bind(m_augend)(augend_binder)


# [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [L : *] -> [From : *] -> [To : *] -> M (Either L (From -> To)) -> M (Either L From) -> M (Either L To)
@curry
@curry
@curry
def apply(
    m_either_value: Any,
    m_either_function: Any,
    m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]],
    m_pure: Callable[[Any], Any],
) -> Any:
    def either_function_binder(either_function: Either[Any, Any]) -> Any:
        match either_function:
            case Left(left):
                return m_pure(Left(left))
            case Right(function):

                def either_value_binder(either_value: Either[Any, Any]) -> Any:
                    match either_value:
                        case Left(left):
                            return m_pure(Left(left))
                        case Right(value):
                            return m_pure(Right(function(value)))

                return m_bind(m_either_value)(either_value_binder)

    return m_bind(m_either_function)(either_function_binder)


# [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [L : *] -> [R : *] -> M (Either L (M (Either L R))) -> M (Either L R)
@curry
@curry
def join(m_either_m_either_value: Any, m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]], m_pure: Callable[[Any], Any]) -> Any:
    def either_m_either_binder(either_m_either_value: Either[Any, Any]) -> Any:
        match either_m_either_value:
            case Left(left):
                return m_pure(Left(left))
            case Right(m_either_value):
                return m_either_value

    return m_bind(m_either_m_either_value)(either_m_either_binder)


# [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [L : *] -> [R : *] -> M R -> M (Either L R) -> M R
@curry
@curry
@curry
def default_to(
    m_either_value: Any,
    default_value: Any,
    m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]],
    m_pure: Callable[[Any], Any],
) -> Any:
    def either_binder(either_value: Either[Any, Any]) -> Any:
        match either_value:
            case Left(_):
                return default_value
            case Right(value):
                return m_pure(value)

    return m_bind(m_either_value)(either_binder)
