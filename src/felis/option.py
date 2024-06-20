from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, cast

import felis.identity
from felis import applicative, monad
from felis.currying import curry, uncurry

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


neutral = cast(Option[Any], None)


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


if TYPE_CHECKING:

    def identity[T](value: T) -> Option[T]: ...

else:
    identity = Some


@curry
def apply[From, To](option_value: Option[From], option_function: Option[Callable[[From], To]]) -> Option[To]:
    match option_function:
        case None:
            return None
        case Some(function):
            return map(function)(option_value)


lift2 = applicative.lift2(map)(apply)


when = applicative.when(identity)


@curry
@curry
def fold[A, T](option_value: Option[T], function: Callable[[T], Callable[[A], A]], accumulator: A) -> A:
    match option_value:
        case None:
            return accumulator
        case Some(value):
            return function(value)(accumulator)


@curry
@curry
@curry
def traverse[From, To, ATo, AOptionTo](
    option: Option[From],
    function: Callable[[From], ATo],
    a_identity: Callable[[Option[To]], AOptionTo],
    a_map: Callable[[Callable[[To], Option[To]]], Callable[[ATo], AOptionTo]],
) -> AOptionTo:
    match option:
        case None:
            return a_identity(neutral)
        case Some(value):
            return a_map(identity)(function(value))


@curry
def inject[T, MOptionT](option_m_option_value: Option[MOptionT], m_identity: Callable[[Option[T]], MOptionT]) -> MOptionT:
    match option_m_option_value:
        case None:
            return m_identity(None)
        case Some(m_option_value):
            return m_option_value


join = inject(felis.identity.identity)


bind = monad.bind(map)(join)


compose = monad.compose(bind)


then = monad.then(bind)


guard = uncurry(monad.guard)(identity, neutral)
