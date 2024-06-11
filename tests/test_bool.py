from felis.bool import both


def test_both_returns_false_when_first_is_false():
    assert both(True)(False) is False


def test_both_returns_false_when_second_is_false():
    assert both(False)(True) is False


def test_both_returns_true_when_both_are_true():
    assert both(True)(True) is True
