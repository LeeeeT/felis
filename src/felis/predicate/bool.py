from felis.predicate import negate

__all__ = ["truthy", "falsey"]


def truthy(value: object) -> bool:
    return bool(value)


falsey = negate(truthy)
