from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import felis.applicative
import felis.functor
import felis.identity
import felis.monad
from felis.applicative import Applicative
from felis.currying import curry
from felis.functor import Functor
from felis.monad import Monad

__all__ = [
    "Lazy",
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
    "join_t",
    "lift",
    "map_by",
    "monad",
    "pure",
    "pure_t",
    "run",
    "take_after",
    "take_before",
    "to_apply",
    "to_apply_t",
    "to_bind",
    "when",
]


type Lazy[T] = Callable[[], T]


def run[T](lazy_value: Lazy[T]) -> T:
    return lazy_value()


@curry
def map_by[From, To](lazy_value: Lazy[From], function: Callable[[From], To]) -> Lazy[To]:
    return lambda: function(lazy_value())


# Functor Lazy
functor = Functor(map_by)


if TYPE_CHECKING:

    @curry
    def by_map[From, To](function: Callable[[From], To], lazy_value: Lazy[From]) -> Lazy[To]: ...

else:
    by_map = felis.functor.by_map(functor)


# [A : * -> *] -> Applicative A -> [T : *] -> T -> Lazy (A T)
@curry
def pure_t(value: Any, applicative: Applicative) -> Lazy[Any]:
    return lambda: felis.applicative.pure(applicative)(value)


if TYPE_CHECKING:

    def pure[T](value: T, /) -> Lazy[T]: ...

else:
    pure = pure_t(felis.identity.applicative)


# [M : * -> *] -> Monad M -> [From : *] -> [To : *] -> Lazy (M (From -> To)) -> Lazy (M From) -> Lazy (M To)
@curry
@curry
def to_apply_t(lazy_m_value: Lazy[Any], lazy_m_function: Lazy[Any], m: Monad) -> Lazy[Any]:
    return lambda: felis.monad.to_bind(m)(lazy_m_function())(
        lambda function: felis.monad.to_bind(m)(lazy_m_value())(lambda value: felis.monad.pure(m)(function(value))),
    )


if TYPE_CHECKING:

    @curry
    def to_apply[From, To](lazy_value: Lazy[From], lazy_function: Lazy[Callable[[From], To]]) -> Lazy[To]: ...

else:
    to_apply = to_apply_t(felis.identity.monad)


# Applicative Lazy
applicative = Applicative(functor, pure, to_apply)


if TYPE_CHECKING:

    @curry
    def apply_to[From, To](lazy_function: Lazy[Callable[[From], To]], lazy_value: Lazy[From]) -> Lazy[To]: ...

else:
    apply_to = felis.applicative.apply_to(applicative)


if TYPE_CHECKING:

    @curry
    @curry
    def lift[First, Second, Result](second: Lazy[Second], first: Lazy[First], function: Callable[[First], Callable[[Second], Result]]) -> Lazy[Result]: ...

else:
    lift = felis.applicative.lift(applicative)


if TYPE_CHECKING:

    @curry
    def take_after[First, Second](second: Lazy[Second], first: Lazy[First]) -> Lazy[Second]: ...

else:
    take_after = felis.applicative.take_after(applicative)


if TYPE_CHECKING:

    @curry
    def discard_before[First, Second](first: Lazy[First], second: Lazy[Second]) -> Lazy[Second]: ...

else:
    discard_before = felis.applicative.discard_before(applicative)


if TYPE_CHECKING:

    @curry
    def discard_after[First, Second](second: Lazy[Second], first: Lazy[First]) -> Lazy[First]: ...

else:
    discard_after = felis.applicative.discard_after(applicative)


if TYPE_CHECKING:

    @curry
    def take_before[First, Second](first: Lazy[First], second: Lazy[Second]) -> Lazy[First]: ...

else:
    take_before = felis.applicative.take_before(applicative)


if TYPE_CHECKING:

    @curry
    def when(lazy_none: Lazy[None], bool: bool) -> Lazy[None]: ...

else:
    when = felis.applicative.when(applicative)


# [M : * -> *] -> Monad M -> [T : *] -> Lazy (M (Lazy (M T))) -> Lazy (M T)
@curry
def join_t(lazy_m_lazy_m_value: Lazy[Any], m: Monad) -> Lazy[Any]:
    return lambda: felis.monad.to_bind(m)(lazy_m_lazy_m_value())(lambda m_lazy_value: m_lazy_value())


if TYPE_CHECKING:

    def join[T](lazy_lazy_value: Lazy[Lazy[T]], /) -> Lazy[T]: ...

else:
    join = join_t(felis.identity.monad)


# Monad Lazy
monad = Monad(applicative, join)


if TYPE_CHECKING:

    @curry
    def bind_to[From, To](lazy_value: Lazy[From], function: Callable[[From], Lazy[To]]) -> Lazy[To]: ...

else:
    bind_to = felis.monad.bind_to(monad)


if TYPE_CHECKING:

    @curry
    def to_bind[From, To](function: Callable[[From], Lazy[To]], lazy_value: Lazy[From]) -> Lazy[To]: ...

else:
    to_bind = felis.monad.to_bind(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_after[From, Intermediate, To](
        value: From,
        second: Callable[[Intermediate], Lazy[To]],
        first: Callable[[From], Lazy[Intermediate]],
    ) -> Lazy[To]: ...

else:
    compose_after = felis.monad.compose_after(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_before[From, Intermediate, To](
        value: From,
        first: Callable[[From], Lazy[Intermediate]],
        second: Callable[[Intermediate], Lazy[To]],
    ) -> Lazy[To]: ...

else:
    compose_before = felis.monad.compose_before(monad)
