import math
from typing import NewType

import felis.predicate.float
from felis.constrained import smart_constructor

__all__ = [
    "Negative",
    "negative",
    "NonPositive",
    "non_positive",
    "NonZero",
    "non_zero",
    "NonNegative",
    "non_negative",
    "Positive",
    "positive",
    "Portion",
    "portion",
    "Finite",
    "finite",
]


Negative = NewType("Negative", float)

negative = smart_constructor(Negative)(felis.predicate.float.negative)


NonPositive = NewType("NonPositive", float)

non_positive = smart_constructor(NonPositive)(felis.predicate.float.non_positive)


NonZero = NewType("NonZero", float)

non_zero = smart_constructor(NonZero)(felis.predicate.float.non_zero)


NonNegative = NewType("NonNegative", float)

non_negative = smart_constructor(NonNegative)(felis.predicate.float.non_negative)


Positive = NewType("Positive", float)

positive = smart_constructor(Positive)(felis.predicate.float.positive)


Portion = NewType("Portion", float)

portion = smart_constructor(Portion)(felis.predicate.float.portion)


Finite = NewType("Finite", float)

finite = smart_constructor(Finite)(math.isfinite)
