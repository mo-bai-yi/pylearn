# 第9章：字典

字典是 Python 中非常实用的数据结构——它通过**键值对**来存储数据，就像一本真正的字典：查"词"找"义"。

## 什么是字典

字典用 `{}` 创建，每个元素由 `键: 值` 组成：

```python
# 创建字典
student = {
    "name": "小明",
    "age": 18,
    "city": "北京"
}

print(student)
```

> 💡 键（key）必须是**不可变类型**（字符串、数字、元组），值（value）可以是任何类型。

## 访问字典元素

```python
student = {"name": "小明", "age": 18, "city": "北京"}

# 方式1：方括号（如果键不存在会报错）
print(student["name"])      # 小明

# 方式2：get() 方法（安全取值，不存在返回 None 或默认值）
print(student.get("age"))           # 18
print(student.get("gender"))        # None
print(student.get("gender", "未知")) # 未知
```

## 修改字典

```python
student = {"name": "小明", "age": 18}

# 添加/修改
student["age"] = 19        # 修改已有键
student["city"] = "上海"   # 添加新键值对

print(student)  # {"name": "小明", "age": 19, "city": "上海"}

# 删除
del student["city"]
print(student)  # {"name": "小明", "age": 19}
```

## 遍历字典

```python
student = {"name": "小明", "age": 18, "city": "北京"}

# 遍历键
for key in student:
    print(key)

# 遍历值
for value in student.values():
    print(value)

# 遍历键值对
for key, value in student.items():
    print(f"{key}: {value}")
```

## 字典的常用操作

```python
# 检查键是否存在
print("name" in student)   # True
print("score" in student)  # False

# 获取所有键/值
print(student.keys())    # dict_keys([...])
print(student.values())  # dict_values([...])

# 合并字典
a = {"a": 1, "b": 2}
b = {"c": 3, "d": 4}
a.update(b)
print(a)  # {"a": 1, "b": 2, "c": 3, "d": 4}

# 清空
a.clear()
```

## 实战：词频统计

```python
text = "apple banana apple orange banana apple"
words = text.split()

count = {}
for word in words:
    if word in count:
        count[word] += 1
    else:
        count[word] = 1

print(count)  # {"apple": 3, "banana": 2, "orange": 1}
```

> 💡 词频统计是字典的经典应用场景，用 `collections.Counter` 可以更简洁。

## 试试看

用字典创建一个你的个人信息卡，包含姓名、年龄、爱好，然后打印出来。
