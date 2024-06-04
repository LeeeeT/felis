from dataclasses import dataclass

from felis import predicate
from felis.currying import curry

__all__ = [
    "Ordering",
    "Worse",
    "Same",
    "Better",
    "worse",
    "same_or_better",
    "not_worse",
    "same",
    "different",
    "better",
    "same_or_worse",
    "not_better",
    "reverse",
    "neutral",
    "add",
]


type Ordering = Worse | Same | Better


@dataclass(frozen=True)
class Worse:
    pass


@dataclass(frozen=True)
class Same:
    pass


@dataclass(frozen=True)
class Better:
    pass


worse = curry(isinstance)(Worse)


same_or_better = not_worse = predicate.negate(worse)


same = curry(isinstance)(Same)


different = predicate.negate(same)


better = curry(isinstance)(Better)


same_or_worse = not_better = predicate.negate(better)


def reverse(ordering: Ordering) -> Ordering:
    match ordering:
        case Worse():
            return Better()
        case Same():
            return Same()
        case Better():
            return Worse()


neutral = Same()


@curry
def add(augend: Ordering, addend: Ordering) -> Ordering:
    match augend:
        case Same():
            return addend
        case _:
            return augend
