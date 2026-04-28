from __future__ import annotations

import inspect
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
                async def make_step(prev_value: Any, *args: Any, **kwargs: Any) -> Any:
                    resolved = await prev_value
                    if isinstance(resolved, tuple):
                        inner = attr(*resolved, *args, **kwargs)
                    else:
                        inner = attr(resolved, *args, **kwargs)
                    inner_value = object.__getattribute__(inner, VALUE)
                    if inspect.isawaitable(inner_value):
                        return await inner_value
                    return inner_value

                return lambda *args, **kwargs: AsyncPipelineResult(
                    instance, make_step(value, *args, **kwargs)
                )
            return attr

        if hasattr(value, name):
            attr = getattr(value, name)
            if callable(attr):
                return lambda *args, **kwargs: attr(*args, **kwargs)
            return attr

        raise AttributeError(name)

    # -- Async-aware functional composition overrides --

    def map(self, fn: Callable[[Any], Any]) -> AsyncPipelineResult[Any]:
        prev_value = object.__getattribute__(self, VALUE)
        instance = object.__getattribute__(self, INSTANCE)

        async def _async_map() -> Any:
            resolved = await prev_value
            return fn(resolved)

        return AsyncPipelineResult(instance, _async_map())

    def filter(self, fn: Callable[[Any], bool]) -> AsyncPipelineResult[Any]:
        prev_value = object.__getattribute__(self, VALUE)
        instance = object.__getattribute__(self, INSTANCE)

        async def _async_filter() -> Any:
            resolved = await prev_value
            if not fn(resolved):
                raise ValueError(
                    f"Filter predicate returned False for {resolved!r}"
                )
            return resolved

        return AsyncPipelineResult(instance, _async_filter())

    def flat_map(self, fn: Callable[[Any], Any]) -> AsyncPipelineResult[Any]:
        prev_value = object.__getattribute__(self, VALUE)
        instance = object.__getattribute__(self, INSTANCE)

        async def _async_flat_map() -> Any:
            resolved = await prev_value
            return fn(resolved)

        return AsyncPipelineResult(instance, _async_flat_map())

    def inspect(self, fn: Callable[[Any], None]) -> AsyncPipelineResult[Any]:
        prev_value = object.__getattribute__(self, VALUE)
        instance = object.__getattribute__(self, INSTANCE)

        async def _async_inspect() -> Any:
            resolved = await prev_value
            fn(resolved)
            return resolved

        return AsyncPipelineResult(instance, _async_inspect())

    def tap(self, fn: Callable[[Any], None]) -> AsyncPipelineResult[Any]:
        return self.inspect(fn)

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
