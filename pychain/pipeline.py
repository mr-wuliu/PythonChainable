from functools import wraps
from typing import Any, Callable
from pychain.common import CommonChain


class PipelineResult(CommonChain):

    def __getattribute__(self, name: str) -> Any:
        if name in ["_instance", "_value"]:
            return object.__getattribute__(self, name)
        instance = object.__getattribute__(self, "_instance")
        value = object.__getattribute__(self, "_value")

        if hasattr(instance, name):
            attr = getattr(instance, name)
            if callable(attr):
                if isinstance(value, tuple):
                    return lambda **kwargs : attr(*value, **kwargs)
                return lambda **kwargs : attr(value, **kwargs)
            return attr

        if hasattr(value, name):
            attr = getattr(value, name)
            if callable(attr):
                return lambda *args, **kwargs: attr(*args, **kwargs)
            return value
        raise AttributeError(name)

    def __call__(self, *args, **kwargs) -> Any:
        return self
def pipeline(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(self, *args, **kwargs) -> PipelineResult:
        result = func(self, *args, **kwargs)
        return PipelineResult(self, result)

    return wrapper
