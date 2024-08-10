from collections.abc import Callable
from typing import TYPE_CHECKING

import felis.identity
from felis import applicative, coroutine, monad, option
from felis.coroutine import Coroutine
from felis.currying import curry
from felis.option import Option

__all__ = ["map", "identity", "apply", "lift2", "when", "join", "bind", "compose", "then"]


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


if TYPE_CHECKING:

    @curry
    def then[First, Second](first: Coroutine[Option[First]], second: Coroutine[Option[Second]]) -> Coroutine[Option[Second]]: ...

else:
    then = monad.then(bind)
