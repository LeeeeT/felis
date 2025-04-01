from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import felis.alternative
import felis.applicative
import felis.functor
import felis.identity
import felis.monad
from felis.alternative import Alternative
from felis.applicative import Applicative
from felis.currying import curry
from felis.functor import Functor
from felis.lazy import Lazy
from felis.monad import Monad

__all__ = [
    "ReversedState",
    "State",
    "applicative",
    "apply_to",
    "bind_to",
    "by_map",
    "compose_after",
    "compose_before",
    "discard_after",
    "discard_before",
    "functor",
    "join",
    "join_t",
    "lift",
    "map_by",
    "map_by_t",
    "monad",
    "neutral_t",
    "pure",
    "pure_t",
    "reversed_applicative",
    "reversed_apply_to",
    "reversed_bind_to",
    "reversed_compose_after",
    "reversed_compose_before",
    "reversed_discard_after",
    "reversed_discard_before",
    "reversed_join",
    "reversed_join_t",
    "reversed_lift",
    "reversed_monad",
    "reversed_take_after",
    "reversed_take_before",
    "reversed_to_apply",
    "reversed_to_apply_t",
    "reversed_to_bind",
    "starting_with_run",
    "starting_with_run_t",
    "take_after",
    "take_before",
    "to_add_t",
    "to_apply",
    "to_apply_t",
    "to_bind",
    "when",
]


type State[S, T] = Callable[[S], tuple[T, S]]


type ReversedState[S, T] = State[Lazy[S], T]


# [S : *] -> [F : * -> *] -> Functor F -> [T : *] -> StateT S F T -> S -> F T
@curry
@curry
def starting_with_run_t[S](state: S, state_value: Callable[[S], Any], f: Functor) -> Any:
    def value_mapper(value_and_state: tuple[Any, S]) -> Any:
        value, _ = value_and_state
        return value

    return felis.functor.map_by(f)(value_mapper)(state_value(state))


if TYPE_CHECKING:

    @curry
    def starting_with_run[S, T](state: S, state_value: State[S, T]) -> T: ...

else:
    starting_with_run = starting_with_run_t(felis.identity.functor)


# [S : *] -> [A : * -> *] -> Alternative A -> [T : *] -> StateT S A T -> StateT S A T -> StateT S A T
@curry
@curry
@curry
def to_add_t[S](state: S, first: Callable[[S], Any], second: Callable[[S], Any], a: Alternative) -> Any:
    return felis.alternative.to_add(a)(second(state))(first(state))


# [S : *] -> [A : * -> *] -> Alternative A -> [T : *] -> StateT S A T
@curry
def neutral_t(state: Any, a: Alternative) -> Any:
    return felis.alternative.neutral(a)


# [S : *] ->
# [F : * -> *] ->
# Functor F ->
# [From : *] -> [To : *] -> (From -> To) -> StateT S F From -> StateT S F To
@curry
@curry
@curry
def map_by_t[S](state: S, state_value: Callable[[S], Any], function: Callable[[Any], Any], f: Functor) -> Any:
    def value_mapper(value_and_new_state: tuple[Any, S]) -> tuple[Any, S]:
        value, new_state = value_and_new_state
        return function(value), new_state

    return felis.functor.map_by(f)(value_mapper)(state_value(state))


if TYPE_CHECKING:

    @curry
    @curry
    def map_by[S, From, To](state: S, state_value: State[S, From], function: Callable[[From], To]) -> tuple[To, S]: ...

else:
    map_by = map_by_t(felis.identity.functor)


# [S : *] -> Functor (State S)
functor = Functor(map_by)


if TYPE_CHECKING:

    @curry
    def by_map[S, From, To](function: Callable[[From], To], state_value: State[S, From]) -> State[S, To]: ...

else:
    by_map = felis.functor.by_map(functor)


# [S : *] -> [A : * -> *] -> Applicative A -> [T : *] -> T -> StateT S A T
@curry
@curry
def pure_t(state: Any, value: Any, a: Applicative) -> Any:
    return felis.applicative.pure(a)((value, state))


if TYPE_CHECKING:

    def pure[T](value: T, /) -> State[Any, T]: ...

else:
    pure = pure_t(felis.identity.applicative)


# [S : *] ->
# [M : * -> *] ->
# Monad M ->
# [From : *] -> [To : *] -> StateT S M (From -> To) -> StateT S M From -> StateT S M To
@curry
@curry
@curry
def to_apply_t[S](state: S, state_value: Callable[[S], Any], state_function: Callable[[S], Any], m: Monad) -> Any:
    def function_binder(function_and_intermediate_state: tuple[Callable[[Any], Any], S]) -> Any:
        function, intermediate_state = function_and_intermediate_state

        def value_binder(value_and_new_state: tuple[Any, S]) -> Any:
            value, new_state = value_and_new_state
            return felis.monad.pure(m)((function(value), new_state))

        return felis.monad.to_bind(m)(state_value(intermediate_state))(value_binder)

    return felis.monad.to_bind(m)(state_function(state))(function_binder)


if TYPE_CHECKING:

    @curry
    def to_apply[S, From, To](state_value: State[S, From], state_function: State[S, Callable[[From], To]]) -> State[S, To]: ...

else:
    to_apply = to_apply_t(felis.identity.monad)


# [S : *] -> Applicative (State S)
applicative = Applicative(functor, pure, to_apply)


if TYPE_CHECKING:

    @curry
    def apply_to[S, From, To](state_function: State[S, Callable[[From], To]], state_value: State[S, From]) -> State[S, To]: ...

else:
    apply_to = felis.applicative.apply_to(applicative)


if TYPE_CHECKING:

    @curry
    @curry
    def lift[S, First, Second, Result](
        second: State[S, Second],
        first: State[S, First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> State[S, Result]: ...

else:
    lift = felis.applicative.lift(applicative)


if TYPE_CHECKING:

    @curry
    def take_after[S, First, Second](second: State[S, Second], first: State[S, First]) -> State[S, Second]: ...

else:
    take_after = felis.applicative.take_after(applicative)


if TYPE_CHECKING:

    @curry
    def discard_before[S, First, Second](first: State[S, First], second: State[S, Second]) -> State[S, Second]: ...

else:
    discard_before = felis.applicative.discard_before(applicative)


if TYPE_CHECKING:

    @curry
    def discard_after[S, First, Second](second: State[S, Second], first: State[S, First]) -> State[S, First]: ...

else:
    discard_after = felis.applicative.discard_after(applicative)


if TYPE_CHECKING:

    @curry
    def take_before[S, First, Second](first: State[S, First], second: State[S, Second]) -> State[S, First]: ...

else:
    take_before = felis.applicative.take_before(applicative)


if TYPE_CHECKING:

    @curry
    def when[S](state_none: State[S, None], bool: bool) -> State[S, None]: ...

else:
    when = felis.applicative.when(applicative)


# [S : *] ->
# [M : * -> *] ->
# Monad M ->
# [T : *] -> StateT S M (StateT S M T) -> StateT S M T
@curry
@curry
def join_t[S](state: S, state_state_value: Callable[[S], Any], m: Monad) -> Any:
    def state_value_binder(state_value_and_intermediate_state: tuple[Any, S]) -> Any:
        state_value, intermediate_state = state_value_and_intermediate_state

        def value_binder(value_and_new_state: tuple[Any, S]) -> Any:
            value, new_state = value_and_new_state
            return felis.monad.pure(m)((value, new_state))

        return felis.monad.to_bind(m)(state_value(intermediate_state))(value_binder)

    return felis.monad.to_bind(m)(state_state_value(state))(state_value_binder)


if TYPE_CHECKING:

    def join[S, T](state_state_value: State[S, State[S, T]], /) -> State[S, T]: ...

else:
    join = join_t(felis.identity.monad)


# [S : *] -> Monad (State S)
monad = Monad(applicative, join)


if TYPE_CHECKING:

    @curry
    def bind_to[S, From, To](state_value: State[S, From], function: Callable[[From], State[S, To]]) -> State[S, To]: ...

else:
    bind_to = felis.monad.bind_to(monad)


if TYPE_CHECKING:

    @curry
    def to_bind[S, From, To](function: Callable[[From], State[S, To]], state_value: State[S, From]) -> State[S, To]: ...

else:
    to_bind = felis.monad.to_bind(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_after[S, From, Intermediate, To](
        value: From,
        second: Callable[[Intermediate], State[S, To]],
        first: Callable[[From], State[S, Intermediate]],
    ) -> State[S, To]: ...

else:
    compose_after = felis.monad.compose_after(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_before[S, From, Intermediate, To](
        value: From,
        first: Callable[[From], State[S, Intermediate]],
        second: Callable[[Intermediate], State[S, To]],
    ) -> State[S, To]: ...

else:
    compose_before = felis.monad.compose_before(monad)


# [S : *] ->
# [M : * -> *] ->
# Monad M ->
# [From : *] -> [To : *] -> ReversedStateT S M (From -> To) -> ReversedStateT S M From -> ReversedStateT S M To
@curry
@curry
@curry
def reversed_to_apply_t[S](state: Lazy[S], reversed_state_value: Callable[[Lazy[S]], Any], reversed_state_function: Callable[[Lazy[S]], Any], m: Monad) -> Any:
    def function_binder(function_and_new_state: tuple[Callable[[Any], Any], Lazy[S]]) -> Any:
        nonlocal state

        function, new_state = function_and_new_state

        def value_binder(value_and_state: tuple[Any, Lazy[S]]) -> Any:
            nonlocal state
            value, state = value_and_state
            return felis.monad.pure(m)((function(value), new_state))

        return felis.monad.to_bind(m)(reversed_state_value(new_state))(value_binder)

    return felis.monad.to_bind(m)(reversed_state_function(lambda: state()))(function_binder)


if TYPE_CHECKING:

    @curry
    def reversed_to_apply[S, From, To](state_value: ReversedState[S, From], state_function: ReversedState[S, Callable[[From], To]]) -> ReversedState[S, To]: ...

else:
    reversed_to_apply = reversed_to_apply_t(felis.identity.monad)


# [S : *] -> Applcative (ReversedState S)
reversed_applicative = Applicative(functor, pure, reversed_to_apply)


if TYPE_CHECKING:

    @curry
    def reversed_apply_to[S, From, To](state_function: ReversedState[S, Callable[[From], To]], state_value: ReversedState[S, From]) -> ReversedState[S, To]: ...

else:
    reversed_apply_to = felis.applicative.apply_to(reversed_applicative)


if TYPE_CHECKING:

    @curry
    @curry
    def reversed_lift[S, First, Second, Result](
        second: ReversedState[S, Second],
        first: ReversedState[S, First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> ReversedState[S, Result]: ...

else:
    reversed_lift = felis.applicative.lift(reversed_applicative)


if TYPE_CHECKING:

    @curry
    def reversed_take_after[S, First, Second](second: ReversedState[S, Second], first: ReversedState[S, First]) -> ReversedState[S, Second]: ...

else:
    reversed_take_after = felis.applicative.take_after(reversed_applicative)


if TYPE_CHECKING:

    @curry
    def reversed_discard_before[S, First, Second](first: ReversedState[S, First], second: ReversedState[S, Second]) -> ReversedState[S, Second]: ...

else:
    reversed_discard_before = felis.applicative.discard_before(reversed_applicative)


if TYPE_CHECKING:

    @curry
    def reversed_discard_after[S, First, Second](second: ReversedState[S, Second], first: ReversedState[S, First]) -> ReversedState[S, First]: ...

else:
    reversed_discard_after = felis.applicative.discard_after(reversed_applicative)


if TYPE_CHECKING:

    @curry
    def reversed_take_before[S, First, Second](first: ReversedState[S, First], second: ReversedState[S, Second]) -> ReversedState[S, First]: ...

else:
    reversed_take_before = felis.applicative.take_before(reversed_applicative)


# [S : *] ->
# [M : * -> *] ->
# Monad M ->
# [T : *] -> ReversedStateT S M (ReversedStateT S M T) -> ReversedStateT S M T
@curry
@curry
def reversed_join_t[S](state: Lazy[S], reversed_state_reversed_state_value: Callable[[Lazy[S]], Any], m: Monad) -> Any:
    def reversed_state_value_binder(reversed_state_value_and_new_state: tuple[Any, S]) -> Any:
        nonlocal state

        reversed_state_value, new_state = reversed_state_value_and_new_state

        def value_binder(value_and_state: tuple[Any, Lazy[S]]) -> Any:
            nonlocal state
            value, state = value_and_state
            return felis.monad.pure(m)((value, new_state))

        return felis.monad.to_bind(m)(reversed_state_value(state))(value_binder)

    return felis.monad.to_bind(m)(reversed_state_reversed_state_value(lambda: state()))(reversed_state_value_binder)


if TYPE_CHECKING:

    def reversed_join[S, T](state_state_value: ReversedState[S, ReversedState[S, T]], /) -> ReversedState[S, T]: ...

else:
    reversed_join = reversed_join_t(felis.identity.monad)


# [S : *] -> Monad (ReversedState S)
reversed_monad = Monad(reversed_applicative, reversed_join)


if TYPE_CHECKING:

    @curry
    def reversed_bind_to[S, From, To](state_value: ReversedState[S, From], function: Callable[[From], ReversedState[S, To]]) -> ReversedState[S, To]: ...

else:
    reversed_bind_to = felis.monad.bind_to(reversed_monad)


if TYPE_CHECKING:

    @curry
    def reversed_to_bind[S, From, To](function: Callable[[From], ReversedState[S, To]], state_value: ReversedState[S, From]) -> ReversedState[S, To]: ...

else:
    reversed_to_bind = felis.monad.to_bind(reversed_monad)


if TYPE_CHECKING:

    @curry
    @curry
    def reversed_compose_after[S, From, Intermediate, To](
        value: From,
        second: Callable[[Intermediate], ReversedState[S, To]],
        first: Callable[[From], ReversedState[S, Intermediate]],
    ) -> ReversedState[S, To]: ...

else:
    reversed_compose_after = felis.monad.compose_after(reversed_monad)


if TYPE_CHECKING:

    @curry
    @curry
    def reversed_compose_before[S, From, Intermediate, To](
        value: From,
        first: Callable[[From], ReversedState[S, Intermediate]],
        second: Callable[[Intermediate], ReversedState[S, To]],
    ) -> ReversedState[S, To]: ...

else:
    reversed_compose_before = felis.monad.compose_before(reversed_monad)
