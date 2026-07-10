# 第2章：变量

变量是编程中最基本的概念之一。你可以把它理解为一个**带标签的盒子**——盒子里可以放东西，标签用来找到它。

## 什么是变量？

变量就是给数据起个名字。有了名字，你就可以随时用它：

```python
name = "小明"       # 字符串
age = 18            # 整数
height = 1.75       # 浮点数（小数）
is_student = True   # 布尔值（真/假）

print(name)
print(age)
print(height)
```

## 变量的命名规则

给变量取名要遵守以下规则：

- 只能包含字母、数字、下划线（`_`）
- **不能以数字开头**
- 不能使用 Python 的**关键字**（如 `if`、`for`、`while` 等）

✅ 正确示范：
```python
my_name = "张三"
score_1 = 95
total_score = 100
```

❌ 错误示范：
```python
1st_name = "李四"    # 以数字开头
my-name = "王五"     # 包含连字符
class = "A班"        # class 是关键字
```

## 修改变量的值

变量就像一个可以随时换内容的盒子：

```python
x = 10
print(x)  # 10

x = 20
print(x)  # 20 — 值被更新了

x = x + 5
print(x)  # 25 — x 原来的值加上 5
```

## 字符串

用引号括起来的内容就是**字符串**：

```python
greeting = "你好，世界！"
name = 'Python'

# 字符串拼接
message = greeting + " 我是 " + name
print(message)

# f-string（推荐！）
age = 30
print(f"我今年 {age} 岁了")
```

> 💡 f-string 是 Python 3.6 引入的格式化字符串方式，在字符串前加 `f`，用 `{}` 插入变量，非常方便！

## 试试看

在右侧编辑器中试试创建你自己的变量吧！
