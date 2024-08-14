from collections.abc import Callable

from felis.currying import curry

__all__ = ["flip"]


@curry
@curry
def flip[First, Second, Result](first: First, second: Second, function: Callable[[First], Callable[[Second], Result]]) -> Result:
    return function(first)(second)
