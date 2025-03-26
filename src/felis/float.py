from felis.currying import curry, flip

__all__ = ["Float", "add_to", "divide_by", "from_subtract", "multiply_by", "to_add"]


Float = float


to_add = curry(float.__add__)


add_to = flip(to_add)


from_subtract = curry(float.__sub__)


multiply_by = curry(float.__mul__)


divide_by = curry(float.__truediv__)
