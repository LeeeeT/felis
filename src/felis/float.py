from felis.currying import curry

__all__ = ["Float", "by_divide", "by_multiply", "from_subtract", "to_add"]


Float = float


to_add = curry(float.__add__)


from_subtract = curry(float.__sub__)


by_multiply = curry(float.__mul__)


by_divide = curry(float.__truediv__)
