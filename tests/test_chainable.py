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
        from pychain.async_chainable import async_chainable, AsyncChainableResult

        class AsyncCalc:
            @async_chainable
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
        from pychain.async_chainable import async_chainable

        class AsyncCalc:
            @async_chainable
            async def multiply(self, x):
                return x * 3

        async def run():
            calc = AsyncCalc()
            val = await calc.multiply(4)
            self.assertEqual(val, 12)

        asyncio.run(run())

    def test_multi_step_chain(self):
        import asyncio
        from pychain.async_chainable import async_chainable

        class AsyncCalc:
            def __init__(self):
                self.value = 0

            @async_chainable
            async def add(self, x):
                self.value += x
                return self.value

        async def run():
            calc = AsyncCalc()
            result = calc.add(3).add(5)
            val = await result
            self.assertEqual(val, 8)

        asyncio.run(run())


class TestAsyncPipeline(unittest.TestCase):
    def test_basic_async_pipeline(self):
        import asyncio
        from pychain.async_pipeline import async_pipeline, AsyncPipelineResult

        class AsyncPipe:
            @async_pipeline
            async def add_one(self, x):
                return x + 1

            @async_pipeline
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
        from pychain.async_pipeline import async_pipeline

        class AsyncPipe:
            @async_pipeline
            async def increment(self, x):
                return x + 1

            @async_pipeline
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
        from pychain.async_pipeline import async_pipeline

        class AsyncPipe:
            @async_pipeline
            async def split(self, x):
                return (x, x * 2)

            @async_pipeline
            async def sum_pair(self, a, b):
                return a + b

        async def run():
            pipe = AsyncPipe()
            result = pipe.split(5).sum_pair()
            val = await result
            self.assertEqual(val, 15)

        asyncio.run(run())


if __name__ == "__main__":
    unittest.main()
