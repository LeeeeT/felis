import felis.identity
from felis import applicative, coroutine, monad, option

__all__ = ["identity", "when", "map", "join", "bind", "compose", "then"]


identity = felis.identity.compose(coroutine.identity)(option.identity)


when = applicative.when(identity)


map = felis.identity.compose(coroutine.map)(option.map)


join = coroutine.bind(option.inject(coroutine.identity))


bind = monad.bind(map)(join)


compose = monad.compose(bind)


then = monad.then(bind)
