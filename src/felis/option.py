from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import felis.identity
from felis import applicative, monad, option_t
from felis.currying import curry, flip
from felis.option_t import Option, Some

__all__ = [
    "Option",
    "Some",
    "apply",
    "bind",
    "bind_to",
    "compose",
    "default_to",
    "discard_after",
    "discard_before",
    "fold",
    "guard",
    "join",
    "lift2",
    "map_by",
    "neutral",
    "pure",
    "take_after",
    "take_before",
    "to_add",
    "traverse",
    "when",
]


if TYPE_CHECKING:
    neutral: Option[Any]
else:
    neutral = option_t.neutral(felis.identity.pure)


if TYPE_CHECKING:

    @curry
    def to_add[T](augend: Option[T], addend: Option[T]) -> Option[T]: ...

else:
    to_add = option_t.to_add(felis.identity.pure)(felis.identity.bind)


@curry
def map_by[From, To](option_value: Option[From], function: Callable[[From], To]) -> Option[To]:
    match option_value:
        case None:
            return None
        case Some(value):
            return Some(function(value))


if TYPE_CHECKING:

    def pure[T](value: T, /) -> Option[T]: ...

else:
    pure = Some


if TYPE_CHECKING:

    @curry
    def apply[From, To](option_value: Option[From], option_function: Option[Callable[[From], To]]) -> Option[To]: ...

else:
    apply = option_t.apply(felis.identity.pure)(felis.identity.bind)


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[First, Second, Result](
        second: Option[Second],
        first: Option[First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> Option[Result]: ...

else:
    lift2 = applicative.lift2(map_by)(apply)


if TYPE_CHECKING:

    @curry
    def take_after[First, Second](second: Option[Second], first: Option[First]) -> Option[Second]: ...

else:
    take_after = applicative.take_after(lift2)


if TYPE_CHECKING:

    @curry
    def discard_before[First, Second](first: Option[First], second: Option[Second]) -> Option[Second]: ...

else:
    discard_before = applicative.discard_before(lift2)


if TYPE_CHECKING:

    @curry
    def discard_after[First, Second](second: Option[Second], first: Option[First]) -> Option[First]: ...

else:
    discard_after = applicative.discard_after(lift2)


if TYPE_CHECKING:

    @curry
    def take_before[First, Second](first: Option[First], second: Option[Second]) -> Option[First]: ...

else:
    take_before = applicative.take_before(lift2)


if TYPE_CHECKING:

    @curry
    def when(option_none: Option[None], bool: bool) -> Option[None]: ...

else:
    when = applicative.when(pure)


@curry
@curry
def fold[A, T](option_value: Option[T], function: Callable[[T], Callable[[A], A]], accumulator: A) -> A:
    match option_value:
        case None:
            return accumulator
        case Some(value):
            return function(value)(accumulator)


# [A : * -> *] ->
# ([From : *] -> [To : *] -> (From -> To) -> A From -> A To) ->
# ([T : *] -> T -> A T) ->
# [From : *] -> [To : *] -> (From -> A To) -> Option From -> A (Option To)
@curry
@curry
@curry
def traverse[From](
    option_value: Option[From],
    function: Callable[[From], Any],
    a_identity: Callable[[Any], Any],
    a_map: Callable[[Callable[[Any], Any]], Callable[[Any], Any]],
) -> Any:
    match option_value:
        case None:
            return a_identity(neutral)
        case Some(value):
            return a_map(pure)(function(value))


if TYPE_CHECKING:

    def join[From, To](option_option_value: Option[Option[From]]) -> Option[To]: ...

else:
    join = option_t.join(felis.identity.pure)(felis.identity.bind)


if TYPE_CHECKING:

    @curry
    def bind_to[From, To](option_value: Option[From], function: Callable[[From], Option[To]]) -> Option[To]: ...

else:
    bind_to = monad.bind_to(map_by)(join)


bind = flip(bind_to)


if TYPE_CHECKING:

    @curry
    @curry
    def compose[From, Intermediate, To](
        value: From,
        first: Callable[[From], Option[Intermediate]],
        second: Callable[[Intermediate], Option[To]],
    ) -> Option[To]: ...

else:
    compose = monad.compose(bind)


if TYPE_CHECKING:

    def guard(bool: bool) -> Option[None]: ...

else:
    guard = monad.guard(neutral)(pure)


if TYPE_CHECKING:

    @curry
    def default_to[T](option_value: Option[T], default_value: T) -> T: ...

else:
    default_to = option_t.default_to(felis.identity.pure)(felis.identity.bind)
