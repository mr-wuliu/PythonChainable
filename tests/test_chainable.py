import unittest
from pychain import chainable, pipeline
import io
import sys
import numpy as np

class TestChainable(unittest.TestCase):
    def test_chainable1(self):
        class MyClass:
            def __init__(self):
                self.value = 0

            @chainable
            def add(self, num):
                self.value += num
                return self.value

            @chainable
            def multiply(self, num):
                self.value *= num
                return self.value

        obj = MyClass()
        result = obj.add(1).add(2).multiply(3)

        self.assertEqual(int(result), 9)
        self.assertEqual(int(result) + 6, 15)
        self.assertEqual(int(result) * 3, 27)
        self.assertEqual(float(result) * 3, 27.0)

    def test_chain_opt2(self):
        class MyClass:
            def __init__(self):
                self.value = 0

            @chainable
            def add(self, num):
                print(self.value + num)
                self.value += 1

        obj = MyClass()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        _ = obj.add(1).add(2).add(3)
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue(), "1\n3\n5\n")
        self.assertEqual(obj.value, 3)

    def test_chain_opt3(self):
        import numpy as np
        from dataclasses import dataclass

        @dataclass(slots=True)
        class Vector:
            x: float
            y: float
            z: float

            @chainable
            def normalized(self):
                x, y, z = self.x, self.y, self.z
                norm = np.sqrt(x * x + y * y + z * z)
                self.x = x / norm
                self.y = y / norm
                self.z = z / norm

            @chainable
            def reflected(self):
                self.x = -self.x
                self.y = -self.y
                self.z = -self.z

        p = Vector(1.0, 2.0, 3.0)
        p.normalized().reflected()
        self.assertEqual(p.x, np.float64(-0.2672612419124244))
        self.assertEqual(p.y, np.float64(-0.5345224838248488))
        self.assertEqual(p.z, np.float64(-0.8017837257372732))

    def test_chain_opt4(self):
        import numpy as np
        from dataclasses import dataclass

        @dataclass(slots=True)
        class Vector:
            x: float
            y: float
            z: float

            @chainable
            def normalized(self):
                x, y, z = self.x, self.y, self.z
                norm = np.sqrt(x * x + y * y + z * z)
                self.x = x / norm
                self.y = y / norm
                self.z = z / norm

            @chainable
            def reflected(self):
                self.x = -self.x
                self.y = -self.y
                self.z = -self.z

        p = Vector(1.0, 2.0, 3.0)
        p.normalized().reflected()
        self.assertEqual(p.x, np.float64(-0.2672612419124244))
        self.assertEqual(p.y, np.float64(-0.5345224838248488))
        self.assertEqual(p.z, np.float64(-0.8017837257372732))

class TestPipeline(unittest.TestCase):
    def test_pipeline_1(self):
        class ChainFunction:
            @pipeline
            def normalized(self, x, y, z):
                norm = np.sqrt(x * x + y * y + z * z)
                return x / norm, y / norm, z / norm

            @pipeline
            def reflected(self, x, y, z):
                return -x, -y, -z
            @pipeline
            def sum(self, x, y, z):
                return x + y + z

            @pipeline
            def negative(self, x):
                return -x

        p = ChainFunction()
        result1 = p.normalized(1.0, 2.0, 3.0).reflected().sum()
        result2 = p.reflected(1.0, 2.0, 3.0).normalized().sum().negative()

        self.assertAlmostEqual(result1, -1.6035674514745464, places=7)
        self.assertAlmostEqual(result2(), 1.6035674514745464, places=7)

    def test_pipeline_2(self):
        class TestClass:
            @pipeline
            def test_method(self, x: int) -> int:
                return x + 1

            @pipeline
            def test_method2(self, x: int) -> int:
                return x + 2

        test = TestClass()

        # 测试每一步调用后的返回类型是否正确封装
        result1 = test.test_method(1)
        self.assertEqual(result1, 2)
        result2 = result1.test_method2()
        self.assertEqual(result2, 4)
        result3 = result2.test_method2()
        self.assertEqual(result3, 6)

        test2 = TestClass()
        res = test2.test_method(2).test_method2().test_method2().test_method2().test_method2().test_method2()
        self.assertEqual(res, 13)
    

    def test_pipeline_3(self):
        from pychain.pipeline import PipelineResult
        class StrTest:
            @pipeline
            def add(self, s : str) -> str:
                return s + "1"

            @pipeline
            def sp(self, s: str, other = '') -> str:
                if other != '':
                    return s + ',' + other
                else:
                    return s + ','
        test3 = StrTest()
        res3 : str = test3.add("someworld").sp().add().sp(other='why').add()
        self.assertEqual(type(res3), PipelineResult)
        self.assertEqual(isinstance(res3, str), True)
        self.assertEqual(res3,'someworld1,1,why1')
        self.assertEqual(type(res3), PipelineResult)
        self.assertEqual(res3.split(','), ['someworld1', '1', 'why1'])
    def test_pipeline_4(self):
        from dataclasses import dataclass
        
        @dataclass(slots=True)
        class TestClass:
            # 定义旋转矩阵的四个参数
            a : float
            b : float
            c : float
            d : float
            # 我们可以定义两个方法 一个用于旋转90度, 一个用于缩放
            @pipeline
            def rotate(self, x, y):
                return (self.a * x + self.b * y, self.c * x + self.d * y)
            
            @pipeline
            def scale(self, x, y, factor: float):
                return (x * factor, y * factor)
        # 旋转矩阵的四个参数
        test = TestClass(0, 1, -1, 0)

        res = test.rotate(2,3).scale(factor=2)
        self.assertEqual(res, (6, -4))

        res2 = res.scale(factor=1/2)
        self.assertEqual(res2, (3 , -2))
        


class TestCommonChain(unittest.TestCase):
    def test_str(self):
        from pychain.common import CommonChain
        proxy = CommonChain("instance", 42)
        self.assertEqual(str(proxy), "42")

    def test_repr(self):
        from pychain.common import CommonChain
        proxy = CommonChain("instance", "hello")
        self.assertEqual(repr(proxy), "'hello'")

    def test_int(self):
        from pychain.common import CommonChain
        proxy = CommonChain("instance", 7)
        self.assertEqual(int(proxy), 7)

    def test_float(self):
        from pychain.common import CommonChain
        proxy = CommonChain("instance", 3.14)
        self.assertAlmostEqual(float(proxy), 3.14)

    def test_bool(self):
        from pychain.common import CommonChain
        self.assertTrue(bool(CommonChain("i", 1)))
        self.assertTrue(bool(CommonChain("i", "nonempty")))
        self.assertFalse(bool(CommonChain("i", 0)))
        self.assertFalse(bool(CommonChain("i", "")))

    def test_index(self):
        from pychain.common import CommonChain
        proxy = CommonChain("instance", 5)
        self.assertEqual([0, 1, 2, 3, 4, 5][proxy], 5)

    def test_arithmetic(self):
        from pychain.common import CommonChain
        p = CommonChain("i", 10)
        self.assertEqual(p + 5, 15)
        self.assertEqual(p - 3, 7)
        self.assertEqual(p * 2, 20)
        self.assertEqual(p / 4, 2.5)
        self.assertEqual(p // 3, 3)
        self.assertEqual(p % 3, 1)
        self.assertEqual(p ** 2, 100)

    def test_reverse_arithmetic(self):
        from pychain.common import CommonChain
        p = CommonChain("i", 10)
        self.assertEqual(5 + p, 15)
        self.assertEqual(20 - p, 10)
        self.assertEqual(3 * p, 30)
        self.assertEqual(100 / p, 10.0)
        self.assertEqual(23 // p, 2)
        self.assertEqual(23 % p, 3)
        self.assertEqual(2 ** p, 1024)

    def test_matmul(self):
        import numpy as np
        from pychain.common import CommonChain
        a = np.array([[1, 2]])
        b = np.array([[3], [4]])
        p = CommonChain("i", a)
        result = p @ b
        expected = a @ b
        self.assertTrue(np.array_equal(result, expected))

    def test_unary(self):
        from pychain.common import CommonChain
        p = CommonChain("i", 5)
        self.assertEqual(-p, -5)
        self.assertEqual(+p, 5)
        self.assertEqual(abs(CommonChain("i", -7)), 7)
        self.assertEqual(~CommonChain("i", 0), -1)

    def test_comparison(self):
        from pychain.common import CommonChain
        p = CommonChain("i", 10)
        self.assertTrue(p == 10)
        self.assertTrue(p != 11)
        self.assertTrue(p > 5)
        self.assertTrue(p < 20)
        self.assertTrue(p >= 10)
        self.assertTrue(p <= 10)
        self.assertFalse(p > 15)

    def test_dir(self):
        from pychain.common import CommonChain
        d = dir(CommonChain("instance_obj", 42))
        self.assertIsInstance(d, list)
        self.assertIn("__class__", d)


class TestFunctionalComposition(unittest.TestCase):
    def test_map(self):
        from pychain.chainable import ChainableResult, chainable

        class Calc:
            @chainable
            def add(self, a, b):
                return a + b

        calc = Calc()
        result = calc.add(3, 4).map(lambda x: x * 2)
        self.assertEqual(int(result), 14)

    def test_filter_pass(self):
        from pychain.chainable import ChainableResult, chainable

        class Calc:
            @chainable
            def add(self, a, b):
                return a + b

        calc = Calc()
        result = calc.add(3, 4).filter(lambda x: x > 0)
        self.assertEqual(int(result), 7)

    def test_filter_fail(self):
        from pychain.chainable import chainable

        class Calc:
            @chainable
            def add(self, a, b):
                return a + b

        calc = Calc()
        with self.assertRaises(ValueError):
            calc.add(3, 4).filter(lambda x: x < 0)

    def test_flat_map(self):
        from pychain.chainable import chainable

        class Calc:
            @chainable
            def add(self, a, b):
                return a + b

        calc = Calc()
        result = calc.add(3, 4).flat_map(lambda x: x * 10)
        self.assertEqual(result, 70)
        self.assertNotIsInstance(result, type(calc.add(1, 2)))

    def test_inspect(self):
        from pychain.chainable import chainable
        collected = []

        class Calc:
            @chainable
            def add(self, a, b):
                return a + b

        calc = Calc()
        result = calc.add(3, 4).inspect(lambda x: collected.append(x))
        self.assertEqual(collected, [7])
        self.assertEqual(int(result), 7)

    def test_tap(self):
        from pychain.chainable import chainable
        collected = []

        class Calc:
            @chainable
            def add(self, a, b):
                return a + b

        calc = Calc()
        result = calc.add(3, 4).tap(lambda x: collected.append(x))
        self.assertEqual(collected, [7])
        self.assertEqual(int(result), 7)

    def test_chain_functional_methods(self):
        from pychain.chainable import chainable
        log = []

        class Calc:
            @chainable
            def add(self, a, b):
                return a + b

            @chainable
            def multiply(self, a, b):
                return a * b

        calc = Calc()
        result = (
            calc.add(2, 3)
            .map(lambda x: x + 1)
            .inspect(lambda x: log.append(x))
            .filter(lambda x: x > 0)
            .map(lambda x: x * 2)
        )
        self.assertEqual(log, [6])
        self.assertEqual(int(result), 12)

    def test_pipeline_functional_methods(self):
        from pychain.pipeline import pipeline

        class Calc:
            @pipeline
            def double(self, x):
                return x * 2

        calc = Calc()
        result = calc.double(5).map(lambda x: x + 1)
        self.assertEqual(int(result), 11)


class TestAsyncChainable(unittest.TestCase):
    def test_basic_async_chain(self):
        import asyncio
        from pychain.async_chainable import AsyncChainableResult

        class AsyncCalc:
            @chainable
            async def add(self, x):
                return x + 10

        async def run():
            calc = AsyncCalc()
            result = calc.add(5)
            self.assertIsInstance(result, AsyncChainableResult)
            val = await result
            self.assertEqual(val, 15)

        asyncio.run(run())

    def test_await_final_result(self):
        import asyncio

        class AsyncCalc:
            @chainable
            async def multiply(self, x):
                return x * 3

        async def run():
            calc = AsyncCalc()
            val = await calc.multiply(4)
            self.assertEqual(val, 12)

        asyncio.run(run())

    def test_multi_step_chain(self):
        import asyncio

        class AsyncCalc:
            def __init__(self):
                self.value = 0

            @chainable
            async def add(self, x):
                self.value += x
                return self.value

        async def run():
            calc = AsyncCalc()
            result = calc.add(3).add(5)
            val = await result
            self.assertEqual(val, 8)

        asyncio.run(run())


class TestAsyncChainableFunctional(unittest.TestCase):
    def test_async_chainable_map(self):
        import asyncio
        from pychain.async_chainable import AsyncChainableResult

        class AsyncCalc:
            @chainable
            async def add(self, x):
                return x + 10

        async def run():
            calc = AsyncCalc()
            result = calc.add(5).map(lambda x: x * 2)
            self.assertIsInstance(result, AsyncChainableResult)
            val = await result
            self.assertEqual(val, 30)

        asyncio.run(run())

    def test_async_chainable_filter_pass(self):
        import asyncio

        class AsyncCalc:
            @chainable
            async def add(self, x):
                return x + 10

        async def run():
            calc = AsyncCalc()
            result = calc.add(5).filter(lambda x: x > 0)
            val = await result
            self.assertEqual(val, 15)

        asyncio.run(run())

    def test_async_chainable_filter_fail(self):
        import asyncio

        class AsyncCalc:
            @chainable
            async def add(self, x):
                return x + 10

        async def run():
            calc = AsyncCalc()
            with self.assertRaises(ValueError):
                await calc.add(5).filter(lambda x: x < 0)

        asyncio.run(run())

    def test_async_chainable_flat_map(self):
        import asyncio
        from pychain.async_chainable import AsyncChainableResult

        class AsyncCalc:
            @chainable
            async def add(self, x):
                return x + 10

        async def run():
            calc = AsyncCalc()
            result = calc.add(5).flat_map(lambda x: x * 10)
            self.assertIsInstance(result, AsyncChainableResult)
            val = await result
            self.assertEqual(val, 150)

        asyncio.run(run())

    def test_async_chainable_inspect(self):
        import asyncio

        class AsyncCalc:
            @chainable
            async def add(self, x):
                return x + 10

        async def run():
            collected = []
            calc = AsyncCalc()
            result = calc.add(5).inspect(lambda x: collected.append(x))
            val = await result
            self.assertEqual(collected, [15])
            self.assertEqual(val, 15)

        asyncio.run(run())

    def test_async_chainable_tap(self):
        import asyncio

        class AsyncCalc:
            @chainable
            async def add(self, x):
                return x + 10

        async def run():
            collected = []
            calc = AsyncCalc()
            result = calc.add(5).tap(lambda x: collected.append(x))
            val = await result
            self.assertEqual(collected, [15])
            self.assertEqual(val, 15)

        asyncio.run(run())

    def test_async_chainable_combined_functional_chain(self):
        import asyncio

        class AsyncCalc:
            @chainable
            async def add(self, x):
                return x + 10

        async def run():
            log = []
            calc = AsyncCalc()
            result = (
                calc.add(5)
                .map(lambda x: x * 2)
                .inspect(lambda x: log.append(x))
                .filter(lambda x: x > 0)
                .map(lambda x: x + 1)
            )
            val = await result
            self.assertEqual(log, [30])
            self.assertEqual(val, 31)

        asyncio.run(run())


class TestAsyncPipeline(unittest.TestCase):
    def test_basic_async_pipeline(self):
        import asyncio
        from pychain.async_pipeline import AsyncPipelineResult

        class AsyncPipe:
            @pipeline
            async def add_one(self, x):
                return x + 1

            @pipeline
            async def double(self, x):
                return x * 2

        async def run():
            pipe = AsyncPipe()
            result = pipe.add_one(5)
            self.assertIsInstance(result, AsyncPipelineResult)
            val = await result
            self.assertEqual(val, 6)

        asyncio.run(run())

    def test_async_pipeline_chaining(self):
        import asyncio

        class AsyncPipe:
            @pipeline
            async def increment(self, x):
                return x + 1

            @pipeline
            async def negate(self, x):
                return -x

        async def run():
            pipe = AsyncPipe()
            result = pipe.increment(10).negate()
            val = await result
            self.assertEqual(val, -11)

        asyncio.run(run())

    def test_async_pipeline_tuple_unpacking(self):
        import asyncio

        class AsyncPipe:
            @pipeline
            async def split(self, x):
                return (x, x * 2)

            @pipeline
            async def sum_pair(self, a, b):
                return a + b

        async def run():
            pipe = AsyncPipe()
            result = pipe.split(5).sum_pair()
            val = await result
            self.assertEqual(val, 15)

        asyncio.run(run())


class TestAsyncPipelineFunctional(unittest.TestCase):
    def test_async_pipeline_map(self):
        import asyncio
        from pychain.async_pipeline import AsyncPipelineResult

        class AsyncPipe:
            @pipeline
            async def double(self, x):
                return x * 2

        async def run():
            pipe = AsyncPipe()
            result = pipe.double(5).map(lambda x: x + 1)
            self.assertIsInstance(result, AsyncPipelineResult)
            val = await result
            self.assertEqual(val, 11)

        asyncio.run(run())

    def test_async_pipeline_filter_pass(self):
        import asyncio

        class AsyncPipe:
            @pipeline
            async def double(self, x):
                return x * 2

        async def run():
            pipe = AsyncPipe()
            result = pipe.double(5).filter(lambda x: x > 0)
            val = await result
            self.assertEqual(val, 10)

        asyncio.run(run())

    def test_async_pipeline_filter_fail(self):
        import asyncio

        class AsyncPipe:
            @pipeline
            async def double(self, x):
                return x * 2

        async def run():
            pipe = AsyncPipe()
            with self.assertRaises(ValueError):
                await pipe.double(5).filter(lambda x: x < 0)

        asyncio.run(run())

    def test_async_pipeline_flat_map(self):
        import asyncio

        class AsyncPipe:
            @pipeline
            async def double(self, x):
                return x * 2

        async def run():
            pipe = AsyncPipe()
            result = pipe.double(5).flat_map(lambda x: [x, x + 1])
            val = await result
            self.assertEqual(val, [10, 11])

        asyncio.run(run())

    def test_async_pipeline_inspect(self):
        import asyncio

        class AsyncPipe:
            @pipeline
            async def double(self, x):
                return x * 2

        async def run():
            collected = []
            pipe = AsyncPipe()
            result = pipe.double(5).inspect(lambda x: collected.append(x))
            val = await result
            self.assertEqual(collected, [10])
            self.assertEqual(val, 10)

        asyncio.run(run())

    def test_async_pipeline_tap(self):
        import asyncio

        class AsyncPipe:
            @pipeline
            async def double(self, x):
                return x * 2

        async def run():
            collected = []
            pipe = AsyncPipe()
            result = pipe.double(5).tap(lambda x: collected.append(x))
            val = await result
            self.assertEqual(collected, [10])
            self.assertEqual(val, 10)

        asyncio.run(run())

    def test_async_pipeline_combined_functional_chain(self):
        import asyncio

        class AsyncPipe:
            @pipeline
            async def increment(self, x):
                return x + 1

            @pipeline
            async def negate(self, x):
                return -x

        async def run():
            log = []
            pipe = AsyncPipe()
            result = (
                pipe.increment(10)
                .map(lambda x: x * 2)
                .inspect(lambda x: log.append(x))
                .filter(lambda x: x > 0)
                .negate()
            )
            val = await result
            self.assertEqual(log, [22])
            self.assertEqual(val, -22)

        asyncio.run(run())


class TestPositionalArgPipeline(unittest.TestCase):
    """Regression tests for positional args during chained pipeline calls."""

    def test_sync_pipeline_positional_args(self):
        class Pipe:
            @pipeline
            def add(self, x: int, y: int) -> int:
                return x + y

            @pipeline
            def multiply(self, x: int, factor: int) -> int:
                return x * factor

        p = Pipe()
        # Previous value (3) auto-injected as first arg; 5 passed as positional extra
        result = p.add(1, 2).multiply(5)
        self.assertEqual(int(result), 15)

    def test_sync_pipeline_positional_args_with_kwargs(self):
        class Pipe:
            @pipeline
            def split(self, x: int) -> tuple:
                return (x, x + 1)

            @pipeline
            def combine(self, a: int, b: int, extra: int = 0) -> int:
                return a + b + extra

        p = Pipe()
        # Tuple (5, 6) unpacked as (a, b), then extra=10 via kwarg
        result = p.split(5).combine(extra=10)
        self.assertEqual(int(result), 21)

    def test_sync_pipeline_positional_args_tuple_unpack(self):
        class Pipe:
            @pipeline
            def pair(self, x: int) -> tuple:
                return (x, x * 2)

            @pipeline
            def sum_with_extra(self, a: int, b: int, extra: int) -> int:
                return a + b + extra

        p = Pipe()
        # Tuple (3, 6) unpacked as (a, b), then 100 as positional extra
        result = p.pair(3).sum_with_extra(100)
        self.assertEqual(int(result), 109)

    def test_async_pipeline_positional_args(self):
        import asyncio

        class AsyncPipe:
            @pipeline
            async def add(self, x: int, y: int) -> int:
                return x + y

            @pipeline
            async def multiply(self, x: int, factor: int) -> int:
                return x * factor

        async def run():
            p = AsyncPipe()
            result = p.add(1, 2).multiply(5)
            val = await result
            self.assertEqual(val, 15)

        asyncio.run(run())

    def test_async_pipeline_positional_args_tuple_unpack(self):
        import asyncio

        class AsyncPipe:
            @pipeline
            async def pair(self, x: int):
                return (x, x * 2)

            @pipeline
            async def sum_with_extra(self, a, b, extra):
                return a + b + extra

        async def run():
            p = AsyncPipe()
            result = p.pair(3).sum_with_extra(100)
            val = await result
            self.assertEqual(val, 109)

        asyncio.run(run())


class TestClassBehavior(unittest.TestCase):
    """Regression tests for __class__ proxy behavior in pipeline results."""

    def test_sync_pipeline_class_returns_value_type(self):
        from pychain.pipeline import PipelineResult

        class Pipe:
            @pipeline
            def double(self, x: int) -> int:
                return x * 2

        p = Pipe()
        result = p.double(5)
        # __class__ should return the wrapped value's type (int)
        self.assertEqual(result.__class__, int)
        # type() bypasses __getattribute__ and returns PipelineResult
        self.assertEqual(type(result), PipelineResult)

    def test_sync_pipeline_class_with_string_value(self):
        from pychain.pipeline import PipelineResult

        class StrPipe:
            @pipeline
            def upper(self, s: str) -> str:
                return s.upper()

        p = StrPipe()
        result = p.upper("hello")
        self.assertEqual(result.__class__, str)
        self.assertEqual(type(result), PipelineResult)

    def test_async_pipeline_class_returns_value_type(self):
        from pychain.async_pipeline import AsyncPipelineResult
        from pychain.enum import VALUE

        class AsyncPipe:
            @pipeline
            async def double(self, x: int) -> int:
                return x * 2

        p = AsyncPipe()
        result = p.double(5)
        # __class__ follows same logic as sync: returns type of _value (coroutine)
        # since _value is a coroutine (truthy), __class__ returns coroutine type
        self.assertNotEqual(result.__class__, AsyncPipelineResult)
        # type() bypasses __getattribute__ and returns AsyncPipelineResult
        self.assertEqual(type(result), AsyncPipelineResult)
        object.__getattribute__(result, VALUE).close()

    def test_sync_pipeline_class_falsy_value(self):
        from pychain.pipeline import PipelineResult

        class Pipe:
            @pipeline
            def zero(self, x: int) -> int:
                return 0

        p = Pipe()
        result = p.zero(5)
        # value is 0 (falsy), so __class__ falls through to instance type
        self.assertEqual(result.__class__, Pipe)


if __name__ == "__main__":
    unittest.main()
