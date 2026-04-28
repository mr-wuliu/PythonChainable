from __future__ import annotations

import inspect
from functools import wraps
from typing import Any, Awaitable, Callable, TypeVar, overload
from pychain.async_chainable import AsyncChainableResult
from pychain.common import CommonChain

T = TypeVar("T")


class ChainableResult(CommonChain[T]):

    def __getattribute__(self, name: str) -> Any:
        if name in ("_instance", "_value"):
            return object.__getattribute__(self, name)

        try:
            proxy_attr = object.__getattribute__(self, name)
            if callable(proxy_attr):
                return proxy_attr
            return proxy_attr
        except AttributeError:
            pass

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

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if callable(object.__getattribute__(self, "_value")):
            return object.__getattribute__(self, "_value")(*args, **kwargs)
        raise TypeError(
            f"'{type(object.__getattribute__(self, '_value')).__name__}' object is not callable"
        )


@overload
def chainable(func: Callable[..., Awaitable[T]]) -> Callable[..., AsyncChainableResult[T]]: ...  # pyright: ignore[reportOverlappingOverload]

@overload
def chainable(func: Callable[..., T]) -> Callable[..., ChainableResult[T]]: ...

def chainable(func: Callable[..., Any]) -> Callable[..., ChainableResult[Any] | AsyncChainableResult[Any]]:
    @wraps(func)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> ChainableResult[Any] | AsyncChainableResult[Any]:
        result = func(self, *args, **kwargs)
        if inspect.iscoroutine(result):
            return AsyncChainableResult(self, result)
        return ChainableResult(self, result)
    return wrapper
