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

Currying and uncurrying functions with `felis.currying`:

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


safe_reciprocal_of_str = either.compose_after(safe_int)(safe_reciprocal)


match safe_reciprocal_of_str(input("Enter a number: ")):
    case either.Left(error):
        print(f"Error: {error}")
    case either.Right(reciprocal):
        print(f"Reciprocal: {reciprocal}")
```

Managing IO (or any other lazy computations) with `felis.lazy`:

```python
from felis.lazy import *

main = \
    take_after(lambda: print("What's your name?"))(
    to_bind(input)(lambda name:
    lambda: print(f"Hi, {name}!")
))

main()
```

Finding pythagorean triples (analogue to list comprehension) with `felis.list`:

```python
from felis.list import *

pythags = \
    to_bind(range_to_from(1)(20))(lambda z:
    to_bind(range_to_from(1)(z))(lambda x:
    to_bind(range_to_from(x)(z))(lambda y:
    take_after(guard(x**2 + y**2 == z**2))(
    pure((x, y, z))
))))

print(pythags)
# [(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17)]
```

Parsing (and evaluating) an arithmetic expression with `felis.parser`:

```python
from felis import float, Float
from felis.option import Some
from felis.parser import *

literal = map_by(Float)(map_by("".join)(some(digit)))
factor: Parser[Float] = lambda string: bracket(character("("))(character(")"))(expression)(string)
term_priority_1 = add_to(factor)(literal)

multiplication = take_after(character("*"))(pure(float.multiply_by))
division = take_after(character("/"))(pure(float.divide_by))
term_priority_2 = chain_left_1(add_to(multiplication)(division))(term_priority_1)

addition = take_after(character("+"))(pure(float.to_add))
subtraction = take_after(character("-"))(pure(float.from_subtract))
term_priority_3 = chain_left_1(add_to(addition)(subtraction))(term_priority_2)

expression = term_priority_3

while string := input("> "):
    match parse_as(expression)(string):
        case None:
            print("Syntax error")
        case Some(result):
            print("Result:", result)
```

That's all monads, btw. 🐈

[docs]: https://felis.LeeeeT.dev
[source]: https://github.com/LeeeeT/felis
[PyPI]: https://pypi.org/project/felis-catus
