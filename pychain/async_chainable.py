from __future__ import annotations

import inspect
from functools import wraps
from typing import Any, Callable, TypeVar
from pychain.common import CommonChain

T = TypeVar("T")


class AsyncChainableResult(CommonChain[T]):

    def __init__(self, instance: Any, awaitable_or_value: Any) -> None:
        super().__init__(instance, awaitable_or_value)

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
                def method_caller(*args: Any, **kwargs: Any) -> AsyncChainableResult[Any]:
                    async def async_step() -> Any:
                        await value
                        inner = attr(*args, **kwargs)
                        inner_value = object.__getattribute__(inner, "_value")
                        if inspect.isawaitable(inner_value):
                            return await inner_value
                        return inner_value
                    return AsyncChainableResult(instance, async_step())
                return method_caller
            return attr

        if hasattr(value, name):
            attr = getattr(value, name)
            if callable(attr):
                return lambda *args, **kwargs: attr(*args, **kwargs)
            return attr

        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{name}'"
        )

    def __await__(self):
        return object.__getattribute__(self, "_value").__await__()

    # -- Async-aware functional composition overrides --
    # These override CommonChain methods so that _value (a coroutine) is
    # awaited before the transformation is applied.

    def map(self, fn: Callable[[Any], Any]) -> AsyncChainableResult[Any]:
        prev_value = object.__getattribute__(self, "_value")
        instance = object.__getattribute__(self, "_instance")

        async def _async_map() -> Any:
            resolved = await prev_value
            return fn(resolved)

        return AsyncChainableResult(instance, _async_map())

    def filter(self, fn: Callable[[Any], bool]) -> AsyncChainableResult[Any]:
        prev_value = object.__getattribute__(self, "_value")
        instance = object.__getattribute__(self, "_instance")

        async def _async_filter() -> Any:
            resolved = await prev_value
            if not fn(resolved):
                raise ValueError(
                    f"Filter predicate returned False for {resolved!r}"
                )
            return resolved

        return AsyncChainableResult(instance, _async_filter())

    def flat_map(self, fn: Callable[[Any], Any]) -> AsyncChainableResult[Any]:
        """Async version: awaits _value, applies fn, returns async proxy.

        Unlike the sync CommonChain.flat_map which returns the raw unwrapped
        value, the async version must return an AsyncChainableResult because
        the result cannot be produced synchronously.
        """
        prev_value = object.__getattribute__(self, "_value")
        instance = object.__getattribute__(self, "_instance")

        async def _async_flat_map() -> Any:
            resolved = await prev_value
            return fn(resolved)

        return AsyncChainableResult(instance, _async_flat_map())

    def inspect(self, fn: Callable[[Any], None]) -> AsyncChainableResult[Any]:
        prev_value = object.__getattribute__(self, "_value")
        instance = object.__getattribute__(self, "_instance")

        async def _async_inspect() -> Any:
            resolved = await prev_value
            fn(resolved)
            return resolved

        return AsyncChainableResult(instance, _async_inspect())

    def tap(self, fn: Callable[[Any], None]) -> AsyncChainableResult[Any]:
        return self.inspect(fn)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if callable(object.__getattribute__(self, "_value")):
            return object.__getattribute__(self, "_value")(*args, **kwargs)
        raise TypeError(
            f"'{type(object.__getattribute__(self, '_value')).__name__}' object is not callable"
        )


def async_chainable(func: Callable[..., Any]) -> Callable[..., AsyncChainableResult[Any]]:
    @wraps(func)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> AsyncChainableResult[Any]:
        coro = func(self, *args, **kwargs)
        return AsyncChainableResult(self, coro)
    return wrapper
