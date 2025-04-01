import collections.abc
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import felis.applicative
import felis.functor
import felis.monad
from felis.applicative import Applicative
from felis.currying import curry
from felis.functor import Functor
from felis.monad import Monad

__all__ = [
    "Coroutine",
    "applicative",
    "apply_to",
    "bind_to",
    "by_map",
    "compose_after",
    "compose_before",
    "discard_after",
    "discard_before",
    "functor",
    "join",
    "lift",
    "map_by",
    "monad",
    "pure",
    "take_after",
    "take_before",
    "to_apply",
    "to_bind",
    "when",
]


type Coroutine[T] = collections.abc.Coroutine[Any, Any, T]


@curry
async def map_by[From, To](coroutine_value: Coroutine[From], function: Callable[[From], To]) -> To:
    return function(await coroutine_value)


functor = Functor(map_by)


if TYPE_CHECKING:

    @curry
    def by_map[From, To](function: Callable[[From], To], coroutine_value: Coroutine[From]) -> Coroutine[To]: ...

else:
    by_map = felis.functor.by_map(functor)


async def pure[T](value: T) -> T:
    return value


@curry
async def to_apply[From, To](coroutine_value: Coroutine[From], coroutine_function: Coroutine[Callable[[From], To]]) -> To:
    return await map_by(await coroutine_function)(coroutine_value)


applicative = Applicative(functor, pure, to_apply)


if TYPE_CHECKING:

    @curry
    async def apply_to[From, To](coroutine_function: Coroutine[Callable[[From], To]], coroutine_value: Coroutine[From]) -> To: ...

else:
    apply_to = felis.applicative.apply_to(applicative)


if TYPE_CHECKING:

    @curry
    @curry
    def lift[First, Second, Result](
        second: Coroutine[Second],
        first: Coroutine[First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> Coroutine[Result]: ...

else:
    lift = felis.applicative.lift(applicative)


if TYPE_CHECKING:

    @curry
    def take_after[First, Second](second: Coroutine[Second], first: Coroutine[First]) -> Coroutine[Second]: ...

else:
    take_after = felis.applicative.take_after(applicative)


if TYPE_CHECKING:

    @curry
    def discard_before[First, Second](first: Coroutine[First], second: Coroutine[Second]) -> Coroutine[Second]: ...

else:
    discard_before = felis.applicative.discard_before(applicative)


if TYPE_CHECKING:

    @curry
    def discard_after[First, Second](second: Coroutine[Second], first: Coroutine[First]) -> Coroutine[First]: ...

else:
    discard_after = felis.applicative.discard_after(applicative)


if TYPE_CHECKING:

    @curry
    def take_before[First, Second](first: Coroutine[First], second: Coroutine[Second]) -> Coroutine[First]: ...

else:
    take_before = felis.applicative.take_before(applicative)


if TYPE_CHECKING:

    @curry
    def when(coroutine_none: Coroutine[None], bool: bool) -> Coroutine[None]: ...

else:
    when = felis.applicative.when(applicative)


async def join[T](coroutine_coroutine_value: Coroutine[Coroutine[T]]) -> T:
    return await (await coroutine_coroutine_value)


monad = Monad(applicative, join)


if TYPE_CHECKING:

    @curry
    def bind_to[From, To](coroutine_value: Coroutine[From], function: Callable[[From], Coroutine[To]]) -> Coroutine[To]: ...

else:
    bind_to = felis.monad.bind_to(monad)


if TYPE_CHECKING:

    @curry
    def to_bind[From, To](function: Callable[[From], Coroutine[To]], coroutine_value: Coroutine[From]) -> Coroutine[To]: ...

else:
    to_bind = felis.monad.to_bind(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_after[From, Intermediate, To](
        value: From,
        second: Callable[[Intermediate], Coroutine[To]],
        first: Callable[[From], Coroutine[Intermediate]],
    ) -> Coroutine[To]: ...

else:
    compose_after = felis.monad.compose_after(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_before[From, Intermediate, To](
        value: From,
        first: Callable[[From], Coroutine[Intermediate]],
        second: Callable[[Intermediate], Coroutine[To]],
    ) -> Coroutine[To]: ...

else:
    compose_before = felis.monad.compose_before(monad)
