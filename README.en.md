# pyChainable

[中文文档](README.md) | [English Documentation](README.md)

**pyChainable** is a Python package that allows you to create chainable method calls while maintaining the ability to operate on the original values.

## Installation

To install, use the following commands:

```bash
pip install -r requirements.txt
python -m build 
pip install dist/<package>.whl

```

Or install from PyPI:

```bash
pip install pyChainable

```


## Usage

### Method Chaining

The `@chainable` decorator allows you to create methods that can be chained together.

```python
from pychain import chainable
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
print(result)

```

## Function Chaining

The `@pipeline` decorator allows multiple functions to be chained together, so they are called sequentially, with the return value of one function passed as the argument to the next.

```python
class TestClass:
    @pipeline
    def add_one(self, x: int) -> int:
        return x + 1

    @pipeline
    def add_two(self, x: int) -> int:
        return x + 2

test = TestClass()
test.add_one(2).add_two().add_two().add_two().add_two().add_two()
print(test)

```

### String Operations

`@pipeline` can also be used for string operations.

```python

from pychain.pipeline import PipelineResult
class StrTest:
    @pipeline
    def add(self, s : str) -> str:
        return s + '.'

    @pipeline
    def sp(self, s: str) -> str:
        return s + ','

getString = StrTest()
res3 : str = test3.add("word").sp().add().sp().add()
print(res3)

```

### Matrix Operations

`@pipeline` also supports other forms of operations, such as matrix transformations.

```python
from dataclasses import dataclass

@dataclass(slots=True)
class Matrix:
    a : float
    b : float
    c : float
    d : float
    @pipeline
    def rotate(self, x, y):
        return (self.a * x + self.b * y, self.c * x + self.d * y)
    
    @pipeline
    def scale(self, x, y, factor: float):
        return (x * factor, y * factor)

m = Matrix(0, 1, -1, 0)

res = m.rotate(2,3).scale(factor=2)

res
# continue with other operations
res2 = res.scale(factor=1/2)

res2
```