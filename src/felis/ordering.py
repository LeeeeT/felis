from felis import predicate
from felis.currying import curry, flip

__all__ = [
    "Better",
    "Ordering",
    "Same",
    "Worse",
    "add_to",
    "better",
    "different",
    "neutral",
    "not_better",
    "not_worse",
    "reverse",
    "same",
    "same_or_better",
    "same_or_worse",
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


neutral = Same()


@curry
def to_add(augend: Ordering, addend: Ordering) -> Ordering:
    match augend:
        case Same():
            return addend
        case _:
            return augend


add_to = flip(to_add)
