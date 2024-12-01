from felis.predicate import negate

__all__ = ["falsey", "truthy"]


def truthy(value: object) -> bool:
    return bool(value)


falsey = negate(truthy)
