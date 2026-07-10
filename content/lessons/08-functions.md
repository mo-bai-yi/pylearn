# 第8章：函数

函数是**可重复使用的代码块**——把一段代码打包起来，给它取个名字，需要的时候叫它就行。

## 定义和调用函数

```python
# 定义函数
def say_hello():
    print("你好！")
    print("欢迎来到 Python 世界！")

# 调用函数
say_hello()
say_hello()  # 可以多次调用
```

## 带参数的函数

```python
def greet(name):
    print(f"你好，{name}！")

greet("小明")  # 你好，小明！
greet("小红")  # 你好，小红！
```

## 多个参数

```python
def introduce(name, age):
    print(f"我叫{name}，今年{age}岁。")

introduce("小明", 18)
introduce(name="小红", age=20)  # 可以指定参数名
```

## 返回值

函数可以用 `return` 返回结果：

```python
def add(a, b):
    return a + b

result = add(3, 5)
print(result)  # 8

# 可以链式调用
print(add(add(1, 2), add(3, 4)))  # 10
```

## 默认参数

```python
def power(base, exp=2):
    """计算 base 的 exp 次方"""
    return base ** exp

print(power(3))     # 9（3²）
print(power(3, 3))  # 27（3³）
```

> 💡 有默认值的参数必须放在**没有默认值的参数后面**。

## 函数文档字符串

在函数开头的三引号字符串就是**文档字符串**（docstring），用来描述函数的功能：

```python
def circle_area(radius):
    """计算圆的面积
    
    参数：
        radius: 圆的半径
    
    返回：
        圆的面积（保留2位小数）
    """
    return round(3.14159 * radius ** 2, 2)

print(circle_area(5))   # 78.54
help(circle_area)        # 查看文档
```

## 实战：综合例子

```python
def is_prime(n):
    """判断一个数是否为质数"""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# 找出 1-50 中的所有质数
primes = [n for n in range(1, 51) if is_prime(n)]
print(primes)
```

## 试试看

在右侧编辑器中，试着写一个自己的函数吧！
