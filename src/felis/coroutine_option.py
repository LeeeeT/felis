import felis.identity
from felis import applicative, coroutine, monad, option

__all__ = ["map", "identity", "apply", "lift2", "when", "join", "bind", "compose", "then"]


map = felis.identity.compose(coroutine.map)(option.map)


identity = felis.identity.compose(coroutine.identity)(option.identity)


apply = coroutine.lift2(option.apply)


lift2 = applicative.lift2(map)(apply)


when = applicative.when(identity)


join = coroutine.bind(option.inject(coroutine.identity))


bind = monad.bind(map)(join)


compose = monad.compose(bind)


then = monad.then(bind)
