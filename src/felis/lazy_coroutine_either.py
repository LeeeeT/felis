from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import felis.applicative
import felis.identity
import felis.monad
import felis.semigroup
from felis import either, lazy_coroutine
from felis.applicative import Applicative
from felis.currying import curry
from felis.either import Either
from felis.functor import Functor
from felis.lazy_coroutine import LazyCoroutine
from felis.monad import Monad
from felis.semigroup import Semigroup

__all__ = [
    "LazyCoroutineEither",
    "add_to",
    "applicative",
    "bind_to",
    "compose_after",
    "compose_before",
    "default_to",
    "discard_after",
    "discard_before",
    "functor",
    "join",
    "lift",
    "map_by",
    "monad",
    "pure",
    "semigroup",
    "take_after",
    "take_before",
    "to_add",
    "to_apply",
    "to_bind",
    "when",
]


type LazyCoroutineEither[L, R] = LazyCoroutine[Either[L, R]]


if TYPE_CHECKING:

    @curry
    def to_add[L, R](
        lazy_coroutine_either_augend: LazyCoroutineEither[L, R],
        lazy_coroutine_either_addend: LazyCoroutineEither[L, R],
    ) -> LazyCoroutineEither[L, R]: ...

else:
    to_add = either.to_add_t(lazy_coroutine.monad)


# [L : *] -> [R : *] -> Semigroup (LazyCoroutineEither L R)
semigroup: Semigroup[LazyCoroutineEither[Any, Any]] = Semigroup(to_add)


if TYPE_CHECKING:

    @curry
    def add_to[L, R](
        lazy_coroutine_either_addend: LazyCoroutineEither[L, R],
        lazy_coroutine_either_augend: LazyCoroutineEither[L, R],
    ) -> LazyCoroutineEither[L, R]: ...

else:
    add_to = felis.semigroup.add_to(semigroup)


if TYPE_CHECKING:

    @curry
    def map_by[L, From, To](lazy_coroutine_either_value: LazyCoroutineEither[L, From], function: Callable[[From], To]) -> LazyCoroutineEither[L, To]: ...

else:
    map_by = felis.identity.compose_after(either.map_by)(lazy_coroutine.map_by)


# [L : *] -> Functor (LazyCoroutineEither L)
functor = Functor(map_by)


pure = lazy_coroutine.map_by(either.pure)


if TYPE_CHECKING:

    @curry
    def to_apply[L, From, To](
        lazy_coroutine_either_value: LazyCoroutineEither[L, From],
        lazy_coroutine_either_function: LazyCoroutineEither[L, Callable[[From], To]],
    ) -> LazyCoroutineEither[L, To]: ...

else:
    to_apply = either.to_apply_t(lazy_coroutine.monad)


# [L : *] -> Applicative (LazyCoroutineEither L)
applicative = Applicative(functor, pure, to_apply)


if TYPE_CHECKING:

    @curry
    def apply_to[L, From, To](
        lazy_coroutine_either_function: LazyCoroutineEither[L, Callable[[From], To]],
        lazy_coroutine_either_value: LazyCoroutineEither[L, From],
    ) -> LazyCoroutineEither[L, To]: ...

else:
    apply_to = felis.applicative.apply_to(applicative)


if TYPE_CHECKING:

    @curry
    @curry
    def lift[L, First, Second, Result](
        second: LazyCoroutineEither[L, Second],
        first: LazyCoroutineEither[L, First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> LazyCoroutineEither[L, Result]: ...

else:
    lift = felis.applicative.lift(applicative)


if TYPE_CHECKING:

    @curry
    def take_after[L, First, Second](second: LazyCoroutineEither[L, Second], first: LazyCoroutineEither[L, First]) -> LazyCoroutineEither[L, Second]: ...

else:
    take_after = felis.applicative.take_after(applicative)


if TYPE_CHECKING:

    @curry
    def discard_before[L, First, Second](first: LazyCoroutineEither[L, First], second: LazyCoroutineEither[L, Second]) -> LazyCoroutineEither[L, Second]: ...

else:
    discard_before = felis.applicative.discard_before(applicative)


if TYPE_CHECKING:

    @curry
    def discard_after[L, First, Second](second: LazyCoroutineEither[L, Second], first: LazyCoroutineEither[L, First]) -> LazyCoroutineEither[L, First]: ...

else:
    discard_after = felis.applicative.discard_after(applicative)


if TYPE_CHECKING:

    @curry
    def take_before[L, First, Second](first: LazyCoroutineEither[L, First], second: LazyCoroutineEither[L, Second]) -> LazyCoroutineEither[L, First]: ...

else:
    take_before = felis.applicative.take_before(applicative)


if TYPE_CHECKING:

    @curry
    def when[L](lazy_coroutine_either_none: LazyCoroutineEither[L, None], bool: bool) -> LazyCoroutineEither[L, None]: ...

else:
    when = felis.applicative.when(applicative)


if TYPE_CHECKING:

    def join[L, R](lazy_coroutine_either_lazy_coroutine_either_value: LazyCoroutineEither[L, LazyCoroutineEither[L, R]], /) -> LazyCoroutineEither[L, R]: ...

else:
    join = either.join_t(lazy_coroutine.monad)


# [L : *] -> Monad (LazyCoroutineEither L)
monad = Monad(applicative, join)


if TYPE_CHECKING:

    @curry
    def bind_to[L, From, To](
        lazy_coroutine_either_value: LazyCoroutineEither[L, From],
        function: Callable[[From], LazyCoroutineEither[L, To]],
    ) -> LazyCoroutineEither[L, To]: ...

else:
    bind_to = felis.monad.bind_to(monad)


if TYPE_CHECKING:

    @curry
    def to_bind[L, From, To](
        function: Callable[[From], LazyCoroutineEither[L, To]],
        lazy_coroutine_either_value: LazyCoroutineEither[L, From],
    ) -> LazyCoroutineEither[L, To]: ...

else:
    to_bind = felis.monad.to_bind(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_after[L, From, Intermediate, To](
        value: From,
        second: Callable[[Intermediate], LazyCoroutineEither[L, To]],
        first: Callable[[From], LazyCoroutineEither[L, Intermediate]],
    ) -> LazyCoroutineEither[L, To]: ...

else:
    compose_after = felis.monad.compose_after(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_before[L, From, Intermediate, To](
        value: From,
        first: Callable[[From], LazyCoroutineEither[L, Intermediate]],
        second: Callable[[Intermediate], LazyCoroutineEither[L, To]],
    ) -> LazyCoroutineEither[L, To]: ...

else:
    compose_before = felis.monad.compose_before(monad)


if TYPE_CHECKING:

    @curry
    def default_to[L, R](lazy_coroutine_either_value: LazyCoroutineEither[L, R], default_value: LazyCoroutine[R]) -> LazyCoroutine[R]: ...

else:
    default_to = either.default_to_t(lazy_coroutine.monad)
