from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import felis.identity
from felis import applicative, monad
from felis.currying import curry, flip
from felis.lazy import Lazy

__all__ = [
    "ReversedState",
    "State",
    "apply",
    "apply_t",
    "bind",
    "bind_to",
    "compose_after",
    "compose_before",
    "discard_after",
    "discard_before",
    "join",
    "join_t",
    "lift2",
    "map_by",
    "map_by_t",
    "neutral_t",
    "pure",
    "pure_t",
    "reversed_apply",
    "reversed_apply_t",
    "reversed_bind",
    "reversed_bind_to",
    "reversed_compose_after",
    "reversed_compose_before",
    "reversed_discard_after",
    "reversed_discard_before",
    "reversed_join",
    "reversed_join_t",
    "reversed_lift2",
    "reversed_take_after",
    "reversed_take_before",
    "starting_with_run",
    "starting_with_run_t",
    "take_after",
    "take_before",
    "to_add_t",
    "when",
]


type State[S, T] = Callable[[S], tuple[T, S]]


type ReversedState[S, T] = State[Lazy[S], T]


# [S : *] -> [M : * -> *] -> ([From : *] -> [To : *] -> (From -> To) -> M From -> M To) -> [T : *] -> StateT S M T -> S -> M T
@curry
@curry
def starting_with_run_t[S](state: S, state_value: Callable[[S], Any], m_map_by: Callable[[Callable[[Any], Any]], Callable[[Any], Any]]) -> Any:
    def value_mapper(value_and_state: tuple[Any, S]) -> Any:
        value, _ = value_and_state
        return value

    return m_map_by(value_mapper)(state_value(state))


if TYPE_CHECKING:

    @curry
    def starting_with_run[S, T](state: S, state_value: State[S, T]) -> T: ...

else:
    starting_with_run = starting_with_run_t(felis.identity.map_by)


# [S : *] -> [M : * -> *] -> ([T : *] -> M T) -> [T : *] -> StateT S M T
@curry
def neutral_t(state: Any, m_neutral: Any) -> Any:
    return m_neutral


# [S : *] -> [M : * -> *] -> ([T : *] -> M T -> M T -> M T) -> [T : *] -> StateT S M T -> StateT S M T -> StateT S M T
@curry
@curry
@curry
def to_add_t[S](state: S, first: Callable[[S], Any], second: Callable[[S], Any], m_to_add: Callable[[Any], Any]) -> Any:
    return m_to_add(second(state))(first(state))


# [S : *] -> [M : * -> *] ->
# ([From : *] -> [To : *] -> (From -> To) -> M From -> T To) ->
# [From : *] -> [To : *] -> (From -> To) -> StateT S M From -> StateT S M To
@curry
@curry
@curry
def map_by_t[S](
    state: S,
    state_value: Callable[[S], Any],
    function: Callable[[Any], Any],
    m_map_by: Callable[[Callable[[Any], Any]], Callable[[Any], Any]],
) -> Any:
    def value_mapper(value_and_new_state: tuple[Any, S]) -> tuple[Any, S]:
        value, new_state = value_and_new_state
        return function(value), new_state

    return m_map_by(value_mapper)(state_value(state))


if TYPE_CHECKING:

    @curry
    @curry
    def map_by[S, From, To](state: S, state_value: State[S, From], function: Callable[[From], To]) -> tuple[To, S]: ...

else:
    map_by = map_by_t(felis.identity.map_by)


# [S : *] -> [M : * -> *] -> ([T : *] -> T -> M T) -> [T : *] -> T -> StateT S M T
@curry
@curry
def pure_t(state: Any, value: Any, m_pure: Callable[[Any], Any]) -> Any:
    return m_pure((value, state))


if TYPE_CHECKING:

    @curry
    def pure[S, T](state: S, value: T) -> tuple[T, S]: ...

else:
    pure = pure_t(felis.identity.pure)


# [S : *] -> [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [From : *] -> [To : *] -> StateT S M (From -> To) -> StateT S M From -> StateT S M To
@curry
@curry
@curry
@curry
def apply_t[S](
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


if TYPE_CHECKING:

    @curry
    @curry
    def apply[S, From, To](state: S, state_value: State[S, From], state_function: State[S, Callable[[From], To]]) -> tuple[To, S]: ...

else:
    apply = apply_t(felis.identity.pure)(felis.identity.bind)


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


# [S : *] -> [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [T : *] -> StateT S M (StateT S M T) -> StateT S M T
@curry
@curry
@curry
def join_t[S](
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


if TYPE_CHECKING:

    @curry
    def join[S, T](state: S, state_state_value: State[S, State[S, T]]) -> tuple[T, S]: ...

else:
    join = join_t(felis.identity.pure)(felis.identity.bind)


if TYPE_CHECKING:

    @curry
    def bind_to[S, From, To](state_value: State[S, From], function: Callable[[From], State[S, To]]) -> State[S, To]: ...

else:
    bind_to = monad.bind_to(map_by)(join)


bind = flip(bind_to)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_after[S, From, Intermediate, To](
        value: From,
        second: Callable[[Intermediate], State[S, To]],
        first: Callable[[From], State[S, Intermediate]],
    ) -> State[S, To]: ...

else:
    compose_after = monad.compose_after(bind)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_before[S, From, Intermediate, To](
        value: From,
        first: Callable[[From], State[S, Intermediate]],
        second: Callable[[Intermediate], State[S, To]],
    ) -> State[S, To]: ...

else:
    compose_before = monad.compose_before(bind)


# [S : *] -> [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [From : *] -> [To : *] -> ReversedStateT S M (From -> To) -> ReversedStateT S M From -> ReversedStateT S M To
@curry
@curry
@curry
@curry
def reversed_apply_t[S](
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


if TYPE_CHECKING:

    @curry
    @curry
    def reversed_apply[S, From, To](
        state: Lazy[S],
        state_value: ReversedState[S, From],
        state_function: ReversedState[S, Callable[[From], To]],
    ) -> tuple[To, Lazy[S]]: ...

else:
    reversed_apply = reversed_apply_t(felis.identity.pure)(felis.identity.bind)


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
    reversed_take_after = applicative.take_after(reversed_lift2)


if TYPE_CHECKING:

    @curry
    def reversed_discard_before[S, First, Second](first: ReversedState[S, First], second: ReversedState[S, Second]) -> ReversedState[S, Second]: ...

else:
    reversed_discard_before = applicative.discard_before(reversed_lift2)


if TYPE_CHECKING:

    @curry
    def reversed_discard_after[S, First, Second](second: ReversedState[S, Second], first: ReversedState[S, First]) -> ReversedState[S, First]: ...

else:
    reversed_discard_after = applicative.discard_after(reversed_lift2)


if TYPE_CHECKING:

    @curry
    def reversed_take_before[S, First, Second](first: ReversedState[S, First], second: ReversedState[S, Second]) -> ReversedState[S, First]: ...

else:
    reversed_take_before = applicative.take_before(reversed_lift2)


# [S : *] -> [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [T : *] -> ReversedStateT S M (ReversedStateT S M T) -> ReversedStateT S M T
@curry
@curry
@curry
def reversed_join_t[S](
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


if TYPE_CHECKING:

    @curry
    def reversed_join[S, T](state: Lazy[S], state_state_value: ReversedState[S, ReversedState[S, T]]) -> tuple[T, Lazy[S]]: ...

else:
    reversed_join = reversed_join_t(felis.identity.pure)(felis.identity.bind)


if TYPE_CHECKING:

    @curry
    def reversed_bind_to[S, From, To](state_value: ReversedState[S, From], function: Callable[[From], ReversedState[S, To]]) -> ReversedState[S, To]: ...

else:
    reversed_bind_to = monad.bind_to(map_by)(reversed_join)


reversed_bind = flip(reversed_bind_to)


if TYPE_CHECKING:

    @curry
    @curry
    def reversed_compose_after[S, From, Intermediate, To](
        value: From,
        second: Callable[[Intermediate], ReversedState[S, To]],
        first: Callable[[From], ReversedState[S, Intermediate]],
    ) -> ReversedState[S, To]: ...

else:
    reversed_compose_after = monad.compose_after(reversed_bind)


if TYPE_CHECKING:

    @curry
    @curry
    def reversed_compose_before[S, From, Intermediate, To](
        value: From,
        first: Callable[[From], ReversedState[S, Intermediate]],
        second: Callable[[Intermediate], ReversedState[S, To]],
    ) -> ReversedState[S, To]: ...

else:
    reversed_compose_before = monad.compose_before(reversed_bind)
