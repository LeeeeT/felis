from felis import monad, state
from felis.currying import curry
from felis.lazy import Lazy
from felis.state import State

__all__ = ["ReversedState", "identity", "map", "join", "bind", "compose", "then"]


type ReversedState[S, T] = State[Lazy[S], T]


identity = state.identity


map = state.map


@curry
def join[S, T](state: Lazy[S], reversed_state_reversed_state_value: ReversedState[S, ReversedState[S, T]]) -> tuple[T, Lazy[S]]:
    reversed_state_value, new_state = reversed_state_reversed_state_value(lambda: state())
    value, state = reversed_state_value(state)
    return value, new_state


bind = monad.bind(map)(join)


compose = monad.compose(bind)


then = monad.then(bind)
