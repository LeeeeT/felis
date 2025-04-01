from collections.abc import Callable
from typing import TYPE_CHECKING

import felis.applicative
import felis.functor
import felis.identity
import felis.monad
from felis import coroutine, lazy
from felis.applicative import Applicative
from felis.coroutine import Coroutine
from felis.currying import curry
from felis.functor import Functor
from felis.lazy import Lazy
from felis.monad import Monad

__all__ = [
    "LazyCoroutine",
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


type LazyCoroutine[T] = Lazy[Coroutine[T]]


if TYPE_CHECKING:

    @curry
    def map_by[From, To](lazy_coroutine_value: LazyCoroutine[From], function: Callable[[From], To]) -> LazyCoroutine[To]: ...

else:
    map_by = felis.identity.compose_after(coroutine.map_by)(lazy.map_by)


# Functor LazyCoroutine
functor = Functor(map_by)


if TYPE_CHECKING:

    @curry
    def by_map[From, To](function: Callable[[From], To], lazy_coroutine_value: LazyCoroutine[From]) -> LazyCoroutine[To]: ...

else:
    by_map = felis.functor.by_map(functor)


if TYPE_CHECKING:

    def pure[T](value: T, /) -> LazyCoroutine[T]: ...

else:
    pure = lazy.pure_t(coroutine.applicative)


if TYPE_CHECKING:

    @curry
    def to_apply[From, To](lazy_coroutine_value: LazyCoroutine[From], lazy_coroutine_function: LazyCoroutine[Callable[[From], To]]) -> LazyCoroutine[To]: ...

else:
    to_apply = lazy.to_apply_t(coroutine.monad)


# Applicative LazyCoroutine
applicative = Applicative(functor, pure, to_apply)


if TYPE_CHECKING:

    @curry
    def apply_to[From, To](lazy_coroutine_function: LazyCoroutine[Callable[[From], To]], lazy_coroutine_value: LazyCoroutine[From]) -> LazyCoroutine[To]: ...

else:
    apply_to = felis.applicative.apply_to(applicative)


if TYPE_CHECKING:

    @curry
    @curry
    def lift[First, Second, Result](
        second: LazyCoroutine[Second],
        first: LazyCoroutine[First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> LazyCoroutine[Result]: ...

else:
    lift = felis.applicative.lift(applicative)


if TYPE_CHECKING:

    @curry
    def take_after[First, Second](second: LazyCoroutine[Second], first: LazyCoroutine[First]) -> LazyCoroutine[Second]: ...

else:
    take_after = felis.applicative.take_after(applicative)


if TYPE_CHECKING:

    @curry
    def discard_before[First, Second](first: LazyCoroutine[First], second: LazyCoroutine[Second]) -> LazyCoroutine[Second]: ...

else:
    discard_before = felis.applicative.discard_before(applicative)


if TYPE_CHECKING:

    @curry
    def discard_after[First, Second](second: LazyCoroutine[Second], first: LazyCoroutine[First]) -> LazyCoroutine[First]: ...

else:
    discard_after = felis.applicative.discard_after(applicative)


if TYPE_CHECKING:

    @curry
    def take_before[First, Second](first: LazyCoroutine[First], second: LazyCoroutine[Second]) -> LazyCoroutine[First]: ...

else:
    take_before = felis.applicative.take_before(applicative)


if TYPE_CHECKING:

    @curry
    def when(lazy_coroutine_none: LazyCoroutine[None], bool: bool) -> LazyCoroutine[None]: ...

else:
    when = felis.applicative.when(applicative)


if TYPE_CHECKING:

    def join[T](lazy_coroutine_lazy_coroutine_value: LazyCoroutine[LazyCoroutine[T]], /) -> LazyCoroutine[T]: ...

else:
    join = lazy.join_t(coroutine.monad)


# Monad LazyCoroutine
monad = Monad(applicative, join)


if TYPE_CHECKING:

    @curry
    def bind_to[From, To](lazy_coroutine_value: LazyCoroutine[From], function: Callable[[From], LazyCoroutine[To]]) -> LazyCoroutine[To]: ...

else:
    bind_to = felis.monad.bind_to(monad)


if TYPE_CHECKING:

    @curry
    def to_bind[From, To](function: Callable[[From], LazyCoroutine[To]], lazy_coroutine_value: LazyCoroutine[From]) -> LazyCoroutine[To]: ...

else:
    to_bind = felis.monad.to_bind(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_after[From, Intermediate, To](
        value: From,
        second: Callable[[Intermediate], LazyCoroutine[To]],
        first: Callable[[From], LazyCoroutine[Intermediate]],
    ) -> LazyCoroutine[To]: ...

else:
    compose_after = felis.monad.compose_after(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_before[From, Intermediate, To](
        value: From,
        first: Callable[[From], LazyCoroutine[Intermediate]],
        second: Callable[[Intermediate], LazyCoroutine[To]],
    ) -> LazyCoroutine[To]: ...

else:
    compose_before = felis.monad.compose_before(monad)
