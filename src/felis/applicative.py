from collections.abc import Callable

from felis.currying import curry

__all__ = ["lift2"]


@curry
@curry
@curry
def lift2[A, AA, AB, AC, CallableBC, ACallableBC](
    first: AA,
    function: Callable[[A], CallableBC],
    a_apply: Callable[[ACallableBC], Callable[[AB], AC]],
    a_map: Callable[[Callable[[A], CallableBC]], Callable[[AA], ACallableBC]],
) -> Callable[[AB], AC]:
    return a_apply(a_map(function)(first))
