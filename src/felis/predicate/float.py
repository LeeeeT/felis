from felis.predicate import comparison, interval

__all__ = ["negative", "non_negative", "non_positive", "non_zero", "portion", "positive"]


negative = comparison.less_than(0.0)


non_positive = comparison.less_than_or_equal_to(0.0)


non_zero = comparison.not_equal_to(0.0)


non_negative = comparison.greater_than_or_equal_to(0.0)


positive = comparison.greater_than(0.0)


portion = interval.to_inclusively_from_inclusively(0.0)(1.0)
