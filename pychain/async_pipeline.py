from __future__ import annotations

from functools import wraps
from typing import Any, Callable, TypeVar
from pychain.common import CommonChain
from pychain.enum import VALUE, INSTANCE

T = TypeVar("T")


class AsyncPipelineResult(CommonChain[T]):

    def __init__(self, instance: Any, awaitable_or_value: Any) -> None:
        super().__init__(instance, awaitable_or_value)

    def __getattribute__(self, name: str) -> Any:
        if name == "__class__":
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
                async def make_step(prev_value: Any, **kwargs: Any) -> Any:
                    resolved = await prev_value
                    if isinstance(resolved, tuple):
                        inner = attr(*resolved, **kwargs)
                    else:
                        inner = attr(resolved, **kwargs)
                    inner_value = object.__getattribute__(inner, VALUE)
                    return await inner_value

                return lambda **kwargs: AsyncPipelineResult(
                    instance, make_step(value, **kwargs)
                )
            return attr

        if hasattr(value, name):
            attr = getattr(value, name)
            if callable(attr):
                return lambda *args, **kwargs: attr(*args, **kwargs)
            return attr

        raise AttributeError(name)

    def __call__(self, *args: Any, **kwargs: Any) -> AsyncPipelineResult[T]:
        return self

    def __await__(self):
        return object.__getattribute__(self, VALUE).__await__()


def async_pipeline(func: Callable[..., Any]) -> Callable[..., AsyncPipelineResult[Any]]:
    @wraps(func)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> AsyncPipelineResult[Any]:
        coro = func(self, *args, **kwargs)
        return AsyncPipelineResult(self, coro)
    return wrapper
