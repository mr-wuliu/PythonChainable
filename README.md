# pyChainable

[中文文档](https://github.com/mr-wuliu/PythonChainable/blob/main/README.md) | [English Documentation](https://github.com/mr-wuliu/PythonChainable/blob/main/README.en.md)

pyChainable 是一个 Python 包，允许您创建可链式调用的方法，同时保持对原始值的操作能力。


## 安装

使用以下命令安装：

```
pip install -r requirements.txt
python -m build
pip install dist/pyChainable-0.1.1-py3-none-any.whl
```

或者

```
pip install pyChainable
```

## 使用

### 方法链式调用

@chainable 装饰器允许您创建可链式调用的方法。

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
### 函数链式调用

@pipeline 装饰器允许将多个函数数链接在一起，以便在执行时按顺序调用它们。上一个函数的返回值将作为下一个函数的参数。

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

### 字符串操作同样可用

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
print(res3.split(','))

```

### 矩阵运算

`@pipeline` 可以结合`dataclass`使用，以实现矩阵运算的链式调用。

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