from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from felis import applicative, function, monad, option, state_t
from felis.currying import curry, uncurry
from felis.option import Option
from felis.predicate import Predicate

__all__ = [
    "Parser",
    "run",
    "neutral",
    "add",
    "map",
    "identity",
    "apply",
    "lift2",
    "take_after",
    "discard_after",
    "take_before",
    "discard_before",
    "when",
    "join",
    "bind",
    "compose",
    "guard",
    "end",
    "any",
    "satisfy",
    "character",
    "text",
    "many",
    "some",
    "separated",
    "bracket",
    "digit",
    "alpha",
    "alnum",
]


type Parser[T] = Callable[[str], Option[tuple[T, str]]]


if TYPE_CHECKING:

    @curry
    def run[T](string: str, parser_value: Parser[T]) -> T: ...

else:
    run = state_t.run(option.map)


if TYPE_CHECKING:
    # [T : Type] -> Parser T
    def neutral(string: str, /) -> Option[tuple[Any, str]]: ...

else:
    neutral = state_t.neutral(option.neutral)


if TYPE_CHECKING:

    @curry
    def add[T](first: Parser[T], second: Parser[T]) -> Parser[T]: ...

else:
    add = state_t.add(option.add)


if TYPE_CHECKING:

    @curry
    def map[From, To](parser_value: Parser[From], function: Callable[[From], To]) -> Parser[To]: ...

else:
    map = state_t.map(option.map)


if TYPE_CHECKING:

    def identity[T](value: T, /) -> Parser[T]: ...

else:
    identity = state_t.identity(option.identity)


if TYPE_CHECKING:

    @curry
    def apply[From, To](parser_value: Parser[From], parser_function: Parser[Callable[[From], To]]) -> Parser[To]: ...

else:
    apply = state_t.apply(option.identity)(option.bind)


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[First, Second, Result](
        second: Parser[Second],
        first: Parser[First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> Parser[Result]: ...

else:
    lift2 = applicative.lift2(map)(apply)


take_after = lift2(function.flip(function.identity))


discard_after = lift2(function.identity)


take_before = function.flip(discard_after)


discard_before = function.flip(take_after)


if TYPE_CHECKING:

    @curry
    def when(bool: bool, parser_none: Parser[None]) -> Parser[None]: ...

else:
    when = applicative.when(identity)


if TYPE_CHECKING:

    def join[T](parser_value: Parser[Parser[T]], /) -> Parser[T]: ...

else:
    join = state_t.join(option.identity)(option.bind)


if TYPE_CHECKING:

    @curry
    def bind[From, To](parser_value: Parser[From], function: Callable[[From], Parser[To]]) -> Parser[To]: ...

else:
    bind = monad.bind(map)(join)


if TYPE_CHECKING:

    @curry
    @curry
    def compose[From, Intermediate, To](
        value: From,
        first: Callable[[From], Parser[Intermediate]],
        second: Callable[[Intermediate], Parser[To]],
    ) -> Parser[To]: ...

else:
    compose = monad.compose(bind)


if TYPE_CHECKING:

    def guard(bool: bool) -> Parser[None]: ...

else:
    guard = monad.guard(neutral)(identity)


def end(string: str) -> Option[tuple[None, str]]:
    return None if string else option.Some((None, ""))


def any(string: str) -> Option[tuple[str, str]]:
    return option.Some((string[0], string[1:])) if string else None


def satisfy(predicate: Predicate[str]) -> Parser[str]:
    return uncurry(bind)(any, lambda character: identity(character) if predicate(character) else neutral)


def character(character: str) -> Parser[str]:
    return satisfy(lambda current: current == character)


def text(string: str) -> Parser[str]:
    return take_after(character(string[0]))(take_after(text(string[1:]))(identity(string))) if string else identity("")


def many[T](parser: Parser[T]) -> Parser[list[T]]:
    return uncurry(add)(uncurry(bind)(parser, lambda first: uncurry(bind)(many(parser), lambda rest: identity([first, *rest]))), identity([]))


def some[T](parser: Parser[T]) -> Parser[list[T]]:
    return uncurry(bind)(parser, lambda first: uncurry(bind)(many(parser), lambda rest: identity([first, *rest])))


@curry
def separated[S, T](parser: Parser[T], separator: Parser[S]) -> Parser[list[T]]:
    return uncurry(add)(
        uncurry(bind)(parser, lambda first: uncurry(bind)(many(take_after(separator)(parser)), lambda rest: identity([first, *rest]))),
        identity([]),
    )


@curry
@curry
def bracket[Left, Right, T](parser: Parser[T], right: Parser[Right], left: Parser[Left]) -> Parser[T]:
    return take_after(left)(take_before(right)(parser))


digit = satisfy(str.isdigit)


alpha = satisfy(str.isalpha)


alnum = satisfy(str.isalnum)
