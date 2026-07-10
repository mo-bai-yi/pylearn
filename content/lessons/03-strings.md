# 第3章：字符串操作

字符串是 Python 中最常用的数据类型之一。这一章我们来学习字符串的各种操作。

## 创建字符串

```python
s1 = "双引号"
s2 = '单引号'
s3 = """三引号
可以换行
写多行文字"""
```

## 字符串索引

字符串中的每个字符都有一个**位置编号**（索引），从 **0** 开始：

```python
text = "Python"
#       P y t h o n
#       0 1 2 3 4 5

print(text[0])   # P
print(text[1])   # y
print(text[-1])  # n（-1 是最后一个字符）
print(text[-2])  # o（-2 是倒数第二个）
```

## 字符串切片

用 `[开始:结束]` 可以截取字符串的一部分：

```python
text = "Hello, Python!"

print(text[0:5])    # Hello（索引0到4）
print(text[7:13])   # Python（索引7到12）
print(text[:5])     # Hello（从开头到4）
print(text[7:])     # Python!（从7到结尾）
print(text[-7:-1])  # Python（从倒数第7到倒数第2）
```

> 💡 切片语法 `[start:end]` 是 **左闭右开** 的，包含 start 位置，不包含 end 位置。

## 常用字符串方法

```python
text = "  Hello, Python!  "

print(text.lower())       # "  hello, python!  " — 转小写
print(text.upper())       # "  HELLO, PYTHON!  " — 转大写
print(text.strip())       # "Hello, Python!" — 去掉首尾空格
print(len(text))          # 18 — 字符串长度（包括空格）
print(text.count('o'))    # 2 — 统计字符出现次数

# 替换
print(text.replace('Python', 'World'))  # "  Hello, World!  "

# 拆分
words = "apple,banana,orange"
print(words.split(','))   # ['apple', 'banana', 'orange']

# 拼接
fruits = ['apple', 'banana', 'orange']
print(' + '.join(fruits)) # "apple + banana + orange"
```

## 判断字符串

```python
print("123".isdigit())    # True — 全是数字
print("abc".isalpha())    # True — 全是字母
print("Hello".startswith("He"))  # True — 以"He"开头
print("Hello".endswith("lo"))    # True — 以"lo"结尾
print("Py" in "Python")   # True — 包含"Py"
```

## 试试看

在右侧编辑器里试试各种字符串操作吧！
