from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol

import felis.identity
from felis import monad
from felis.currying import curry

__all__ = ["Option", "Nothing", "Some", "identity", "map", "inject", "join", "bind", "compose"]


type Option[T] = Nothing | Some[T]


@dataclass(frozen=True)
class Nothing:
    pass


@dataclass(frozen=True)
class Some[T]:
    value: T


def identity[T](value: T) -> Option[T]:
    return Some(value)


@curry
def map[From, To](option_value: Option[From], function: Callable[[From], To]) -> Option[To]:
    match option_value:
        case Nothing():
            return Nothing()
        case Some(value):
            return Some(function(value))


@curry
def inject[T, MOptionT](option_m_option_value: Option[MOptionT], m_identity: Callable[[Option[T]], MOptionT]) -> MOptionT:
    match option_m_option_value:
        case Nothing():
            return m_identity(Nothing())
        case Some(m_option_value):
            return m_option_value


class Join(Protocol):
    @staticmethod
    def __call__[T](option_option_value: Option[Option[T]], /) -> Option[T]: ...


join: Join = inject(felis.identity.identity)


class Bind(Protocol):
    @staticmethod
    @curry
    def __call__[From, To](option_value: Option[From], function: Callable[[From], Option[To]], /) -> Option[To]: ...


bind: Bind = monad.bind(map)(join)


class Compose(Protocol):
    @staticmethod
    @curry
    @curry
    def __call__[From, Intermediate, To](
        value: From,
        first: Callable[[From], Option[Intermediate]],
        second: Callable[[Intermediate], Option[To]],
        /,
    ) -> Option[To]: ...


compose: Compose = monad.compose(bind)
