from collections.abc import Callable

import felis.bool
from felis import function, identity

__all__ = ["Predicate", "both", "different", "either", "false", "negate", "same", "true"]


type Predicate[T] = Callable[[T], bool]


true = function.pure(True)


false = function.pure(False)


both = function.to_add(felis.bool.both_and)


either = function.to_add(felis.bool.either_or)


negate = identity.compose(felis.bool.negate)


same = function.to_add(felis.bool.same_as)


different = function.to_add(felis.bool.different_from)
