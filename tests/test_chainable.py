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

        @dataclass(slots=True, frozen=False)
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

        @dataclass(slots=True, frozen=False)
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
        result1 = p.normalized(1.0, 2.0, 3.0).reflected().sum()()
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
        self.assertEqual(res3,'someworld1,1,1')
        self.assertEqual(type(res3), PipelineResult)
        self.assertEqual(res3.split(','), ['someworld1', '1', '1'])

if __name__ == "__main__":
    unittest.main()
