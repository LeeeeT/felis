from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Final

import felis.applicative
import felis.functor
import felis.identity
import felis.monad
import felis.semigroup
from felis.applicative import Applicative
from felis.currying import curry
from felis.functor import Functor
from felis.monad import Monad
from felis.semigroup import Semigroup

if TYPE_CHECKING:
    from felis import Option

__all__ = [
    "Either",
    "Left",
    "Right",
    "add_to",
    "applicative",
    "bind_to",
    "catch",
    "compose_after",
    "compose_before",
    "default_to",
    "default_to_t",
    "discard_after",
    "discard_before",
    "fold",
    "functor",
    "join",
    "join_t",
    "lift",
    "map_by",
    "monad",
    "pure",
    "semigroup",
    "take_after",
    "take_before",
    "to_add",
    "to_add_t",
    "to_apply",
    "to_apply_t",
    "to_bind",
    "to_option",
    "traverse",
    "traverse_t",
    "when",
]


type Either[L, R] = Left[L] | Right[R]


class Left[L]:
    __match_args__ = ("value",)

    def __init__(self, value: L):
        self.value: Final = value


class Right[R]:
    __match_args__ = ("value",)

    def __init__(self, value: R):
        self.value: Final = value


# [L : *] -> [M : * -> *] -> Monad M -> [R : *] -> M (Either L R) -> M (Either L R) -> M (Either L R)
@curry
@curry
def to_add_t(m_augend: Any, m_addend: Any, m: Monad) -> Any:
    def augend_binder(augend: Either[Any, Any]) -> Any:
        match augend:
            case Left(_):
                return m_addend
            case Right(right):
                return felis.monad.pure(m)(Right(right))

    return felis.monad.to_bind(m)(m_augend)(augend_binder)


if TYPE_CHECKING:

    @curry
    def to_add[L, R](augend: Either[L, R], addend: Either[L, R]) -> Either[L, R]: ...

else:
    to_add = to_add_t(felis.identity.monad)


# [L : *] -> [R : *] -> Semigroup (Either L R)
semigroup: Semigroup[Either[Any, Any]] = Semigroup(to_add)


if TYPE_CHECKING:

    @curry
    def add_to[L, R](addend: Either[L, R], augend: Either[L, R]) -> Either[L, R]: ...

else:
    add_to = felis.semigroup.add_to(semigroup)


@curry
def map_by[L, From, To](either_value: Either[L, From], function: Callable[[From], To]) -> Either[L, To]:
    match either_value:
        case Left(value):
            return Left(value)
        case Right(value):
            return Right(function(value))


# [L : *] -> Functor (Either L)
functor = Functor(map_by)


if TYPE_CHECKING:

    @curry
    def by_map[L, From, To](function: Callable[[From], To], either_value: Either[L, From]) -> Either[L, To]: ...

else:
    by_map = felis.functor.by_map(functor)


if TYPE_CHECKING:
    # [L : *] -> [R : *] -> R -> Either L R
    def pure[R](value: R) -> Either[Any, R]: ...

else:
    pure = Right


# [L : *] ->
# [M : * -> *] ->
# Monad M ->
# [From : *] -> [To : *] -> M (Either L (From -> To)) -> M (Either L From) -> M (Either L To)
@curry
@curry
def to_apply_t(m_either_value: Any, m_either_function: Any, m: Monad) -> Any:
    def either_function_binder(either_function: Either[Any, Any]) -> Any:
        match either_function:
            case Left(left):
                return felis.monad.pure(m)(Left(left))
            case Right(function):

                def either_value_binder(either_value: Either[Any, Any]) -> Any:
                    match either_value:
                        case Left(left):
                            return felis.monad.pure(m)(Left(left))
                        case Right(value):
                            return felis.monad.pure(m)(Right(function(value)))

                return felis.monad.to_bind(m)(m_either_value)(either_value_binder)

    return felis.monad.to_bind(m)(m_either_function)(either_function_binder)


if TYPE_CHECKING:

    @curry
    def to_apply[L, From, To](either_value: Either[L, From], either_function: Either[L, Callable[[From], To]]) -> Either[L, To]: ...

else:
    to_apply = to_apply_t(felis.identity.monad)


# [L : *] -> Applicative (Either L)
applicative = Applicative(functor, pure, to_apply)


if TYPE_CHECKING:

    @curry
    def apply_to[L, From, To](either_function: Either[L, Callable[[From], To]], either_value: Either[L, From]) -> Either[L, To]: ...

else:
    apply_to = felis.applicative.apply_to(applicative)


if TYPE_CHECKING:

    @curry
    @curry
    def lift[L, First, Second, Result](
        second: Either[L, Second],
        first: Either[L, First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> Either[L, Result]: ...

else:
    lift = felis.applicative.lift(applicative)


if TYPE_CHECKING:

    @curry
    def take_after[L, First, Second](second: Either[L, Second], first: Either[L, First]) -> Either[L, Second]: ...

else:
    take_after = felis.applicative.take_after(applicative)


if TYPE_CHECKING:

    @curry
    def discard_before[L, First, Second](first: Either[L, First], second: Either[L, Second]) -> Either[L, Second]: ...

else:
    discard_before = felis.applicative.discard_before(applicative)


if TYPE_CHECKING:

    @curry
    def discard_after[L, First, Second](second: Either[L, Second], first: Either[L, First]) -> Either[L, First]: ...

else:
    discard_after = felis.applicative.discard_after(applicative)


if TYPE_CHECKING:

    @curry
    def take_before[L, First, Second](first: Either[L, First], second: Either[L, Second]) -> Either[L, First]: ...

else:
    take_before = felis.applicative.take_before(applicative)


if TYPE_CHECKING:

    @curry
    def when[L](either_none: Either[L, None], bool: bool) -> Either[L, None]: ...

else:
    when = felis.applicative.when(applicative)


# [L : *] ->
# [M : * -> *] ->
# Monad M ->
# [R : *] -> M (Either L (M (Either L R))) -> M (Either L R)
@curry
def join_t(m_either_m_either_value: Any, m: Monad) -> Any:
    def either_m_either_binder(either_m_either_value: Either[Any, Any]) -> Any:
        match either_m_either_value:
            case Left(left):
                return felis.monad.pure(m)(Left(left))
            case Right(m_either_value):
                return m_either_value

    return felis.monad.to_bind(m)(m_either_m_either_value)(either_m_either_binder)


if TYPE_CHECKING:

    def join[L, R](either_either_value: Either[L, Either[L, R]], /) -> Either[L, R]: ...

else:
    join = join_t(felis.identity.monad)


# [L : *] -> Monad (Either L)
monad = Monad(applicative, join)


if TYPE_CHECKING:

    @curry
    def bind_to[L, From, To](either_value: Either[L, From], function: Callable[[From], Either[L, To]]) -> Either[L, To]: ...

else:
    bind_to = felis.monad.bind_to(monad)


if TYPE_CHECKING:

    @curry
    def to_bind[L, From, To](function: Callable[[From], Either[L, To]], either_value: Either[L, From]) -> Either[L, To]: ...

else:
    to_bind = felis.monad.to_bind(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_after[L, From, Intermediate, To](
        value: From,
        second: Callable[[Intermediate], Either[L, To]],
        first: Callable[[From], Either[L, Intermediate]],
    ) -> Either[L, To]: ...

else:
    compose_after = felis.monad.compose_after(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_before[L, From, Intermediate, To](
        value: From,
        first: Callable[[From], Either[L, Intermediate]],
        second: Callable[[Intermediate], Either[L, To]],
    ) -> Either[L, To]: ...

else:
    compose_before = felis.monad.compose_before(monad)


# [L : *] -> [A : *] -> A -> [R : *] -> (R -> A -> A) -> Either L R -> A
@curry
@curry
def fold[A, R](either_value: Either[Any, R], function: Callable[[R], Callable[[A], A]], accumulator: A) -> A:
    match either_value:
        case Left(value):
            return accumulator
        case Right(value):
            return function(value)(accumulator)


# [L : *] ->
# [A : * -> *] ->
# Applicative A ->
# [From : *] -> [To : *] -> (From -> A To) -> Either L From -> A (Either L To)
@curry
@curry
def traverse_t[From](either_value: Either[Any, From], function: Callable[[From], Any], a: Applicative) -> Any:
    match either_value:
        case Left(value):
            return felis.applicative.pure(a)(Left(value))
        case Right(value):
            return felis.applicative.map_by(a)(pure)(function(value))


if TYPE_CHECKING:

    @curry
    def traverse[L, From, To](either_value: Either[L, From], function: Callable[[From], To]) -> Either[L, To]: ...

else:
    traverse = traverse_t(felis.identity.applicative)


# [L : *] ->
# [M : * -> *] ->
# Monad M ->
# [R : *] -> M R -> M (Either L R) -> M R
@curry
@curry
def default_to_t(m_either_value: Any, default_value: Any, m: Monad) -> Any:
    def either_binder(either_value: Either[Any, Any]) -> Any:
        match either_value:
            case Left(_):
                return default_value
            case Right(value):
                return felis.monad.pure(m)(value)

    return felis.monad.to_bind(m)(m_either_value)(either_binder)


if TYPE_CHECKING:

    @curry
    def default_to[L, R](either_value: Either[L, R], default_value: R) -> R: ...

else:
    default_to = default_to_t(felis.identity.monad)


@curry
@curry
def catch[E: BaseException, From, To](value: From, function: Callable[[From], To], exception_type: type[E]) -> Either[E, To]:
    try:
        return Right(function(value))
    except exception_type as exception:
        return Left(exception)


# [L : *] -> Either L R -> Option R
def to_option[R](either_value: Either[Any, R]) -> Option[R]:
    from felis import option

    match either_value:
        case Left(_):
            return None
        case Right(value):
            return option.Some(value)
