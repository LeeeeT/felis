from collections.abc import Callable
from typing import TYPE_CHECKING

from felis import applicative, monad
from felis.currying import curry
from felis.lazy import Lazy

__all__ = [
    "State",
    "ReversedState",
    "map",
    "identity",
    "apply",
    "lift2",
    "when",
    "join",
    "bind",
    "compose",
    "then",
    "reversed_apply",
    "reversed_lift2",
    "reversed_join",
    "reversed_bind",
    "reversed_compose",
    "reversed_then",
]


type State[S, T] = Callable[[S], tuple[T, S]]


type ReversedState[S, T] = State[Lazy[S], T]


@curry
@curry
def map[S, From, To](state: S, state_value: State[S, From], function: Callable[[From], To]) -> tuple[To, S]:
    value, new_state = state_value(state)
    return function(value), new_state


@curry
def identity[S, T](state: S, value: T) -> tuple[T, S]:
    return (value, state)


@curry
@curry
def apply[S, From, To](state: S, state_value: State[S, From], state_function: State[S, Callable[[From], To]]) -> tuple[To, S]:
    function, state = state_function(state)
    return map(function)(state_value)(state)


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[S, First, Second, Result](
        second: State[S, Second],
        first: State[S, First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> State[S, Result]: ...

else:
    lift2 = applicative.lift2(map)(apply)


if TYPE_CHECKING:

    @curry
    def when[S](bool: bool, either_none: State[S, None]) -> State[S, None]: ...

else:
    when = applicative.when(identity)


@curry
def join[S, T](state: S, state_state_value: State[S, State[S, T]]) -> tuple[T, S]:
    state_value, state = state_state_value(state)
    value, new_state = state_value(state)
    return value, new_state


if TYPE_CHECKING:

    @curry
    def bind[S, From, To](either_value: State[S, From], function: Callable[[From], State[S, To]]) -> State[S, To]: ...

else:
    bind = monad.bind(map)(join)


if TYPE_CHECKING:

    @curry
    @curry
    def compose[S, From, Intermediate, To](
        value: From,
        first: Callable[[From], State[S, Intermediate]],
        second: Callable[[Intermediate], State[S, To]],
    ) -> State[S, To]: ...

else:
    compose = monad.compose(bind)


if TYPE_CHECKING:

    @curry
    def then[S, First, Second](first: State[S, First], second: State[S, Second]) -> State[S, Second]: ...

else:
    then = monad.then(bind)


@curry
@curry
def reversed_apply[S, From, To](
    state: Lazy[S],
    reversed_state_value: ReversedState[S, From],
    reversed_state_function: ReversedState[S, Callable[[From], To]],
) -> tuple[To, Lazy[S]]:
    function, new_state = reversed_state_function(lambda: state())
    value, state = map(function)(reversed_state_value)(new_state)
    return value, new_state


if TYPE_CHECKING:

    @curry
    @curry
    def reversed_lift2[S, First, Second, Result](
        second: ReversedState[S, Second],
        first: ReversedState[S, First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> ReversedState[S, Result]: ...

else:
    reversed_lift2 = applicative.lift2(map)(reversed_apply)


@curry
def reversed_join[S, T](state: Lazy[S], reversed_state_reversed_state_value: ReversedState[S, ReversedState[S, T]]) -> tuple[T, Lazy[S]]:
    reversed_state_value, new_state = reversed_state_reversed_state_value(lambda: state())
    value, state = reversed_state_value(state)
    return value, new_state


if TYPE_CHECKING:

    @curry
    def reversed_bind[S, From, To](either_value: ReversedState[S, From], function: Callable[[From], ReversedState[S, To]]) -> ReversedState[S, To]: ...

else:
    reversed_bind = monad.bind(map)(reversed_join)


if TYPE_CHECKING:

    @curry
    @curry
    def reversed_compose[S, From, Intermediate, To](
        value: From,
        first: Callable[[From], ReversedState[S, Intermediate]],
        second: Callable[[Intermediate], ReversedState[S, To]],
    ) -> ReversedState[S, To]: ...

else:
    reversed_compose = monad.compose(reversed_bind)


if TYPE_CHECKING:

    @curry
    def reversed_then[S, First, Second](first: ReversedState[S, First], second: ReversedState[S, Second]) -> ReversedState[S, Second]: ...

else:
    reversed_then = monad.then(reversed_bind)
