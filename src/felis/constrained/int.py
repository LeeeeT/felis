from typing import NewType

import felis.predicate.float
from felis.constrained import smart_constructor

__all__ = ["Negative", "negative", "NonPositive", "non_positive", "NonZero", "non_zero", "NonNegative", "non_negative", "Positive", "positive"]


Negative = NewType("Negative", int)

negative = smart_constructor(Negative)(felis.predicate.float.negative)


NonPositive = NewType("NonPositive", int)

non_positive = smart_constructor(NonPositive)(felis.predicate.float.non_positive)


NonZero = NewType("NonZero", int)

non_zero = smart_constructor(NonZero)(felis.predicate.float.non_zero)


NonNegative = NewType("NonNegative", int)

non_negative = smart_constructor(NonNegative)(felis.predicate.float.non_negative)


Positive = NewType("Positive", int)

positive = smart_constructor(Positive)(felis.predicate.float.positive)
