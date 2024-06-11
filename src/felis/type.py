from collections.abc import Callable
from typing import NewType

from felis import option, predicate
from felis.currying import curry
from felis.option import Option
from felis.predicate import Predicate

__all__ = [
    "smart_constructor",
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
]


@curry
@curry
def smart_constructor[From, To](value: From, predicate: Predicate[From], constructor: Callable[[From], To]) -> Option[To]:
    return option.Some(constructor(value)) if predicate(value) else None


Negative = NewType("Negative", int)

negative = smart_constructor(Negative)(predicate.less(0))


NonPositive = NewType("NonPositive", int)

non_positive = smart_constructor(NonPositive)(predicate.less_or_equal(0))


NonZero = NewType("NonZero", int)

non_zero = smart_constructor(NonZero)(predicate.not_equal(0))


NonNegative = NewType("NonNegative", int)

non_negative = smart_constructor(NonNegative)(predicate.greater_or_equal(0))


Positive = NewType("Positive", int)

positive = smart_constructor(Positive)(predicate.greater(0))
