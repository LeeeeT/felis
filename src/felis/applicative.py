from collections.abc import Callable

from felis.currying import curry

__all__ = ["lift2", "when"]


@curry
@curry
@curry
def lift2[A, AA, AB, AC, CallableBC, ACallableBC](
    first: AA,
    function: Callable[[A], CallableBC],
    apply: Callable[[ACallableBC], Callable[[AB], AC]],
    map: Callable[[Callable[[A], CallableBC]], Callable[[AA], ACallableBC]],
) -> Callable[[AB], AC]:
    return apply(map(function)(first))


@curry
@curry
def when[ANone](a_none: ANone, bool: bool, identity: Callable[[None], ANone]) -> ANone:
    return a_none if bool else identity(None)
