from collections.abc import Callable
from dataclasses import dataclass

import felis.identity
from felis import monad
from felis.currying import curry

__all__ = ["Option", "Some", "identity", "map", "inject", "join", "bind", "compose", "then"]


type Option[T] = None | Some[T]


@dataclass(frozen=True)
class Some[T]:
    value: T


identity = Some


@curry
def map[From, To](option_value: Option[From], function: Callable[[From], To]) -> Option[To]:
    match option_value:
        case None:
            return None
        case Some(value):
            return Some(function(value))


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
