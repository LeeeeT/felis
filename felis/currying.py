from collections.abc import Callable

__all__ = ["curry", "uncurry"]


def curry[First, *Rest, Result](function: Callable[[First, *Rest], Result]) -> Callable[[*Rest], Callable[[First], Result]]:
    return lambda *rest: lambda first: function(first, *rest)


def uncurry[First, *Rest, Result](function: Callable[[*Rest], Callable[[First], Result]]) -> Callable[[First, *Rest], Result]:
    return lambda first, *rest: function(*rest)(first)
