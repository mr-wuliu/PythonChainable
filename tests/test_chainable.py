import unittest
from pychain import chainable
import io
import sys
class TestChainable(unittest.TestCase):
    def test_chainable(self):
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

if __name__ == '__main__':
    unittest.main()