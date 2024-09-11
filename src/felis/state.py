from collections.abc import Callable
from typing import TYPE_CHECKING

import felis.identity
from felis import applicative, function, monad, state_t
from felis.currying import curry
from felis.lazy import Lazy

__all__ = [
    "State",
    "ReversedState",
    "run",
    "map",
    "identity",
    "apply",
    "lift2",
    "take_after",
    "discard_after",
    "take_before",
    "discard_before",
    "when",
    "join",
    "bound",
    "bind",
    "compose",
    "reversed_apply",
    "reversed_lift2",
    "reversed_take_after",
    "reversed_discard_after",
    "reversed_take_before",
    "reversed_discard_before",
    "reversed_join",
    "reversed_bound",
    "reversed_bind",
    "reversed_compose",
]


type State[S, T] = Callable[[S], tuple[T, S]]


type ReversedState[S, T] = State[Lazy[S], T]


if TYPE_CHECKING:

    @curry
    def run[S, T](state: S, state_value: State[S, T]) -> T: ...

else:
    run = state_t.run(felis.identity.map)


if TYPE_CHECKING:

    @curry
    @curry
    def map[S, From, To](state: S, state_value: State[S, From], function: Callable[[From], To]) -> tuple[To, S]: ...

else:
    map = state_t.map(felis.identity.map)


if TYPE_CHECKING:

    @curry
    def identity[S, T](state: S, value: T) -> tuple[T, S]: ...

else:
    identity = state_t.identity(felis.identity.identity)


if TYPE_CHECKING:

    @curry
    @curry
    def apply[S, From, To](state: S, state_value: State[S, From], state_function: State[S, Callable[[From], To]]) -> tuple[To, S]: ...

else:
    apply = state_t.apply(felis.identity.identity)(felis.identity.bind)


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


take_after = lift2(function.flip(function.identity))


discard_after = lift2(function.identity)


take_before = function.flip(discard_after)


discard_before = function.flip(take_after)


if TYPE_CHECKING:

    @curry
    def when[S](bool: bool, state_none: State[S, None]) -> State[S, None]: ...

else:
    when = applicative.when(identity)


if TYPE_CHECKING:

    @curry
    def join[S, T](state: S, state_state_value: State[S, State[S, T]]) -> tuple[T, S]: ...

else:
    join = state_t.join(felis.identity.identity)(felis.identity.bind)


if TYPE_CHECKING:

    @curry
    def bound[S, From, To](state_value: State[S, From], function: Callable[[From], State[S, To]]) -> State[S, To]: ...

else:
    bound = monad.bound(map)(join)


bind = function.flip(bound)


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
    @curry
    def reversed_apply[S, From, To](
        state: Lazy[S],
        state_value: ReversedState[S, From],
        state_function: ReversedState[S, Callable[[From], To]],
    ) -> tuple[To, Lazy[S]]: ...

else:
    reversed_apply = state_t.reversed_apply(felis.identity.identity)(felis.identity.bind)


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


reversed_take_after = reversed_lift2(function.flip(function.identity))


reversed_discard_after = reversed_lift2(function.identity)


reversed_take_before = function.flip(reversed_discard_after)


reversed_discard_before = function.flip(reversed_take_after)


if TYPE_CHECKING:

    @curry
    def reversed_join[S, T](state: Lazy[S], state_state_value: ReversedState[S, ReversedState[S, T]]) -> tuple[T, Lazy[S]]: ...

else:
    reversed_join = state_t.reversed_join(felis.identity.identity)(felis.identity.bind)


if TYPE_CHECKING:

    @curry
    def reversed_bound[S, From, To](state_value: ReversedState[S, From], function: Callable[[From], ReversedState[S, To]]) -> ReversedState[S, To]: ...

else:
    reversed_bound = monad.bound(map)(reversed_join)


reversed_bind = function.flip(reversed_bound)


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
