from collections.abc import Callable

from felis.currying import curry

__all__ = ["bind", "compose", "then", "guard"]


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


@curry
@curry
def then[First, MFirst, MSecond](first: MFirst, second: MSecond, bind: Callable[[Callable[[First], MSecond]], Callable[[MFirst], MSecond]]) -> MSecond:
    return bind(lambda _: second)(first)


@curry
@curry
def guard[MNone](bool: bool, identity: Callable[[None], MNone], neutral: MNone) -> MNone:
    return identity(None) if bool else neutral
