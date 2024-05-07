from dataclasses import dataclass

from felis.currying import curry

__all__ = ["Ordering", "Worse", "Same", "Better", "worse", "not_worse", "same", "different", "better", "not_better", "reverse", "neutral", "add"]


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


def worse(ordering: Ordering) -> bool:
    return isinstance(ordering, Worse)


def not_worse(ordering: Ordering) -> bool:
    return not worse(ordering)


def same(ordering: Ordering) -> bool:
    return isinstance(ordering, Same)


def different(ordering: Ordering) -> bool:
    return not same(ordering)


def better(ordering: Ordering) -> bool:
    return isinstance(ordering, Better)


def not_better(ordering: Ordering) -> bool:
    return not better(ordering)


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
def add(first: Ordering, second: Ordering) -> Ordering:
    match first:
        case Same():
            return second
        case _:
            return first
