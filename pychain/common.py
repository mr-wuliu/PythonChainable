from __future__ import annotations

import operator
from typing import Any, Callable, Generic, TypeVar
from pychain.enum import VALUE, INSTANCE

T = TypeVar("T")
U = TypeVar("U")


class CommonChain(Generic[T]):

    def __init__(self, instance: Any, value: T) -> None:
        object.__setattr__(self, INSTANCE, instance)
        object.__setattr__(self, VALUE, value)

    def __str__(self) -> str:
        return str(object.__getattribute__(self, VALUE))

    def __repr__(self) -> str:
        return repr(object.__getattribute__(self, VALUE))

    def __dir__(self) -> list[str]:
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

    def __add__(self, other: Any) -> Any:
        return object.__getattribute__(self, VALUE) + other

    def __sub__(self, other: Any) -> Any:
        return object.__getattribute__(self, VALUE) - other

    def __mul__(self, other: Any) -> Any:
        return object.__getattribute__(self, VALUE) * other

    def __truediv__(self, other: Any) -> Any:
        return object.__getattribute__(self, VALUE) / other

    def __floordiv__(self, other: Any) -> Any:
        return object.__getattribute__(self, VALUE) // other

    def __mod__(self, other: Any) -> Any:
        return object.__getattribute__(self, VALUE) % other

    def __pow__(self, other: Any) -> Any:
        return object.__getattribute__(self, VALUE) ** other

    def __radd__(self, other: Any) -> Any:
        return other + object.__getattribute__(self, VALUE)

    def __rsub__(self, other: Any) -> Any:
        return other - object.__getattribute__(self, VALUE)

    def __rmul__(self, other: Any) -> Any:
        return other * object.__getattribute__(self, VALUE)

    def __rtruediv__(self, other: Any) -> Any:
        return other / object.__getattribute__(self, VALUE)

    def __rfloordiv__(self, other: Any) -> Any:
        return other // object.__getattribute__(self, VALUE)

    def __rmod__(self, other: Any) -> Any:
        return other % object.__getattribute__(self, VALUE)

    def __rpow__(self, other: Any) -> Any:
        return other ** object.__getattribute__(self, VALUE)

    def __matmul__(self, other: Any) -> Any:
        return object.__getattribute__(self, VALUE) @ other

    def __rmatmul__(self, other: Any) -> Any:
        return other @ object.__getattribute__(self, VALUE)

    def __neg__(self) -> Any:
        return -object.__getattribute__(self, VALUE)

    def __pos__(self) -> Any:
        return +object.__getattribute__(self, VALUE)

    def __abs__(self) -> Any:
        return abs(object.__getattribute__(self, VALUE))

    def __invert__(self) -> Any:
        return ~object.__getattribute__(self, VALUE)

    def __ne__(self, value: object) -> bool:
        return object.__getattribute__(self, VALUE) != value

    def __eq__(self, value: object) -> bool:
        return object.__getattribute__(self, VALUE) == value

    def __ge__(self, value: object) -> bool:
        return object.__getattribute__(self, VALUE) >= value

    def __gt__(self, value: object) -> bool:
        return object.__getattribute__(self, VALUE) > value

    def __le__(self, value: object) -> bool:
        return object.__getattribute__(self, VALUE) <= value

    def __lt__(self, value: object) -> bool:
        return object.__getattribute__(self, VALUE) < value

    # -- Functional composition methods --

    def map(self, fn: Callable[[T], U]) -> CommonChain[U]:
        value = object.__getattribute__(self, VALUE)
        result = fn(value)
        instance = object.__getattribute__(self, INSTANCE)
        return type(self)(instance, result)  # pyright: ignore[reportReturnType,reportArgumentType]

    def filter(self, fn: Callable[[T], bool]) -> CommonChain[T]:
        """Return self if fn(_value) is truthy, otherwise raise ValueError."""
        value = object.__getattribute__(self, VALUE)
        if not fn(value):
            raise ValueError(f"Filter predicate returned False for {value!r}")
        return self

    def flat_map(self, fn: Callable[[T], Any]) -> Any:
        """Transform _value with fn and unwrap the result (no wrapping in proxy)."""
        value = object.__getattribute__(self, VALUE)
        return fn(value)

    def inspect(self, fn: Callable[[T], None]) -> CommonChain[T]:
        """Execute fn on _value for side effects (e.g., debugging), return self unchanged."""
        value = object.__getattribute__(self, VALUE)
        fn(value)
        return self

    def tap(self, fn: Callable[[T], None]) -> CommonChain[T]:
        """Alias for inspect."""
        return self.inspect(fn)
