from typing import Final

__all__ = ["Pair"]


class Pair[L, R]:
    __match_args__ = ("left", "right")

    def __init__(self, left: L, right: R):
        self.left: Final = left
        self.right: Final = right
