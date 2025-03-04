from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import felis.list
import felis.option
from felis import applicative, function, monad, option_t, state_t
from felis.currying import curry
from felis.option import Option
from felis.predicate import Predicate

__all__ = [
    "Parser",
    "add",
    "alnum",
    "alpha",
    "any",
    "apply",
    "bind",
    "bound",
    "bracket",
    "chain_left",
    "chain_left_1",
    "chain_right",
    "chain_right_1",
    "character",
    "compose",
    "digit",
    "discard_after",
    "discard_before",
    "end",
    "guard",
    "identity",
    "join",
    "lift2",
    "many",
    "map",
    "neutral",
    "option",
    "run",
    "satisfy",
    "separated",
    "some",
    "take_after",
    "take_before",
    "text",
    "when",
]


type Parser[T] = Callable[[str], Option[tuple[T, str]]]


if TYPE_CHECKING:

    @curry
    def run[T](string: str, parser_value: Parser[T]) -> Option[T]: ...

else:
    run = state_t.run(felis.option.map)


if TYPE_CHECKING:
    # [T : Type] -> Parser T
    def neutral(string: str, /) -> Option[tuple[Any, str]]: ...

else:
    neutral = option_t.neutral(function.identity)


if TYPE_CHECKING:

    @curry
    def add[T](first: Parser[T], second: Parser[T]) -> Parser[T]: ...

else:
    add = option_t.add(function.bind)


if TYPE_CHECKING:

    @curry
    def map[From, To](parser_value: Parser[From], function: Callable[[From], To]) -> Parser[To]: ...

else:
    map = state_t.map(felis.option.map)


if TYPE_CHECKING:

    def identity[T](value: T, /) -> Parser[T]: ...

else:
    identity = state_t.identity(felis.option.identity)


if TYPE_CHECKING:

    @curry
    def apply[From, To](parser_value: Parser[From], parser_function: Parser[Callable[[From], To]]) -> Parser[To]: ...

else:
    apply = state_t.apply(felis.option.identity)(felis.option.bind)


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
    join = state_t.join(felis.option.identity)(felis.option.bind)


if TYPE_CHECKING:

    @curry
    def bound[From, To](parser_value: Parser[From], function: Callable[[From], Parser[To]]) -> Parser[To]: ...

else:
    bound = monad.bound(map)(join)


bind = function.flip(bound)


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
    return None if string else felis.option.Some((None, ""))


def any(string: str) -> Option[tuple[str, str]]:
    return felis.option.Some((string[0], string[1:])) if string else None


def satisfy(predicate: Predicate[str]) -> Parser[str]:
    return bind(any)(lambda character: identity(character) if predicate(character) else neutral)


def character(character: str) -> Parser[str]:
    return satisfy(lambda current: current == character)


def text(string: str) -> Parser[str]:
    return take_after(character(string[0]))(take_after(text(string[1:]))(identity(string))) if string else identity("")


def many[T](parser: Parser[T]) -> Parser[list[T]]:
    return add(identity(felis.list.neutral))(bind(parser)(lambda first: bind(many(parser))(lambda rest: identity([first, *rest]))))


def some[T](parser: Parser[T]) -> Parser[list[T]]:
    return bind(parser)(lambda first: bind(many(parser))(lambda rest: identity([first, *rest])))


def option[T](parser: Parser[T]) -> Parser[Option[T]]:
    return add(identity(felis.option.neutral))(map(felis.option.identity)(parser))


# [S : Type] -> Parser S -> [T : Type] -> Parser T -> Parser (list T)
@curry
def separated[T](parser: Parser[T], separator: Parser[Any]) -> Parser[list[T]]:
    return add(identity(felis.list.neutral))(bind(parser)(lambda first: bind(many(take_after(separator)(parser)))(lambda rest: identity([first, *rest]))))


# [L : Type] -> Parser L -> [R : Type] -> Parser R -> [T : Type] -> Parser T -> Parser T
@curry
@curry
def bracket[T](parser: Parser[T], right: Parser[Any], left: Parser[Any]) -> Parser[T]:
    return take_after(left)(take_before(right)(parser))


@curry
@curry
def chain_right[R, T](parser_value: Parser[T], parser_function: Parser[Callable[[T], Callable[[R], R]]], accumulator: R) -> Parser[R]:
    return add(identity(accumulator))(
        bind(parser_function)(
            lambda function: bind(parser_value)(
                lambda value: bind(chain_right(accumulator)(parser_function)(parser_value))(lambda accumulator: identity(function(value)(accumulator))),
            ),
        ),
    )


@curry
def chain_right_1[T](parser_value: Parser[T], parser_function: Parser[Callable[[T], Callable[[T], T]]]) -> Parser[T]:
    def rest(accumulator: T) -> Parser[T]:
        return add(identity(accumulator))(
            bind(parser_function)(lambda function: bind(parser_value)(lambda value: bind(rest(value))(lambda value: identity(function(accumulator)(value))))),
        )

    return bind(parser_value)(rest)


@curry
@curry
def chain_left[R, T](parser_value: Parser[T], parser_function: Parser[Callable[[R], Callable[[T], R]]], accumulator: R) -> Parser[R]:
    return add(identity(accumulator))(
        bind(parser_function)(lambda function: bind(parser_value)(lambda value: chain_left(function(accumulator)(value))(parser_function)(parser_value))),
    )


@curry
def chain_left_1[T](parser: Parser[T], function: Parser[Callable[[T], Callable[[T], T]]]) -> Parser[T]:
    return bind(parser)(lambda first: chain_left(first)(function)(parser))


digit = satisfy(str.isdigit)


alpha = satisfy(str.isalpha)


alnum = satisfy(str.isalnum)
