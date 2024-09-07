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