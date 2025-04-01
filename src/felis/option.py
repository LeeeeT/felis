from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Final

import felis.alternative
import felis.applicative
import felis.functor
import felis.identity
import felis.monad
import felis.semigroup
from felis.alternative import Alternative
from felis.applicative import Applicative
from felis.currying import curry
from felis.functor import Functor
from felis.monad import Monad
from felis.monoid import Monoid
from felis.semigroup import Semigroup

if TYPE_CHECKING:
    from felis import Either

__all__ = [
    "Option",
    "Some",
    "add_to",
    "alternative",
    "applicative",
    "apply_to",
    "bind_to",
    "by_map",
    "compose_after",
    "compose_before",
    "default_to",
    "default_to_t",
    "discard_after",
    "discard_before",
    "fold",
    "functor",
    "guard",
    "join",
    "join_t",
    "lift",
    "map_by",
    "monad",
    "monoid",
    "neutral",
    "neutral_t",
    "pure",
    "semigroup",
    "take_after",
    "take_before",
    "to_add",
    "to_add_t",
    "to_apply",
    "to_apply_t",
    "to_bind",
    "to_either",
    "to_either_t",
    "traverse",
    "traverse_t",
    "when",
]


type Option[T] = None | Some[T]


class Some[T]:
    __match_args__ = ("value",)

    def __init__(self, value: T):
        self.value: Final = value


# [M : * -> *] -> Monad M -> [T : *] -> M (Option T) -> M (Option T) -> M (Option T)
@curry
@curry
def to_add_t(m_augend: Any, m_addend: Any, m: Monad) -> Any:
    def augend_binder(augend: Option[Any]) -> Any:
        match augend:
            case None:
                return m_addend
            case Some(value):
                return felis.monad.pure(m)(Some(value))

    return felis.monad.to_bind(m)(m_augend)(augend_binder)


if TYPE_CHECKING:

    @curry
    def to_add[T](augend: Option[T], addend: Option[T]) -> Option[T]: ...

else:
    to_add = to_add_t(felis.identity.monad)


# [T : *] -> Semigroup (Option T)
semigroup: Semigroup[Any] = Semigroup(to_add)


if TYPE_CHECKING:

    @curry
    def add_to[T](addend: Option[T], augend: Option[T]) -> Option[T]: ...

else:
    add_to = felis.semigroup.add_to(semigroup)


# [M : * -> *] -> Monad M -> [T : *] -> M (Option T)
def neutral_t(m: Monad) -> Any:
    return felis.monad.pure(m)(None)


# [T : *] -> Option T
neutral: Option[Any] = neutral_t(felis.identity.monad)


monoid = Monoid(semigroup, neutral)


@curry
def map_by[From, To](option_value: Option[From], function: Callable[[From], To]) -> Option[To]:
    match option_value:
        case None:
            return None
        case Some(value):
            return Some(function(value))


# Functor Option
functor = Functor(map_by)


if TYPE_CHECKING:

    @curry
    def by_map[From, To](function: Callable[[From], To], option_value: Option[From]) -> Option[To]: ...

else:
    by_map = felis.functor.by_map(functor)


if TYPE_CHECKING:

    def pure[T](value: T, /) -> Option[T]: ...

else:
    pure = Some


# [M : * -> *] -> Monad M -> [From : *] -> [To : *] -> M (Option (From -> To)) -> M (Option From) -> M (Option To)
@curry
@curry
def to_apply_t(m_either_value: Any, m_either_function: Any, m: Monad) -> Any:
    def option_function_binder(option_function: Option[Callable[[Any], Any]]) -> Any:
        match option_function:
            case None:
                return felis.monad.pure(m)(None)
            case Some(function):

                def option_value_binder(option_value: Option[Any]) -> Any:
                    match option_value:
                        case None:
                            return felis.monad.pure(m)(None)
                        case Some(value):
                            return felis.monad.pure(m)(Some(function(value)))

                return felis.monad.to_bind(m)(m_either_value)(option_value_binder)

    return felis.monad.to_bind(m)(m_either_function)(option_function_binder)


if TYPE_CHECKING:

    @curry
    def to_apply[From, To](option_value: Option[From], option_function: Option[Callable[[From], To]]) -> Option[To]: ...

else:
    to_apply = to_apply_t(felis.identity.monad)


# Applicative Option
applicative = Applicative(functor, pure, to_apply)


if TYPE_CHECKING:

    @curry
    def apply_to[From, To](option_function: Option[Callable[[From], To]], option_value: Option[From]) -> Option[To]: ...

else:
    apply_to = felis.applicative.apply_to(applicative)


if TYPE_CHECKING:

    @curry
    @curry
    def lift[First, Second, Result](
        second: Option[Second],
        first: Option[First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> Option[Result]: ...

else:
    lift = felis.applicative.lift(applicative)


if TYPE_CHECKING:

    @curry
    def take_after[First, Second](second: Option[Second], first: Option[First]) -> Option[Second]: ...

else:
    take_after = felis.applicative.take_after(applicative)


if TYPE_CHECKING:

    @curry
    def discard_before[First, Second](first: Option[First], second: Option[Second]) -> Option[Second]: ...

else:
    discard_before = felis.applicative.discard_before(applicative)


if TYPE_CHECKING:

    @curry
    def discard_after[First, Second](second: Option[Second], first: Option[First]) -> Option[First]: ...

else:
    discard_after = felis.applicative.discard_after(applicative)


if TYPE_CHECKING:

    @curry
    def take_before[First, Second](first: Option[First], second: Option[Second]) -> Option[First]: ...

else:
    take_before = felis.applicative.take_before(applicative)


if TYPE_CHECKING:

    @curry
    def when(option_none: Option[None], bool: bool) -> Option[None]: ...

else:
    when = felis.applicative.when(applicative)


# Alternative Option
alternative = Alternative(monoid, applicative)


if TYPE_CHECKING:

    def guard(bool: bool, /) -> Option[None]: ...

else:
    guard = felis.alternative.guard(alternative)


# [M : * -> *] -> Monad M -> [T : *] -> M (Option (M (Option T))) -> M (Option T)
@curry
def join_t(m_option_m_option_value: Any, m: Monad) -> Any:
    def binder(option_m_option_value: Option[Any]) -> Any:
        match option_m_option_value:
            case None:
                return felis.monad.pure(m)(None)
            case Some(m_option_value):
                return m_option_value

    return felis.monad.to_bind(m)(m_option_m_option_value)(binder)


if TYPE_CHECKING:

    def join[From, To](option_option_value: Option[Option[From]], /) -> Option[To]: ...

else:
    join = join_t(felis.identity.monad)


# Monad Option
monad = Monad(applicative, join)


if TYPE_CHECKING:

    @curry
    def bind_to[From, To](option_value: Option[From], function: Callable[[From], Option[To]]) -> Option[To]: ...

else:
    bind_to = felis.monad.bind_to(monad)


if TYPE_CHECKING:

    @curry
    def to_bind[From, To](function: Callable[[From], Option[To]], option_value: Option[From]) -> Option[To]: ...

else:
    to_bind = felis.monad.to_bind(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_after[From, Intermediate, To](
        value: From,
        second: Callable[[Intermediate], Option[To]],
        first: Callable[[From], Option[Intermediate]],
    ) -> Option[To]: ...

else:
    compose_after = felis.monad.compose_after(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_before[From, Intermediate, To](
        value: From,
        first: Callable[[From], Option[Intermediate]],
        second: Callable[[Intermediate], Option[To]],
    ) -> Option[To]: ...

else:
    compose_before = felis.monad.compose_before(monad)


@curry
@curry
def fold[A, T](option_value: Option[T], function: Callable[[T], Callable[[A], A]], accumulator: A) -> A:
    match option_value:
        case None:
            return accumulator
        case Some(value):
            return function(value)(accumulator)


# [A : * -> *] -> Applicative A -> [From : *] -> [To : *] -> (From -> A To) -> Option From -> A (Option To)
@curry
@curry
def traverse_t[From](option_value: Option[From], function: Callable[[From], Any], a: Applicative) -> Any:
    match option_value:
        case None:
            return felis.applicative.pure(a)(neutral)
        case Some(value):
            return felis.applicative.map_by(a)(pure)(function(value))


if TYPE_CHECKING:

    @curry
    def traverse[From, To](option_value: Option[From], function: Callable[[From], To]) -> Option[To]: ...

else:
    traverse = traverse_t(felis.identity.applicative)


# [M : * -> *] -> Monad M -> [T : *] -> M T -> M (Option T) -> M T
@curry
@curry
def default_to_t(m_option_value: Any, default_value: Any, m: Monad) -> Any:
    def binder(option_value: Option[Any]) -> Any:
        match option_value:
            case None:
                return default_value
            case Some(value):
                return felis.monad.pure(m)(value)

    return felis.monad.to_bind(m)(m_option_value)(binder)


if TYPE_CHECKING:

    @curry
    def default_to[T](option_value: Option[T], default_value: T) -> T: ...

else:
    default_to = default_to_t(felis.identity.monad)


# [M : * -> *] -> Monad M -> [L : *] -> M L -> [R : *] -> M (Option R) -> M (Either L R)
@curry
@curry
@curry
def to_either_t(m_option_value: Option[Any], m_left: Any, m: Monad) -> Any:
    from felis import either

    def binder(option_value: Option[Any]) -> Any:
        match option_value:
            case None:
                return felis.monad.to_bind(m)(m_left)(lambda left: felis.monad.pure(m)(either.Left(left)))
            case Some(value):
                return felis.monad.pure(m)(either.Right(value))

    return felis.monad.to_bind(m)(m_option_value)(binder)


if TYPE_CHECKING:

    @curry
    def to_either[L, R](option_value: Option[R], left: L) -> Either[L, R]: ...

else:
    to_either = to_either_t(felis.identity.monad)
