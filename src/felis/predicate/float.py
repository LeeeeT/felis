from felis.predicate import comparison, interval

__all__ = ["negative", "non_negative", "non_positive", "non_zero", "portion", "positive"]


negative = comparison.less(0.0)


non_positive = comparison.less_or_equal(0.0)


non_zero = comparison.not_equal(0.0)


non_negative = comparison.greater_or_equal(0.0)


positive = comparison.greater(0.0)


portion = interval.inclusive(0.0)(1.0)
