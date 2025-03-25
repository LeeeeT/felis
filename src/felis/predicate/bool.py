from felis.predicate import negate

__all__ = ["falsy", "truthy"]


truthy = bool


falsy = negate(truthy)
