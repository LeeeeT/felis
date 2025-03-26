from felis.currying import curry

__all__ = ["Float", "divide_by", "multiply_by", "from_subtract", "to_add"]


Float = float


to_add = curry(float.__add__)


from_subtract = curry(float.__sub__)


multiply_by = curry(float.__mul__)


divide_by = curry(float.__truediv__)
