import operator
from functools import wraps
from typing import Any
from pychain.common import CommonChain


class ChainableResult(CommonChain):

    def __getattribute__(self, name) -> Any:
        if name in ["_instance", "_value"]:
            return object.__getattribute__(self, name)

        instance = object.__getattribute__(self, "_instance")
        value = object.__getattribute__(self, "_value")

        if hasattr(instance, name):
            attr = getattr(instance, name)
            if callable(attr):
                return lambda *args, **kwargs: ChainableResult(
                    instance, attr(*args, **kwargs)
                )
            return attr

        if hasattr(value, name):
            attr = getattr(value, name)
            if callable(attr):
                return lambda *args, **kwargs: attr(*args, **kwargs)
            return attr

        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{name}'"
        )

    def __call__(self, *args, **kwargs) -> Any:
        if callable(self._value):
            return self._value(*args, **kwargs)
        raise TypeError(f"'{type(self._value).__name__}' object is not callable")


def chainable(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        return ChainableResult(self, result)

    return wrapper


def make_operator_method(op):
    def method(self, other):
        value = object.__getattribute__(self, "_value")
        instance = object.__getattribute__(self, "_instance")
        return ChainableResult(instance, op(value, other))

    return method


for name, op in operator.__dict__.items():
    if name.startswith("__") and name.endswith("__") and callable(op):
        setattr(ChainableResult, name, make_operator_method(op))
