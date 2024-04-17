from collections.abc import Callable
from typing import Protocol

from felis import monad
from felis.currying import curry

__all__ = ["State", "identity", "map", "join", "bind", "compose"]


type State[S, T] = Callable[[S], tuple[T, S]]


@curry
def identity[S, T](state: S, value: T) -> tuple[T, S]:
    return (value, state)


@curry
@curry
def map[S, From, To](state: S, state_value: State[S, From], function: Callable[[From], To]) -> tuple[To, S]:
    match state_value(state):
        case value, new_state:
            return function(value), new_state


@curry
def join[S, T](state: S, state_state_value: State[S, State[S, T]]) -> tuple[T, S]:
    state_value, state = state_state_value(state)
    value, new_state = state_value(state)
    return value, new_state


class Bind(Protocol):
    @staticmethod
    @curry
    def __call__[S, From, To](state_value: State[S, From], function: Callable[[From], State[S, To]], /) -> State[S, To]: ...


bind: Bind = monad.bind(map)(join)


class Compose(Protocol):
    @staticmethod
    @curry
    @curry
    def __call__[S, From, Intermediate, To](
        value: From,
        first: Callable[[From], State[S, Intermediate]],
        second: Callable[[Intermediate], State[S, To]],
        /,
    ) -> State[S, To]: ...


compose: Compose = monad.compose(bind)
