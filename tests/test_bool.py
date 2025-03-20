from felis.bool import both_and


def test_both_returns_false_when_first_is_false():
    assert both_and(True)(False) is False


def test_both_returns_false_when_second_is_false():
    assert both_and(False)(True) is False


def test_both_returns_true_when_both_are_true():
    assert both_and(True)(True) is True
