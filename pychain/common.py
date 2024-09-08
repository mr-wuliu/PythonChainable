import operator
from functools import wraps
from typing import Any, Callable

class CommonChain:

    def __init__(self, instance, value, kwargs=None) -> None:
        object.__setattr__(self, "_instance", instance)
        object.__setattr__(self, "_value", value)

    def __str__(self):
        return str(object.__getattribute__(self, "_value"))

    def __repr__(self) -> str:
        return repr(object.__getattribute__(self, "_value"))

    def __dir__(self) -> list:
        instance = object.__getattribute__(self, "_instance")
        value = object.__getattribute__(self, "_value")
        return sorted(set(dir(instance) + dir(value)))

    def __int__(self) -> int:
        return int(object.__getattribute__(self, "_value"))

    def __float__(self) -> float:
        return float(object.__getattribute__(self, "_value"))

    def __bool__(self) -> bool:
        return bool(object.__getattribute__(self, "_value"))

    def __index__(self) -> int:
        return operator.index(object.__getattribute__(self, "_value"))

    def __add__(self, other: Any):
        return object.__getattribute__(self, "_value") + other
    
    def __sub__(self, other: Any):
        return object.__getattribute__(self, "_value") - other
    
    def __mul__(self, other: Any):
        return object.__getattribute__(self, "_value") * other
    
    def __truediv__(self, other: Any):
        return object.__getattribute__(self, "_value") / other
    
    def __floordiv__(self, other: Any):
        return object.__getattribute__(self, "_value") // other
    
    def __mod__(self, other: Any):
        return object.__getattribute__(self, "_value") % other
    
    def __pow__(self, other: Any):
        return object.__getattribute__(self, "_value") ** other
    def __radd__(self, other: Any):
        return other + object.__getattribute__(self, "_value")
    
    def __rsub__(self, other: Any):
        return other - object.__getattribute__(self, "_value")
    
    def __rmul__(self, other: Any):
        return other * object.__getattribute__(self, "_value")
    
    def __rtruediv__(self, other: Any):
        return other / object.__getattribute__(self, "_value")
    
    def __rfloordiv__(self, other: Any):
        return other // object.__getattribute__(self, "_value")
    
    def __rmod__(self, other: Any):
        return other % object.__getattribute__(self, "_value")
    
    def __rpow__(self, other: Any):
        return other ** object.__getattribute__(self, "_value")
    
    def __matmul__(self, other: Any):
        return object.__getattribute__(self, "_value") @ other
    
    def __rmatmul__(self, other: Any):
        return other @ object.__getattribute__(self, "_value")
    
    def __neg__(self):
        return -object.__getattribute__(self, "_value")
    
    def __pos__(self):
        return +object.__getattribute__(self, "_value")
    
    def __abs__(self):
        return abs(object.__getattribute__(self, "_value"))
    
    def __invert__(self):
        return ~object.__getattribute__(self, "_value")
    
    def __ne__(self, value: object):
        return object.__getattribute__(self, "_value") != value
    
    def __eq__(self, value: object) -> bool:
        return object.__getattribute__(self, "_value") == value
    def __ge__(self, value: object):
        return object.__getattribute__(self, "_value") >= value
    def __gt__(self, value: object):
        return object.__getattribute__(self, "_value") > value
    
    def __le__(self, value: object):
        return object.__getattribute__(self, "_value") <= value
    
    def __lt__(self, value: object):
        return object.__getattribute__(self, "_value") < value