# pyChainable

pyChainable 是一个 Python 包，允许您创建可链式调用的方法，同时保持对原始值的操作能力。


# 安装

```
pip install -r requirements.txt
python -m build
pip install dist/pyChainable-0.1.0-py3-none-any.whl
```

或者

```
pip install pyChainable
```

# 使用

## 方法链式调用

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
## 函数链式调用

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

对于字符串也可以操作

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