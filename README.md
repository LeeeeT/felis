## 🐈 Felis Catus

**Felis Catus** is your taxonomic nomenclature, an endothermic quadruped, carnivorous by nature; your visual, olfactory, and auditory senses contribute to your hunting skills and natural defenses. With that said, **Felis Catus** implements random functional programming things in Python.

## Installation

Install from [PyPI]:

```console
pip install felis-catus
```

Build and install from [source]:

```console
pip install git+https://github.com/LeeeeT/felis
```

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

Managing IO (or any other lazy computations) with `felis.lazy`:

```python
from felis import lazy
from felis.currying import uncurry


main = \
    uncurry(lazy.then)(lambda: print("What's your name?"),
    uncurry(lazy.bind)(input, lambda name:
    lambda: print(f"Hi, {name}!")
))


lazy.run(main)
```

Finding pythagorean triples (analogue to list comprehension):

```python
from felis.currying import uncurry
from felis.list import bind, guard, identity, range, then

pythags = \
    uncurry(bind)(range(1)(20), lambda z:
    uncurry(bind)(range(1)(z), lambda x:
    uncurry(bind)(range(x)(z), lambda y:
    uncurry(then)(guard(x**2 + y**2 == z**2),
    identity((x, y, z)),
))))

print(pythags)
# [(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17)]
```

That's all monads, btw. 🐈

[docs]: https://felis.LeeeeT.dev
[source]: https://github.com/LeeeeT/felis
[PyPI]: https://pypi.org/project/felis-catus
