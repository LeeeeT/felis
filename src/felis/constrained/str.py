from typing import NewType

import felis.predicate.bool
from felis.constrained import smart_constructor

__all__ = ["NonEmpty", "non_empty"]


NonEmpty = NewType("NonEmpty", str)

non_empty = smart_constructor(NonEmpty)(felis.predicate.bool.truthy)
