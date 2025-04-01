from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import felis.alternative
import felis.applicative
import felis.functor
import felis.identity
import felis.monad
import felis.semigroup
from felis import function, option
from felis.alternative import Alternative
from felis.applicative import Applicative
from felis.currying import curry
from felis.function import Function
from felis.functor import Functor
from felis.monad import Monad
from felis.monoid import Monoid
from felis.option import Option
from felis.semigroup import Semigroup

__all__ = [
    "FunctionOption",
    "add_to",
    "alternative",
    "applicative",
    "apply_to",
    "bind_to",
    "by_map",
    "compose_after",
    "compose_before",
    "discard_after",
    "discard_before",
    "functor",
    "guard",
    "join",
    "lift",
    "map_by",
    "monad",
    "monoid",
    "neutral",
    "pure",
    "semigroup",
    "take_after",
    "take_before",
    "to_add",
    "to_apply",
    "to_bind",
    "when",
]


type FunctionOption[From, To] = Function[From, Option[To]]


if TYPE_CHECKING:

    @curry
    def to_add[From, To](function_option_augend: FunctionOption[From, To], function_option_addend: FunctionOption[From, To]) -> FunctionOption[From, To]: ...

else:
    to_add = option.to_add_t(function.monad)


# [From : *] -> [To : *] -> Semigroup (FunctionOption From To)
semigroup: Semigroup[Any] = Semigroup(to_add)


if TYPE_CHECKING:

    @curry
    def add_to[From, To](function_option_addend: FunctionOption[From, To], function_option_augend: FunctionOption[From, To]) -> FunctionOption[From, To]: ...

else:
    add_to = felis.semigroup.add_to(semigroup)


neutral: FunctionOption[Any, Any] = option.neutral_t(function.monad)


# [From : *] -> [To : *] -> Monoid (FunctionOption From To)
monoid = Monoid(semigroup, neutral)


if TYPE_CHECKING:

    @curry
    def map_by[T, From, To](function_option_value: FunctionOption[T, From], function: Callable[[From], To]) -> FunctionOption[T, To]: ...

else:
    map_by = felis.identity.compose_after(option.map_by)(function.map_by)


# [T : *] -> Functor (FunctionOption T)
functor = Functor(map_by)


if TYPE_CHECKING:

    @curry
    def by_map[T, From, To](function: Callable[[From], To], function_option_value: FunctionOption[T, From]) -> FunctionOption[T, To]: ...

else:
    by_map = felis.functor.by_map(functor)


pure = function.map_by(option.pure)


if TYPE_CHECKING:

    @curry
    def to_apply[T, From, To](function_option_value: FunctionOption[T, From], function: FunctionOption[T, Callable[[From], To]]) -> FunctionOption[T, To]: ...

else:
    to_apply = option.to_apply_t(function.monad)


# [T : *] -> Applicative (FunctionOption T)
applicative = Applicative(functor, pure, to_apply)


if TYPE_CHECKING:

    @curry
    def apply_to[T, From, To](function: FunctionOption[T, Callable[[From], To]], function_option_value: FunctionOption[T, From]) -> FunctionOption[T, To]: ...

else:
    apply_to = felis.applicative.apply_to(applicative)


if TYPE_CHECKING:

    @curry
    @curry
    def lift[T, First, Second, Result](
        second: FunctionOption[T, Second],
        first: FunctionOption[T, First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> FunctionOption[T, Result]: ...

else:
    lift = felis.applicative.lift(applicative)


if TYPE_CHECKING:

    @curry
    def take_after[T, First, Second](second: FunctionOption[T, Second], first: FunctionOption[T, First]) -> FunctionOption[T, Second]: ...

else:
    take_after = felis.applicative.take_after(applicative)


if TYPE_CHECKING:

    @curry
    def discard_before[T, First, Second](first: FunctionOption[T, First], second: FunctionOption[T, Second]) -> FunctionOption[T, Second]: ...

else:
    discard_before = felis.applicative.discard_before(applicative)


if TYPE_CHECKING:

    @curry
    def discard_after[T, First, Second](second: FunctionOption[T, Second], first: FunctionOption[T, First]) -> FunctionOption[T, First]: ...

else:
    discard_after = felis.applicative.discard_after(applicative)


if TYPE_CHECKING:

    @curry
    def take_before[T, First, Second](first: FunctionOption[T, First], second: FunctionOption[T, Second]) -> FunctionOption[T, First]: ...

else:
    take_before = felis.applicative.take_before(applicative)


if TYPE_CHECKING:

    @curry
    def when[T](function_option_none: FunctionOption[T, None], bool: bool) -> FunctionOption[T, None]: ...

else:
    when = felis.applicative.when(applicative)


# [T : *] -> Alternative (FunctionOption T)
alternative = Alternative(monoid, applicative)


if TYPE_CHECKING:

    def guard(bool: bool, /) -> FunctionOption[Any, None]: ...

else:
    guard = felis.alternative.guard(alternative)


if TYPE_CHECKING:

    def join[T, From, To](function_option_function_option_value: FunctionOption[T, FunctionOption[T, From]]) -> FunctionOption[T, To]: ...

else:
    join = option.join_t(function.monad)


# [T : *] -> Monad (FunctionOption T)
monad = Monad(applicative, join)


if TYPE_CHECKING:

    @curry
    def bind_to[T, From, To](function_option_value: FunctionOption[T, From], function: Callable[[From], FunctionOption[T, To]]) -> FunctionOption[T, To]: ...

else:
    bind_to = felis.monad.bind_to(monad)


if TYPE_CHECKING:

    @curry
    def to_bind[T, From, To](function: Callable[[From], FunctionOption[T, To]], function_option_value: FunctionOption[T, From]) -> FunctionOption[T, To]: ...

else:
    to_bind = felis.monad.to_bind(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_after[T, From, Intermediate, To](
        value: From,
        second: Callable[[Intermediate], FunctionOption[T, To]],
        first: Callable[[From], FunctionOption[T, Intermediate]],
    ) -> FunctionOption[T, To]: ...

else:
    compose_after = felis.monad.compose_after(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_before[T, From, Intermediate, To](
        value: From,
        first: Callable[[From], FunctionOption[T, Intermediate]],
        second: Callable[[Intermediate], FunctionOption[T, To]],
    ) -> FunctionOption[T, To]: ...

else:
    compose_before = felis.monad.compose_before(monad)
