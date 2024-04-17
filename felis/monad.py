from collections.abc import Callable

from felis.currying import curry

__all__ = ["bind", "compose"]


@curry
@curry
@curry
def bind[From, MFrom, MTo, MMTo](
    m_value: MFrom,
    function: Callable[[From], MTo],
    join: Callable[[MMTo], MTo],
    map: Callable[[Callable[[From], MTo]], Callable[[MFrom], MMTo]],
) -> MTo:
    return join(map(function)(m_value))


@curry
@curry
@curry
def compose[From, Intermediate, MIntermediate, MTo](
    value: From,
    first: Callable[[From], MIntermediate],
    second: Callable[[Intermediate], MTo],
    bind: Callable[[Callable[[Intermediate], MTo]], Callable[[MIntermediate], MTo]],
) -> MTo:
    return bind(second)(first(value))
