from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import felis.identity
from felis import applicative, monad
from felis.currying import curry

__all__ = [
    "Option",
    "Some",
    "neutral",
    "add",
    "map",
    "identity",
    "apply",
    "lift2",
    "when",
    "fold",
    "traverse",
    "inject",
    "join",
    "bind",
    "compose",
    "then",
    "guard",
]


type Option[T] = None | Some[T]


@dataclass(frozen=True)
class Some[T]:
    value: T


neutral = None


@curry
def add[T](augend: Option[T], addend: Option[T]) -> Option[T]:
    match augend:
        case None:
            return addend
        case Some(value):
            return Some(value)


@curry
def map[From, To](option_value: Option[From], function: Callable[[From], To]) -> Option[To]:
    match option_value:
        case None:
            return None
        case Some(value):
            return Some(function(value))


identity = Some


@curry
def apply[From, To](option_value: Option[From], option_function: Option[Callable[[From], To]]) -> Option[To]:
    match option_function:
        case None:
            return None
        case Some(function):
            return map(function)(option_value)


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[First, Second, Result](
        second: Option[Second],
        first: Option[First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> Option[Result]: ...

else:
    lift2 = applicative.lift2(map)(apply)


if TYPE_CHECKING:

    @curry
    def when(bool: bool, option_none: Option[None]) -> Option[None]: ...

else:
    when = applicative.when(identity)


@curry
@curry
def fold[A, T](option_value: Option[T], function: Callable[[T], Callable[[A], A]], accumulator: A) -> A:
    match option_value:
        case None:
            return accumulator
        case Some(value):
            return function(value)(accumulator)


# [A : Type -> Type] ->
# ([From : Type] -> [To : Type] -> (From -> To) -> A From -> A To) ->
# ([T : Type] -> T -> A T) ->
# [From : Type] -> [To : Type] -> (From -> A To) -> Option From -> A (Option To)
@curry
@curry
@curry
def traverse[From](
    option_value: Option[From],
    function: Callable[[From], Any],
    a_identity: Callable[[Any], Any],
    a_map: Callable[[Callable[[Any], Any]], Callable[[Any], Any]],
) -> Any:
    match option_value:
        case None:
            return a_identity(neutral)
        case Some(value):
            return a_map(identity)(function(value))


# [M : Type -> Type] -> ([T : Type] -> T -> M T) -> [T : Type] -> Option (M (Option T)) -> M (Option T)
@curry
def inject(option_m_option_value: Option[Any], m_identity: Callable[[Any], Any]) -> Any:
    match option_m_option_value:
        case None:
            return m_identity(None)
        case Some(m_option_value):
            return m_option_value


join = inject(felis.identity.identity)


if TYPE_CHECKING:

    @curry
    def bind[From, To](option_value: Option[From], function: Callable[[From], Option[To]]) -> Option[To]: ...

else:
    bind = monad.bind(map)(join)


if TYPE_CHECKING:

    @curry
    @curry
    def compose[From, Intermediate, To](
        value: From,
        first: Callable[[From], Option[Intermediate]],
        second: Callable[[Intermediate], Option[To]],
    ) -> Option[To]: ...

else:
    compose = monad.compose(bind)


if TYPE_CHECKING:

    @curry
    def then[First, Second](first: Option[First], second: Option[Second]) -> Option[Second]: ...

else:
    then = monad.then(bind)


if TYPE_CHECKING:

    def guard(bool: bool) -> Option[None]: ...

else:
    guard = monad.guard(neutral)(identity)
