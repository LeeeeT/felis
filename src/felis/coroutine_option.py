import felis.identity
from felis import applicative, coroutine, monad, option

__all__ = ["map", "identity", "when", "join", "bind", "compose", "then"]


map = felis.identity.compose(coroutine.map)(option.map)


identity = felis.identity.compose(coroutine.identity)(option.identity)


when = applicative.when(identity)


join = coroutine.bind(option.inject(coroutine.identity))


bind = monad.bind(map)(join)


compose = monad.compose(bind)


then = monad.then(bind)
