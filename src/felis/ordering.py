from typing import TYPE_CHECKING

import felis.semigroup
from felis import predicate
from felis.currying import curry
from felis.monoid import Monoid
from felis.semigroup import Semigroup

__all__ = [
    "Better",
    "Ordering",
    "Same",
    "Worse",
    "add_to",
    "add_to",
    "better",
    "different",
    "monoid",
    "neutral",
    "not_better",
    "not_worse",
    "reverse",
    "same",
    "same_or_better",
    "same_or_worse",
    "semigroup",
    "to_add",
    "worse",
]


type Ordering = Worse | Same | Better


class Worse:
    pass


class Same:
    pass


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


@curry
def to_add(augend: Ordering, addend: Ordering) -> Ordering:
    match augend:
        case Same():
            return addend
        case _:
            return augend


semigroup = Semigroup(to_add)


if TYPE_CHECKING:

    @curry
    def add_to(addend: Ordering, augend: Ordering) -> Ordering: ...

else:
    add_to = felis.semigroup.add_to(semigroup)


neutral = Same()


monoid = Monoid(semigroup, neutral)
