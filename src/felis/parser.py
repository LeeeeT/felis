from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import felis.list
import felis.option
from felis import applicative, function, monad, option_t, state_t
from felis.currying import curry, flip
from felis.option import Option
from felis.predicate import Predicate

__all__ = [
    "Parser",
    "alnum",
    "alpha",
    "any",
    "apply",
    "bind",
    "bind_to",
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
    "join",
    "lift2",
    "many",
    "map_by",
    "neutral",
    "option",
    "parse_as",
    "pure",
    "satisfies",
    "separated_by",
    "some",
    "take_after",
    "take_before",
    "text",
    "to_add",
    "when",
]


type Parser[T] = Callable[[str], Option[tuple[T, str]]]


if TYPE_CHECKING:

    @curry
    def parse_as[T](string: str, parser_value: Parser[T]) -> Option[T]: ...

else:
    parse_as = state_t.starting_with_run(felis.option.map_by)


if TYPE_CHECKING:
    # [T : *] -> Parser T
    def neutral(string: str, /) -> Option[tuple[Any, str]]: ...

else:
    neutral = option_t.neutral(function.pure)


if TYPE_CHECKING:

    @curry
    def to_add[T](first: Parser[T], second: Parser[T]) -> Parser[T]: ...

else:
    to_add = option_t.to_add(function.pure)(function.bind)


if TYPE_CHECKING:

    @curry
    def map_by[From, To](parser_value: Parser[From], function: Callable[[From], To]) -> Parser[To]: ...

else:
    map_by = state_t.map_by(felis.option.map_by)


if TYPE_CHECKING:

    def pure[T](value: T, /) -> Parser[T]: ...

else:
    pure = state_t.pure(felis.option.pure)


if TYPE_CHECKING:

    @curry
    def apply[From, To](parser_value: Parser[From], parser_function: Parser[Callable[[From], To]]) -> Parser[To]: ...

else:
    apply = state_t.apply(felis.option.pure)(felis.option.bind)


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[First, Second, Result](
        second: Parser[Second],
        first: Parser[First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> Parser[Result]: ...

else:
    lift2 = applicative.lift2(map_by)(apply)


take_after = applicative.take_after(lift2)


discard_after = applicative.discard_after(lift2)


take_before = applicative.take_before(lift2)


discard_before = applicative.discard_before(lift2)


if TYPE_CHECKING:

    @curry
    def when(parser_none: Parser[None], bool: bool) -> Parser[None]: ...

else:
    when = applicative.when(pure)


if TYPE_CHECKING:

    def join[T](parser_value: Parser[Parser[T]], /) -> Parser[T]: ...

else:
    join = state_t.join(felis.option.pure)(felis.option.bind)


if TYPE_CHECKING:

    @curry
    def bind_to[From, To](parser_value: Parser[From], function: Callable[[From], Parser[To]]) -> Parser[To]: ...

else:
    bind_to = monad.bind_to(map_by)(join)


bind = flip(bind_to)


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
    guard = monad.guard(neutral)(pure)


def end(string: str) -> Option[tuple[None, str]]:
    return None if string else felis.option.Some((None, ""))


def any(string: str) -> Option[tuple[str, str]]:
    return felis.option.Some((string[0], string[1:])) if string else None


def satisfies(predicate: Predicate[str]) -> Parser[str]:
    return bind(any)(lambda character: pure(character) if predicate(character) else neutral)


def character(character: str) -> Parser[str]:
    return satisfies(lambda current: current == character)


def text(string: str) -> Parser[str]:
    return take_after(character(string[0]))(take_after(text(string[1:]))(pure(string))) if string else pure("")


def many[T](parser: Parser[T]) -> Parser[list[T]]:
    return to_add(pure(felis.list.neutral))(bind(parser)(lambda first: bind(many(parser))(lambda rest: pure([first, *rest]))))


def some[T](parser: Parser[T]) -> Parser[list[T]]:
    return bind(parser)(lambda first: bind(many(parser))(lambda rest: pure([first, *rest])))


def option[T](parser: Parser[T]) -> Parser[Option[T]]:
    return to_add(pure(felis.option.neutral))(map_by(felis.option.pure)(parser))


# [S : *] -> Parser S -> [T : *] -> Parser T -> Parser (list T)
@curry
def separated_by[T](parser: Parser[T], separator: Parser[Any]) -> Parser[list[T]]:
    return to_add(pure(felis.list.neutral))(bind(parser)(lambda first: bind(many(take_after(separator)(parser)))(lambda rest: pure([first, *rest]))))


# [L : *] -> Parser L -> [R : *] -> Parser R -> [T : *] -> Parser T -> Parser T
@curry
@curry
def bracket[T](parser: Parser[T], right: Parser[Any], left: Parser[Any]) -> Parser[T]:
    return take_after(left)(take_before(right)(parser))


@curry
@curry
def chain_right[R, T](parser_value: Parser[T], parser_function: Parser[Callable[[T], Callable[[R], R]]], accumulator: R) -> Parser[R]:
    return to_add(pure(accumulator))(
        bind(parser_function)(
            lambda function: bind(parser_value)(
                lambda value: bind(chain_right(accumulator)(parser_function)(parser_value))(lambda accumulator: pure(function(value)(accumulator))),
            ),
        ),
    )


@curry
def chain_right_1[T](parser_value: Parser[T], parser_function: Parser[Callable[[T], Callable[[T], T]]]) -> Parser[T]:
    def rest(accumulator: T) -> Parser[T]:
        return to_add(pure(accumulator))(
            bind(parser_function)(lambda function: bind(parser_value)(lambda value: bind(rest(value))(lambda value: pure(function(accumulator)(value))))),
        )

    return bind(parser_value)(rest)


@curry
@curry
def chain_left[R, T](parser_value: Parser[T], parser_function: Parser[Callable[[R], Callable[[T], R]]], accumulator: R) -> Parser[R]:
    return to_add(pure(accumulator))(
        bind(parser_function)(lambda function: bind(parser_value)(lambda value: chain_left(function(accumulator)(value))(parser_function)(parser_value))),
    )


@curry
def chain_left_1[T](parser: Parser[T], function: Parser[Callable[[T], Callable[[T], T]]]) -> Parser[T]:
    return bind(parser)(lambda first: chain_left(first)(function)(parser))


digit = satisfies(str.isdigit)


alpha = satisfies(str.isalpha)


alnum = satisfies(str.isalnum)
