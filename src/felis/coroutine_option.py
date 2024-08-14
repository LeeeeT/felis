from collections.abc import Callable
from typing import TYPE_CHECKING

import felis.identity
from felis import applicative, coroutine, function, monad, option
from felis.coroutine import Coroutine
from felis.currying import curry
from felis.option import Option

__all__ = ["map", "identity", "apply", "lift2", "take_after", "discard_after", "take_before", "discard_before", "when", "join", "bind", "compose"]


if TYPE_CHECKING:

    @curry
    def map[From, To](coroutine_option_value: Coroutine[Option[From]], function: Callable[[From], To]) -> Coroutine[Option[To]]: ...

else:
    map = felis.identity.compose(coroutine.map)(option.map)


identity = felis.identity.compose(coroutine.identity)(option.identity)


apply = coroutine.lift2(option.apply)


if TYPE_CHECKING:

    @curry
    @curry
    def lift2[First, Second, Result](
        second: Coroutine[Option[Second]],
        first: Coroutine[Option[First]],
        function: Callable[[First], Callable[[Second], Result]],
    ) -> Coroutine[Option[Result]]: ...

else:
    lift2 = applicative.lift2(map)(apply)


take_after = lift2(function.flip(function.identity))


discard_after = lift2(function.identity)


take_before = function.flip(discard_after)


discard_before = function.flip(take_after)


if TYPE_CHECKING:

    @curry
    def when(bool: bool, coroutine_option_none: Coroutine[Option[None]]) -> Coroutine[Option[None]]: ...

else:
    when = applicative.when(identity)


join = coroutine.bind(option.inject(coroutine.identity))


if TYPE_CHECKING:

    @curry
    def bind[From, To](coroutine_option_value: Coroutine[Option[From]], function: Callable[[From], Coroutine[Option[To]]]) -> Coroutine[Option[To]]: ...

else:
    bind = monad.bind(map)(join)


if TYPE_CHECKING:

    @curry
    @curry
    def compose[From, Intermediate, To](
        value: From,
        first: Callable[[From], Coroutine[Option[Intermediate]]],
        second: Callable[[Intermediate], Coroutine[Option[To]]],
    ) -> Coroutine[Option[To]]: ...

else:
    compose = monad.compose(bind)
