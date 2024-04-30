## 🐈 Felis Catus

**Felis Catus** is your taxonomic nomenclature, an endothermic quadruped, carnivorous by nature; your visual, olfactory, and auditory senses contribute to your hunting skills and natural defenses. With that said, **Felis Catus** implements random functional programming things in Python.

## Installation

Build the latest version from [source]:

```console
pip install git+https://github.com/LeeeeT/felis
```

[docs]: https://valtypes.rtfd.io
[source]: https://github.com/LeeeeT/felis

## Examples

Curry and uncurry functions:

```python
from felis.currying import curry, uncurry


@curry
@curry
def curried(a: int, b: str, c: bool) -> None:
    pass


uncurried = uncurry(uncurry(curried))


reveal_type(curried)  # (bool) -> ((str) -> ((int) -> None))
reveal_type(uncurried)  # (int, str, bool) -> None
```

Safe error handling with `felis.either`:

```python
from felis import either


safe_int = either.catch(ValueError)(int)


@either.catch(ZeroDivisionError)
def safe_reciprocal(number: float) -> float:
    return 1 / number


safe_reciprocal_of_str = either.compose(safe_reciprocal)(safe_int)


match safe_reciprocal_of_str(input("Enter a number: ")):
    case either.Left(error):
        print(f"Error: {error}")
    case either.Right(reciprocal):
        print(f"Reciprocal: {reciprocal}")
```

Managing IO with `felis.io`:

```python
from felis import io
from felis.currying import uncurry


main = \
    uncurry(io.then)(io.print("What's your name?"),
    uncurry(io.bind)(io.input, lambda name:
    io.print(f"Hi, {name}!")
))


io.run(main)
```

That's all monads, btw 🐈.
