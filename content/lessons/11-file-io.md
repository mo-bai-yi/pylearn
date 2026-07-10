# 第11章：文件读写

程序经常需要读取和保存数据——Python 让文件操作变得非常简单。

## 打开和关闭文件

```python
# 打开文件
file = open("notes.txt", "r", encoding="utf-8")
content = file.read()
print(content)
file.close()  # 记得关闭！
```

> ⚠️ 忘记 `close()` 可能导致数据丢失或文件损坏。

## 用 with 语句（推荐）

```python
# with 会自动关闭文件，即使出错也会关
with open("notes.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)
# 到这里文件已经自动关闭了
```

## 文件模式

| 模式 | 说明 |
|------|------|
| `"r"` | 读取（默认，文件不存在报错）|
| `"w"` | 写入（覆盖已有内容，文件不存在则创建）|
| `"a"` | 追加（在文件末尾添加）|
| `"x"` | 创建新文件（文件已存在报错）|
| `"r+"` | 读写 |

## 读取文件

```python
# 读取全部内容
with open("poem.txt", "r", encoding="utf-8") as f:
    content = f.read()  # 整个文件作为一个字符串

# 逐行读取
with open("poem.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())  # strip() 去掉换行符

# 读取所有行到列表
with open("poem.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    print(lines)  # ["第一行\n", "第二行\n", ...]
```

## 写入文件

```python
# 写入（覆盖）
with open("diary.txt", "w", encoding="utf-8") as f:
    f.write("2026年7月10日\n")
    f.write("今天学习了Python文件操作！\n")

# 追加
with open("diary.txt", "a", encoding="utf-8") as f:
    f.write("又补充了一行内容\n")
```

## 实战：简易日记本

```python
import datetime

def write_diary():
    content = input("今天发生了什么？")
    with open("my_diary.txt", "a", encoding="utf-8") as f:
        f.write(f"\n[{datetime.date.today()}]\n")
        f.write(content + "\n")

def read_diary():
    try:
        with open("my_diary.txt", "r", encoding="utf-8") as f:
            print(f.read())
    except FileNotFoundError:
        print("还没有日记内容哦~")

# 运行
write_diary()
read_diary()
```

## 试试看

写一个程序：创建一个 `shopping.txt` 文件，写入你的购物清单（每行一项），然后读取并打印出来。
