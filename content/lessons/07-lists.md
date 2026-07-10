# 第7章：列表

列表是 Python 中最常用的数据结构，可以存放**一组数据**。

## 创建列表

```python
# 空列表
empty = []

# 数字列表
numbers = [1, 2, 3, 4, 5]

# 字符串列表
fruits = ["苹果", "香蕉", "橙子"]

# 混合类型
mixed = [1, "hello", 3.14, True]

# 嵌套列表（列表里的列表）
matrix = [[1, 2], [3, 4], [5, 6]]
```

## 访问列表元素

```python
fruits = ["苹果", "香蕉", "橙子", "葡萄"]

print(fruits[0])    # 苹果（索引从0开始）
print(fruits[-1])   # 葡萄（最后一个）
print(fruits[1:3])  # ["香蕉", "橙子"]（切片）
```

## 修改列表

```python
fruits = ["苹果", "香蕉", "橙子"]

# 修改元素
fruits[1] = "草莓"
print(fruits)  # ["苹果", "草莓", "橙子"]

# 添加元素
fruits.append("葡萄")     # 末尾添加
print(fruits)

# 插入元素
fruits.insert(1, "蓝莓")  # 在索引1处插入
print(fruits)

# 删除元素
fruits.remove("苹果")     # 删除指定元素
print(fruits)

popped = fruits.pop()     # 删除并返回最后一个
print(popped)
```

## 列表常用操作

```python
numbers = [3, 1, 4, 1, 5, 9, 2]

print(len(numbers))     # 7 — 列表长度
print(max(numbers))     # 9 — 最大值
print(min(numbers))     # 1 — 最小值
print(sum(numbers))     # 25 — 求和

numbers.sort()          # 排序（原地修改）
print(numbers)          # [1, 1, 2, 3, 4, 5, 9]

numbers.reverse()       # 反转
print(numbers)          # [9, 5, 4, 3, 2, 1, 1]

print(3 in numbers)     # True — 是否包含
print(numbers.count(1)) # 2 — 统计出现次数
```

## 遍历列表

```python
fruits = ["苹果", "香蕉", "橙子"]

# 方式1：直接遍历元素
for fruit in fruits:
    print(fruit)

# 方式2：同时获取索引和元素
for i, fruit in enumerate(fruits):
    print(f"第{i+1}个水果是：{fruit}")
```

## 列表推导式

一种创建列表的简洁写法：

```python
# 常规写法
squares = []
for i in range(1, 6):
    squares.append(i ** 2)
print(squares)  # [1, 4, 9, 16, 25]

# 列表推导式（一行搞定！）
squares = [i ** 2 for i in range(1, 6)]
print(squares)  # [1, 4, 9, 16, 25]

# 带条件的推导式
evens = [i for i in range(10) if i % 2 == 0]
print(evens)    # [0, 2, 4, 6, 8]
```

## 试试看

创建一个包含你最爱水果的列表，然后试试各种操作！
