from typing import Protocol

import felis.identity
from felis import Coroutine, Option, coroutine, monad, option

__all__ = ["identity", "map", "join", "bind", "compose", "then"]


class Identity(Protocol):
    @staticmethod
    def __call__[T](value: T, /) -> Coroutine[Option[T]]: ...


identity = felis.identity.compose(coroutine.identity)(option.identity)


map = felis.identity.compose(coroutine.map)(option.map)


join = coroutine.bind(option.inject(coroutine.identity))


bind = monad.bind(map)(join)


compose = monad.compose(bind)


then = monad.then(bind)
