"""Tests to verify performance improvements in fold operations."""

from felis.list import fold_left, fold_right


def test_fold_right_with_large_list():
    """Test that fold_right can handle large lists efficiently."""
    # This would fail with the old recursive implementation due to:
    # 1. Stack overflow (recursion depth)
    # 2. O(n²) complexity from list slicing
    large_list = list(range(1000))
    result = fold_right(0)(lambda x: lambda acc: acc + x)(large_list)
    assert result == sum(large_list)


def test_fold_left_with_large_list():
    """Test that fold_left can handle large lists efficiently."""
    # This would fail with the old recursive implementation due to:
    # 1. Stack overflow (recursion depth)
    # 2. O(n²) complexity from list slicing
    large_list = list(range(1000))
    result = fold_left(0)(lambda acc: lambda x: acc + x)(large_list)
    assert result == sum(large_list)


def test_fold_right_order():
    """Test that fold_right maintains correct right-to-left order."""
    # fold_right: (1 - (2 - (3 - 0))) = 1 - (2 - 3) = 1 - (-1) = 2
    result = fold_right(0)(lambda x: lambda acc: x - acc)([1, 2, 3])
    assert result == 2


def test_fold_left_order():
    """Test that fold_left maintains correct left-to-right order."""
    # fold_left: ((0 - 1) - 2) - 3 = -6
    result = fold_left(0)(lambda acc: lambda x: acc - x)([1, 2, 3])
    assert result == -6


def test_fold_right_string_concatenation():
    """Test fold_right with string operations."""
    result = fold_right("")(lambda x: lambda acc: x + acc)(["a", "b", "c"])
    assert result == "abc"


def test_fold_left_string_concatenation():
    """Test fold_left with string operations."""
    result = fold_left("")(lambda acc: lambda x: acc + x)(["a", "b", "c"])
    assert result == "abc"
