from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Final

import felis.identity
from felis import applicative, monad
from felis.currying import curry, flip

if TYPE_CHECKING:
    from felis import Either

__all__ = [
    "Option",
    "Some",
    "add_to",
    "apply",
    "apply_t",
    "bind",
    "bind_to",
    "compose_after",
    "compose_before",
    "default_to",
    "default_to_t",
    "discard_after",
    "discard_before",
    "fold",
    "guard",
    "join",
    "join_t",
    "lift2",
    "map_by",
    "neutral",
    "neutral_t",
    "pure",
    "take_after",
    "take_before",
    "to_add",
    "to_add_t",
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


# [M : * -> *] -> ([T : *] -> T -> M T) -> [T : *] -> M (Option T)
def neutral_t(m_pure: Callable[[Any], Any]) -> Any:
    return m_pure(None)


if TYPE_CHECKING:
    # [T : *] -> Option T
    neutral: Option[Any]
else:
    neutral = neutral_t(felis.identity.pure)


# [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [T : *] -> M (Option T) -> M (Option T) -> M (Option T)
@curry
@curry
@curry
def to_add_t(m_augend: Any, m_addend: Any, m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]], m_pure: Callable[[Any], Any]) -> Any:
    def augend_binder(augend: Option[Any]) -> Any:
        match augend:
            case None:
                return m_addend
            case Some(value):
                return m_pure(Some(value))

    return m_bind(m_augend)(augend_binder)


if TYPE_CHECKING:

    @curry
    def to_add[T](augend: Option[T], addend: Option[T]) -> Option[T]: ...

else:
    to_add = to_add_t(felis.identity.pure)(felis.identity.bind)


add_to = flip(to_add)


@curry
def map_by[From, To](option_value: Option[From], function: Callable[[From], To]) -> Option[To]:
    match option_value:
        case None:
            return None
        case Some(value):
            return Some(function(value))


if TYPE_CHECKING:

    def pure[T](value: T, /) -> Option[T]: ...

else:
    pure = Some


# [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [From : *] -> [To : *] -> M (Option (From -> To)) -> M (Option From) -> M (Option To)
@curry
@curry
@curry
def apply_t(
    m_either_value: Any,
    m_either_function: Any,
    m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]],
    m_pure: Callable[[Any], Any],
) -> Any:
    def option_function_binder(option_function: Option[Callable[[Any], Any]]) -> Any:
        match option_function:
            case None:
                return m_pure(None)
            case Some(function):

                def option_value_binder(option_value: Option[Any]) -> Any:
                    match option_value:
                        case None:
                            return m_pure(None)
                        case Some(value):
                            return m_pure(Some(function(value)))

                return m_bind(m_either_value)(option_value_binder)

    return m_bind(m_either_function)(option_function_binder)


if TYPE_CHECKING:

    @curry
    def apply[From, To](option_value: Option[From], option_function: Option[Callable[[From], To]]) -> Option[To]: ...

else:
    apply = apply_t(felis.identity.pure)(felis.identity.bind)


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[First, Second, Result](
        second: Option[Second],
        first: Option[First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> Option[Result]: ...

else:
    lift2 = applicative.lift2(map_by)(apply)


if TYPE_CHECKING:

    @curry
    def take_after[First, Second](second: Option[Second], first: Option[First]) -> Option[Second]: ...

else:
    take_after = applicative.take_after(lift2)


if TYPE_CHECKING:

    @curry
    def discard_before[First, Second](first: Option[First], second: Option[Second]) -> Option[Second]: ...

else:
    discard_before = applicative.discard_before(lift2)


if TYPE_CHECKING:

    @curry
    def discard_after[First, Second](second: Option[Second], first: Option[First]) -> Option[First]: ...

else:
    discard_after = applicative.discard_after(lift2)


if TYPE_CHECKING:

    @curry
    def take_before[First, Second](first: Option[First], second: Option[Second]) -> Option[First]: ...

else:
    take_before = applicative.take_before(lift2)


if TYPE_CHECKING:

    @curry
    def when(option_none: Option[None], bool: bool) -> Option[None]: ...

else:
    when = applicative.when(pure)


# [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [T : *] -> M (Option (M (Option T))) -> M (Option T)
@curry
@curry
def join_t(m_option_m_option_value: Any, m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]], m_pure: Callable[[Any], Any]) -> Any:
    def binder(option_m_option_value: Option[Any]) -> Any:
        match option_m_option_value:
            case None:
                return m_pure(None)
            case Some(m_option_value):
                return m_option_value

    return m_bind(m_option_m_option_value)(binder)


if TYPE_CHECKING:

    def join[From, To](option_option_value: Option[Option[From]]) -> Option[To]: ...

else:
    join = join_t(felis.identity.pure)(felis.identity.bind)


if TYPE_CHECKING:

    @curry
    def bind_to[From, To](option_value: Option[From], function: Callable[[From], Option[To]]) -> Option[To]: ...

else:
    bind_to = monad.bind_to(map_by)(join)


bind = flip(bind_to)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_after[From, Intermediate, To](
        value: From,
        second: Callable[[Intermediate], Option[To]],
        first: Callable[[From], Option[Intermediate]],
    ) -> Option[To]: ...

else:
    compose_after = monad.compose_after(bind)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_before[From, Intermediate, To](
        value: From,
        first: Callable[[From], Option[Intermediate]],
        second: Callable[[Intermediate], Option[To]],
    ) -> Option[To]: ...

else:
    compose_before = monad.compose_before(bind)


if TYPE_CHECKING:

    def guard(bool: bool) -> Option[None]: ...

else:
    guard = monad.guard(neutral)(pure)


@curry
@curry
def fold[A, T](option_value: Option[T], function: Callable[[T], Callable[[A], A]], accumulator: A) -> A:
    match option_value:
        case None:
            return accumulator
        case Some(value):
            return function(value)(accumulator)


# [A : * -> *] ->
# ([From : *] -> [To : *] -> (From -> To) -> A From -> A To) ->
# ([T : *] -> T -> A T) ->
# [From : *] -> [To : *] -> (From -> A To) -> Option From -> A (Option To)
@curry
@curry
@curry
def traverse_t[From](
    option_value: Option[From],
    function: Callable[[From], Any],
    a_pure: Callable[[Any], Any],
    a_map_by: Callable[[Callable[[Any], Any]], Callable[[Any], Any]],
) -> Any:
    match option_value:
        case None:
            return a_pure(neutral)
        case Some(value):
            return a_map_by(pure)(function(value))


if TYPE_CHECKING:

    @curry
    def traverse[From, To](option_value: Option[From], function: Callable[[From], To]) -> Option[To]: ...

else:
    traverse = traverse_t(felis.identity.map_by)(felis.identity.pure)


# [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [T : *] -> M T -> M (Option T) -> M T
@curry
@curry
@curry
def default_to_t(
    m_option_value: Any,
    default_value: Any,
    m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]],
    m_pure: Callable[[Any], Any],
) -> Any:
    def binder(option_value: Option[Any]) -> Any:
        match option_value:
            case None:
                return default_value
            case Some(value):
                return m_pure(value)

    return m_bind(m_option_value)(binder)


if TYPE_CHECKING:

    @curry
    def default_to[T](option_value: Option[T], default_value: T) -> T: ...

else:
    default_to = default_to_t(felis.identity.pure)(felis.identity.bind)


# [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [L : *] -> M L -> [R : *] -> M (Option R) -> M (Either L R)
@curry
@curry
@curry
def to_either_t(m_option_value: Option[Any], m_left: Any, m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]], m_pure: Callable[[Any], Any]) -> Any:
    from felis import either

    def binder(option_value: Option[Any]) -> Any:
        match option_value:
            case None:
                return m_bind(m_left)(lambda left: m_pure(either.Left(left)))
            case Some(value):
                return m_pure(either.Right(value))

    return m_bind(m_option_value)(binder)


if TYPE_CHECKING:

    @curry
    def to_either[L, R](option_value: Option[R], left: L) -> Either[L, R]: ...

else:
    to_either = to_either_t(felis.identity.pure)(felis.identity.bind)
