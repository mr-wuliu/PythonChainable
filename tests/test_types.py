# pyright: reportUnusedImport=none
"""Type-checking assertions for pychain public API.

Validated by basedpyright, not executed by pytest.
Verifies that type inference works correctly for all public APIs.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from pychain import async_chainable, async_pipeline, chainable, pipeline
from pychain.async_chainable import AsyncChainableResult
from pychain.async_pipeline import AsyncPipelineResult
from pychain.chainable import ChainableResult
from pychain.common import CommonChain
from pychain.pipeline import PipelineResult

if TYPE_CHECKING:

    class Calc:
        @chainable
        def add(self, a: int, b: int) -> int: ...

    c = Calc()
    r: ChainableResult[int] = c.add(1, 2)
    mapped: CommonChain[int] = c.add(1, 2).map(lambda x: x * 2)
    filtered: CommonChain[int] = c.add(1, 2).filter(lambda x: x > 0)
    inspected: CommonChain[int] = c.add(1, 2).inspect(lambda x: None)
    tapped: CommonChain[int] = c.add(1, 2).tap(lambda x: None)

    class Pipe:
        @pipeline
        def double(self, x: int) -> int: ...

    p = Pipe()
    pr: PipelineResult[int] = p.double(5)
    pmapped: CommonChain[int] = p.double(5).map(lambda x: x + 1)

    proxy: CommonChain[int] = CommonChain("i", 42)
    add_result: int = proxy + 1
    eq_result: bool = proxy == 42
    str_result: str = str(proxy)

    class AsyncCalc:
        @async_chainable
        async def compute(self, x: int) -> int: ...

    ac = AsyncCalc()
    ar: AsyncChainableResult[int] = ac.compute(5)

    class AsyncPipe:
        @async_pipeline
        async def step(self, x: int) -> int: ...

    ap = AsyncPipe()
    apr: AsyncPipelineResult[int] = ap.step(3)
