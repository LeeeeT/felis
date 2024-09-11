from collections.abc import Callable
from typing import Any

from felis.currying import curry
from felis.lazy import Lazy

__all__ = [
    "run",
    "neutral",
    "add",
    "map",
    "identity",
    "apply",
    "join",
    "reversed_apply",
    "reversed_join",
]


# [S : Type] -> [M : Type -> Type] -> ([From : Type] -> [To : Type] -> (From -> To) -> M From -> M To) -> [T : Type] -> StateT S M T -> S -> M T
@curry
@curry
def run[S](state: S, state_value: Callable[[S], Any], m_map: Callable[[Callable[[Any], Any]], Callable[[Any], Any]]) -> Any:
    def value_mapper(value_and_state: tuple[Any, S]) -> Any:
        value, _ = value_and_state
        return value

    return m_map(value_mapper)(state_value(state))


# [S : Type] -> [M : Type -> Type] -> ([T : Type] -> M T) -> [T : Type] -> StateT S M T
@curry
def neutral(state: Any, m_neutral: Any) -> Any:
    return m_neutral


# [S : Type] -> [M : Type -> Type] -> ([T : Type] -> M T -> M T -> M T) -> [T : Type] -> StateT S M T -> StateT S M T -> StateT S M T
@curry
@curry
@curry
def add[S](state: S, first: Callable[[S], Any], second: Callable[[S], Any], m_add: Callable[[Any], Any]) -> Any:
    return m_add(second(state))(first(state))


# [S : Type] -> [M : Type -> Type] ->
# ([From : Type] -> [To : Type] -> (From -> To) -> M From -> T To) ->
# [From : Type] -> [To : Type] -> (From -> To) -> StateT S M From -> StateT S M To
@curry
@curry
@curry
def map[S](
    state: S,
    state_value: Callable[[S], Any],
    function: Callable[[Any], Any],
    m_map: Callable[[Callable[[Any], Any]], Callable[[Any], Any]],
) -> Any:
    def value_mapper(value_and_state: tuple[Any, S]) -> tuple[Any, S]:
        value, state = value_and_state
        return function(value), state

    return m_map(value_mapper)(state_value(state))


# [S : Type] -> [M : Type -> Type] -> ([T : Type] -> T -> M T) -> [T : Type] -> T -> StateT S M T
@curry
@curry
def identity(state: Any, value: Any, m_identity: Callable[[Any], Any]) -> Any:
    return m_identity((value, state))


# [S : Type] -> [M : Type -> Type] ->
# ([T : Type] -> T -> M T) ->
# ([From : Type] -> [To : Type] -> M From -> (From -> M To) -> M To) ->
# [From : Type] -> [To : Type] -> StateT S M (From -> To) -> StateT S M From -> StateT S M To
@curry
@curry
@curry
@curry
def apply[S](
    state: S,
    state_value: Callable[[S], Any],
    state_function: Callable[[S], Any],
    m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]],
    m_identity: Callable[[Any], Any],
) -> Any:
    def function_binder(function_and_state: tuple[Callable[[Any], Any], S]) -> Any:
        function, state = function_and_state

        def value_binder(value_and_state: tuple[Any, S]) -> Any:
            value, state = value_and_state
            return m_identity((function(value), state))

        return m_bind(state_value(state))(value_binder)

    return m_bind(state_function(state))(function_binder)


# [S : Type] -> [M : Type -> Type] ->
# ([T : Type] -> T -> M T) ->
# ([From : Type] -> [To : Type] -> M From -> (From -> M To) -> M To) ->
# [T : Type] -> StateT S M (StateT S M T) -> StateT S M T
@curry
@curry
@curry
def join[S](
    state: S,
    state_state_value: Callable[[S], Any],
    m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]],
    m_identity: Callable[[Any], Any],
) -> Any:
    def state_value_binder(state_value_and_state: tuple[Any, S]) -> Any:
        state_value, state = state_value_and_state

        def value_binder(value_and_state: tuple[Any, S]) -> Any:
            value, state = value_and_state
            return m_identity((value, state))

        return m_bind(state_value(state))(value_binder)

    return m_bind(state_state_value(state))(state_value_binder)


# [S : Type] -> [M : Type -> Type] ->
# ([T : Type] -> T -> M T) ->
# ([From : Type] -> [To : Type] -> M From -> (From -> M To) -> M To) ->
# [From : Type] -> [To : Type] -> ReversedStateT S M (From -> To) -> ReversedStateT S M From -> ReversedStateT S M To
@curry
@curry
@curry
@curry
def reversed_apply[S](
    state: Lazy[S],
    reversed_state_value: Callable[[Lazy[S]], Any],
    reversed_state_function: Callable[[Lazy[S]], Any],
    m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]],
    m_identity: Callable[[Any], Any],
) -> Any:
    def function_binder(function_and_new_state: tuple[Callable[[Any], Any], Lazy[S]], /) -> Any:
        nonlocal state
        function, new_state = function_and_new_state

        def value_binder(value_and_state: tuple[Any, Lazy[S]], /) -> Any:
            nonlocal state
            value, state = value_and_state
            return m_identity((function(value), new_state))

        return m_bind(reversed_state_value(new_state))(value_binder)

    return m_bind(reversed_state_function(lambda: state()))(function_binder)


# [S : Type] -> [M : Type -> Type] ->
# ([T : Type] -> T -> M T) ->
# ([From : Type] -> [To : Type] -> M From -> (From -> M To) -> M To) ->
# [T : Type] -> ReversedStateT S M (ReversedStateT S M T) -> ReversedStateT S M T
@curry
@curry
@curry
def reversed_join[S](
    state: Lazy[S],
    reversed_state_reversed_state_value: Callable[[Lazy[S]], Any],
    m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]],
    m_identity: Callable[[Any], Any],
) -> Any:
    def reversed_state_value_binder(reversed_state_value_and_state: tuple[Any, S]) -> Any:
        nonlocal state
        reversed_state_value, new_state = reversed_state_value_and_state

        def value_binder(value_and_state: tuple[Any, Lazy[S]]) -> Any:
            nonlocal state
            value, state = value_and_state
            return m_identity((value, new_state))

        return m_bind(reversed_state_value(state))(value_binder)

    return m_bind(reversed_state_reversed_state_value(lambda: state()))(reversed_state_value_binder)
