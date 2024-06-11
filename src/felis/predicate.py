from collections.abc import Callable

import felis.bool
from felis import function, identity
from felis.bool import Bool

__all__ = ["Predicate", "both", "either", "negate", "same", "different"]


type Predicate[T] = Callable[[T], Bool]


both = function.add(felis.bool.both)


either = function.add(felis.bool.either)


negate = identity.compose(felis.bool.negate)


same = function.add(felis.bool.same)


different = function.add(felis.bool.different)
