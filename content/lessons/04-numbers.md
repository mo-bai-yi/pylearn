# 第4章：数字和运算

Python 可以当作一个强大的计算器来用。这一章我们学习数字和基本运算。

## Python 中的数字类型

```python
# 整数 (int)
a = 42
b = -10

# 浮点数 (float)
c = 3.14
d = -0.5

# 查看类型
print(type(a))  # <class 'int'>
print(type(c))  # <class 'float'>
```

## 基本运算

```python
a = 10
b = 3

print(a + b)   # 13 — 加法
print(a - b)   # 7  — 减法
print(a * b)   # 30 — 乘法
print(a / b)   # 3.333... — 除法（结果总是浮点数）
print(a // b)  # 3  — 整除（取整数部分）
print(a % b)   # 1  — 取余（求模）
print(a ** b)  # 1000 — 乘方（10的3次方）
```

## 运算顺序

和数学一样，Python 也有运算优先级：

```python
# 先乘除，后加减
print(2 + 3 * 4)      # 14（不是20）
print((2 + 3) * 4)    # 20 — 括号优先
print(10 - 2 ** 3)    # 2（先算 2³ = 8）
```

> 💡 **PEMDAS**：括号 > 指数 > 乘除 > 加减

## 增强赋值运算符

```python
x = 10
x += 5   # 相当于 x = x + 5
print(x) # 15

x -= 3   # 相当于 x = x - 3
print(x) # 12

x *= 2   # 相当于 x = x * 2
print(x) # 24

x /= 4   # 相当于 x = x / 4
print(x) # 6.0
```

## 数字和字符串的转换

```python
# 字符串 → 数字
s = "42"
n = int(s)      # 42（整数）
f = float(s)    # 42.0（浮点数）

# 数字 → 字符串
age = 18
text = str(age)  # "18"

print(f"我今年 {text} 岁了")
```

> ⚠️ 字符串和数字**不能直接用 `+`**：
> ```python
> "年龄：" + 18  # ❌ 报错！
> "年龄：" + str(18)  # ✅ 正确
> ```

## 试试看

用右侧的编辑器做一些计算练习吧！
