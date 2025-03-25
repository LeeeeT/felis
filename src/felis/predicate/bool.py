from felis.predicate import negate

__all__ = ["falsy", "truthy"]


def truthy(value: object) -> bool:
    return bool(value)


falsy = negate(truthy)
