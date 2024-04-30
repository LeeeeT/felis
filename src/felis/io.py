import builtins
from collections.abc import Callable
from dataclasses import dataclass

from felis import Lazy, monad
from felis.currying import curry

__all__ = ["IO", "run", "identity", "map", "join", "bind", "compose", "then", "input", "print"]


@dataclass(frozen=True)
class IO[T]:
    value: Lazy[T]


def run[T](io_value: IO[T]) -> T:
    return io_value.value()


identity = IO


@curry
def map[From, To](io_value: IO[From], function: Callable[[From], To]) -> IO[To]:
    return IO(lambda: function(io_value.value()))


def join[T](io_io_value: IO[IO[T]]) -> IO[T]:
    return IO(lambda: io_io_value.value().value())


bind = monad.bind(map)(join)


compose = monad.compose(bind)


then = monad.then(bind)


input = IO(builtins.input)


def print(value: object) -> IO[None]:
    return IO(lambda: builtins.print(value))
