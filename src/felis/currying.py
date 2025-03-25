from collections.abc import Callable

__all__ = ["curry", "flip", "uncurry"]


def curry[First, *Rest, Result](function: Callable[[First, *Rest], Result]) -> Callable[[*Rest], Callable[[First], Result]]:
    return lambda *rest: lambda first: function(first, *rest)


def uncurry[First, *Rest, Result](function: Callable[[*Rest], Callable[[First], Result]]) -> Callable[[First, *Rest], Result]:
    return lambda first, *rest: function(*rest)(first)


def flip[First, Second, Result](function: Callable[[First], Callable[[Second], Result]]) -> Callable[[Second], Callable[[First], Result]]:
    return lambda second: lambda first: function(first)(second)
