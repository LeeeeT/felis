from collections.abc import Callable

from felis import monad
from felis.currying import curry

__all__ = ["Environment", "identity", "map", "join", "bind", "compose", "then"]


type Environment[E, T] = Callable[[E], T]


@curry
def identity[T, E](environment: object, value: T) -> T:
    return value


@curry
@curry
def map[E, From, To](environment: E, environment_value: Environment[E, From], function: Callable[[From], To]) -> To:
    return function(environment_value(environment))


@curry
def join[E, T](environment: E, environment_environment_value: Environment[E, Environment[E, T]]) -> T:
    return environment_environment_value(environment)(environment)


bind = monad.bind(map)(join)


compose = monad.compose(bind)


then = monad.then(bind)
