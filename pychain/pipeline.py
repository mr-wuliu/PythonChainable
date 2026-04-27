from __future__ import annotations

from functools import wraps
from typing import Any, Callable, TypeVar
from pychain.common import CommonChain
from pychain.enum import VALUE, INSTANCE

T = TypeVar("T")


class PipelineResult(CommonChain[T]):

    def __getattribute__(self, name: str) -> Any:
        if name == "__class__":
            if value := object.__getattribute__(self, VALUE):
                return type(value)
            elif instance := object.__getattribute__(self, INSTANCE):
                return type(instance)
            else:
                return type(self)

        if name in (INSTANCE, VALUE):
            return object.__getattribute__(self, name)

        try:
            proxy_attr = object.__getattribute__(self, name)
            if callable(proxy_attr):
                return proxy_attr
            return proxy_attr
        except AttributeError:
            pass

        instance = object.__getattribute__(self, INSTANCE)
        value = object.__getattribute__(self, VALUE)

        if hasattr(instance, name):
            attr = getattr(instance, name)
            if callable(attr):
                if isinstance(value, tuple):
                    return lambda **kwargs: attr(*value, **kwargs)
                return lambda **kwargs: attr(value, **kwargs)
            return attr

        if hasattr(value, name):
            attr = getattr(value, name)
            if callable(attr):
                return lambda *args, **kwargs: attr(*args, **kwargs)
            return attr
        raise AttributeError(name)

    def __call__(self, *args: Any, **kwargs: Any) -> PipelineResult[T]:
        return self


def pipeline(func: Callable[..., T]) -> Callable[..., PipelineResult[T]]:
    @wraps(func)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> PipelineResult[T]:
        result = func(self, *args, **kwargs)
        return PipelineResult(self, result)
    return wrapper
