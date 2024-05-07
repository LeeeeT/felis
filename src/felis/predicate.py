from collections.abc import Callable

import felis.bool
from felis import identity

__all__ = ["Predicate", "both", "either", "negate", "same", "different"]


type Predicate[T] = Callable[[T], bool]


both = identity.add(felis.bool.both)


either = identity.add(felis.bool.either)


negate = identity.compose(felis.bool.negate)


same = identity.add(felis.bool.same)


different = identity.add(felis.bool.different)
