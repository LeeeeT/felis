from collections.abc import Callable

import felis.bool
from felis import function, identity

__all__ = ["Predicate", "both", "different", "either", "false", "negate", "same", "true"]


type Predicate[T] = Callable[[T], bool]


true = function.identity(True)


false = function.identity(False)


both = function.add(felis.bool.both)


either = function.add(felis.bool.either)


negate = identity.compose(felis.bool.negate)


same = function.add(felis.bool.same)


different = function.add(felis.bool.different)
