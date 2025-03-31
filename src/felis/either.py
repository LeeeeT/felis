from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Final

import felis.identity
from felis import applicative, monad
from felis.currying import curry, flip

if TYPE_CHECKING:
    from felis import Option

__all__ = [
    "Either",
    "Left",
    "Right",
    "add_to",
    "apply",
    "apply_t",
    "bind",
    "bind_to",
    "catch",
    "compose_after",
    "compose_before",
    "default_to",
    "default_to_t",
    "discard_after",
    "discard_before",
    "fold",
    "join",
    "join_t",
    "lift2",
    "map_by",
    "pure",
    "take_after",
    "take_before",
    "to_add",
    "to_add_t",
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


# [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [L : *] -> [R : *] -> M (Either L R) -> M (Either L R) -> M (Either L R)
@curry
@curry
@curry
def to_add_t(m_augend: Any, m_addend: Any, m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]], m_pure: Callable[[Any], Any]) -> Any:
    def augend_binder(augend: Either[Any, Any]) -> Any:
        match augend:
            case Left(_):
                return m_addend
            case Right(right):
                return m_pure(Right(right))

    return m_bind(m_augend)(augend_binder)


if TYPE_CHECKING:

    @curry
    def to_add[L, R](augend: Either[L, R], addend: Either[L, R]) -> Either[L, R]: ...

else:
    to_add = to_add_t(felis.identity.pure)(felis.identity.bind)


add_to = flip(to_add)


@curry
def map_by[L, From, To](either_value: Either[L, From], function: Callable[[From], To]) -> Either[L, To]:
    match either_value:
        case Left(value):
            return Left(value)
        case Right(value):
            return Right(function(value))


if TYPE_CHECKING:
    # [L : *] -> [R : *] -> R -> Either L R
    def pure[R](value: R) -> Either[Any, R]: ...

else:
    pure = Right


# [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [L : *] -> [From : *] -> [To : *] -> M (Either L (From -> To)) -> M (Either L From) -> M (Either L To)
@curry
@curry
@curry
def apply_t(
    m_either_value: Any,
    m_either_function: Any,
    m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]],
    m_pure: Callable[[Any], Any],
) -> Any:
    def either_function_binder(either_function: Either[Any, Any]) -> Any:
        match either_function:
            case Left(left):
                return m_pure(Left(left))
            case Right(function):

                def either_value_binder(either_value: Either[Any, Any]) -> Any:
                    match either_value:
                        case Left(left):
                            return m_pure(Left(left))
                        case Right(value):
                            return m_pure(Right(function(value)))

                return m_bind(m_either_value)(either_value_binder)

    return m_bind(m_either_function)(either_function_binder)


if TYPE_CHECKING:

    @curry
    def apply[L, From, To](either_value: Either[L, From], either_function: Either[L, Callable[[From], To]]) -> Either[L, To]: ...

else:
    apply = apply_t(felis.identity.pure)(felis.identity.bind)


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[L, First, Second, Result](
        second: Either[L, Second],
        first: Either[L, First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> Either[L, Result]: ...

else:
    lift2 = applicative.lift2(map_by)(apply)


if TYPE_CHECKING:

    @curry
    def take_after[L, First, Second](second: Either[L, Second], first: Either[L, First]) -> Either[L, Second]: ...

else:
    take_after = applicative.take_after(lift2)


if TYPE_CHECKING:

    @curry
    def discard_before[L, First, Second](first: Either[L, First], second: Either[L, Second]) -> Either[L, Second]: ...

else:
    discard_before = applicative.discard_before(lift2)


if TYPE_CHECKING:

    @curry
    def discard_after[L, First, Second](second: Either[L, Second], first: Either[L, First]) -> Either[L, First]: ...

else:
    discard_after = applicative.discard_after(lift2)


if TYPE_CHECKING:

    @curry
    def take_before[L, First, Second](first: Either[L, First], second: Either[L, Second]) -> Either[L, First]: ...

else:
    take_before = applicative.take_before(lift2)


if TYPE_CHECKING:

    @curry
    def when[L](either_none: Either[L, None], bool: bool) -> Either[L, None]: ...

else:
    when = applicative.when(pure)


# [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [L : *] -> [R : *] -> M (Either L (M (Either L R))) -> M (Either L R)
@curry
@curry
def join_t(m_either_m_either_value: Any, m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]], m_pure: Callable[[Any], Any]) -> Any:
    def either_m_either_binder(either_m_either_value: Either[Any, Any]) -> Any:
        match either_m_either_value:
            case Left(left):
                return m_pure(Left(left))
            case Right(m_either_value):
                return m_either_value

    return m_bind(m_either_m_either_value)(either_m_either_binder)


if TYPE_CHECKING:

    def join[L, R](either_either_value: Either[L, Either[L, R]], /) -> Either[L, R]: ...

else:
    join = join_t(felis.identity.pure)(felis.identity.bind)


if TYPE_CHECKING:

    @curry
    def bind_to[L, From, To](either_value: Either[L, From], function: Callable[[From], Either[L, To]]) -> Either[L, To]: ...

else:
    bind_to = monad.bind_to(map_by)(join)


bind = flip(bind_to)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_after[L, From, Intermediate, To](
        value: From,
        second: Callable[[Intermediate], Either[L, To]],
        first: Callable[[From], Either[L, Intermediate]],
    ) -> Either[L, To]: ...

else:
    compose_after = monad.compose_after(bind)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_before[L, From, Intermediate, To](
        value: From,
        first: Callable[[From], Either[L, Intermediate]],
        second: Callable[[Intermediate], Either[L, To]],
    ) -> Either[L, To]: ...

else:
    compose_before = monad.compose_before(bind)


# [L : *] -> [A : *] -> A -> [R : *] -> (R -> A -> A) -> Either L R -> A
@curry
@curry
def fold[A, R](either_value: Either[Any, R], function: Callable[[R], Callable[[A], A]], accumulator: A) -> A:
    match either_value:
        case Left(value):
            return accumulator
        case Right(value):
            return function(value)(accumulator)


# [L : *] -> [A : * -> *] ->
# ([From : *] -> [To : *] -> (From -> To) -> A From -> A To) ->
# ([T : *] -> T -> A T) ->
# [From : *] -> [To : *] -> (From -> A To) -> Either L From -> A (Either L To)
@curry
@curry
@curry
def traverse_t[From](
    either_value: Either[Any, From],
    function: Callable[[From], Any],
    a_identity: Callable[[Any], Any],
    a_map_by: Callable[[Any], Callable[[Callable[[Any], Any]], Any]],
) -> Any:
    match either_value:
        case Left(value):
            return a_identity(Left(value))
        case Right(value):
            return a_map_by(pure)(function(value))


if TYPE_CHECKING:

    @curry
    def traverse[L, From, To](either_value: Either[L, From], function: Callable[[From], To]) -> Either[L, To]: ...

else:
    traverse = traverse_t(felis.identity.map_by)(felis.identity.pure)


# [M : * -> *] ->
# ([T : *] -> T -> M T) ->
# ([From : *] -> [To : *] -> M From -> (From -> M To) -> M To) ->
# [L : *] -> [R : *] -> M R -> M (Either L R) -> M R
@curry
@curry
@curry
def default_to_t(
    m_either_value: Any,
    default_value: Any,
    m_bind: Callable[[Any], Callable[[Callable[[Any], Any]], Any]],
    m_pure: Callable[[Any], Any],
) -> Any:
    def either_binder(either_value: Either[Any, Any]) -> Any:
        match either_value:
            case Left(_):
                return default_value
            case Right(value):
                return m_pure(value)

    return m_bind(m_either_value)(either_binder)


if TYPE_CHECKING:

    @curry
    def default_to[L, R](either_value: Either[L, R], default_value: R) -> R: ...

else:
    default_to = default_to_t(felis.identity.pure)(felis.identity.bind)


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
