# 第5章：条件判断

程序经常需要根据不同的情况做不同的事情——这就是条件判断。

## if 语句

```python
age = 18

if age >= 18:
    print("你是成年人")
```

> 💡 Python 用**缩进**（通常是4个空格或1个Tab）来表示代码块。这是 Python 的特色！

## if-else 语句

```python
age = 15

if age >= 18:
    print("你可以进入")
else:
    print("你还未成年")
```

## if-elif-else 语句

```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"你的等级是：{grade}")
```

## 比较运算符

```python
a = 10
b = 20

print(a == b)   # False — 相等
print(a != b)   # True  — 不相等
print(a < b)    # True  — 小于
print(a > b)    # False — 大于
print(a <= b)   # True  — 小于等于
print(a >= b)   # False — 大于等于
```

## 逻辑运算符

```python
age = 20
has_id = True

# and — 两个条件都成立
if age >= 18 and has_id:
    print("可以进入")

# or — 至少一个条件成立
if age < 12 or age > 60:
    print("免费入场")

# not — 取反
if not has_id:
    print("请出示证件")
```

## 判断数字奇偶

```python
n = 7

if n % 2 == 0:
    print(f"{n} 是偶数")
else:
    print(f"{n} 是奇数")
```

## 试试看

在右侧编辑器中试试不同的条件判断！
