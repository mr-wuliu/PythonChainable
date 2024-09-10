import operator
from typing import Any
from pychain.enum import VALUE, INSTANCE


class CommonChain:

    def __init__(self, instance, value) -> None:
        object.__setattr__(self, INSTANCE, instance)
        object.__setattr__(self, VALUE, value)

    def __str__(self):
        return str(object.__getattribute__(self, VALUE))

    def __repr__(self) -> str:
        return repr(object.__getattribute__(self, VALUE))

    def __dir__(self) -> list:
        instance = object.__getattribute__(self, INSTANCE)
        value = object.__getattribute__(self, VALUE)
        return sorted(set(dir(instance) + dir(value)))

    def __int__(self) -> int:
        return int(object.__getattribute__(self, VALUE))

    def __float__(self) -> float:
        return float(object.__getattribute__(self, VALUE))

    def __bool__(self) -> bool:
        return bool(object.__getattribute__(self, VALUE))

    def __index__(self) -> int:
        return operator.index(object.__getattribute__(self, VALUE))

    def __add__(self, other: Any):
        return object.__getattribute__(self, VALUE) + other

    def __sub__(self, other: Any):
        return object.__getattribute__(self, VALUE) - other

    def __mul__(self, other: Any):
        return object.__getattribute__(self, VALUE) * other

    def __truediv__(self, other: Any):
        return object.__getattribute__(self, VALUE) / other

    def __floordiv__(self, other: Any):
        return object.__getattribute__(self, VALUE) // other

    def __mod__(self, other: Any):
        return object.__getattribute__(self, VALUE) % other

    def __pow__(self, other: Any):
        return object.__getattribute__(self, VALUE) ** other

    def __radd__(self, other: Any):
        return other + object.__getattribute__(self, VALUE)

    def __rsub__(self, other: Any):
        return other - object.__getattribute__(self, VALUE)

    def __rmul__(self, other: Any):
        return other * object.__getattribute__(self, VALUE)

    def __rtruediv__(self, other: Any):
        return other / object.__getattribute__(self, VALUE)

    def __rfloordiv__(self, other: Any):
        return other // object.__getattribute__(self, VALUE)

    def __rmod__(self, other: Any):
        return other % object.__getattribute__(self, VALUE)

    def __rpow__(self, other: Any):
        return other ** object.__getattribute__(self, VALUE)

    def __matmul__(self, other: Any):
        return object.__getattribute__(self, VALUE) @ other

    def __rmatmul__(self, other: Any):
        return other @ object.__getattribute__(self, VALUE)

    def __neg__(self):
        return -object.__getattribute__(self, VALUE)

    def __pos__(self):
        return +object.__getattribute__(self, VALUE)

    def __abs__(self):
        return abs(object.__getattribute__(self, VALUE))

    def __invert__(self):
        return ~object.__getattribute__(self, VALUE)

    def __ne__(self, value: object):
        return object.__getattribute__(self, VALUE) != value

    def __eq__(self, value: object) -> bool:
        return object.__getattribute__(self, VALUE) == value

    def __ge__(self, value: object):
        return object.__getattribute__(self, VALUE) >= value

    def __gt__(self, value: object):
        return object.__getattribute__(self, VALUE) > value

    def __le__(self, value: object):
        return object.__getattribute__(self, VALUE) <= value

    def __lt__(self, value: object):
        return object.__getattribute__(self, VALUE) < value
