from dataclasses import dataclass

from felis.currying import curry

__all__ = ["Ordering", "Worse", "Equal", "Better", "worse", "not_worse", "better", "not_better", "reverse", "neutral", "add"]


type Ordering = Worse | Equal | Better


@dataclass(frozen=True)
class Worse:
    pass


@dataclass(frozen=True)
class Equal:
    pass


@dataclass(frozen=True)
class Better:
    pass


def worse(ordering: Ordering) -> bool:
    match ordering:
        case Worse():
            return True
        case _:
            return False


def not_worse(ordering: Ordering) -> bool:
    match ordering:
        case Worse():
            return False
        case _:
            return True


def better(ordering: Ordering) -> bool:
    match ordering:
        case Better():
            return True
        case _:
            return False


def not_better(ordering: Ordering) -> bool:
    match ordering:
        case Better():
            return False
        case _:
            return True


def reverse(ordering: Ordering) -> Ordering:
    match ordering:
        case Worse():
            return Better()
        case Equal():
            return Equal()
        case Better():
            return Worse()


neutral = Equal()


@curry
def add(first: Ordering, second: Ordering) -> Ordering:
    match first:
        case Equal():
            return second
        case _:
            return first
