# Functional Programming Style Guide

This document explains the functional programming style used in **Felis Catus** and provides comprehensive examples of key concepts.

## Table of Contents

1. [Core Principles](#core-principles)
2. [Pure Functions](#pure-functions)
3. [Immutability](#immutability)
4. [Currying](#currying)
5. [Function Composition](#function-composition)
6. [Functors](#functors)
7. [Applicatives](#applicatives)
8. [Monads](#monads)
9. [Practical Examples](#practical-examples)

## Core Principles

Functional programming is based on several core principles:

1. **Pure Functions**: Functions that always produce the same output for the same input and have no side effects.
2. **Immutability**: Data structures that cannot be modified after creation.
3. **First-Class Functions**: Functions are treated as values that can be passed around.
4. **Higher-Order Functions**: Functions that take other functions as arguments or return functions.
5. **Composition**: Building complex functionality by combining simple functions.

## Pure Functions

Pure functions are the foundation of functional programming. They have two key properties:

1. **Deterministic**: Same input always produces the same output
2. **No Side Effects**: Don't modify external state or perform I/O operations

### Examples

**Impure Function** (has side effects):
```python
total = 0

def add_to_total(x):
    global total
    total += x  # Modifies external state
    return total
```

**Pure Function**:
```python
def add(x, y):
    return x + y  # Only depends on inputs, no side effects
```

**Using Pure Functions from Felis**:
```python
from felis.float import to_add, multiply_by

# Pure function that adds two numbers
result = to_add(5)(3.5)  # 8.5

# Pure function composition
double = multiply_by(2)
add_ten = to_add(10)

result = add_ten(double(5))  # 20.0
```

## Immutability

Immutability means that once data is created, it cannot be changed. Instead of modifying data, we create new data with the desired changes.

### Examples

**Mutable Approach** (avoid in FP):
```python
numbers = [1, 2, 3]
numbers.append(4)  # Mutates the list
```

**Immutable Approach**:
```python
numbers = [1, 2, 3]
new_numbers = numbers + [4]  # Creates a new list
```

**Using Immutable Data Structures in Felis**:
```python
from felis.option import Some
from felis.either import Right, Left

# Option represents a value that may or may not exist
maybe_value = Some(42)
# Cannot modify the value inside Some, can only transform it

# Either represents a value that can be one of two types
success = Right(100)
failure = Left("Error occurred")
# Immutable - transformations create new instances
```

## Currying

Currying transforms a function that takes multiple arguments into a sequence of functions that each take a single argument.

### Why Curry?

- **Partial Application**: Create specialized functions from general ones
- **Function Reuse**: Build libraries of composable functions
- **Better Type Inference**: Each step has a clear type

### Examples

**Uncurried Function**:
```python
def add(x, y, z):
    return x + y + z

result = add(1, 2, 3)  # 6
```

**Curried Function**:
```python
from felis.currying import curry

# Note: curry moves the first parameter to the last position
# For a 3-parameter function, apply @curry twice to fully curry it
@curry
@curry
def add(x, y, z):
    return x + y + z

# Can be called in multiple ways:
result1 = add(1)(2)(3)  # 6
result2 = add(1)(2, 3)  # 6

# Partial application
add_one = add(1)
add_one_and_two = add(1)(2)
result3 = add_one_and_two(3)  # 6
```

**Practical Example**:
```python
from felis.currying import curry

@curry
@curry
def greet(greeting, name, punctuation):
    return f"{greeting}, {name}{punctuation}"

# Create specialized greeting functions
say_hello = greet("Hello")
say_hello_to_alice = say_hello("Alice")

print(say_hello_to_alice("!"))  # "Hello, Alice!"
print(say_hello("Bob")("?"))     # "Hello, Bob?"

# Different greeting style
say_goodbye = greet("Goodbye")
print(say_goodbye("Charlie")("."))  # "Goodbye, Charlie."
```

**Uncurrying**:
```python
from felis.currying import curry, uncurry

@curry
@curry
def curried_add(x, y, z):
    return x + y + z

# Convert back to regular function
# Need to uncurry twice (once for each @curry)
regular_add = uncurry(uncurry(curried_add))
result = regular_add(1, 2, 3)  # 6
```

**Flipping Arguments**:
```python
from felis.currying import curry, flip

@curry
def divide(x, y):
    return x / y

# flip swaps the order of arguments
divide_by = flip(divide)

result1 = divide(10)(2)     # 10 / 2 = 5.0
result2 = divide_by(2)(10)  # 10 / 2 = 5.0 (arguments flipped)
```

## Function Composition

Function composition combines simple functions to build more complex ones. If you have functions `f` and `g`, composing them creates a new function `h(x) = g(f(x))`.

### Examples

**Manual Composition**:
```python
def add_ten(x):
    return x + 10

def double(x):
    return x * 2

def add_ten_then_double(x):
    return double(add_ten(x))

result = add_ten_then_double(5)  # (5 + 10) * 2 = 30
```

**Using Composition in Felis**:
```python
from felis.function import compose_after, compose_before

# compose_after: applies first function, then second
add_ten = lambda x: x + 10
double = lambda x: x * 2

# First add ten, then double
transform = compose_after(double)(add_ten)
result = transform(5)  # (5 + 10) * 2 = 30

# compose_before: reversed order
transform2 = compose_before(add_ten)(double)
result2 = transform2(5)  # (5 * 2) + 10 = 20
```

**Practical Example with Either**:
```python
from felis import either

# Compose error-handling functions
safe_int = either.catch(ValueError)(int)
safe_reciprocal = either.catch(ZeroDivisionError)(lambda x: 1 / x)

# Compose: parse string to int, then calculate reciprocal
safe_reciprocal_of_str = either.compose_after(safe_int)(safe_reciprocal)

match safe_reciprocal_of_str("2"):
    case either.Right(value):
        print(f"Success: {value}")  # Success: 0.5
    case either.Left(error):
        print(f"Error: {error}")

match safe_reciprocal_of_str("0"):
    case either.Right(value):
        print(f"Success: {value}")
    case either.Left(error):
        print(f"Error: {error}")  # Error: division by zero

match safe_reciprocal_of_str("abc"):
    case either.Right(value):
        print(f"Success: {value}")
    case either.Left(error):
        print(f"Error: {error}")  # Error: invalid literal for int()
```

## Functors

A **Functor** is a container that can be mapped over. It implements a `map` operation that applies a function to the value(s) inside the container without changing the container's structure.

### The Functor Laws

1. **Identity**: `map(id) = id` (mapping the identity function does nothing)
2. **Composition**: `map(f ∘ g) = map(f) ∘ map(g)` (mapping composed functions equals composing mapped functions)

### Examples

**List as a Functor** (built-in Python):
```python
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))  # [2, 4, 6, 8, 10]
```

**Option Functor**:
```python
from felis.option import Some, map_by

# Map over a Some value
maybe_number = Some(5)
maybe_doubled = map_by(lambda x: x * 2)(maybe_number)  # Some(10)

# Map over None
maybe_nothing = None
result = map_by(lambda x: x * 2)(maybe_nothing)  # None

# The function is only applied if the value exists
```

**Either Functor**:
```python
from felis.either import Right, Left, map_by

# Map over a Right value
success = Right(10)
doubled = map_by(lambda x: x * 2)(success)  # Right(20)

# Map over a Left value (error case)
failure = Left("Something went wrong")
result = map_by(lambda x: x * 2)(failure)  # Left("Something went wrong")
# The function is not applied to Left values
```

**Lazy Functor**:
```python
from felis.lazy import map_by, run

# Create a lazy computation
lazy_value = lambda: 5 + 3

# Map over it (creates a new lazy computation)
lazy_doubled = map_by(lambda x: x * 2)(lazy_value)

# Nothing is computed yet!
# Run the computation when needed
result = run(lazy_doubled)  # 16
```

## Applicatives

An **Applicative** is a Functor that can also apply a function wrapped in a context to a value wrapped in a context. It has two key operations:

- `pure`: Wraps a value in the context
- `apply` (or `<*>`): Applies a wrapped function to a wrapped value

### Why Applicatives?

They allow you to:
- Apply multi-argument functions to wrapped values
- Combine multiple independent computations
- Sequence operations while maintaining context

### Examples

**Option Applicative**:
```python
from felis.option import Some, pure, lift, to_apply

# Pure wraps a value
value = pure(42)  # Some(42)

# Lift a binary function to work with Option values
from felis.currying import curry

@curry
def add(x, y):
    return x + y

# Apply a binary function to two Option values
maybe_x = Some(5)
maybe_y = Some(3)
maybe_sum = lift(add)(maybe_x)(maybe_y)  # Some(8)

# If any value is None, result is None
maybe_none = None
result = lift(add)(maybe_x)(maybe_none)  # None
```

**Either Applicative**:
```python
from felis.either import Right, Left, lift
from felis.currying import curry

@curry
def divide(x, y):
    return x / y if y != 0 else None

# Both values must be Right for success
result1 = lift(divide)(Right(10))(Right(2))  # Right(5.0)

# If either is Left, the first Left is returned
result2 = lift(divide)(Left("Error 1"))(Right(2))  # Left("Error 1")
result3 = lift(divide)(Right(10))(Left("Error 2"))  # Left("Error 2")
```

**Sequencing Operations**:
```python
from felis.option import Some, take_after, discard_after

# take_after: execute first, return second
first = Some(1)
second = Some(2)
result = take_after(second)(first)  # Some(2)

# discard_after: execute both, return first
result2 = discard_after(second)(first)  # Some(1)
```

**Practical Example - Validation**:
```python
from felis.option import Some, lift
from felis.currying import curry

@curry
@curry
def create_user(name, age, email):
    return {"name": name, "age": age, "email": email}

def validate_name(name):
    return Some(name) if name and len(name) > 0 else None

def validate_age(age):
    return Some(age) if age >= 18 else None

def validate_email(email):
    return Some(email) if "@" in email else None

# Validate all fields and create user if all valid
user = lift(lift(create_user)(
    validate_name("Alice")
)(
    validate_age(25)
))(
    validate_email("alice@example.com")
)
# Some({"name": "Alice", "age": 25, "email": "alice@example.com"})

# If any validation fails, result is None
invalid_user = lift(lift(create_user)(
    validate_name("Bob")
)(
    validate_age(15)  # Under 18!
))(
    validate_email("bob@example.com")
)
# None
```

## Monads

A **Monad** is an Applicative that adds the ability to chain operations that return wrapped values. It provides:

- `pure` (from Applicative): Wraps a value
- `bind` (or `>>=`, also called `flatMap` or `chain`): Chains operations that return wrapped values

### Why Monads?

Monads are perfect for:
- Sequencing computations with context (error handling, state, I/O, etc.)
- Avoiding nested wrapping (e.g., `Some(Some(value))` becomes `Some(value)`)
- Building pipelines of dependent operations

### The Monad Laws

1. **Left Identity**: `pure(a).bind(f) = f(a)`
2. **Right Identity**: `m.bind(pure) = m`
3. **Associativity**: `m.bind(f).bind(g) = m.bind(x => f(x).bind(g))`

### Examples

**Option Monad**:
```python
from felis.option import Some, to_bind, pure

# Without monad: nested Options
def parse_int(s):
    try:
        return Some(int(s))
    except ValueError:
        return None

def reciprocal(x):
    return Some(1 / x) if x != 0 else None

# Using bind to chain operations
input_str = "4"
result = to_bind(parse_int(input_str))(reciprocal)  # Some(0.25)

# Chain handles None automatically
result2 = to_bind(parse_int("0"))(reciprocal)  # None (reciprocal returns None)
result3 = to_bind(parse_int("abc"))(reciprocal)  # None (parse_int returns None)
```

**Either Monad for Error Handling**:
```python
from felis.either import Right, Left, to_bind

def parse_int(s):
    try:
        return Right(int(s))
    except ValueError:
        return Left(f"Invalid number: {s}")

def reciprocal(x):
    if x == 0:
        return Left("Division by zero")
    return Right(1 / x)

def format_result(x):
    return Right(f"Result: {x:.2f}")

# Chain multiple operations
input_str = "4"
result = to_bind(
    to_bind(parse_int(input_str))(reciprocal)
)(format_result)  # Right("Result: 0.25")

# Errors propagate automatically
result2 = to_bind(
    to_bind(parse_int("0"))(reciprocal)
)(format_result)  # Left("Division by zero")

result3 = to_bind(
    to_bind(parse_int("abc"))(reciprocal)
)(format_result)  # Left("Invalid number: abc")
```

**List Monad** (representing non-deterministic computations):
```python
from felis.list import to_bind, pure, range_to_from

# List monad allows exploring multiple possibilities
# Example: Finding Pythagorean triples

pythags = to_bind(range_to_from(20)(1))(lambda z:
    to_bind(range_to_from(z)(1))(lambda x:
    to_bind(range_to_from(z)(x))(lambda y:
        pure((x, y, z)) if x**2 + y**2 == z**2 else []
    )))

print(pythags)
# [(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17)]
```

**Lazy Monad for Deferred Computations**:
```python
from felis.lazy import to_bind, pure, run

# Lazy computations are not executed until run is called
def get_user_input():
    return lambda: input("Enter a number: ")

def parse_and_double(s):
    return lambda: int(s) * 2

def format_output(n):
    return lambda: f"Result: {n}"

# Build a lazy computation pipeline
computation = to_bind(get_user_input())(lambda user_input:
    to_bind(parse_and_double(user_input))(lambda doubled:
        format_output(doubled)
    ))

# Nothing happens yet - no input is requested
# Run when ready
# result = run(computation)  # Now it asks for input and processes
```

**Practical Example - Safe Pipeline**:
```python
from felis.either import Right, Left, to_bind, catch

# Create safe versions of operations
safe_int = catch(ValueError)(int)
safe_divide = catch(ZeroDivisionError)(lambda x: 100 / x)

def validate_positive(x):
    if x > 0:
        return Right(x)
    return Left("Number must be positive")

# Build a pipeline
def process_input(s):
    return to_bind(
        to_bind(
            to_bind(safe_int(s))(validate_positive)
        )(safe_divide)
    )(lambda result: Right(f"Final result: {result:.2f}"))

# Test the pipeline
print(process_input("5"))     # Right("Final result: 20.00")
print(process_input("-5"))    # Left("Number must be positive")
print(process_input("0"))     # Left(ZeroDivisionError(...))
print(process_input("abc"))   # Left(ValueError(...))
```

## Practical Examples

### Example 1: Building a Calculator with Error Handling

```python
from felis.either import Right, Left, to_bind, catch
from felis.currying import curry

# Safe operations
safe_int = catch(ValueError)(int)

@curry
def safe_divide(x, y):
    if y == 0:
        return Left("Division by zero")
    return Right(x / y)

@curry
def safe_add(x, y):
    return Right(x + y)

# Calculator pipeline
def calculate(operation, x_str, y_str):
    def operate(x):
        def apply_op(y):
            if operation == "add":
                return safe_add(x)(y)
            elif operation == "divide":
                return safe_divide(x)(y)
            else:
                return Left(f"Unknown operation: {operation}")
        return to_bind(safe_int(y_str))(apply_op)
    return to_bind(safe_int(x_str))(operate)

# Usage
match calculate("add", "10", "5"):
    case Right(result):
        print(f"Result: {result}")  # Result: 15
    case Left(error):
        print(f"Error: {error}")

match calculate("divide", "10", "0"):
    case Right(result):
        print(f"Result: {result}")
    case Left(error):
        print(f"Error: {error}")  # Error: Division by zero
```

### Example 2: List Comprehension with Guards

```python
from felis.list import to_bind, pure, range_to_from, guard, take_after

# Traditional list comprehension:
# even_squares = [x**2 for x in range(1, 11) if x % 2 == 0]

# Functional style with list monad:
# range_to_from(stop)(start) creates range(start, stop)
even_squares = to_bind(range_to_from(11)(1))(lambda x:
    take_after(guard(x % 2 == 0))(
        pure(x ** 2)
    ))

print(even_squares)  # [4, 16, 36, 64, 100]

# More complex: pairs where sum equals 10
pairs = to_bind(range_to_from(11)(1))(lambda x:
    to_bind(range_to_from(11)(1))(lambda y:
        take_after(guard(x + y == 10))(
            pure((x, y))
        )))

print(pairs)  # [(1, 9), (2, 8), (3, 7), (4, 6), (5, 5), (6, 4), (7, 3), (8, 2), (9, 1)]
```

### Example 3: Managing I/O with Lazy

```python
from felis.lazy import to_bind, pure, take_after, run

# Build a lazy I/O program
main = \
    take_after(lambda: print("What's your name?"))(
    to_bind(lambda: input())(lambda name:
    take_after(lambda: print("What's your age?"))(
    to_bind(lambda: input())(lambda age:
    lambda: print(f"Hello, {name}! You are {age} years old.")
    ))))

# Run the program
# run(main)
```

### Example 4: Parser Combinators

```python
from felis.parser import *
from felis.option import Some

# Parse a simple arithmetic expression
digit_parser = some(digit)
number = map_by("".join)(digit_parser)

# Parse integer
integer = map_by(int)(number)

# Parse addition expression: "123+456"
addition_parser = \
    to_bind(integer)(lambda left:
    to_bind(character("+"))(lambda _:
    to_bind(integer)(lambda right:
        pure(left + right)
    )))

# Test the parser
match parse_as("123+456", addition_parser):
    case None:
        print("Parse failed")
    case Some(result):
        print(f"Result: {result}")  # Result: 579
```

### Example 5: Optional Chaining

```python
from felis.option import Some, to_bind, map_by

# Safely navigate nested dictionaries
def get_nested(d, *keys):
    result = Some(d)
    for key in keys:
        result = to_bind(result)(lambda obj:
            Some(obj.get(key)) if isinstance(obj, dict) and key in obj else None
        )
    return result

user = {
    "name": "Alice",
    "address": {
        "city": "Wonderland",
        "zip": "12345"
    }
}

# Safe navigation
city = get_nested(user, "address", "city")  # Some("Wonderland")
country = get_nested(user, "address", "country")  # None
phone = get_nested(user, "contact", "phone")  # None
```

## Summary

Functional programming in **Felis Catus** provides powerful abstractions for handling:

- **Functors**: Transform values in containers
- **Applicatives**: Combine multiple containers
- **Monads**: Chain operations that produce containers

These patterns enable:
- **Type-safe error handling** with `Either`
- **Optional values** with `Option`
- **Lazy evaluation** with `Lazy`
- **Non-deterministic computations** with `List`
- **Parser combinators** with `Parser`

By understanding and using these functional programming concepts, you can write more composable, maintainable, and type-safe code.

## Further Reading

- The README.md contains practical examples of using Felis
- Each module in the `felis` package includes type signatures that follow functional programming conventions
- Study the source code to see how functors, applicatives, and monads are implemented
