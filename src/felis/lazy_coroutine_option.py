from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import felis.alternative
import felis.applicative
import felis.functor
import felis.identity
import felis.monad
import felis.semigroup
from felis import lazy_coroutine, option
from felis.alternative import Alternative
from felis.applicative import Applicative
from felis.currying import curry
from felis.functor import Functor
from felis.lazy_coroutine import LazyCoroutine
from felis.monad import Monad
from felis.monoid import Monoid
from felis.option import Option
from felis.semigroup import Semigroup

if TYPE_CHECKING:
    from felis import Either

__all__ = [
    "LazyCoroutineOption",
    "add_to",
    "alternative",
    "applicative",
    "bind_to",
    "compose_after",
    "compose_before",
    "default_to",
    "discard_after",
    "discard_before",
    "functor",
    "guard",
    "join",
    "lift",
    "map_by",
    "monad",
    "neutral",
    "pure",
    "semigroup",
    "take_after",
    "take_before",
    "to_add",
    "to_apply",
    "to_bind",
    "to_either",
    "when",
]


type LazyCoroutineOption[T] = LazyCoroutine[Option[T]]


if TYPE_CHECKING:

    @curry
    def to_add[T](lazy_coroutine_option_augend: LazyCoroutineOption[T], lazy_coroutine_option_addend: LazyCoroutineOption[T]) -> LazyCoroutineOption[T]: ...

else:
    to_add = option.to_add_t(lazy_coroutine.monad)


# [T : *] -> Semigroup (LazyCoroutineOption T)
semigroup: Semigroup[Any] = Semigroup(to_add)


if TYPE_CHECKING:

    @curry
    def add_to[T](lazy_coroutine_option_addend: LazyCoroutineOption[T], lazy_coroutine_option_augend: LazyCoroutineOption[T]) -> LazyCoroutineOption[T]: ...

else:
    add_to = felis.semigroup.add_to(semigroup)


# [T : *] -> LazyCoroutineOption T
neutral: LazyCoroutineOption[Any] = option.neutral_t(lazy_coroutine.monad)


# [T : *] -> Monoid (LazyCoroutineOption T)
monoid = Monoid(semigroup, neutral)


if TYPE_CHECKING:

    @curry
    def map_by[From, To](lazy_coroutine_option_value: LazyCoroutineOption[From], function: Callable[[From], To]) -> LazyCoroutineOption[To]: ...

else:
    map_by = felis.identity.compose_after(option.map_by)(lazy_coroutine.map_by)


# Functor LazyCoroutineOption
functor = Functor(map_by)


if TYPE_CHECKING:

    @curry
    def by_map[From, To](function: Callable[[From], To], lazy_coroutine_option_value: LazyCoroutineOption[From]) -> LazyCoroutineOption[To]: ...

else:
    by_map = felis.functor.by_map(functor)


pure = lazy_coroutine.map_by(option.pure)


if TYPE_CHECKING:

    @curry
    def to_apply[From, To](
        lazy_coroutine_option_value: LazyCoroutineOption[From],
        lazy_coroutine_option_function: LazyCoroutineOption[Callable[[From], To]],
    ) -> LazyCoroutineOption[To]: ...

else:
    to_apply = option.to_apply_t(lazy_coroutine.monad)


# Applicative LazyCoroutineOption
applicative = Applicative(functor, pure, to_apply)


if TYPE_CHECKING:

    @curry
    @curry
    def lift[First, Second, Result](
        second: LazyCoroutineOption[Second],
        first: LazyCoroutineOption[First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> LazyCoroutineOption[Result]: ...

else:
    lift = felis.applicative.lift(applicative)


if TYPE_CHECKING:

    @curry
    def take_after[First, Second](second: LazyCoroutineOption[Second], first: LazyCoroutineOption[First]) -> LazyCoroutineOption[Second]: ...

else:
    take_after = felis.applicative.take_after(applicative)


if TYPE_CHECKING:

    @curry
    def discard_before[First, Second](first: LazyCoroutineOption[First], second: LazyCoroutineOption[Second]) -> LazyCoroutineOption[Second]: ...

else:
    discard_before = felis.applicative.discard_before(applicative)


if TYPE_CHECKING:

    @curry
    def discard_after[First, Second](second: LazyCoroutineOption[Second], first: LazyCoroutineOption[First]) -> LazyCoroutineOption[First]: ...

else:
    discard_after = felis.applicative.discard_after(applicative)


if TYPE_CHECKING:

    @curry
    def take_before[First, Second](first: LazyCoroutineOption[First], second: LazyCoroutineOption[Second]) -> LazyCoroutineOption[First]: ...

else:
    take_before = felis.applicative.take_before(applicative)


if TYPE_CHECKING:

    @curry
    def when(lazy_coroutine_option_none: LazyCoroutineOption[None], bool: bool) -> LazyCoroutineOption[None]: ...

else:
    when = felis.applicative.when(applicative)


# Alternative LazyCoroutineOption
alternative = Alternative(monoid, applicative)


if TYPE_CHECKING:

    def guard(bool: bool, /) -> LazyCoroutineOption[None]: ...

else:
    guard = felis.alternative.guard(alternative)


if TYPE_CHECKING:

    def join[T](lazy_coroutine_option_lazy_coroutine_option_value: LazyCoroutineOption[LazyCoroutineOption[T]], /) -> LazyCoroutineOption[T]: ...

else:
    join = option.join_t(lazy_coroutine.monad)


# Monad LazyCoroutineOption
monad = Monad(applicative, join)


if TYPE_CHECKING:

    @curry
    def bind_to[From, To](
        lazy_coroutine_option_value: LazyCoroutineOption[From],
        function: Callable[[From], LazyCoroutineOption[To]],
    ) -> LazyCoroutineOption[To]: ...

else:
    bind_to = felis.monad.bind_to(monad)


if TYPE_CHECKING:

    @curry
    def to_bind[From, To](
        function: Callable[[From], LazyCoroutineOption[To]],
        lazy_coroutine_option_value: LazyCoroutineOption[From],
    ) -> LazyCoroutineOption[To]: ...

else:
    to_bind = felis.monad.to_bind(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_after[From, Intermediate, To](
        value: From,
        second: Callable[[Intermediate], LazyCoroutineOption[To]],
        first: Callable[[From], LazyCoroutineOption[Intermediate]],
    ) -> LazyCoroutineOption[To]: ...

else:
    compose_after = felis.monad.compose_after(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_before[From, Intermediate, To](
        value: From,
        first: Callable[[From], LazyCoroutineOption[Intermediate]],
        second: Callable[[Intermediate], LazyCoroutineOption[To]],
    ) -> LazyCoroutineOption[To]: ...

else:
    compose_before = felis.monad.compose_before(monad)


if TYPE_CHECKING:

    @curry
    def default_to[T](lazy_coroutine_option_value: LazyCoroutineOption[T], default_value: LazyCoroutine[T]) -> LazyCoroutine[T]: ...

else:
    default_to = option.default_to_t(lazy_coroutine.monad)


if TYPE_CHECKING:

    @curry
    def to_either[L, R](coroutine_option_value: LazyCoroutineOption[R], left: LazyCoroutine[L]) -> LazyCoroutine[Either[L, R]]: ...

else:
    to_either = option.to_either_t(lazy_coroutine.monad)
