import pytest
from felis.bool import No, Yes, both


def test_both_returns_no_when_first_is_no():
    match both(Yes())(No()):
        case No():
            pass
        case Yes():
            pytest.fail("`both` should return `No` when the first argument is `No`")


def test_both_returns_no_when_second_is_no():
    match both(No())(Yes()):
        case No():
            pass
        case Yes():
            pytest.fail("`both` should return `No` when the second argument is `No`")


def test_both_returns_yes_when_both_are_yes():
    match both(Yes())(Yes()):
        case Yes():
            pass
        case No():
            pytest.fail("`both` should return `Yes` when both arguments are `Yes`")
