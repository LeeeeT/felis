from collections.abc import Callable
from typing import Any

from felis.currying import curry
from felis.lazy import Lazy

__all__ = [
    "apply",
    "join",
    "map_by",
    "neutral",
    "pure",
    "reversed_apply",
    "reversed_join",
    "starting_with_run",
    "to_add",
]


# [S : *] -> [M : * -> *] -> ([From : *] -> [To : *] -> (From -> To) -> M From -> M To) -> [T : *] -> StateT S M T -> S -> M T
@curry
@curry
def starting_with_run[S](state: S, state_value: Callable[[S], Any], m_map_by: Callable[[Callable[[Any], Any]], Callable[[Any], Any]]) -> Any:
    def value_mapper(value_and_state: tuple[Any, S]) -> Any:
        value, _ = value_and_state
        return value

    return m_map_by(value_mapper)(state_value(state))


# [S : *] -> [M : * -> *] -> ([T : *] -> M T) -> [T : *] -> StateT S M T
@curry
def neutral(state: Any, m_neutral: Any) -> Any:
    return m_neutral


# [S : *] -> [M : * -> *] -> ([T : *] -> M T -> M T -> M T) -> [T : *] -> StateT S M T -> StateT S M T -> StateT S M T
@curry
@curry
@curry
def to_add[S](state: S, first: Callable[[S], Any], second: Callable[[S], Any], m_to_add: Callable[[Any], Any]) -> Any:
    return m_to_add(second(state))(first(state))


# [S : *] -> [M : * -> *] ->
# ([From : *] -> [To : *] -> (From -> To) -> M From -> T To) ->
# [From : *] -> [To : *] -> (From -> To) -> StateT S M From -> StateT S M To
@curry
@curry
@curry
def map_by[S](
    state: S,
    state_value: Callable[[S], Any],
    function: Callable[[Any], Any],
    m_map_by: Callable[[Callable[[Any], Any]], Callable[[Any], Any]],
) -> Any:
    def value_mapper(value_and_new_state: tuple[Any, S]) -> tuple[Any, S]:
        value, new_state = value_and_new_state
        return function(value), new_state

    return m_map_by(value_mapper)(state_value(state))


# [S : *] -> [M : * -> *] -> ([T : *] -> T -> M T) -> [T : *] -> T -> StateT S M T
@curry
@curry
def pure(state: Any, value: Any, m_pure: Callable[[Any], Any]) -> Any:
    return m_pure((value, state))


# [S : *] -> [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [From : *] -> [To : *] -> StateT S M (From -> To) -> StateT S M From -> StateT S M To
@curry
@curry
@curry
@curry
def apply[S](
    state: S,
    state_value: Callable[[S], Any],
    state_function: Callable[[S], Any],
    m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]],
    m_pure: Callable[[Any], Any],
) -> Any:
    def function_binder(function_and_intermediate_state: tuple[Callable[[Any], Any], S]) -> Any:
        function, intermediate_state = function_and_intermediate_state

        def value_binder(value_and_new_state: tuple[Any, S]) -> Any:
            value, new_state = value_and_new_state
            return m_pure((function(value), new_state))

        return m_bind(state_value(intermediate_state))(value_binder)

    return m_bind(state_function(state))(function_binder)


# [S : *] -> [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [T : *] -> StateT S M (StateT S M T) -> StateT S M T
@curry
@curry
@curry
def join[S](
    state: S,
    state_state_value: Callable[[S], Any],
    m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]],
    m_pure: Callable[[Any], Any],
) -> Any:
    def state_value_binder(state_value_and_intermediate_state: tuple[Any, S]) -> Any:
        state_value, intermediate_state = state_value_and_intermediate_state

        def value_binder(value_and_new_state: tuple[Any, S]) -> Any:
            value, new_state = value_and_new_state
            return m_pure((value, new_state))

        return m_bind(state_value(intermediate_state))(value_binder)

    return m_bind(state_state_value(state))(state_value_binder)


# [S : *] -> [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [From : *] -> [To : *] -> ReversedStateT S M (From -> To) -> ReversedStateT S M From -> ReversedStateT S M To
@curry
@curry
@curry
@curry
def reversed_apply[S](
    state: Lazy[S],
    reversed_state_value: Callable[[Lazy[S]], Any],
    reversed_state_function: Callable[[Lazy[S]], Any],
    m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]],
    m_pure: Callable[[Any], Any],
) -> Any:
    def function_binder(function_and_new_state: tuple[Callable[[Any], Any], Lazy[S]], /) -> Any:
        nonlocal state
        function, new_state = function_and_new_state

        def value_binder(value_and_state: tuple[Any, Lazy[S]], /) -> Any:
            nonlocal state
            value, state = value_and_state
            return m_pure((function(value), new_state))

        return m_bind(reversed_state_value(new_state))(value_binder)

    return m_bind(reversed_state_function(lambda: state()))(function_binder)


# [S : *] -> [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [T : *] -> ReversedStateT S M (ReversedStateT S M T) -> ReversedStateT S M T
@curry
@curry
@curry
def reversed_join[S](
    state: Lazy[S],
    reversed_state_reversed_state_value: Callable[[Lazy[S]], Any],
    m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]],
    m_pure: Callable[[Any], Any],
) -> Any:
    def reversed_state_value_binder(reversed_state_value_and_new_state: tuple[Any, S]) -> Any:
        nonlocal state
        reversed_state_value, new_state = reversed_state_value_and_new_state

        def value_binder(value_and_state: tuple[Any, Lazy[S]]) -> Any:
            nonlocal state
            value, state = value_and_state
            return m_pure((value, new_state))

        return m_bind(reversed_state_value(state))(value_binder)

    return m_bind(reversed_state_reversed_state_value(lambda: state()))(reversed_state_value_binder)
