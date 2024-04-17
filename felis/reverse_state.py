from collections.abc import Callable
from typing import Protocol

from felis import monad, state
from felis.currying import curry
from felis.lazy import Lazy
from felis.state import State

__all__ = ["ReverseState", "identity", "map", "join", "bind", "compose"]


type ReverseState[S, T] = State[Lazy[S], T]


class Identity(Protocol):
    @staticmethod
    def __call__[S, T](value: T, /) -> ReverseState[S, T]: ...


identity: Identity = state.identity


class Map(Protocol):
    @staticmethod
    @curry
    def __call__[S, From, To](reverse_state_value: ReverseState[S, From], function: Callable[[From], To], /) -> ReverseState[S, To]: ...


map: Map = state.map


@curry
def join[S, T](state: Lazy[S], reverse_state_reverse_state_value: ReverseState[S, ReverseState[S, T]]) -> tuple[T, Lazy[S]]:
    reverse_state_value, new_state = reverse_state_reverse_state_value(lambda: state())
    value, state = reverse_state_value(state)
    return value, new_state


class Bind(Protocol):
    @staticmethod
    @curry
    def __call__[S, From, To](reverse_state_value: ReverseState[S, From], function: Callable[[From], ReverseState[S, To]], /) -> ReverseState[S, To]: ...


bind: Bind = monad.bind(map)(join)


class Compose(Protocol):
    @staticmethod
    @curry
    @curry
    def __call__[S, From, Intermediate, To](
        value: From,
        first: Callable[[From], ReverseState[S, Intermediate]],
        second: Callable[[Intermediate], ReverseState[S, To]],
        /,
    ) -> ReverseState[S, To]: ...


compose: Compose = monad.compose(bind)
