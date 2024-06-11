import builtins

from felis import lazy
from felis.lazy import Lazy

__all__ = ["IO", "run", "identity", "map", "join", "bind", "compose", "then", "input", "print"]


type IO[T] = Lazy[T]


run = lazy.run


identity = lazy.identity


map = lazy.map


join = lazy.join


bind = lazy.bind


compose = lazy.compose


then = lazy.then


input = builtins.input


def print(value: object) -> IO[None]:
    return lambda: builtins.print(value)
