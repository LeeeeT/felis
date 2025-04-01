from collections.abc import Callable

import felis.bool
from felis import function

__all__ = ["Predicate", "both_and", "different_from", "either_or", "false", "negate", "same_as", "true"]


type Predicate[T] = Callable[[T], bool]


true = function.pure(True)


false = function.pure(False)


both_and = function.to_add_t(felis.bool.both_and)


either_or = function.to_add_t(felis.bool.either_or)


negate = function.map_by(felis.bool.negate)


same_as = function.to_add_t(felis.bool.same_as)


different_from = function.to_add_t(felis.bool.different_from)
