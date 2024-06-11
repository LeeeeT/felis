from collections.abc import Callable

from felis import Option, Predicate, option
from felis.currying import curry

__all__ = ["smart_constructor"]


@curry
@curry
def smart_constructor[From, To](value: From, predicate: Predicate[From], constructor: Callable[[From], To]) -> Option[To]:
    return option.Some(constructor(value)) if predicate(value) else None
