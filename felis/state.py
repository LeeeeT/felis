from collections.abc import Callable

from felis import Lazy, monad
from felis.currying import curry

__all__ = [
    "State",
    "ReversedState",
    "identity",
    "map",
    "join",
    "bind",
    "compose",
    "then",
    "reversed_join",
    "reversed_bind",
    "reversed_compose",
    "reversed_then",
]


type State[S, T] = Callable[[S], tuple[T, S]]


type ReversedState[S, T] = State[Lazy[S], T]


@curry
def identity[S, T](state: S, value: T) -> tuple[T, S]:
    return (value, state)


@curry
@curry
def map[S, From, To](state: S, state_value: State[S, From], function: Callable[[From], To]) -> tuple[To, S]:
    value, new_state = state_value(state)
    return function(value), new_state


@curry
def join[S, T](state: S, state_state_value: State[S, State[S, T]]) -> tuple[T, S]:
    state_value, state = state_state_value(state)
    value, new_state = state_value(state)
    return value, new_state


bind = monad.bind(map)(join)


compose = monad.compose(bind)


then = monad.then(bind)


@curry
def reversed_join[S, T](state: Lazy[S], reversed_state_reversed_state_value: ReversedState[S, ReversedState[S, T]]) -> tuple[T, Lazy[S]]:
    reversed_state_value, new_state = reversed_state_reversed_state_value(lambda: state())
    value, state = reversed_state_value(state)
    return value, new_state


reversed_bind = monad.bind(map)(reversed_join)


reversed_compose = monad.compose(reversed_bind)


reversed_then = monad.then(reversed_bind)
