from collections.abc import Callable
from typing import TYPE_CHECKING

import felis.identity
from felis import applicative, monad, state_t
from felis.currying import curry, flip
from felis.lazy import Lazy

__all__ = [
    "ReversedState",
    "State",
    "apply",
    "bind",
    "bind_to",
    "compose",
    "discard_after",
    "discard_before",
    "join",
    "lift2",
    "map_by",
    "pure",
    "reversed_apply",
    "reversed_bind",
    "reversed_bind_to",
    "reversed_compose",
    "reversed_discard_after",
    "reversed_discard_before",
    "reversed_join",
    "reversed_lift2",
    "reversed_take_after",
    "reversed_take_before",
    "starting_with_run",
    "take_after",
    "take_before",
    "when",
]


type State[S, T] = Callable[[S], tuple[T, S]]


type ReversedState[S, T] = State[Lazy[S], T]


if TYPE_CHECKING:

    @curry
    def starting_with_run[S, T](state: S, state_value: State[S, T]) -> T: ...

else:
    starting_with_run = state_t.starting_with_run(felis.identity.map_by)


if TYPE_CHECKING:

    @curry
    @curry
    def map_by[S, From, To](state: S, state_value: State[S, From], function: Callable[[From], To]) -> tuple[To, S]: ...

else:
    map_by = state_t.map_by(felis.identity.map_by)


if TYPE_CHECKING:

    @curry
    def pure[S, T](state: S, value: T) -> tuple[T, S]: ...

else:
    pure = state_t.pure(felis.identity.pure)


if TYPE_CHECKING:

    @curry
    @curry
    def apply[S, From, To](state: S, state_value: State[S, From], state_function: State[S, Callable[[From], To]]) -> tuple[To, S]: ...

else:
    apply = state_t.apply(felis.identity.pure)(felis.identity.bind)


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[S, First, Second, Result](
        second: State[S, Second],
        first: State[S, First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> State[S, Result]: ...

else:
    lift2 = applicative.lift2(map_by)(apply)


if TYPE_CHECKING:

    @curry
    def take_after[S, First, Second](second: State[S, Second], first: State[S, First]) -> State[S, Second]: ...

else:
    take_after = applicative.take_after(lift2)


if TYPE_CHECKING:

    @curry
    def discard_before[S, First, Second](first: State[S, First], second: State[S, Second]) -> State[S, Second]: ...

else:
    discard_before = applicative.discard_before(lift2)


if TYPE_CHECKING:

    @curry
    def discard_after[S, First, Second](second: State[S, Second], first: State[S, First]) -> State[S, First]: ...

else:
    discard_after = applicative.discard_after(lift2)


if TYPE_CHECKING:

    @curry
    def take_before[S, First, Second](first: State[S, First], second: State[S, Second]) -> State[S, First]: ...

else:
    take_before = applicative.take_before(lift2)


if TYPE_CHECKING:

    @curry
    def when[S](state_none: State[S, None], bool: bool) -> State[S, None]: ...

else:
    when = applicative.when(pure)


if TYPE_CHECKING:

    @curry
    def join[S, T](state: S, state_state_value: State[S, State[S, T]]) -> tuple[T, S]: ...

else:
    join = state_t.join(felis.identity.pure)(felis.identity.bind)


if TYPE_CHECKING:

    @curry
    def bind_to[S, From, To](state_value: State[S, From], function: Callable[[From], State[S, To]]) -> State[S, To]: ...

else:
    bind_to = monad.bind_to(map_by)(join)


bind = flip(bind_to)


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
    reversed_apply = state_t.reversed_apply(felis.identity.pure)(felis.identity.bind)


if TYPE_CHECKING:

    @curry
    @curry
    def reversed_lift2[S, First, Second, Result](
        second: ReversedState[S, Second],
        first: ReversedState[S, First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> ReversedState[S, Result]: ...

else:
    reversed_lift2 = applicative.lift2(map_by)(reversed_apply)


if TYPE_CHECKING:

    @curry
    def reversed_take_after[S, First, Second](second: ReversedState[S, Second], first: ReversedState[S, First]) -> ReversedState[S, Second]: ...

else:
    reversed_take_after = applicative.take_after(lift2)


if TYPE_CHECKING:

    @curry
    def reversed_discard_before[S, First, Second](first: ReversedState[S, First], second: ReversedState[S, Second]) -> ReversedState[S, Second]: ...

else:
    reversed_discard_before = applicative.discard_before(lift2)


if TYPE_CHECKING:

    @curry
    def reversed_discard_after[S, First, Second](second: ReversedState[S, Second], first: ReversedState[S, First]) -> ReversedState[S, First]: ...

else:
    reversed_discard_after = applicative.discard_after(lift2)


if TYPE_CHECKING:

    @curry
    def reversed_take_before[S, First, Second](first: ReversedState[S, First], second: ReversedState[S, Second]) -> ReversedState[S, First]: ...

else:
    reversed_take_before = applicative.take_before(lift2)


if TYPE_CHECKING:

    @curry
    def reversed_join[S, T](state: Lazy[S], state_state_value: ReversedState[S, ReversedState[S, T]]) -> tuple[T, Lazy[S]]: ...

else:
    reversed_join = state_t.reversed_join(felis.identity.pure)(felis.identity.bind)


if TYPE_CHECKING:

    @curry
    def reversed_bind_to[S, From, To](state_value: ReversedState[S, From], function: Callable[[From], ReversedState[S, To]]) -> ReversedState[S, To]: ...

else:
    reversed_bind_to = monad.bind_to(map_by)(reversed_join)


reversed_bind = flip(reversed_bind_to)


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
