from felis import monad, state
from felis.currying import curry
from felis.lazy import Lazy
from felis.state import State

__all__ = ["ReverseState", "identity", "map", "join", "bind", "compose"]


type ReverseState[S, T] = State[Lazy[S], T]


identity = state.identity


map = state.map


@curry
def join[S, T](state: Lazy[S], reverse_state_reverse_state_value: ReverseState[S, ReverseState[S, T]]) -> tuple[T, Lazy[S]]:
    reverse_state_value, new_state = reverse_state_reverse_state_value(lambda: state())
    value, state = reverse_state_value(state)
    return value, new_state


bind = monad.bind(map)(join)


compose = monad.compose(bind)
