from felis import predicate

__all__ = ["truthy", "falsey"]


def truthy(value: object) -> bool:
    return bool(value)


falsey = predicate.negate(truthy)
