from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import felis.alternative
import felis.applicative
import felis.functor
import felis.list
import felis.monad
import felis.option
import felis.semigroup
from felis import function, state
from felis.alternative import Alternative
from felis.applicative import Applicative
from felis.currying import curry
from felis.functor import Functor
from felis.monad import Monad
from felis.monoid import Monoid
from felis.option import Option
from felis.predicate import Predicate
from felis.semigroup import Semigroup

__all__ = [
    "Parser",
    "add_to",
    "alnum",
    "alpha",
    "alternative",
    "any",
    "applicative",
    "apply_to",
    "bind_to",
    "bracket",
    "by_map",
    "chain_left",
    "chain_left_1",
    "chain_right",
    "chain_right_1",
    "character",
    "compose_after",
    "compose_before",
    "digit",
    "discard_after",
    "discard_before",
    "end",
    "functor",
    "guard",
    "join",
    "lift",
    "many",
    "map_by",
    "monad",
    "monoid",
    "neutral",
    "option",
    "parse_as",
    "pure",
    "satisfies",
    "semigroup",
    "separated_by",
    "some",
    "take_after",
    "take_before",
    "text",
    "to_add",
    "to_apply",
    "to_bind",
    "when",
]


type Parser[T] = Callable[[str], Option[tuple[T, str]]]


if TYPE_CHECKING:

    @curry
    def parse_as[T](string: str, parser_value: Parser[T]) -> Option[T]: ...

else:
    parse_as = state.starting_with_run_t(felis.option.functor)


if TYPE_CHECKING:

    @curry
    def to_add[T](augend: Parser[T], addend: Parser[T]) -> Parser[T]: ...

else:
    to_add = felis.option.to_add_t(function.monad)


# [T : *] -> Semigroup (Parser T)
semigroup: Semigroup[Parser[Any]] = Semigroup(to_add)


if TYPE_CHECKING:

    @curry
    def add_to[T](addend: Parser[T], augend: Parser[T]) -> Parser[T]: ...

else:
    add_to = felis.semigroup.add_to(semigroup)


# [T : *] -> Parser T
neutral: Parser[Any] = felis.option.neutral_t(function.monad)


# [T : *] -> Monoid (Parser T)
monoid = Monoid(semigroup, neutral)


if TYPE_CHECKING:

    @curry
    def map_by[From, To](parser_value: Parser[From], function: Callable[[From], To]) -> Parser[To]: ...

else:
    map_by = state.map_by_t(felis.option.functor)


# Functor Parser
functor = Functor(map_by)


if TYPE_CHECKING:

    @curry
    def by_map[From, To](function: Callable[[From], To], parser_value: Parser[From]) -> Parser[To]: ...

else:
    by_map = felis.functor.by_map(functor)


if TYPE_CHECKING:

    def pure[T](value: T, /) -> Parser[T]: ...

else:
    pure = state.pure_t(felis.option.applicative)


if TYPE_CHECKING:

    @curry
    def to_apply[From, To](parser_value: Parser[From], parser_function: Parser[Callable[[From], To]]) -> Parser[To]: ...

else:
    to_apply = state.to_apply_t(felis.option.monad)


# Applicative Parser
applicative = Applicative(functor, pure, to_apply)


if TYPE_CHECKING:

    @curry
    def apply_to[From, To](parser_function: Parser[Callable[[From], To]], parser_value: Parser[From]) -> Parser[To]: ...

else:
    apply_to = felis.applicative.apply_to(applicative)


if TYPE_CHECKING:

    @curry
    @curry
    def lift[First, Second, Result](
        second: Parser[Second],
        first: Parser[First],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> Parser[Result]: ...

else:
    lift = felis.applicative.lift(applicative)


if TYPE_CHECKING:

    @curry
    def take_after[First, Second](second: Parser[Second], first: Parser[First]) -> Parser[Second]: ...

else:
    take_after = felis.applicative.take_after(applicative)


if TYPE_CHECKING:

    @curry
    def discard_before[First, Second](first: Parser[First], second: Parser[Second]) -> Parser[Second]: ...

else:
    discard_before = felis.applicative.discard_before(applicative)


if TYPE_CHECKING:

    @curry
    def discard_after[First, Second](second: Parser[Second], first: Parser[First]) -> Parser[First]: ...

else:
    discard_after = felis.applicative.discard_after(applicative)


if TYPE_CHECKING:

    @curry
    def take_before[First, Second](first: Parser[First], second: Parser[Second]) -> Parser[First]: ...

else:
    take_before = felis.applicative.take_before(applicative)


if TYPE_CHECKING:

    @curry
    def when(parser_none: Parser[None], bool: bool) -> Parser[None]: ...

else:
    when = felis.applicative.when(applicative)


# Alternative Parser
alternative = Alternative(monoid, applicative)


if TYPE_CHECKING:

    def guard(bool: bool, /) -> Parser[None]: ...

else:
    guard = felis.alternative.guard(alternative)


if TYPE_CHECKING:

    def join[T](parser_value: Parser[Parser[T]], /) -> Parser[T]: ...

else:
    join = state.join_t(felis.option.monad)


# Monad Parser
monad = Monad(applicative, join)


if TYPE_CHECKING:

    @curry
    def bind_to[From, To](parser_value: Parser[From], function: Callable[[From], Parser[To]]) -> Parser[To]: ...

else:
    bind_to = felis.monad.bind_to(monad)


if TYPE_CHECKING:

    @curry
    def to_bind[From, To](function: Callable[[From], Parser[To]], parser_value: Parser[From]) -> Parser[To]: ...

else:
    to_bind = felis.monad.to_bind(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_after[From, Intermediate, To](
        value: From,
        second: Callable[[Intermediate], Parser[To]],
        first: Callable[[From], Parser[Intermediate]],
    ) -> Parser[To]: ...

else:
    compose_after = felis.monad.compose_after(monad)


if TYPE_CHECKING:

    @curry
    @curry
    def compose_before[From, Intermediate, To](
        value: From,
        first: Callable[[From], Parser[Intermediate]],
        second: Callable[[Intermediate], Parser[To]],
    ) -> Parser[To]: ...

else:
    compose_before = felis.monad.compose_before(monad)


def end(string: str) -> Option[tuple[None, str]]:
    return None if string else felis.option.Some((None, ""))


def any(string: str) -> Option[tuple[str, str]]:
    return felis.option.Some((string[0], string[1:])) if string else None


def satisfies(predicate: Predicate[str]) -> Parser[str]:
    return to_bind(any)(lambda character: pure(character) if predicate(character) else neutral)


def character(character: str) -> Parser[str]:
    return satisfies(lambda current: current == character)


def text(string: str) -> Parser[str]:
    return take_after(character(string[0]))(take_after(text(string[1:]))(pure(string))) if string else pure("")


def many[T](parser: Parser[T]) -> Parser[list[T]]:
    return to_add(pure(felis.list.neutral))(to_bind(parser)(lambda first: to_bind(many(parser))(lambda rest: pure([first, *rest]))))


def some[T](parser: Parser[T]) -> Parser[list[T]]:
    return to_bind(parser)(lambda first: to_bind(many(parser))(lambda rest: pure([first, *rest])))


def option[T](parser: Parser[T]) -> Parser[Option[T]]:
    return to_add(pure(felis.option.neutral))(map_by(felis.option.pure)(parser))


# [S : *] -> Parser S -> [T : *] -> Parser T -> Parser (list T)
@curry
def separated_by[T](parser: Parser[T], separator: Parser[Any]) -> Parser[list[T]]:
    return to_add(pure(felis.list.neutral))(to_bind(parser)(lambda first: to_bind(many(take_after(separator)(parser)))(lambda rest: pure([first, *rest]))))


# [L : *] -> Parser L -> [R : *] -> Parser R -> [T : *] -> Parser T -> Parser T
@curry
@curry
def bracket[T](parser: Parser[T], right: Parser[Any], left: Parser[Any]) -> Parser[T]:
    return take_after(left)(take_before(right)(parser))


@curry
@curry
def chain_right[R, T](parser_value: Parser[T], parser_function: Parser[Callable[[T], Callable[[R], R]]], accumulator: R) -> Parser[R]:
    return to_add(pure(accumulator))(
        to_bind(parser_function)(
            lambda function: to_bind(parser_value)(
                lambda value: to_bind(chain_right(accumulator)(parser_function)(parser_value))(lambda accumulator: pure(function(value)(accumulator))),
            ),
        ),
    )


@curry
def chain_right_1[T](parser_value: Parser[T], parser_function: Parser[Callable[[T], Callable[[T], T]]]) -> Parser[T]:
    def rest(accumulator: T) -> Parser[T]:
        return to_add(pure(accumulator))(
            to_bind(parser_function)(
                lambda function: to_bind(parser_value)(lambda value: to_bind(rest(value))(lambda value: pure(function(value)(accumulator)))),
            ),
        )

    return to_bind(parser_value)(rest)


@curry
@curry
def chain_left[R, T](parser_value: Parser[T], parser_function: Parser[Callable[[T], Callable[[R], R]]], accumulator: R) -> Parser[R]:
    return to_add(pure(accumulator))(
        to_bind(parser_function)(lambda function: to_bind(parser_value)(lambda value: chain_left(function(value)(accumulator))(parser_function)(parser_value))),
    )


@curry
def chain_left_1[T](parser: Parser[T], function: Parser[Callable[[T], Callable[[T], T]]]) -> Parser[T]:
    return to_bind(parser)(lambda first: chain_left(first)(function)(parser))


digit = satisfies(str.isdigit)


alpha = satisfies(str.isalpha)


alnum = satisfies(str.isalnum)
