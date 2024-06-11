from dataclasses import dataclass

__all__ = ["Pair"]


@dataclass(frozen=True)
class Pair[L, R]:
    left: L
    right: R
