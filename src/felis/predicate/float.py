from felis.predicate import comparison, interval

__all__ = ["negative", "non_negative", "non_positive", "non_zero", "portion", "positive"]


negative = comparison.less_than(0.0)


non_positive = comparison.less_than_or_same_as(0.0)


non_zero = comparison.different(0.0)


non_negative = comparison.greater_than_or_same_as(0.0)


positive = comparison.greater_than(0.0)


portion = interval.inclusive(0.0)(1.0)
